"""Transactional PostgreSQL store for a public synthetic FastAPI case study.

Tenant-qualified SQL plus signed claims and DB membership are deliberately
application-level controls, NOT database Row Level Security / a production SLA.
"""
import hashlib,json,re
import psycopg
from psycopg.types.json import Jsonb

TENANT=re.compile(r"^[a-z][a-z0-9-]{1,39}$")
SUBJECT=re.compile(r"^[A-Za-z0-9._:-]{1,100}$")
ITEM=re.compile(r"^[A-Za-z0-9._:-]{2,100}$")
ALLOWED=frozenset({"records:read","records:write"})

class Denied(PermissionError):pass
class Conflict(Exception):pass

def require(value,regex,label):
    if not isinstance(value,str) or not regex.fullmatch(value):
        raise ValueError("Invalid "+label)

class PgStore:
    def __init__(self,dsn):
        if not isinstance(dsn,str) or not dsn:raise ValueError("Explicit test DSN required")
        self.dsn=dsn
    def connect(self):
        return psycopg.connect(self.dsn,connect_timeout=2)
    def migrate(self):
        # Explicit setup on a disposable database; never migrates at import.
        with self.connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS av_public_membership (
                tenant_id TEXT NOT NULL, actor TEXT NOT NULL,
                scope TEXT NOT NULL CHECK(scope IN ('records:read','records:write')),
                PRIMARY KEY(tenant_id,actor,scope))""")
            db.execute("""CREATE TABLE IF NOT EXISTS av_public_records (
                tenant_id TEXT NOT NULL, record_id TEXT NOT NULL,
                payload JSONB NOT NULL, version INTEGER NOT NULL CHECK(version>0),
                PRIMARY KEY(tenant_id,record_id))""")
            db.execute("""CREATE TABLE IF NOT EXISTS av_public_intents (
                tenant_id TEXT NOT NULL, idem TEXT NOT NULL,
                fingerprint TEXT NOT NULL, receipt JSONB NOT NULL,
                PRIMARY KEY(tenant_id,idem))""")
    def grant(self,actor,tenant,scope):
        require(actor,SUBJECT,"actor");require(tenant,TENANT,"tenant")
        if scope not in ALLOWED:raise ValueError("Unsupported permission")
        with self.connect() as db:
            db.execute("""INSERT INTO av_public_membership(tenant_id,actor,scope)
                VALUES(%s,%s,%s) ON CONFLICT DO NOTHING""",(tenant,actor,scope))
    def revoke(self,actor,tenant,scope):
        require(actor,SUBJECT,"actor");require(tenant,TENANT,"tenant")
        if scope not in ALLOWED:raise ValueError("Unsupported permission")
        with self.connect() as db:
            db.execute("""DELETE FROM av_public_membership
                WHERE tenant_id=%s AND actor=%s AND scope=%s""",(tenant,actor,scope))
    def seed(self,tenant,record,payload):
        # Test fixtures only; not callable from the public HTTP interface.
        require(tenant,TENANT,"tenant");require(record,ITEM,"record")
        if not isinstance(payload,dict):raise ValueError("Object required")
        with self.connect() as db:
            db.execute("""INSERT INTO av_public_records(tenant_id,record_id,payload,version)
                VALUES(%s,%s,%s,1) ON CONFLICT(tenant_id,record_id)
                DO UPDATE SET payload=EXCLUDED.payload, version=1""",
                (tenant,record,Jsonb(payload)))
    @staticmethod
    def check_actor(db,principal,tenant,scope):
        if principal["tenant"]!=tenant or scope not in principal["scope"]:
            raise Denied("Insufficient tenant authorization")
        granted=db.execute("""SELECT 1 FROM av_public_membership
            WHERE tenant_id=%s AND actor=%s AND scope=%s FOR SHARE""",
            (tenant,principal["sub"],scope)).fetchone()
        if not granted:raise Denied("No active membership")
    def list_records(self,principal,tenant,limit,offset):
        require(tenant,TENANT,"tenant")
        with self.connect() as db:
            self.check_actor(db,principal,tenant,"records:read")
            total=db.execute("""SELECT count(*) FROM av_public_records
                WHERE tenant_id=%s""",(tenant,)).fetchone()[0]
            found=db.execute("""SELECT record_id,payload,version FROM av_public_records
                WHERE tenant_id=%s ORDER BY record_id LIMIT %s OFFSET %s""",
                (tenant,limit,offset)).fetchall()
            return {"items":[{"record_id":r[0],"payload":r[1],"version":r[2]} for r in found],
                    "total":total,"limit":limit,"offset":offset}
    def get_record(self,principal,tenant,record):
        require(tenant,TENANT,"tenant");require(record,ITEM,"record")
        with self.connect() as db:
            self.check_actor(db,principal,tenant,"records:read")
            result=db.execute("""SELECT payload,version FROM av_public_records
                WHERE tenant_id=%s AND record_id=%s""",(tenant,record)).fetchone()
            return {"record_id":record,"payload":result[0],"version":result[1]} if result else None
    def put_record(self,principal,tenant,record,payload,expected_version,idem):
        require(tenant,TENANT,"tenant");require(record,ITEM,"record")
        require(idem,ITEM,"idempotency key")
        if type(expected_version) is not int or not 0<=expected_version<=2_147_483_000:
            raise ValueError("Invalid expected version")
        if not isinstance(payload,dict):
            raise ValueError("JSON object required")
        serialized=json.dumps(payload,sort_keys=True,allow_nan=False,separators=(",",":"))
        if len(serialized)>4096:raise ValueError("Payload too large")
        intent=json.dumps({"record":record,"payload":payload,"expected":expected_version},
                          sort_keys=True,allow_nan=False,separators=(",",":"))
        fingerprint=hashlib.sha256(intent.encode()).hexdigest()
        with self.connect() as db:
            self.check_actor(db,principal,tenant,"records:write")
            # Unique key is tenant-qualified, insert blocks on uncommitted rival intent.
            row=db.execute("""INSERT INTO av_public_intents(tenant_id,idem,fingerprint,receipt)
                VALUES(%s,%s,%s,'{}'::jsonb)
                ON CONFLICT DO NOTHING RETURNING idem""",
                (tenant,idem,fingerprint)).fetchone()
            if not row:
                prev=db.execute("""SELECT fingerprint,receipt FROM av_public_intents
                    WHERE tenant_id=%s AND idem=%s FOR UPDATE""",(tenant,idem)).fetchone()
                if not prev or prev[0]!=fingerprint:raise Conflict("Idempotency conflict")
                return {"receipt":prev[1],"replayed":True}
            old=db.execute("""SELECT version FROM av_public_records
                WHERE tenant_id=%s AND record_id=%s FOR UPDATE""",
                (tenant,record)).fetchone()
            ver=old[0] if old else 0
            if ver!=expected_version:raise Conflict("Record version conflict")
            next_ver=ver+1
            changed=db.execute("""INSERT INTO av_public_records
                (tenant_id,record_id,payload,version)
                VALUES(%s,%s,%s,%s)
                ON CONFLICT(tenant_id,record_id) DO UPDATE
                SET payload=EXCLUDED.payload,version=EXCLUDED.version
                WHERE av_public_records.version=%s RETURNING version""",
                (tenant,record,Jsonb(payload),next_ver,expected_version)).fetchone()
            if not changed:raise Conflict("Concurrent write conflict")
            receipt={"record_id":record,"version":next_ver}
            db.execute("""UPDATE av_public_intents SET receipt=%s
                WHERE tenant_id=%s AND idem=%s""",(Jsonb(receipt),tenant,idem))
            return {"receipt":receipt,"replayed":False}

"""Run an actual in-process HTTP / PostgreSQL roundtrip with synthetic keys.

Requires an explicit disposable ARAZVERA_PUBLIC_TEST_PG_DSN. Never binds an
Internet port, uses customer credentials, or provisions production tables.
"""
import base64,json,os,time,uuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding,rsa
from fastapi.testclient import TestClient
from service import build_app
from storage import PgStore

def b64(v):
    if isinstance(v,dict):v=json.dumps(v,separators=(",",":")).encode()
    return base64.urlsafe_b64encode(v).rstrip(b"=").decode()

def demo():
    dsn=os.getenv("ARAZVERA_PUBLIC_TEST_PG_DSN")
    if not dsn:
        raise SystemExit("Explicit disposable ARAZVERA_PUBLIC_TEST_PG_DSN required")
    key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    pub=key.public_key().public_numbers()
    def i64(n):return b64(n.to_bytes((n.bit_length()+7)//8,"big"))
    jwks={"keys":[{"kty":"RSA","kid":"synthetic-demo","alg":"RS256","use":"sig",
                  "n":i64(pub.n),"e":i64(pub.e)}]}
    issuer="https://synthetic-idp.invalid";audience="arazvera-public-lab"
    store=PgStore(dsn);store.migrate()
    tenant="lab"+uuid.uuid4().hex[:18];other="other"+uuid.uuid4().hex[:18]
    user="demo-"+uuid.uuid4().hex[:12]
    store.grant(user,tenant,"records:read")
    store.grant(user,tenant,"records:write")
    now=int(time.time())
    payload={"iss":issuer,"aud":audience,"sub":user,"tenant":tenant,
             "iat":now-1,"nbf":now-1,"exp":now+120,
             "scope":"records:read records:write"}
    token=b64({"alg":"RS256","typ":"at+jwt","kid":"synthetic-demo"})+"."+b64(payload)
    jwt=token+"."+b64(key.sign(token.encode(),padding.PKCS1v15(),hashes.SHA256()))
    client=TestClient(build_app(store,jwks,issuer,audience))
    headers={"Authorization":"Bearer "+jwt}
    uri="/v1/tenants/"+tenant+"/records/demo-record"
    accepted=client.put(uri,headers={**headers,"Idempotency-Key":"demo-idem-1"},
        json={"payload":{"label":"synthetic-case","qty":3},"expected_version":0})
    read=client.get(uri,headers=headers)
    denied=client.get("/v1/tenants/"+other+"/records",headers=headers)
    store.revoke(user,tenant,"records:read")
    revoked=client.get(uri,headers=headers)
    report={"synthetic":True,"production_approved":False,
            "http_create":accepted.status_code,"http_read":read.status_code,
            "denied_cross_tenant":denied.status_code,
            "revoked_read":revoked.status_code,
            "database":"postgresql-transactional"}
    assert report["http_create"]==201 and report["http_read"]==200
    assert report["denied_cross_tenant"]==403 and report["revoked_read"]==403
    print(json.dumps(report,sort_keys=True))
if __name__=="__main__":demo()

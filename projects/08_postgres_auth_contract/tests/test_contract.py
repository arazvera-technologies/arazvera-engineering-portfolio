"""Contract tests use actual disposable Postgres + in-memory RSA signing keys."""
import base64,json,os,sys,time,unittest,uuid
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding,rsa
from fastapi.testclient import TestClient
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from service import build_app
from storage import PgStore

def b64(v):
    if isinstance(v,dict):v=json.dumps(v,separators=(",",":")).encode()
    return base64.urlsafe_b64encode(v).rstrip(b"=").decode()

class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.getenv("ARAZVERA_PUBLIC_TEST_PG_DSN"):
            raise unittest.SkipTest("Explicit disposable PostgreSQL DSN required")
        cls.key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        n=cls.key.public_key().public_numbers()
        jwks={"keys":[{"kty":"RSA","kid":"synthetic-key-01","use":"sig","alg":"RS256",
                       "n":b64(n.n.to_bytes((n.n.bit_length()+7)//8,"big")),
                       "e":b64(n.e.to_bytes((n.e.bit_length()+7)//8,"big"))}]}
        cls.issuer="https://synthetic-idp.invalid"
        cls.audience="arazvera-public-lab"
        cls.store=PgStore(os.environ["ARAZVERA_PUBLIC_TEST_PG_DSN"])
        cls.store.migrate()
        cls.client=TestClient(build_app(cls.store,jwks,cls.issuer,cls.audience))
    def setUp(self):
        x=uuid.uuid4().hex[:14]
        self.a="ta"+x;self.b="tb"+x;self.user="user-"+x
        self.store.grant(self.user,self.a,"records:read")
        self.store.grant(self.user,self.a,"records:write")
        self.store.seed(self.a,"shared-one",{"label":"ALPHA"})
        self.store.seed(self.b,"shared-one",{"label":"BETA"})
    def jwt(self,**patch):
        now=int(time.time())
        body={"iss":self.issuer,"aud":self.audience,"sub":self.user,"tenant":self.a,
              "scope":"records:read records:write","iat":now-1,"nbf":now-1,"exp":now+240}
        body.update(patch)
        msg=b64({"alg":"RS256","kid":"synthetic-key-01","typ":"at+jwt"})+"."+b64(body)
        sig=self.key.sign(msg.encode(),padding.PKCS1v15(),hashes.SHA256())
        return msg+"."+b64(sig)
    def headers(self,**patch):return {"Authorization":"Bearer "+self.jwt(**patch)}
    def url(self,tenant=None,record=None):
        out="/v1/tenants/"+(tenant or self.a)+"/records"
        return out+("/"+record if record else "")
    def put(self,record,key,payload,version=0,headers=None):
        h=headers or self.headers();h={**h,"Idempotency-Key":key}
        return self.client.put(self.url(record=record),headers=h,
            json={"payload":payload,"expected_version":version})
    def test_authorized_read_and_no_data_leak(self):
        r=self.client.get(self.url(),headers=self.headers())
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json()["items"][0]["payload"]["label"],"ALPHA")
        self.assertNotIn("BETA",r.text)
        self.assertEqual(r.headers["cache-control"],"no-store")
    def test_cross_tenant_rejected_even_if_record_exists(self):
        self.assertEqual(self.client.get(self.url(self.b),headers=self.headers()).status_code,403)
        self.store.grant(self.user,self.b,"records:read")
        r=self.client.get(self.url(self.b),headers=self.headers(tenant=self.b))
        self.assertEqual(r.json()["items"][0]["payload"]["label"],"BETA")
    def test_revoke_blocks_same_valid_token(self):
        h=self.headers()
        self.assertEqual(self.client.get(self.url(),headers=h).status_code,200)
        self.store.revoke(self.user,self.a,"records:read")
        self.assertEqual(self.client.get(self.url(),headers=h).status_code,403)
    def test_no_token_bad_token_wrong_audience_rejected(self):
        self.assertEqual(self.client.get(self.url()).status_code,401)
        self.assertEqual(self.client.get(self.url(),headers={"Authorization":"Bearer garbage"}).status_code,401)
        self.assertEqual(self.client.get(self.url(),headers=self.headers(aud="incorrect")).status_code,401)
        self.assertEqual(self.client.get(self.url(),headers=self.headers(iss="https://evil.invalid")).status_code,401)
    def test_alg_none_and_bad_signature_rejected(self):
        h,p,s=self.jwt().split(".")
        fake=b64({"alg":"none","kid":"synthetic-key-01","typ":"at+jwt"})+"."+p+"."
        self.assertEqual(self.client.get(self.url(),headers={"Authorization":"Bearer "+fake}).status_code,401)
        broken=h+"."+p+"."+b64(b"bad-signature")
        self.assertEqual(self.client.get(self.url(),headers={"Authorization":"Bearer "+broken}).status_code,401)
    def test_expired_nbf_future_and_iat_future_rejected(self):
        now=int(time.time())
        for change in ({"exp":now-1},{"nbf":now+80},{"iat":now+80}):
            self.assertEqual(self.client.get(self.url(),headers=self.headers(**change)).status_code,401)
    def test_db_membership_not_replaceable_by_token_scope(self):
        self.assertEqual(self.client.get(self.url(),headers=self.headers(sub="anonymous")).status_code,403)
        self.assertEqual(self.client.get(self.url(),headers=self.headers(scope="records:write")).status_code,403)
    def test_write_and_readback_postgres(self):
        r=self.put("created-01","idem-01",{"label":"created","q":3})
        self.assertEqual(r.status_code,201,r.text)
        self.assertEqual(r.json()["version"],1)
        read=self.client.get(self.url(record="created-01"),headers=self.headers())
        self.assertEqual(read.json()["payload"]["q"],3)
    def test_idempotent_retry_and_conflicting_payload(self):
        a=self.put("created-02","idem-02",{"v":1})
        b=self.put("created-02","idem-02",{"v":1})
        c=self.put("created-02","idem-02",{"v":2})
        self.assertEqual((a.status_code,b.status_code,c.status_code),(201,200,409))
        self.assertEqual(a.json()["version"],b.json()["version"])
    def test_version_conflict_no_lost_write(self):
        a=self.put("shared-one","idem-03",{"label":"updated"},version=1)
        b=self.put("shared-one","idem-04",{"label":"lost"},version=1)
        self.assertEqual((a.status_code,b.status_code),(200,409))
        self.assertEqual(self.client.get(self.url(record="shared-one"),headers=self.headers()).json()["payload"]["label"],"updated")
    def test_write_requires_scope_and_db_grant(self):
        self.assertEqual(self.put("write-01","idem-05",{"x":1},headers=self.headers(scope="records:read")).status_code,403)
        self.store.revoke(self.user,self.a,"records:write")
        self.assertEqual(self.put("write-01","idem-05",{"x":1}).status_code,403)
    def test_bad_inputs_and_bounds(self):
        for q in ({"limit":0},{"limit":101},{"offset":-1},{"offset":10001}):
            self.assertEqual(self.client.get(self.url(),headers=self.headers(),params=q).status_code,422)
        self.assertEqual(self.client.get("/v1/tenants/invalid_name/records",headers=self.headers()).status_code,422)
        self.assertEqual(self.client.put(self.url(record="new"),headers=self.headers(),json={"payload":{"x":1},"expected_version":0}).status_code,422)
    def test_database_failure_is_generic(self):
        old=self.store.dsn
        try:
            self.store.dsn="postgresql://synthetic:invalid@127.0.0.1:1/nodb?connect_timeout=1"
            r=self.client.get(self.url(),headers=self.headers())
            self.assertEqual(r.status_code,503)
            self.assertNotIn("127.0.0.1",r.text)
        finally:self.store.dsn=old
    def test_health_and_missing_record(self):
        self.assertFalse(self.client.get("/health").json()["production_approved"])
        self.assertEqual(self.client.get(self.url(record="absent"),headers=self.headers()).status_code,404)
if __name__=="__main__":unittest.main()

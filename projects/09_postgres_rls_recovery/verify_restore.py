"""Verify source vs restored synthetic PostgreSQL rows, RLS policy and privileges."""
import hashlib,json,os
import psycopg
from psycopg.conninfo import make_conninfo
from proof_db import safe_config

def run():
    conf=safe_config()
    def db(name,user="l3admin",password="synthetic_local_fixture"):
        return psycopg.connect(make_conninfo("",**{**conf,"dbname":name,"user":user,"password":password}))
    def rows(database):
        with db(database) as c:
            return c.execute("""SELECT tenant_id::text,record_id,payload::text,version
                FROM level3.records ORDER BY tenant_id,record_id""").fetchall()
    a,b=rows("l3proof"),rows("l3proof_restore")
    assert len(a)>=2 and a==b
    for name,expected,not_expected in (("av_l3_tenant_a","ALPHA","BETA"),("av_l3_tenant_b","BETA","ALPHA")):
        password={"av_l3_tenant_a":"synthetic_test_a_only","av_l3_tenant_b":"synthetic_test_b_only"}[name]
        with db("l3proof_restore",name,password) as c:
            value=[v[0] for v in c.execute("SELECT payload->>'label' FROM level3.records").fetchall()]
            assert expected in value and not_expected not in value,(name,value)
    with db("l3proof_restore") as c:
        settings=c.execute("""SELECT relrowsecurity,relforcerowsecurity
            FROM pg_class WHERE oid='level3.records'::regclass""").fetchone()
        assert settings==(True,True)
        policy=c.execute("SELECT count(*) FROM pg_policies WHERE schemaname='level3' AND tablename='records' AND policyname='isolate_logged_tenant'").fetchone()[0]
        assert policy==1
    report={"status":"PASS","lab":"synthetic-postgresql-rls-restoration",
        "db_engine":"PostgreSQL 16","source_database":"l3proof",
        "restore_database":"l3proof_restore","rows_equal":True,
        "restored_row_count":len(b),"restored_rls_enabled":True,
        "restored_rls_forced":True,"restored_policy_present":True,
        "independent_logins_isolated_after_restore":True,
        "production_approved":False,
        "limitations":["No customer data or production system","Roles are cluster-global and require separate provisioning on a different server","No TLS ingress, Supabase or external IdP integration","Restore tested in same isolated test container, not cross-region disaster recovery"]}
    out=os.path.join(os.path.dirname(__file__),"EVIDENCE_RESTORE_SYNTHETIC.json")
    with open(out,"w",encoding="utf-8") as f:json.dump(report,f,indent=2)
    print(json.dumps(report,sort_keys=True))
if __name__=="__main__":run()

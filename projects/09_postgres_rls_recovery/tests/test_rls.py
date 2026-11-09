"""Level 3 candidate proof: DB-enforced RLS with independent tenant logins.

All tests run against a disposable localhost PostgreSQL 16 container.
They are not proof of production certification or external SaaS deployment.
"""
import os,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import psycopg
from proof_db import connect_admin,connect_tenant,prepare_fixture,COUNT_SQL,A_TENANT,B_TENANT

class TestRlsBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.getenv("ARAZVERA_L3_ADMIN_DSN"):
            raise unittest.SkipTest("Explicit disposable database required")
        prepare_fixture()
    def test_each_login_sees_only_its_own_row(self):
        for login,expected in (("a","ALPHA"),("b","BETA")):
            with connect_tenant(login) as c:
                rows=c.execute("SELECT payload->>'label' FROM level3.records ORDER BY record_id").fetchall()
                self.assertEqual(rows,[(expected,)])
    def test_tenant_id_is_derived_from_login_not_client_setting(self):
        with connect_tenant("a") as c:
            c.execute("SELECT set_config('app.tenant_id',%s,false)",(str(B_TENANT),))
            self.assertEqual(c.execute("SELECT level3.current_tenant()").fetchone()[0],A_TENANT)
            self.assertEqual(c.execute(COUNT_SQL).fetchone()[0],1)
    def test_app_role_cannot_read_membership_map(self):
        with connect_tenant("a") as c:
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                c.execute("SELECT * FROM level3.login_map").fetchall()
    def test_other_tenant_insert_is_rejected_by_db(self):
        with connect_tenant("a") as c:
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                c.execute("INSERT INTO level3.records(tenant_id,record_id,payload,version) VALUES(%s,'attack','{}',1)",(B_TENANT,))
    def test_other_tenant_update_changes_zero_rows(self):
        with connect_tenant("a") as c:
            row=c.execute("UPDATE level3.records SET payload='{}' WHERE tenant_id=%s RETURNING record_id",(B_TENANT,)).fetchall()
            self.assertEqual(row,[])
        with connect_tenant("b") as c:
            self.assertEqual(c.execute("SELECT payload->>'label' FROM level3.records").fetchone()[0],"BETA")
    def test_role_switch_to_other_login_is_forbidden(self):
        with connect_tenant("a") as c:
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                c.execute("SET ROLE av_l3_tenant_b")
    def test_setting_row_security_off_does_not_bypass_rls(self):
        with connect_tenant("a") as c:
            c.execute("SET row_security = off")
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                c.execute("SELECT * FROM level3.records").fetchall()
    def test_test_role_has_no_bypassrls_or_superuser(self):
        with connect_admin() as c:
            rows=c.execute("""SELECT rolname,rolsuper,rolbypassrls
                FROM pg_roles WHERE rolname IN ('av_l3_tenant_a','av_l3_tenant_b')
                ORDER BY rolname""").fetchall()
            self.assertEqual(rows,[("av_l3_tenant_a",False,False),("av_l3_tenant_b",False,False)])
            r=c.execute("SELECT relrowsecurity,relforcerowsecurity FROM pg_class WHERE oid='level3.records'::regclass").fetchone()
            self.assertEqual(r,(True,True))
    def test_valid_in_tenant_insert_commits(self):
        with connect_tenant("a") as c:
            c.execute("""INSERT INTO level3.records(tenant_id,record_id,payload,version)
                VALUES(level3.current_tenant(),'own_insert','{"label":"OWN"}',1)
                ON CONFLICT DO NOTHING""")
        with connect_tenant("a") as c:
            self.assertEqual(c.execute("SELECT payload->>'label' FROM level3.records WHERE record_id='own_insert'").fetchone()[0],"OWN")
        with connect_tenant("b") as c:
            self.assertIsNone(c.execute("SELECT record_id FROM level3.records WHERE record_id='own_insert'").fetchone())
    def test_optimistic_concurrency_stale_revision_denied(self):
        with connect_tenant("a") as c:
            changed=c.execute("""UPDATE level3.records SET version=version+1
                WHERE record_id='alpha' AND version=1 RETURNING version""").fetchone()
            self.assertEqual(changed[0],2)
        with connect_tenant("a") as c:
            stale=c.execute("""UPDATE level3.records SET version=version+1
                WHERE record_id='alpha' AND version=1 RETURNING version""").fetchone()
            self.assertIsNone(stale)
    def test_explicit_transaction_rollback_restores_previous_value(self):
        with connect_tenant("b") as c:
            before=c.execute("SELECT payload FROM level3.records WHERE record_id='beta'").fetchone()[0]
            c.execute("UPDATE level3.records SET payload='{\"label\":\"BROKEN\"}' WHERE record_id='beta'")
            c.rollback()
        with connect_tenant("b") as c:
            self.assertEqual(c.execute("SELECT payload FROM level3.records WHERE record_id='beta'").fetchone()[0],before)
    def test_sql_parameter_does_not_escape_tenant_boundary(self):
        with connect_tenant("a") as c:
            attack="alpha' OR true --"
            self.assertEqual(c.execute("SELECT record_id FROM level3.records WHERE record_id=%s",(attack,)).fetchall(),[])
            self.assertEqual(c.execute(COUNT_SQL).fetchone()[0]>=1,True)
    def test_no_delete_grant_for_login(self):
        with connect_tenant("a") as c:
            with self.assertRaises(psycopg.errors.InsufficientPrivilege):
                c.execute("DELETE FROM level3.records")
    def test_nonmapped_role_no_rows(self):
        with connect_tenant("guest") as c:
            self.assertEqual(c.execute(COUNT_SQL).fetchone()[0],0)
if __name__=="__main__":unittest.main()

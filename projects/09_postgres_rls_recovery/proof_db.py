"""Database-enforced row isolation demonstration with separate tenant logins.

Synthetic PostgreSQL 16 training lab; no production or customer access.
"""
from __future__ import annotations
import os,uuid
import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict,make_conninfo
from psycopg.types.json import Jsonb

A_TENANT=uuid.UUID("aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa")
B_TENANT=uuid.UUID("bbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb")
COUNT_SQL="SELECT count(*) FROM level3.records"

LOGINS={
    "a":("av_l3_tenant_a","synthetic_test_a_only"),
    "b":("av_l3_tenant_b","synthetic_test_b_only"),
    "guest":("av_l3_guest","synthetic_test_guest_only"),
}
def safe_config():
    value=os.environ.get("ARAZVERA_L3_ADMIN_DSN","")
    if not value:raise RuntimeError("Explicit disposable PostgreSQL DSN required")
    c=conninfo_to_dict(value)
    if c.get("host") not in {"127.0.0.1","localhost"}:
        raise RuntimeError("Refuse non-local or remote database")
    if c.get("dbname")!="l3proof" or c.get("user")!="l3admin":
        raise RuntimeError("Refuse non-disposable database")
    if c.get("password")!="synthetic_local_fixture":
        raise RuntimeError("Refuse non-synthetic credential")
    return c

def connect_admin():
    return psycopg.connect(make_conninfo("",**safe_config()),connect_timeout=4)

def connect_tenant(which):
    if which not in LOGINS:raise ValueError("Unknown synthetic login")
    user,passphrase=LOGINS[which]
    params=safe_config()
    params.update(user=user,password=passphrase)
    return psycopg.connect(make_conninfo("",**params),connect_timeout=4)

def prepare_fixture():
    """Create only a local synthetic test fixture in the verified l3proof DB."""
    safe_config()
    with connect_admin() as c:
        for user,passphrase in LOGINS.values():
            present=c.execute("SELECT 1 FROM pg_roles WHERE rolname=%s",(user,)).fetchone()
            command="ALTER ROLE" if present else "CREATE ROLE"
            statement=sql.SQL(command+" {} WITH LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS").format(
                sql.Identifier(user),sql.Literal(passphrase))
            c.execute(statement)
        c.execute("CREATE SCHEMA IF NOT EXISTS level3")
        c.execute("""CREATE TABLE IF NOT EXISTS level3.login_map (
            role_name NAME PRIMARY KEY,tenant_id UUID NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS level3.records (
            tenant_id UUID NOT NULL,record_id TEXT NOT NULL,
            payload JSONB NOT NULL,version INTEGER NOT NULL CHECK(version > 0),
            PRIMARY KEY(tenant_id,record_id))""")
        c.execute("ALTER TABLE level3.records ENABLE ROW LEVEL SECURITY")
        c.execute("ALTER TABLE level3.records FORCE ROW LEVEL SECURITY")
        # Use session_user; SECURITY DEFINER would change current_user to owner.
        # Qualified object names and a fixed search path avoid object shadowing.
        c.execute("""CREATE OR REPLACE FUNCTION level3.current_tenant()
            RETURNS UUID LANGUAGE SQL STABLE SECURITY DEFINER
            SET search_path = pg_catalog
            AS $$ SELECT tenant_id FROM level3.login_map
                 WHERE role_name = session_user $$""")
        c.execute("REVOKE ALL ON SCHEMA level3 FROM PUBLIC")
        c.execute("REVOKE ALL ON TABLE level3.login_map FROM PUBLIC")
        c.execute("REVOKE ALL ON TABLE level3.records FROM PUBLIC")
        c.execute("REVOKE ALL ON FUNCTION level3.current_tenant() FROM PUBLIC")
        c.execute("DROP POLICY IF EXISTS isolate_logged_tenant ON level3.records")
        c.execute("""CREATE POLICY isolate_logged_tenant ON level3.records
            FOR ALL TO PUBLIC
            USING (tenant_id = level3.current_tenant())
            WITH CHECK (tenant_id = level3.current_tenant())""")
        for user,_ in LOGINS.values():
            c.execute(sql.SQL("GRANT USAGE ON SCHEMA level3 TO {}").format(sql.Identifier(user)))
            c.execute(sql.SQL("GRANT EXECUTE ON FUNCTION level3.current_tenant() TO {}").format(sql.Identifier(user)))
            c.execute(sql.SQL("GRANT SELECT ON level3.records TO {}").format(sql.Identifier(user)))
        for which in ("a","b"):
            user,_=LOGINS[which]
            c.execute(sql.SQL("GRANT INSERT,UPDATE ON level3.records TO {}").format(sql.Identifier(user)))
        c.execute("TRUNCATE TABLE level3.records, level3.login_map")
        c.execute("""INSERT INTO level3.login_map(role_name,tenant_id)
            VALUES (%s,%s),(%s,%s)""",
            (LOGINS["a"][0],A_TENANT,LOGINS["b"][0],B_TENANT))
        c.execute("""INSERT INTO level3.records
            (tenant_id,record_id,payload,version)
            VALUES (%s,'alpha',%s,1),(%s,'beta',%s,1)""",
            (A_TENANT,Jsonb({"label":"ALPHA"}),B_TENANT,Jsonb({"label":"BETA"})))

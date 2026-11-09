# Level 3 evidence lab - PostgreSQL RLS & a verifiable recovery drill

**Independent, synthetic engineering demonstration. Not an external client review or production certification.**

## Why this is harder than an ordinary CRUD example

In the [public Level 2 API case](../08_postgres_auth_contract/), access was restricted by application SQL filters and a membership table. Here **PostgreSQL itself** denies cross-tenant queries, inserts and updates through `ENABLE ROW LEVEL SECURITY`, `FORCE ROW LEVEL SECURITY`, least-privileged tenant database logins and a policy tied to `session_user`.

The test setup has two independently authenticated tenant database logins and a third unmapped guest role. The tenant mapping is in a table inaccessible to those roles. A read-only `SECURITY DEFINER` lookup is explicitly granted, fixes its `search_path` and references `session_user` so a user setting `app.tenant_id` cannot change their assigned tenant.

This **per-tenant-login model is a lab design**, not a drop-in model for a shared-connection SaaS or Supabase. A production implementation needs its own audited trust boundaries and operational role provisioning.

## Reproduce the tests

Requires Docker, Python 3.11+, and psycopg 3.2+.

```bash
docker run --rm -d --name av-l3-proof -e POSTGRES_USER=l3admin -e POSTGRES_PASSWORD=synthetic_local_fixture -e POSTGRES_DB=l3proof -p 127.0.0.1:55439:5432 postgres:16-alpine
python -m pip install 'psycopg[binary]>=3.2,<4'
export ARAZVERA_L3_ADMIN_DSN='postgresql://l3admin:synthetic_local_fixture@127.0.0.1:55439/l3proof'
python -m unittest discover -s tests -v
```

On Windows PowerShell, set the same variable with `$env:ARAZVERA_L3_ADMIN_DSN = '...'`. The setup code **refuses a non-local host, any database other than `l3proof` or non-synthetic credentials**. It creates or alters only fixture roles in the throwaway PostgreSQL cluster. Do not point it at customer databases.

## 14 executable negative-path tests

- Separate tenant logins only read their own rows; an unmapped guest reads none.
- Attempts to insert or mutate another tenant's rows fail at the database boundary.
- Setting a spoofed `app.tenant_id` does not change the policy's mapping.
- Restricted logins cannot read the role/tenant map or switch tenant roles.
- `row_security=off` does not enable bypass by an unprivileged role.
- Neither tenant login has `SUPERUSER` or `BYPASSRLS`.
- `ENABLE` and `FORCE ROW LEVEL SECURITY` are both active.
- Same-tenant insert, optimistic version conflict and transaction rollback are tested.
- Bound SQL arguments do not become executable SQL, and DELETE is not granted.

## Reproduce an isolated backup / restore rehearsal

After running the tests above:

```bash
docker exec av-l3-proof pg_dump -U l3admin -d l3proof -Fc -n level3 -f /tmp/l3proof_schema_data.dump
docker exec av-l3-proof createdb -U l3admin l3proof_restore
docker exec av-l3-proof pg_restore -U l3admin -d l3proof_restore --exit-on-error /tmp/l3proof_schema_data.dump
python verify_restore.py
docker stop av-l3-proof
```

The independent restore verifier confirms record equality, restored RLS configuration, active policy and tenant logins still isolating data in the restored database. Its result is in [synthetic evidence JSON](EVIDENCE_RESTORE_SYNTHETIC.json).

**Crucial limitation:** the rehearsal restores into *another database on the same isolated PostgreSQL test server*. Global database roles exist in the same cluster and need separate provisioning during disaster recovery to a completely new server. No cross-region, infrastructure, TLS, token or client-data recovery is claimed.

## Client delivery boundaries

Use authorized staging only and scoped evidence. A real review should include authorization mapping and security-definer threat modeling, schema/function privileges, migration and rollback planning, full backup/restore exercise including globals and secrets, tenant-isolation regressions, credential lifetime controls, and an explicit PASS / HOLD release recommendation. This source does **not** claim a prior client audit, regulatory certification, signed penetration test or operational responsibility for an actual SaaS.

[View the Level 2 public portfolio](../../README.md) | [Level 3 evidence and readiness](../../docs/LEVEL3_SPECIALIST_READINESS_20261109.md)

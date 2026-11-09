# 08 - Verified JWT + FastAPI + PostgreSQL Tenant Contract

**Status: synthetic, executable public Level 2 engineering reference; NOT a production deployment.**

This self-contained public example demonstrates a realistic *multi-component* request path with no live identity provider, credentials, cloud APIs, customer records, or private ARAZVERA kit sources.

```text
Synthetic RS256 access token
        | explicit JWKS public key and issuer/audience/expiry checks
        v
 FastAPI /v1/tenants/{tenant}/records
        | token tenant and required scope
        v
 PostgreSQL active membership (transaction-locked)
        | tenant-qualified, parameterized SQL
        v
 Versioned JSONB records + idempotent receipts
```

## Real contracts

- `GET /health`: no privileged information; explicitly says not production approved.
- `GET /v1/tenants/{tenant}/records?limit=&offset=`: bounded, tenant-scoped listing.
- `GET /v1/tenants/{tenant}/records/{record}`: get one authorized record.
- `PUT /v1/tenants/{tenant}/records/{record}`: body `{"payload":{"label":"sample"},"expected_version":0}`, plus the `Idempotency-Key` header; creates (201), updates (200), replays exactly once (200), rejects stale versions/key reuse (409).

An access token **cannot grant database membership by itself**. Both the signed tenant/scope and active server-side PostgreSQL membership must match. Membership revocation blocks reuse of the very same signed token on the next request. Reads and writes use a DB transaction and `SELECT ... FOR SHARE` to coordinate with concurrent permission changes. There are no grant/revoke APIs exposed to clients.

## Run reproducibly (isolated test database only)

Install Python 3.11+ and Docker, then:

```bash
docker run --rm --name av-public-pg -e POSTGRES_USER=avdemo -e POSTGRES_PASSWORD=synthetic_only -e POSTGRES_DB=avdemo -p 127.0.0.1:55432:5432 -d postgres:16-alpine
python -m pip install -r requirements.txt
export ARAZVERA_PUBLIC_TEST_PG_DSN="postgresql://avdemo:synthetic_only@127.0.0.1:55432/avdemo"
python demo.py
python -m unittest discover -s tests -v
docker stop av-public-pg
```

On Windows PowerShell, replace `export ...` with `$env:ARAZVERA_PUBLIC_TEST_PG_DSN = "postgresql://..."`. Use a fresh disposable DB and a **local** Docker listener only. GitHub Actions provisions its own isolated PostgreSQL 16 service, runs this demo and its 14 negative-path/integration tests on Python 3.11 and 3.12, and runs the public history/secret scanner.

## Test matrix

The 14 tests prove: RS256 signature rejection, `alg=none` rejection, issuer/audience/time-bound checks, strict tenant isolation, current database membership, immediate revocation, read/write scope enforcement, actual persisted JSONB data, optimistic version checking, duplicate-safe idempotency, input limits, fail-closed database outage behavior, health redaction, and 404 handling. Keys are **generated in test memory**, not committed.

## Explicitly not provided

No OAuth/OIDC login or remote JWKS discovery, no managed external IdP, no token revocation/jti registry, no remote listener/TLS ingress, no PostgreSQL RLS, no customer data, no queue/ERP/CRM or paid external provider. `migrate()` and fixture `grant()` are trusted test/setup functions, never exposed over the HTTP service. **No commercial-production approval or SLA is implied.** See [public verification](../../docs/LEVEL2_VERIFIED_RESULTS.md) and [service matrix](../../docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md).

This independent public sample is maintained apart from the **private** reusable ARAZVERA Level 2 kit library.

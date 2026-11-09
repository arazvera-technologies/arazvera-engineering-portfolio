# ARAZVERA Level 2 | Verifiable Engineering Evidence

**Updated 9 November 2026.** The evidence below deliberately distinguishes public testable code from private starter-kit validation. Neither is external certification, commercial production deployment or guaranteed SLA.

## Public engineering cases

| Case | Tests | Actual integration | Key negative-path evidence | Boundary |
| --- | ---: | --- | --- | --- |
| Projects 01-05 | 10 | Small pure-Python and config simulations | Validation, idempotency and mocked adapters | No production systems |
| Project 06 - Reliable Webhook Pipeline | 16 | Real localhost HTTP + durable SQLite | Forged HMAC, replay conflict, lease recovery, retry, dead letter and manual reconciliation | Mock CRM only |
| Project 07 - Transactional Reconciliation | 21 | Real SQLite/CSV transactions | Stale version, injected rollback, bad inputs and concurrent batches | No real customer ERP |
| **Project 08 - Authorized PostgreSQL API** | **14** | **FastAPI TestClient requests, RS256 signatures and an actual PostgreSQL 16 database** | Cross-tenant denial, DB membership revocation, token failures, optimistic conflict, idempotent replay and DB outage | No external IdP, TLS ingress or RLS |
| **Total public cases** | **61** | **Eight runnable synthetic case studies** | Negative cases executed, not merely documented | No deployment acceptance |

Project 08 fixtures generate 2048-bit RSA signing keys in memory, supply explicitly trusted public JWKS, exercise HTTP authentication/authorization, and create disposable PostgreSQL tables. No customer secrets or private kit sources are committed.

**Test instructions:** `projects/08_postgres_auth_contract/README.md` documents a one-command disposable PostgreSQL container, fixed requirements and the same tests executed in GitHub Actions on Python 3.11 and 3.12.

[Public CI history](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions) - check the latest commit's `engineering-demos` jobs, which include a real PostgreSQL service and the public Git history scanner.

## Separate private engineering baseline (not publicly reproducible)

As of **9 November 2026**, the separate *private* Level 2 repository was verified at commit `2dadbe19330d0138afae23d7add88f9ce4b0e074`: **25 reusable starter-kit families**, mapping 30 service directions to initial private source, with **313 local tests passing** (0 failed, 0 errors, 0 skipped) against PostgreSQL 16. The private repository's main GitHub Actions run `42603689140` passed Python 3.11/3.12, Docker smoke and dependency review.

These private numbers are owner-reported engineering checks, not reproducible by anonymous public users. Their code, backup and customer credentials are intentionally excluded from the public repository. The phrase "30 directions" does **not** mean 30 production-ready products.

Level 1's separate historical recovery baseline was **172 tests** across four earlier private kit repositories, not part of the 61 public or 313 private Level 2 counts.

## Release and commercial boundaries

- Public source contains no production deployment, third-party integration keys or private client data.
- The real PostgreSQL case provides application-level tenant checks, **not database-enforced RLS**.
- Signed offline JWKS checking does **not** include real OAuth/OIDC login, remote key fetch, token revocation registry or TLS.
- The public n8n-to-FastAPI locally recorded example remains separate. The vendor n8n runtime has **not** been cleared for production deployment.
- Customer-specific provider access, contractual acceptance, incident response, monitoring, regulated data rules and supported deployments require independent sign-off.

The public repository runs a secret/history scan; a passing scan reduces exposure risk but is not a guarantee of zero vulnerabilities.

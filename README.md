# ARAZVERA TECHNOLOGIES | Engineering Portfolio

**Production-minded Python engineering | Secure APIs | Reliable Integrations | Transactional Data**

We build scoped backend and automation solutions with testable acceptance criteria, explicit failure handling, and clean delivery documentation. This public repository hosts **nine independently runnable, synthetic engineering case studies** (not deployed customer systems). It deliberately excludes the proprietary ARAZVERA starter-kit library and all customer credentials.

**[Level 3 specialist resume (PDF)](resumes/level-3/ARAZVERA_Level3_Backend_Reliability_Specialist_Profile_EN_20261109.pdf)** | **[Level 3 Word](resumes/level-3/ARAZVERA_Level3_Backend_Reliability_Specialist_Profile_EN_20261109.docx)** | **[Explore the advanced Level 2 service catalog](catalog/ARAZVERA_Level2_Client_Engineering_Catalog_EN_20261109.pdf)** | **[Level 2 resume (PDF)](resumes/level-2/ARAZVERA_Level2_Backend_Systems_Resume_EN.pdf)** | **[Service verification matrix](docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md)** | **[CI test runs](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions)**

## Featured engineering case studies

| Case | What runs | Evidence | Limits |
| --- | --- | --- | --- |
| **[09 - PostgreSQL RLS & Restore Lab](projects/09_postgres_rls_recovery/)** | Separate tenant DB logins, forced Row-Level Security and backup/restore rehearsal | **14 tests**: row bypass, role spoofing, unauthorized insert/update, rollback and version conflicts | Same-server synthetic database recovery only; not production Supabase or customer RLS audit |
| **[08 - Authorized PostgreSQL API](projects/08_postgres_auth_contract/)** | FastAPI + signed RS256 JWT + explicit PostgreSQL membership and versioned JSONB records | **14 tests**: tenant isolation, revocation, signature checks, optimistic updates, idempotent replay and outage failure; actual PostgreSQL 16 | Synthetic IdP only; no production RLS, TLS, OAuth login |
| **[06 - Webhook Reliability & Recovery](projects/06_resilient_webhook_pipeline/)** | Local signed HTTP ingress, SQLite event queue, leasing, retry and dead-letter recovery | **16 tests**: HMAC, concurrent deliveries, crash recovery, auditability and manual reconciliation | CRM adapter mocked; no vendor n8n runtime |
| **[07 - Transactional Data Reconciliation](projects/07_data_reconciliation_lab/)** | CSV validation, SQLite atomic import, idempotency, optimistic revisions and quarantine | **21 tests**: dry-run, rollback, version conflicts and concurrent batch processing | CSV/SQLite laboratory, not customer ERP/DB migration |
| **[01-05 - Targeted integrations](projects/)** | Small isolated Python prototypes for tenant notes, leads, human review, API contracts and Docker configuration | **10 tests** across five deliberately bounded samples | Demonstration modules, not customer-ready platforms |

**Public test evidence:** **75 tests across 9 projects** (61 Level 2 tests + 14 new database-enforced RLS tests). CI uses Python **3.11 and 3.12** with an actual disposable PostgreSQL 16 service, runs all demos, and audits public Git history for secrets. [Inspect live GitHub Actions](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions).

**Private engineering baseline (not publicly distributed):** 25 reusable starter-kit families mapped to 30 scoped service directions; **313 tests passing locally** against a separate disposable PostgreSQL 16, and private CI passing on Python 3.11/3.12, Docker smoke and dependency review as of **9 November 2026**. Private-kit tests are **not runnable or independently reviewable from this public repository**. The private source, bundle, supplier/customer secrets and internal build assets are not published.

## Level 3 specialist evidence (not a production credential)

The [PostgreSQL RLS and recovery lab](projects/09_postgres_rls_recovery/) is our **first Level 3 specialization proof**: 14 additional tests of actual database-enforced tenant isolation plus a verified restore into a second isolated database in the same disposable container. It is **not** 14 enterprise deployments, a SOC 2 audit or experience running Supabase production systems. See the [targeted Level 3 readiness plan](docs/LEVEL3_SPECIALIST_READINESS_20261109.md).

## What makes this Level 2 work

A good engineering deliverable handles failure, not only the happy path. These projects demonstrate explicit contracts around **authorization, request replay, stale writes, client-owned state, bounded retries, safe rollback and evidence capture**. Each case includes source code, test cases, a quick-start, and an honest account of what it does **not** prove.

```text
Client contract -> validated request -> verified identity/scope
        -> tenant-safe transaction / durable processing
        -> explicit receipt or fail-closed error -> tests & handover
```

Level 2 is an **internal delivery tier**, not a certification or a claim of enterprise production experience. The private starter kits accelerate client-specific engineering but cannot replace a signed scope, real provider authorization, production threat review, deployment tests or user acceptance.

## Services that can be scoped for clients

- **Secure Python / FastAPI backend:** typed endpoints, tenant isolation, RBAC boundary and negative-path tests.
- **Webhook and workflow reliability:** signed ingress, replay-safe queues, recoverable retries and audit events.
- **Data integrity and migration tooling:** validated imports, dry-run previews, optimistic versions and rollback.
- **CRM / ERP / API integrations:** bounded adapters and contract/fault testing; real account/API access supplied lawfully by the client.
- **Docker + CI delivery:** repeatable environment setup, health verification, protected release gates and handover.
- **Human-reviewed AI intake:** explicit uncertainty routes, review before actions, and model/API integration only when approved.

Browse the **[30-domain proof-status matrix](docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md)**. A mapped starter is not evidence that 30 full commercial services are deployed.

## Choose the right resume

| Tier | Focus | Current PDF |
| --- | --- | --- |
| Level 1 | Small Python fixes, utilities, single-step automation | [Level 1 resume](resumes/level-1/ARAZVERA_Level1_Engineering_Resume_EN.pdf) |
| Level 2 | Backend systems, integration reliability, transactions and secure boundaries | [Level 2 resume](resumes/level-2/ARAZVERA_Level2_Backend_Systems_Resume_EN.pdf) |

The legacy documents under `resumes/` are preserved as historical snapshots. See the [resume index](resumes/README.md) for current editable files.

## How a client engagement works

1. **Discovery:** define business outcome, dependencies, scope, data and legal/provider access.
2. **Acceptance contract:** agree endpoint schemas, negative-path tests, ownership, security gates and milestones.
3. **Engineering:** adapt a private reusable starter under the client contract; add integration tests and documented assumptions.
4. **Client-specific validation:** test in an authorized staging environment, including recovery, monitoring and release controls.
5. **Handover:** deliver agreed source, runbooks, deployment/recovery evidence and acceptance results.

Customer-owned VPS/API resources, credentials and approval gates remain in the customer's control. No direct trading, unauthorized account control, CAPTCHA bypass, unsupported production n8n runtime, guaranteed SLA or live customer deployment is represented by this repository.

## Independent verification

[Verified engineering results](docs/LEVEL2_VERIFIED_RESULTS.md) | [Workflow runs](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions) | [Public release audit source](tools/public_release_audit.py)

**Contact:** contact.arazvera@gmail.com

ARAZVERA TECHNOLOGIES — [GitHub organization](https://github.com/arazvera-technologies)

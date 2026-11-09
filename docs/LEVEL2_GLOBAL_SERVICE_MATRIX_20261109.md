# ARAZVERA TECHNOLOGIES — Level 2 Global Service Matrix

Research snapshot: **2026-11-09**. Public, client-safe roadmap. **Not a certification, award, signed contract, production-availability claim or guaranteed price list.** Do not infer Iran/payment eligibility from a "worldwide" job label.

## Positioning

Level 1: small code corrections, one-step scripts and short troubleshooting.
Level 2: **scoped modules and multi-step integrations with contracts, negative-path tests, safe retries, auditable state, handover and bounded client-specific rollout.** Indicative negotiated fixed-scope project band: **US $100–3,000**, not a rate card or assurance that a listing will pay this amount.
Level 3: broader architectures, multi-service operations, production SRE and complex integrations that require client infrastructure, proof of production experience and stronger delivery responsibility. Indicative discovery threshold **above $3,000** for multi-milestone scopes, not an automatic entitlement.

## Evidence labels

- **DEMO VERIFIED:** code and automated local tests are visible in this public repository; synthetic-only.
- **PRIVATE STARTER:** a separate reusable engineering prototype exists, but cannot be audited from this public source; client deployment unverified.
- **NEXT BUILD:** proposed; not yet implemented or tested here.
- **CLIENT DEPENDENCY:** depends on lawful provider access, real credentials, paid API, permitted geography or customer infrastructure.

## Opportunities organized by actual sellable deliverable

| # | Level 2 engineering service | Example bounded customer deliverable | Status on 2026-11-09 | Priority |
| --- | --- | --- | --- | --- |
| 01 | Python/FastAPI REST backend | 3–10 typed endpoints, validation, OpenAPI, tests | PRIVATE STARTER, simple public demo | P0 |
| 02 | Multi-tenant data boundaries | tenant-scoped CRUD, negative permission tests, no cross-tenant leakage | PRIVATE STARTER, simple public demo | P0 |
| 03 | Scoped RBAC and authorization audit | roles and permission matrix, deny-by-default tests | PRIVATE STARTER with demo tokens; real identity CLIENT DEPENDENCY | P0 |
| 04 | Signed webhook receiver | HMAC, timestamp window, durable event dedup, replay conflict | **DEMO VERIFIED: public project 06** | P0 |
| 05 | Persistent job processing | on-disk queue, atomic claim, state visibility, restart recovery | **DEMO VERIFIED: public project 06** | P0 |
| 06 | Retry / dead-letter / manual reconciliation | backoff, quarantine uncertain effects, operator-run recovery | **DEMO VERIFIED: public project 06** | P0 |
| 07 | CRM and lead integration | normalized intake, duplicates, review, mocked CRM adapter | PRIVATE STARTER, customer integration CLIENT DEPENDENCY | P0 |
| 08 | API-to-API orchestration | two service adapters, typed mapping, negative-path tests | PRIVATE STARTER, mock adapters only | P0 |
| 09 | Existing backend repair and hardening | bug reproduction, transaction review, regression suite | NEXT BUILD evidence pack | P0 |
| 10 | Data import and synchronization | CSV/JSON validation, schema mapping, versioned reconciliation | **DEMO VERIFIED: public project 07** (CSV/SQLite); JSON provider integration NOT BUILT | P0 |
| 11 | PostgreSQL schema and migration | Alembic revisions, rollback, constraints and data integrity | NEXT BUILD; PostgreSQL not verified here | P0 |
| 12 | Dockerized delivery module | nonroot image, local health endpoint, read-only runtime, smoke tests | PRIVATE STARTER; previous Docker CI separately verified | P0 |
| 13 | GitHub Actions and test automation | gated unit/integration tests, secret checks and audited release notes | DEMO VERIFIED for public repo CI baseline | P0 |
| 14 | Backup and restore proof | checksummed local snapshot, integrity test, restore on clean state | PRIVATE STARTER; customer infrastructure CLIENT DEPENDENCY | P0 |
| 15 | Lead pipeline and customer follow-up | multiple sources, human approval, no duplicate notifications | PRIVATE STARTER, actual channels CLIENT DEPENDENCY | P1 |
| 16 | n8n workflow quality engineering | workflow design, error-path tests, safe retry and handover | Level 1 isolated real n8n evidence; full vendor runtime security NOT CLEARED | P1 |
| 17 | CRM / ERP / inventory adapters | API mapping, stock event, audit and fault tests | NEXT BUILD, provider credentials CLIENT DEPENDENCY | P1 |
| 18 | Structured logging and operational metrics | event-state metrics, privacy-safe logs, audit and dashboards | project 06 basic auditable state; monitoring NEXT BUILD | P1 |
| 19 | Invoice and document automation | PDF reports, validated templates, business approval workflow | NEXT BUILD | P1 |
| 20 | Data-quality and scheduled ETL | clean/dedup, import jobs, retry and reconciliation receipts | **PARTIAL: public project 07** (batch preview, quarantine, safe commit); scheduling NOT BUILT | P1 |
| 21 | Human-reviewed AI intake | provider interface, uncertainty routing, user-approved records | PRIVATE STARTER with mock classifier; no live model | P1 |
| 22 | LLM provider abstraction | typed outputs, fallback control, spend/rate-limit logging | NEXT BUILD; live usage CLIENT DEPENDENCY | P1 |
| 23 | Lightweight internal reporting | operational statistics, filtered queries, client-safe export | NEXT BUILD | P1 |
| 24 | Client project starter generator | isolated project skeleton and editable configuration | PRIVATE STARTER, local automated tests | P1 |
| 25 | Internal notification and ticket routing | status-change rules, duplicate-safe outbox, approval workflow | NEXT BUILD | P1 |
| 26 | AI evaluation without model training | synthetic test cases, redaction and deterministic regression | NEXT BUILD | P2 |
| 27 | Retrieval / knowledge-base API | embedding adapter, citation mapping, access-control checks | NEXT BUILD; actual provider/index CLIENT DEPENDENCY | P2 |
| 28 | MQTT / IoT event ingestion backend | authorized broker-to-API event contract, isolation and replay tests | NEXT BUILD; broker CLIENT DEPENDENCY | P2 |
| 29 | Operator dashboard frontend | narrow review/metrics screen with safe role-filtering | NEXT BUILD | P2 |
| 30 | Production incident playbook | alert levels, testable restore, release and rollback evidence | NEXT BUILD, client deployment dependent | P2 |

## What we intentionally do not promise

- Video generation, generative video rendering, huge model training, local GPU inference for 24–32 GB models, paid commercial video/LLM APIs or unproven real-time voice infrastructure.
- Real customer CRM / Instagram / WhatsApp / payments connectivity without official access and signed terms.
- Unrestricted scraping, CAPTCHA bypass, sanctions/payment workarounds or unreviewed proprietary vendor runtimes.
- Certified security, 24/7 SLA, performance at scale, production uptime, enterprise compliance or 5+ years of commercial production experience based only on local demos.

## Priority build sequence — capability before résumé

1. Public project 06, real localhost signed HTTP + durable SQLite, concurrency, retry, unknown-outcome review: **implemented with 16 automated tests**.
2. Public project 07, atomic import, dry-run, revision reconciliation, quarantine, injected rollback and 21 tests: **implemented locally**.
3. Harden the public multi-tenant example with a real transaction-oriented PostgreSQL test fixture and deny-by-default auth boundary.
4. Extend data reconciliation to actual schema migrations, typed JSON contracts and PostgreSQL transaction checks (not yet built).
5. Add API integration contract testing for one fake CRM and one fake inventory service, with fault injection, timeouts and idempotent outbox.
6. Introduce structured telemetry, customer-readable handover, and a Docker smoke-test matrix.
7. Only after verifying additional capabilities update the Level 2 résumé/catalog so their technical claims surpass Level 1 and link directly to evidence.

## Differentiator: verified recovery, not flashy technology names

Strong proof demonstrates **what happens when a workflow fails halfway through**: a crash, a delayed response, conflicting webhook, cross-tenant request, wrong signature, duplicate input, retry exhaustion, or uncertain outcome. Every public project should include a reproducer, a test and a deliberate boundary. This is more defensible than claiming an "AI system" without proving its contracts.

## Demand research references (not endorsements or proof of eligibility)

- Webhooks into PostgreSQL, Python/FastAPI, Docker, hourly $30–60 **in the posted listing**: https://www.upwork.com/freelance-jobs/apply/Python-Developer-Data-Integration-Webhooks_~022107139072478696659/
- Multi-tenant SaaS, background jobs, secure APIs and observability demand: https://wellfound.com/jobs/4602425-backend-developer
- Business dashboard: Next.js, FastAPI, n8n, CRM/API integration: https://www.upwork.com/freelance-jobs/apply/Automated-Business-Dashboard-React-Python-FASTAPI-n8n-Workflow-Integration_~022114343563899151467
- FastAPI code-hardening, tenant/RBAC, migrations, log and recovery: https://www.upwork.com/freelance-jobs/apply/Backend-Developer-Harden-and-Finalize-Existing-Platform_~022098583900155323537/
- API security, webhooks, reconciliation and incident diagnosis: https://wellfound.com/jobs/4617751-senior-backend-and-integrations-engineer
- CI/CD, Docker, secure SaaS backend, object storage and documentation: https://wellfound.com/jobs/4191859-backend-lead-developer-node-js-postgresql-google-cloud

Some listed marketplaces and hiring regions may not permit applicants in Iran; this matrix is **technical demand research, not an application or eligible-lead list**. Prices in advertisements reflect particular projects, not market guarantees.

## Customer engagement and delivery boundary

Contracted client owns approved VPS, API accounts, keys, paid plans and compliance approvals. Agree scope, acceptance tests, change requests, payment mechanism and legitimate settlement in writing before using live systems. Keep ARAZVERA's reusable private engineering library separate from these public runnable samples.

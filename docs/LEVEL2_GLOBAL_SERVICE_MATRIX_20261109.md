# ARAZVERA | 30-Domain Level 2 Engineering Service Matrix

**Evidence snapshot: 9 November 2026.** This is a **scope and proof-status matrix**, not a claim that 30 services are deployed. Level 2 is an internal engineering tier, not a certification. All prices, contracts, provider/API access and acceptance conditions are defined for each client.

## Proof labels

- **PUBLIC - verified:** a self-contained synthetic public example runs and has tests visible in this repository.
- **PRIVATE - reusable starter:** one of the 25 proprietary private kit families maps to this topic; *not inspectable from public GitHub*. This does not mean a complete customer integration.
- **CUSTOMER-SCOPED:** substantial customer-specific access, engineering and acceptance are still required.
- **NEXT EVIDENCE:** public proof of the full requested feature is not available, even if a partial private starter exists.

## Concrete customer deliverables and limits

| # | Service direction | Example deliverable for a scoped contract | Evidence status (do not conflate) |
| --- | --- | --- | --- |
| 01 | Python / FastAPI REST backend | Typed endpoints, validation, OpenAPI and unit tests | **PUBLIC 08** authenticated HTTP; actual customer contract next |
| 02 | Multi-tenant boundaries | Tenant-scoped reads and writes, negative tenant tests | **PUBLIC 08** PostgreSQL + tenant checks |
| 03 | RBAC and authorization | Membership matrix, signed access token, deny-by-default tests | **PUBLIC 08** offline RS256, DB grants; hosted IdP next |
| 04 | Signed Webhook receiver | HMAC, timestamp window, duplicate/replay handling | **PUBLIC 06** synthetic local HTTP |
| 05 | Durable job handling | Persistent queue, atomic work claims and restart recovery | **PUBLIC 06** SQLite lab |
| 06 | Retry, dead letter, reconciliation | Bounded retry and explicit uncertain-outcome review | **PUBLIC 06** local test evidence |
| 07 | CRM and lead integration | Normalization, deduplication, authorized CRM mapping | **PRIVATE** starter; real CRM access CUSTOMER-SCOPED |
| 08 | API-to-API orchestration | Typed mappings, two adapters, contract and fault tests | **PUBLIC 04** mocked; production adapters CUSTOMER-SCOPED |
| 09 | Existing backend repair | Reproduce issue, regression test, focused code fix | **PRIVATE** starter mapped; customer repository needed |
| 10 | Data import and sync | Validated CSV import, dry-run, versioned safe updates | **PUBLIC 07** SQLite; actual target DB CUSTOMER-SCOPED |
| 11 | PostgreSQL design and migrations | Schema, constraints, migration/rollback and integrity | **PUBLIC 08** repeatable test DDL; Alembic/rollback NEXT EVIDENCE |
| 12 | Docker delivery | Nonroot service image, health check, tested packaging | **PUBLIC 05** config + private CI; production hardening CUSTOMER-SCOPED |
| 13 | GitHub Actions testing | CI matrix, integration DB, secret/history gate | **PUBLIC** active Python 3.11/3.12 + PG 16 |
| 14 | Backups and restoration | Checksummed snapshots, recovery proof and runbook | **PRIVATE** starter; client infrastructure acceptance needed |
| 15 | Lead follow-up | Approved events, idempotent notifications, handoff | **PRIVATE** starter; messaging permission needed |
| 16 | n8n reliability engineering | Error handling, workflow audit, controlled retry | Separate local evidence; **vendor runtime production BLOCKED** |
| 17 | CRM/ERP/inventory adapters | Normalize inventory and external records, error mapping | **PRIVATE** mapped starter; real provider/customer API needed |
| 18 | Telemetry and audit trails | Structured events, metrics and operational receipts | **PUBLIC 06** basic audit; full observability NEXT EVIDENCE |
| 19 | Document and invoice automation | Validated template rendering and review handoff | **PRIVATE** mapped starter; invoices/provider needs scoped work |
| 20 | Scheduled data quality/ETL | Validated batch ingest, quarantine, scheduled retry | **PUBLIC 07** batch; production scheduler NEXT EVIDENCE |
| 21 | Human-reviewed AI intake | Provider interface, confidence gates, manual approval | **PUBLIC 03** rules mock; live model CUSTOMER-SCOPED |
| 22 | LLM provider abstraction | Typed outputs, provider routing, cost controls | **PRIVATE** mapped starter; real API/customer billing needed |
| 23 | Internal reporting | Bounded, tenant-filtered record reports | **PUBLIC 08** read API; dashboards and BI NEXT EVIDENCE |
| 24 | Project starter generator | Scaffolding, tests and editable configuration | **PRIVATE** generator; tailored handoff needed |
| 25 | Internal notification routing | Approval workflow, retry-safe event dispatch | **PRIVATE** mapped starter; channels CUSTOMER-SCOPED |
| 26 | AI evaluation | Synthetic fixtures, regression tests and redaction | **PRIVATE** mapped starter; production evaluation NEXT EVIDENCE |
| 27 | Retrieval and knowledge APIs | Document access filters, search and citation contracts | **PRIVATE** mapped starter; actual model/index CUSTOMER-SCOPED |
| 28 | IoT / MQTT gateway | Validated event envelopes, tenant isolation and replay tests | **PRIVATE** mapped starter; broker/customer access needed |
| 29 | Operator dashboard | Narrow review and status interface with role filtering | **PRIVATE** mapped starter; production UI NEXT EVIDENCE |
| 30 | Incident response and recovery | Restore drill, staged release and rollback protocol | **PRIVATE** mapped starter; client operational runbook needed |

**Counts:** eight public case studies with 61 tests (47 previous + 14 public PostgreSQL API), distinct from 25 private reusable kit families with 313 separate local passing tests at private `main` commit `2dadbe1`. The 30 rows are **service directions**, not 30 production applications or commercial certifications.

## Practical offer ladder

1. **Focused engineering repair:** narrow bug or integration, acceptance test and a tested handoff.
2. **Level 2 verified module:** scoped API, transactional import or recoverable webhook with test report, documented boundaries and reviewable source.
3. **Customer deployment milestone:** only after provider access, staging approval, security/data ownership, backup/rollback and a signed acceptance checklist.

**Projects available to inspect:** [08 - PostgreSQL authorization](../projects/08_postgres_auth_contract/), [06 - Webhook recovery](../projects/06_resilient_webhook_pipeline/), [07 - Data reconciliation](../projects/07_data_reconciliation_lab/).

## Engagement boundaries

Customer owns all approved VPS, API tokens, paid provider services, account access, data and policy obligations. No guaranteed job eligibility, specific client pricing, real service uptime, unrestricted scraping or bypass of third-party rules is implied. No live trading, production n8n or external identity provider operation is authorized by these demonstrations.

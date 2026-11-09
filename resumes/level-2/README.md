# Level 2 | Backend Systems, API Integration & Reliability

[Portfolio home](../../README.md) | [All resume levels](../README.md) | [Level 1](../level-1/README.md)

**Current Level 2 resume — English, two pages, PDF + editable Word.**

- [Download Level 2 resume (PDF)](ARAZVERA_Level2_Backend_Systems_Resume_EN.pdf)
- [Download editable Level 2 resume (Word)](ARAZVERA_Level2_Backend_Systems_Resume_EN.docx)

Level 2 is an **internal contract-scoping tier**, not an accredited qualification. These examples are runnable synthetic evidence, **not production customer deployments**.

## Featured runnable projects

| Project | Implemented and tested engineering behavior | Tests |
| --- | --- | ---: |
| [06. Resilient Webhook & Job Recovery](../../projects/06_resilient_webhook_pipeline/) | HMAC signing, tenant-scoped durable processing, atomic job claims, retry/backoff, dead-letter recovery and audit/concurrency tests | [16](../../projects/06_resilient_webhook_pipeline/tests/test_pipeline.py) |
| [07. Atomic Data Reconciliation & Safe Import](../../projects/07_data_reconciliation_lab/) | Transactional CSV dry-run, batch idempotency, revision conflicts, quarantine, atomic rollback, SQLite persistence and concurrency | [21](../../projects/07_data_reconciliation_lab/tests/test_reconcile.py) |

Five additional public standalone examples have **10** tests, bringing the total to **47** across seven projects. Both Python 3.11 and 3.12 jobs passed in [public GitHub Actions run 42574597847](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions/runs/42574597847). See [verification details](../../docs/LEVEL2_VERIFIED_RESULTS.md).

The private Level 2 starter had 16 separately recorded tests and an isolated Python 3.12 Docker CI check. Historical Level 1 had 172 independently recorded tests; the totals are **not combined**.

## Ready-to-customize engineering delivery

Before a client engagement, we prepare scoped code modules, contract tests, sample outputs and handover documents. Per customer, we then adapt approved API/data mappings, credentials, hosting, security checks and acceptance scenarios. No delivery time or production readiness is promised before the customer-specific tests.

[Technical scope and proof matrix](../../docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md) | [Engineering catalog](../../catalog/ARAZVERA_Level2_Advanced_Engineering_Catalog_EN_20261109.pdf)

**Excluded:** unlicensed service access, unbudgeted paid APIs, AI video rendering and GPU-intensive model training. The self-hosted n8n production-runtime gate remains blocked pending supported security remediation.

**Contact:** contact.arazvera@gmail.com

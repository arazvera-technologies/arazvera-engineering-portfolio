# ARAZVERA TECHNOLOGIES — Engineering Portfolio

**Python • API Systems • Integration Reliability • Evidence-Based Automation**

An independent, public engineering portfolio showcasing **runnable synthetic prototypes**, real tests, and detailed limits. Level 2 is our internal delivery tier for scoped multi-component client projects, **not a certification**. This repository deliberately contains no private customer starter-kit sources, keys or commercial client data.

## 01 — Engineering Resumes

- [Level 2 engineering résumé (PDF)](resumes/ARAZVERA_Level2_Engineering_Resume_EN.pdf)
- [Level 2 résumé (editable Word)](resumes/ARAZVERA_Level2_Engineering_Resume_EN.docx)
- [Level 1 résumé (PDF)](resumes/ARAZVERA_Level1_Engineering_Resume_EN.pdf)
- [Level 1 résumé (editable Word)](resumes/ARAZVERA_Level1_Engineering_Resume_EN.docx)

**New technical evidence:** [Level 2 global services and proof matrix](docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md), which separates tested examples, private starters and not-yet-built capabilities. We update claims only after working tests, not by simply decorating an earlier résumé.

## 02 — Public Runnable Projects

### Flagship Level 2 engineering case

**[06 — Resilient Webhook & Job Recovery Lab](projects/06_resilient_webhook_pipeline/)** — a real localhost HTTP + SQLite system, **16 tested scenarios** covering:

- HMAC-signed Webhooks, timestamp verification, cross-tenant access denial
- Durable event processing, concurrent delivery, deduplication and replay conflicts
- Atomic job leasing, bounded retries and backoff
- Dead-letter recovery, uncertain side-effect quarantine and manual reconciliation
- Auditable transitions and process-restart persistence

Run with Python 3.11+ only; no paid APIs, cloud account, GPU or production n8n engine required. The demo has a functioning HTTP transport and a deliberately **mocked** CRM provider, not an active customer integration. All server listeners bind localhost.

### Second advanced Level 2 case — Data integrity and migration

**[07 — Atomic Data Reconciliation & Safe Import Lab](projects/07_data_reconciliation_lab/)** — a real CSV/SQLite system with **21 tests** for transaction-safe dry-run, idempotent batch import, versioned updates, quarantined records, concurrent same-batch processing, and injected-fault rollback. No paid provider or live customer data is used.

### Additional Level 2 topic samples

The five earlier synthetic examples are **smaller** than the flagship and demonstrate isolated behavior, not complete client products:

1. [Tenant isolation and idempotent notes](projects/01_multi_tenant_api/) — 2 tests, pure Python illustration
2. [Reliable lead queue](projects/02_reliable_leads/) — 2 tests, local mock
3. [Review-first text intake](projects/03_ai_intake/) — 2 tests, rules-only mock
4. [Mock API adapter and HMAC](projects/04_api_integration/) — 2 tests
5. [Docker configuration readiness](projects/05_docker_delivery/) — 2 tests, with separate private Docker runtime CI evidence

**Public automated tests:** 10 in the original five samples + 16 for project 06 + 21 for project 07 = **47 locally verified cases**. Prior [GitHub Actions run #42572071973](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions/runs/42572071973) proved six demos on Python 3.11/3.12; project 07 requires its own CI run before claiming new remote acceptance.

**Private reference baseline:** Level 1 had 172 documented passing recovery tests across four independent repositories. Private Level 2 had 16 locally passing tests in a separately verified source revision, plus a Python 3.12 Docker smoke job in private CI. None of these counts imply a production SLA.

## 03 — Services and Delivery Catalog

- [Level 2 global project and service research matrix — 30 specific services, with proof status](docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md)
- [Level 2 engineering services catalog (PDF — earlier portfolio snapshot)](catalog/ARAZVERA_Level2_Premium_Engineering_Catalog_EN.pdf)
- [Level 2 catalog (Word — earlier portfolio snapshot)](catalog/ARAZVERA_Level2_Premium_Engineering_Catalog_EN.docx)
- [Level 2 capability sheet (PDF)](catalog/ARAZVERA_Level2_Capability_Sheet_EN.pdf)
- [Editable capability sheet (Word)](catalog/ARAZVERA_Level2_Capability_Sheet_EN.docx)
- [Three contractor proposal drafts](catalog/ARAZVERA_Level2_Three_Proposal_Examples_EN.md)
- [Engineering verification and CI evidence](docs/LEVEL2_VERIFIED_RESULTS.md)

### What we intentionally exclude

No video generation, no GPU-heavy model training, no unverifiable enterprise capabilities, no unauthorized platform access or live customer credentials. A client may supply an authorized API or server for a separately scoped assignment, but such connectivity is **not part of the synthetic public evidence**.

## Verified n8n evidence and deployment boundary

We have a separate real, locally recorded two-minute n8n-to-FastAPI execution demonstration. Public viewing permission is not independently verified, so this repository does not link it. The official self-hosted n8n vendor runtime remains under a **separate production-security block** and is not distributed here.

The source code and tests prove local engineering behavior only. Every commercial customer integration requires legal eligibility, an approved environment, appropriate identity and authorization controls, external fault tests, client data rules, license checks, backups, performance review and signed acceptance.

**Contact:** contact.arazvera@gmail.com

**Organization:** https://github.com/arazvera-technologies

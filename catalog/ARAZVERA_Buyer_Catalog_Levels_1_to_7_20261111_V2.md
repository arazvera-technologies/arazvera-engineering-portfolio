# ARAZVERA TECHNOLOGIES
## Buyer Catalog — Seven Levels of Testable Engineering

**11 November 2026 | V2 client-facing edition | Independent freelance products**
**Contact:** contact.arazvera@gmail.com · [Portfolio and public demonstrations](https://github.com/arazvera-technologies/arazvera-engineering-portfolio)

### Choose by the problem to solve—not by a claimed certification

We scope **secure Python backends, recoverable integrations, evidence-based operations and bounded AI-agent controls**. Each engagement has a written problem statement, specific acceptance tests and transparent exclusions. **Levels 1–7 are internal categories**, not a third-party maturity or compliance grade. Public examples are synthetic engineering labs; private-source products are not deployed customer systems.

### Four ways to start a scoped project

| Buyer problem | Initial engagement we can propose | Example acceptance evidence |
| --- | --- | --- |
| An API or importer loses data, duplicates jobs or mishandles tenant boundaries | **API & data-integrity assessment / bounded repair** | Invalid-token and cross-tenant negatives, replay checks, transactional rollback tests |
| Webhooks, queues or workers fail after retries or restarts | **Integration reliability pilot** | Signed events, crash/restart rehearsal, dead-letter accounting, reproducible receipts |
| Changes are released without recovery or rollback evidence | **Resilience & recovery exercise** | Staging-only canary/HOLD decision, backup/restore integrity, incident audit trail |
| Agents or supplier records act without adequate controls | **Governance / evidence-quality preflight** | Denied tool actions, approval events, deterministic record validation and exception report |

These are **proposal templates**, not promises that one generic package fits every customer. We establish price, dates and IP rights only after scope and compliance review.

---

## Level 1 — Focused Python & automation

**Best for:** narrowly defined scripts, data formatting, targeted bug fixes, simple REST troubleshooting and repetitive operator tasks.

**Potential deliverables:** reviewed script/module, sample inputs and outputs, run instructions, small regression suite, documented assumptions.

**Evidence:** historical private Level 1 recovery baseline records **172 tests across four private engineering-kit repositories**. Private starter code is not public.

**Buyer provides:** redacted sample data, expected behavior, Python/runtime constraints and permission to test against any real service.

[Level 1 public profile](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/resumes/level-1/README.md)

## Level 2 — Authenticated APIs & transactional data

**Best for:** a business process needing a dependable backend boundary, reliable webhook delivery, or a reversible import.

**Potential deliverables:** FastAPI endpoint contracts, signed authentication checks, tenant isolation tests, idempotency, atomic import/reconciliation, Docker/CI and a testable handover.

**Evidence:** **9 runnable public synthetic cases with 75 automated tests**; separate private starter lab records **313 tests**. Public examples include [authenticated PostgreSQL API](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/tree/main/projects/08_postgres_auth_contract), [reliable webhooks](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/tree/main/projects/06_resilient_webhook_pipeline) and [safe reconciliation](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/tree/main/projects/07_data_reconciliation_lab).

**Buyer provides:** API specifications, authorized test account, data rules and deployment environment. Real identity-provider, CRM or ERP integration needs separate validation.

[Level 2 public profile](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/resumes/level-2/README.md)

## Level 3 — Backend reliability & security specialists

**Best for:** recurring incidents, unsafe tenant boundaries, lost background events, token validation defects and risky schema migrations.

**Potential deliverables:** a reproduced fault, isolated repair, tenant/RLS negative tests, transactional outbox recovery, JWT/JWKS validation, migration or rollback runbook.

**Evidence:** Level 3/4 set of **10 private specialist repositories** with CI success recorded at the 11 November checkpoint. Public [PostgreSQL RLS and restore lab](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/tree/main/projects/09_postgres_rls_recovery) is inspectable.

**Buyer provides:** written failure scenario, approved staging access, sanitized logs and acceptance rules. Enterprise IAM and production reliability claims require buyer-side verification.

[Level 3 specialist showcase](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/level-3/README.md)

## Level 4 — Resilience, controlled releases & recovery

**Best for:** teams needing change-risk evidence, worker recovery, PostgreSQL restore checks, observability and repeatable incident decisions.

**Potential deliverables:** synthetic/staging control-plane pilot, measured canary trial, HOLD/rollback evidence, recovery checklist and test report.

**Evidence:** isolated Level 4 lab has **129 documented local tests** and scoped hosted Docker CI evidence. Its Kubernetes/GitOps, DR or SLO components are **not** claimed to be customer production deployments.

**Buyer provides:** architecture, RPO/RTO objectives, staging infrastructure, recovery authorization and on-call ownership.

[Level 4 capability overview](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/level-4/README.md)

## Level 5 — Agent governance & bounded tool access

**Best for:** evaluation teams that want clear limits on which AI-agent actions are allowed, reviewed, budgeted and logged.

**Potential deliverables:** deny-by-default tool policies, reviewer gate, quota/budget checks, trace records, MCP manifest/schema checks and a restricted test gateway.

**Evidence:** **13 private SKU entries** (11 independent + 2 composites), **158 distinct local tests**, plus private hosted CI evidence.

**Not included by default:** production SSO, actual enterprise-tool enforcement, complete MCP interoperability, independent security accreditation.

**Buyer provides:** approved list of tools/actions, trust model, required reviewer roles, policy examples and a safe sandbox.

[Level 5 governance capabilities](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/docs/LEVEL5_PUBLIC_CAPABILITIES_20261111.md)

## Level 6 — Industrial & regulatory evidence preflight

**Best for:** teams assessing inconsistent supplier records or rehearsing structured evidence review before specialist compliance work.

**Three distinct synthetic pilot families:**
- **Battery supplier QA:** broken references, conflicting suppliers/models, duplicates and structured export checks.
- **CRA incident-readiness exercise:** evidence timelines, missing records and human-review prompts.
- **DORA ICT-provider record triage:** consistency and completeness checks on simulated provider data.

**Evidence:** latest documented suites cover **146 local tests** across these pilot families. These tools do **not** perform official regulatory filings, certify conformity or replace legal counsel.

**Buyer provides:** authorized data dictionary, non-sensitive examples and expert-approved regulatory interpretations.

[Level 6 detailed pilot catalog](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/docs/level6/ARAZVERA_Level6_Public_Capability_Catalog_EN.md)

## Level 7 — Three independent customer-adaptable modules

**1. Supplier Evidence Network v0.3.0:** versioned supplier data contracts, conflict validation, review and approved export; buyer-specific ERP/DPP work remains separate.

**2. AI Agent Security Control v0.2.0:** tenant tool policies, approvals, quotas and safe allowlisted text-tool execution; real buyer tool integrations require engineering and security review.

**3. Recovery Evidence Orchestrator v0.2.0:** multi-SQLite snapshot integrity and isolated recovery evidence; multi-host disaster recovery, PostgreSQL support and RPO/RTO certification are not claimed.

**Evidence:** **82 full local tests**, **71 retests after clean private package extraction**, **4 hosted CI jobs** on the latest documented commit. No independent enterprise acceptance or production audit has occurred.

**Buyer provides:** target schema/architecture, specific interfaces, authentication expectations, acceptance tests and their own VPS/API licenses.

[Level 7 three-product buyer catalog](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/catalog/level-7/README.md)

---

## Public evidence vs. private-source review

**Immediately inspectable:** nine synthetic case studies, their Python tests and public CI under [this GitHub portfolio](https://github.com/arazvera-technologies/arazvera-engineering-portfolio). Source-private modules, package archives, internal CI and customer credentials are **not** offered for anonymous download. A buyer can request a carefully scoped non-sensitive demonstration or a contractual private technical review where lawful and authorized.

**Important accounting:** test numbers above cover different suites, dates and code boundaries. They are **not additive** and do not measure production reliability or third-party certification.

## Engagement milestones and definition of done

1. **Written discovery:** business outcome, integration inventory, sample schema, risks, data classification, acceptance criteria.
2. **Proposal:** fixed deliverables or milestone scope; exclusions, dependency list, price, schedule, IP/source terms and acceptance owner.
3. **Isolated prototype:** synthetic inputs, explicit success and failure paths, tests recorded without customer secrets.
4. **Authorized customization:** approved APIs, customer-owned accounts, appropriate licensing and staged testing.
5. **Acceptance & handover:** agreed tests, change log, README/runbook, known gaps and owner sign-off. Production launch is a separate approved gate when needed.

### What we need from the buyer

Send **a short written brief** including the problem, current stack, redacted examples, expected outputs, target date, budget range if known, and your available staging/API/hosting options. **Never send secrets, private keys, customer personal data or live database dumps by email.**

**Email:** contact.arazvera@gmail.com
**Engineering resume:** [Public capability profile](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/blob/main/resumes/ARAZVERA_Client_Engineering_Profile_20261111_V2.md)

### Scope, rights and honesty

Nothing here represents a completed customer production rollout, independent security/compliance certification, guaranteed SLA, achieved sales, or a promise that API credentials alone make every system production-ready. Additional development, integration, legal/IP review, threat analysis, security testing and buyer acceptance may be necessary. The freelance portfolio is **strictly separate from AERON and Iran-specific projects**, with no technical connections among them.

The engineering owner operates in Iran. Any engagement must be permitted under applicable sanctions/export controls, licensing, privacy/data, contracting and lawful-payment requirements. Collaboration is in **asynchronous written English**.

# ARAZVERA TECHNOLOGIES | Level 3 Specialist Engineering

**Multi-tenant security · Reliable event processing · PostgreSQL recovery · JWT/JWKS identity assurance · Incident readiness**

> **Client-facing specialist capability portfolio.** We investigate complex backend failure modes, implement bounded repairs and safeguards, and deliver reproducible acceptance evidence. "Level 3" is an internal service tier, **not a certification, enterprise deployment history or production SLA**.

**[Specialist catalog PDF](../catalog/ARAZVERA_Level3_Specialist_Engineering_Catalog_EN_20261109.pdf)** · **[Editable Word catalog](../catalog/ARAZVERA_Level3_Specialist_Engineering_Catalog_EN_20261109.docx)** · **[Capability profile PDF](../resumes/level-3/ARAZVERA_Level3_Backend_Reliability_Specialist_Profile_EN_20261109.pdf)** · **[Public CI results](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions)** · **contact.arazvera@gmail.com**

## Five specialist engineering services

| High-value service | What we can engineer and test | Requires separate customer validation |
| --- | --- | --- |
| **1. Tenant isolation & authorization** | FastAPI permissions, restricted PostgreSQL roles, FORCE RLS, cross-tenant negative tests and policy reviews | Real customer IAM, schema and approved staging access |
| **2. Event reliability & transactional outbox** | Atomic business-event writes, leases and worker recovery, idempotency, bounded retry, dead-letter reconciliation | Destination-specific API semantics, load limits and operations |
| **3. Database recovery & safe change** | Backup/restore integrity, rollback, controlled transport-failure injection, migration and runbook evidence | Independent physical infrastructure, measured RPO/RTO and restore approval |
| **4. Public-key JWT / JWKS hardening** | Pinned issuer and audience, RS256 validation, signing-key rotation, invalid token and JWKS outage tests | Genuine enterprise OIDC/SSO identity provider, TLS, PKCE and secret lifecycle |
| **5. Release/incident risk controls** | Tenant-scoped operational metrics, fail-closed staging decisions, evidence gates, durable alert journaling and deduplication tests | Live telemetry, on-call paging, 24/7 support, real service monitoring |

We propose **bounded, acceptance-based contracts**: reproducible failure case, agreed tests, reviewed design, documented exclusions and client-owned handover. We do not present a simulated laboratory as a deployed customer platform.

## Open-source proof you can inspect now

| Public synthetic case | Source and tests | Verification |
| --- | --- | --- |
| [09 — PostgreSQL RLS & recovery](../projects/09_postgres_rls_recovery/) | Real PostgreSQL tenant role and policy boundaries, same-host restore | 14 tests |
| [08 — Authorized FastAPI/PostgreSQL](../projects/08_postgres_auth_contract/) | Signed JWT, authorization, idempotent and transactional writes | 14 tests |
| [06 — Resilient webhooks](../projects/06_resilient_webhook_pipeline/) | Signed ingress, bounded retry, dead letters, restart tests | 16 tests |
| [07 — Safe data reconciliation](../projects/07_data_reconciliation_lab/) | Atomic import, idempotency, rollback, quarantine | 21 tests |
| [01–05 — Scoped Python integrations](../projects/) | Small review, lead, validation and automation cases | 10 tests |

**Public baseline: 9 runnable synthetic cases / 75 automated tests**, with Python 3.11/3.12 and disposable PostgreSQL CI. [Inspect actual workflow results](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions).

## Additional proprietary engineering — demonstrated, not publicly distributed

The private Level 3 code is **not contained in this public repository**. Its recorded synthetic evidence includes:

| Private lab capability | Recorded verification |
| --- | --- |
| PostgreSQL transactional outbox and worker crash recovery | 21 unit tests + 12 Docker integration checks |
| Restricted FastAPI/RLS/independent worker and queue readiness | 19 integration checks |
| Mock-provider RS256 / pinned JWKS / key rotation and outage | 13 integration checks |
| Simulated localhost TCP-path cut and transaction rollback | 9 integration checks |
| Tenant-specific incident notification and durable receipt reconciliation | 11 integration checks |
| **Combined private unit-test suite** | **107 unit tests** |

The latest recorded private CI passed on **9 November 2026**. These private tests cannot be independently reproduced from this public source. We can provide a **reviewed technical walkthrough or separately contracted client-authorized staging demonstration**, without exposing proprietary code, third-party secrets or customer data.

## Why Level 3 is a higher-value service tier

| Tier | Typical scope | Responsibility |
| --- | --- | --- |
| **Level 1** | Scripts, small fixes and utilities | Feature correctness and documented delivery |
| **Level 2** | API development, transactional integrations and backend automation | Secure application contracts, tested failure paths and maintainable handover |
| **Level 3** | Multi-tenant boundaries, recovery integrity and change/incident safeguards | Threat and risk analysis, negative-path acceptance, rollback evidence and controlled release decisions |

**Proposed Level 3 quotation target: USD $150–$250+/hour**, or negotiated milestone pricing. This is **not an achieved rate, external market guarantee, previous invoice or client reference**. Actual price depends on scope, accountability, external costs and client acceptance.

## Delivery process

1. **Discovery:** Business risk, precise affected components, authorization and exclusions.
2. **Acceptance plan:** Tests for normal and failure paths, evidence, security boundaries and milestones.
3. **Engineering:** Scoped implementation in a client-approved environment.
4. **Verification and handover:** Runbooks, CI results, rollback/restore plan, limitations and signed acceptance.

**Not yet proven by these laboratories:** real corporate SSO integration, independently hosted multi-region failover, a guaranteed RTO/RPO or uptime SLA, genuine 24/7 paging and escalation, external enterprise security certification, or completed customer production deployments. These require separate lawful access and acceptance.

**Explore:** [Full Level 3 catalog and verification register](../catalog/ARAZVERA_Level3_Specialist_Engineering_Catalog_EN_20261109.md) · [Specialist résumé](../resumes/level-3/README.md) · [Readiness and current limitations](../docs/LEVEL3_SPECIALIST_READINESS_20261109.md) · [Portfolio home](../README.md)

**Contact:** contact.arazvera@gmail.com

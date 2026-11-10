# ARAZVERA — Tenant Isolation & PostgreSQL Restore Engineering Sprint

**Version:** 2026-11-10 | **Offer:** limited-scope engineering service, not a pre-certified database product

## The customer problem

Multi-tenant backends can leak one customer's records to another through application authorization bugs, database privilege errors, unsafe role changes, stale memberships or poorly tested backups. ARAZVERA can review and strengthen a specified tenant boundary, then test negative paths and recovery in an authorized staging environment.

## Proposed paid deliverables (subject to written scope)

1. Map the actual account, user, role and data model; identify where trust in client-provided tenant IDs would be unsafe.
2. Implement or review a specifically agreed tenant authorization approach: verified token claims, server-side membership checks, tenant-qualified transactions and/or an **appropriately designed** PostgreSQL RLS policy.
3. Test denial scenarios: cross-tenant read/write attempts, revoked access, forged claims, role elevation, SQL parameter boundaries, transaction conflict and replay.
4. Demonstrate a buyer-approved *disposable staging* database backup and restore; check roles, policies and record integrity after restore.
5. Deliver reproducible test results, a written risk/limitations report, migration/rollback notes and a written acceptance decision.

**RLS design is not portable automatically:** the public lab uses separate PostgreSQL logins per tenant and a SECURITY DEFINER lookup based on `session_user`. This does **not** make it a drop-in Supabase, shared-connection-pool, customer IAM or managed-SaaS implementation. Any real architecture requires a separate design review.

## Proof available today

- Public case 08: **14 passed** — FastAPI, locally generated RS256 signatures, active PostgreSQL membership, tenant-qualified API and versioned JSONB operations. Application filtering is used; this case does **not** implement RLS.
- Public case 09: **14 passed** — real PostgreSQL RLS, two separately authenticated tenant roles, least privilege and negative-path validation.
- A same-container synthetic PostgreSQL 16 backup/restore rehearsal passed, including rows, RLS policy state and post-restore tenant isolation.
- A repeatable local verifier creates a unique loopback-only disposable PostgreSQL container, runs these **28 tests** in copies of the cases, checks restore and cleans up its container.

No customer infrastructure, real identity provider, external data, penetration-test certification or production migration was used.

## Indicative commercial scope — not market-validated pricing

A written, bounded tenant-boundary audit/hardening and recovery rehearsal might be offered at **USD 3,000–5,500**, *only as an initial pricing hypothesis*. The final quote requires an architecture review and exact accepted scope. More integrations, enterprise IAM, full disaster recovery, exclusivity or post-release support are separate estimates.

A smaller fixed-price discovery and risk report may be proposed if the system is too large or risky for one implementation milestone.

Client owns hosting, databases, accounts, secrets and subscriptions. Private ARAZVERA source is not bundled into the publicly visible lab. Rights to adapted deliverables, nonexclusive licenses or exclusive IP transfer must be negotiated separately, in writing.

## Limitations and exclusions

No guarantee that RLS alone prevents all data leakage. No SOC 2, ISO 27001, HIPAA/GDPR certification or penetration test is asserted. No cross-region or fresh-cluster disaster-recovery exercise has been demonstrated. Cluster-global roles and secrets must be independently restored and checked in real recovery. No 24/7 SLA, production on-call, public login service or customer-approved release is included by default.

## Commercial and communication constraints

All discussions, technical evaluation, scope, reports and handover are **asynchronous written English only**; no audio/video/in-person calls. Contractor is based in Iran and must be disclosed truthfully. Contracting, export restrictions and any payment (including USDT) must be lawful and compliant for all parties before work or payment.

**Engineering evidence:** https://github.com/arazvera-technologies/arazvera-engineering-portfolio
**Contact:** contact.arazvera@gmail.com

# ARAZVERA | Level 3 specialization readiness

**Evidence recorded 9 November 2026. Not a production credential, certification or years-of-experience claim.**

## Chosen niche
**Backend reliability and multi-tenant data isolation** for existing SaaS applications: PostgreSQL policy boundaries, failed/missing authorization, idempotent external events, transaction integrity and evidence-based release gates.

This niche combines three observable public cases:
- [09 - PostgreSQL RLS & restore lab](../projects/09_postgres_rls_recovery/): **14 database-enforced tenant isolation tests** plus a same-server disposable restore exercise.
- [08 - Authorized PostgreSQL API](../projects/08_postgres_auth_contract/): 14 application/API authorization and transactional tests; explicitly **not** database RLS.
- [06 - Webhook replay/recovery](../projects/06_resilient_webhook_pipeline/): 19 HTTP, signed webhook, fenced-lease and reliable queue scenarios.
- [07 - Data reconciliation](../projects/07_data_reconciliation_lab/): 21 atomic import/rollback and concurrency tests.

Other public cases 01-05 contribute 10 additional focused tests. Public total after this RLS case: **78 tests across nine synthetic case studies**. Private Level 2 remains separate (25 reusable kit families, 313 recorded tests). A simulated case and a local restore do not prove a customer production deployment.

## Customer problems this supports approaching

1. **Multi-tenant authorization review:** review tenant boundary design, permissions, negative tests, SQL policy coverage and a written release-blocker list. Staging code and authorized access only.
2. **API and webhook reliability hardening:** trace duplicate deliveries and partial failures, add idempotency/recovery evidence, and repair a bounded workflow after reproducing the bug.
3. **Pre-release database recovery rehearsal:** inspect backup/migration plan, rehearse a restore in an isolated environment, compare integrity, and document what has not been verified.

Avoid pitching as an independent SOC 2 auditor, full penetration tester, production cloud architect, Supabase production specialist, Stripe payment-ledger author or SaaS SRE lead without external client proof and relevant credentials.

## Additional evidence needed before a true Level 3 production offer

- Contract for an authorized external IdP / customer session and a threat review.
- Controlled policy and migration changes with rollback tests in a disposable clone.
- Backup/restore drill on an independent server, including global roles and key handling.
- Concurrent multi-tenant load, role escalation and network failure injection.
- Monitoring, response thresholds, incident runbook and handover acceptance.
- At least one real customer-approved assignment/reference, or transparent equivalent independent review, before claiming shipped production experience.

## Proposal rule

State the exact verified commit, which tests were run, limits, expected client access, milestones, deliverables, exclusions, and who signs acceptance. A smaller verified job is more credible than claiming unproven enterprise-scale delivery. Do not add a $100+/hour rate to the resume as though it were achieved.

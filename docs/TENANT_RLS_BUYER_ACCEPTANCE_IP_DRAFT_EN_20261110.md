# Buyer Acceptance / Commercial Rights — Tenant Access & Restore

**2026-11-10 | Nonbinding engineering scope draft. Not an executed contract or legal advice.**

## Mandatory discovery before price or delivery

| Category | Buyer must specify |
| --- | --- |
| Application | Actual authorization architecture, framework, token issuer and lifecycle |
| Database | PostgreSQL version, tenant boundary, schemas, privileges, connection pooling and roles |
| Data | Record types, retention, classification, migration/backups and staging dataset |
| Access | Authorized staging endpoints, buyer-owned accounts, secret-management procedure |
| Downtime | Recovery point/time targets, rollback rules, incident owner and test windows |
| Law/contract | Contractor eligibility (Iran), export/payment restrictions, written-only process |
| Rights | Existing code provenance, third-party licenses, rights to custom deliverables |

## Proposed written acceptance tests

| Acceptance test | Required buyer-stage result |
| --- | --- |
| Verified token/account scope | Altered signatures and forged tenant claims are denied |
| Revoked membership | Previously issued tokens cannot override revoked server-side rights |
| Cross-tenant reads | Other tenants' data cannot be read through authorized APIs |
| Cross-tenant writes | Unauthorized records cannot be inserted, modified or deleted |
| Database privilege boundary | Restricted database role cannot bypass active row policy or escalate roles |
| Pooling/session policy | Tenant context isolation works with the buyer's actual connection strategy |
| Race and replay | Conflicting writes and repeated request IDs have agreed deterministic behavior |
| Backup/restore | Controlled restore retains agreed data, roles/policies and required grants |
| Recovery scope | New-cluster global roles, external identity keys and secrets are explicitly accounted for |
| Handover | Buyer receives test logs, risk register, release/rollback note and written acceptance |

Tests above are **proposed acceptance criteria**. Public synthetic cases do not prove any customer's implementation has satisfied them.

## Licensing and commercial options — negotiate before signature

1. **Fixed-scope engineering service:** deliver implementation/test patches and client-specific rights as defined in a written agreement; ARAZVERA retains its pre-existing independent reusable IP.
2. **Nonexclusive reusable component license:** separately identify the proprietary component inventory, licensee, permitted resale/customer usage, update entitlement and redistribution limits.
3. **Exclusive source transfer:** negotiate separate audited asset list, provenance, third-party restrictions, full payment and exclusivity boundaries. It is **not** included in a regular service quote.

Public sample code is provided as an independently viewable lab for evaluation, not as proof of unrestricted commercial resale. This draft grants no rights by itself.

## Evidence and delivery status

- [x] Public case 08: 14 tested contract scenarios on disposable PostgreSQL 16.
- [x] Public case 09: 14 tested database RLS scenarios on disposable PostgreSQL 16.
- [x] Same-container synthetic backup/restore proof: PASS.
- [x] Local one-command verifier for those two cases; 28 passed, zero skipped.
- [ ] Packaged buyer-review ZIP and independent extraction test.
- [ ] CI confirmation of newly published feature branch.
- [ ] Actual buyer requirements, threat model and authorized staging environment.
- [ ] Full production rollback and fresh-cluster disaster recovery.
- [ ] Signed customer acceptance, IP terms, lawful contracting/payment.
- [ ] No customer deployment, sale, security certification or SLA is yet verified.

**Safe selling proposition:** a scoped tenant-isolation engineering / QA engagement with acceptance tests, not a ready-to-buy turnkey IAM or database product.

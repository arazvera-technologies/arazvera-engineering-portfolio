# Buyer Acceptance & IP Checklist — Webhook/API Recovery

**Working draft, 2026-11-10 — for scoping, not legal advice or an executed contract.**

## Required inputs before a fixed-price quote

| Item | Must be confirmed in writing |
| --- | --- |
| Legal eligibility | Buyer, individual contractor in Iran, export/sanctions and lawful payment method |
| Provider | Exact upstream vendor, event types, official signature spec, webhook rate and version |
| Destination | Authorized CRM/ERP/SaaS API, credentials controlled by buyer, idempotency key support |
| Security boundary | Tenant/account separation, data classifications, retention, logging restrictions |
| Infrastructure | Buyer-controlled hosting, database, monitoring, deployment rights, test access |
| Success criteria | Expected duplicates, delayed retries, maximum queue age, acceptable recovery process |
| Ownership | License for original ARAZVERA code, rights for client-specific code, third-party licenses |
| Delivery boundary | Number of integrations, support window, excluded incidents and operational owner |

## Proposed acceptance matrix for a bounded single-integration sprint

| Test | Expected evidence |
| --- | --- |
| Valid signed delivery | Official provider's approved staging event accepted once |
| Missing/altered signature | Rejected without committing a side effect |
| Duplicate event/payload | Stable event identity; no duplicated confirmed destination action |
| Same ID/conflicting payload | Explicit conflict or quarantine, with audit record |
| Backoff/retry | Recoverable provider errors delayed and retried within documented bounds |
| Unknown downstream outcome | Manual investigation before a potentially duplicative retry |
| Worker crash & lease expiry | Stale worker cannot commit after replacement worker has claimed event |
| Destination throttling | Logged status and bounded recovery behavior with rate-limit policy |
| Process restart | Durable queue state and replay evidence retained |
| Buyer handover | Deployment steps, rollback instructions, alert interpretation and owner acceptance |

Every accepted test must be reproduced against the buyer's actual authorized provider and environment. Public synthetic tests are **separate evidence** and do not substitute for these acceptance tests.

## Source-code and commercial rights: choices to negotiate

**Option A — service / adapted delivery:** Buyer receives agreed client-specific source and use rights under a written agreement; the independently written public reference and general ARAZVERA reusable libraries remain separate.

**Option B — nonexclusive commercial component license:** A specified, privately delivered component may be licensed for a stated number of projects, clients or seats, subject to the written permitted-use, update and redistribution terms.

**Option C — exclusive transfer:** Separately negotiated asset inventory, provenance/IP audit, third-party permission review, exclusivity scope and full payment. No exclusivity is implied by an ordinary service quote.

No specific option is granted by this draft. An unsigned proposal or a preview file is **not** a grant of commercial redistribution rights. Publicly visible third-party components remain subject to their own licensing rules, and the exact rights to any code must be checked before exchange.

## Sales and delivery gate

- [x] Public webhook reference code runs locally, including 19 contract tests.
- [x] All nine public synthetic cases have a repeatable local Docker/PostgreSQL verifier: 78 passed, 0 skipped.
- [x] Repeatable local ZIP extraction and smoke tests were executed for the public review sample.
- [ ] Latest feature branch public CI must pass after push (local tests are not remote CI).
- [ ] Buyer-specific provider and deployment requirements not yet supplied.
- [ ] Buyer acceptance matrix not executed against a real integration.
- [ ] Paid license/IP agreement not yet approved or signed.
- [ ] Buyer compliance and payment eligibility not yet established.
- [ ] No sale or customer production deployment has been confirmed.

**Sales-safe statement:** Available now for **written enquiry and a scoped paid engineering proposal**, not as a preapproved turnkey, 24/7 production application.

# AI Agent Security Control — L7-002

**Version 0.2.0 — CUSTOMER_CUSTOMIZABLE_LAB_VERIFIED**
*Private source; safe, bounded customer-pilot evidence.*

### Buyer problem
Tool requests initiated by AI workflows should not rely on model
instructions alone for permission, spending or risky-action approval.

### Working, tested core
- Durable, tenant/agent/tool-scoped policy decisions, deny by default,
  quotas, idempotency and pending human approval/rejection.
- Separate local API principal roles for admin, executor, reviewer and
  auditor. Users do not select their own tenant via request body.
- Strictly allowlisted **real execution** of two harmless text utilities,
  SHA-256 hashing and character counting, after authorization.
- Repeated successfully completed requests return recorded results instead
  of executing again; changed payloads are rejected, unknown in-flight
  outcomes fail closed for manual investigation.
- Local nonroot Docker Compose API verified with a synthetic HTTP workflow.
- **18 focused tests passed** after fresh extraction, with shared suite and
  four hosted CI jobs also passing.

### Customer-specific, not yet included
Any real email/file/cloud/tool execution, customer MCP gateway, production
identity provider, OIDC, external approval identity, agent sandbox, actual
cross-platform enforcement, adversarial/security assessment or an SLA.
This lab proves a bounded technical pattern, **not** the safety of real
customer tools.

### Potential engagement
Paid adaptation of the policy-and-approval kernel *behind the buyer's
existing authenticated tool environment* with detailed negative-path tests
and written acceptance criteria. Limited private source rights subject to
IP/contract review.

Owner resides in Iran; all participation subject to lawful export,
contract and payment eligibility. Written English/asynchronous only.
No video/voice interviews.

**Contact:** contact.arazvera@gmail.com

[Back to Level 7 catalog](README.md)

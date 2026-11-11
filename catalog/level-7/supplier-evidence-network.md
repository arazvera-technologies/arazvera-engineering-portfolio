# Supplier Evidence Network — L7-001

**Version 0.3.0 — CUSTOMER_CUSTOMIZABLE_LAB_VERIFIED**
*Private Python source; source-free buyer summary.*

### Buyer problem
Different suppliers provide records using different formats, validation
rules and identifier conventions. Poorly reconciled upstream data may
break the customer's ERP, procurement or Digital Product Passport workflow.

### Working, tested core
- **Industry-neutral, versioned contracts** define arbitrary named fields,
  required flags, text/numeric/integer/boolean types and numeric bounds.
- Unique source mappings and pinned schema versions for each supplier/tenant.
- Imports with idempotency and cross-supplier identifier inconsistency
  detection, duplicate/missing/invalid field findings and review ledger.
- Human approval blocked while a record has unresolved validation findings;
  only approved records appear in the export.
- Backward-compatible local CSV/JSON operator interface and existing V1
  small battery-data preflight; V2 general-purpose engine is separate.
- Locally bound FastAPI with server-owned tenant identity, operator,
  reviewer and admin roles, plus nonroot Docker Compose pilot.
- **37 focused tests passed after fresh extraction** of the latest private
  source package; shared 82-test suite and local HTTP tests also passed.

### Customer-specific, not yet included
Live ERP, SAP, PLM, DPP registry or specific supplier connections;
workforce SSO/OIDC, production PostgreSQL cluster, full security review,
industrial-scale load tests, customer-defined retention and regulatory
conformity assessments. It is **not an EU-certified DPP issuer**.

### Potential engagement
A bounded paid supplier intake/reconciliation adapter to the customer's
approved schema, synthetic examples and acceptance tests. Separate
technical scope for real integration and support.

Owner based in Iran; buyer-specific lawful contracting/payment/export and
source-rights review required. English written-only collaboration, no
phone/video. Buyer funds and owns required servers and APIs.

**Contact:** contact.arazvera@gmail.com

[Back to Level 7 catalog](README.md)

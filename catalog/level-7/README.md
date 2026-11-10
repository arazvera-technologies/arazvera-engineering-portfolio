# ARAZVERA | Level 7 — Independent Engineering Products

**Private-source engineering products • Written-only B2B delivery • Controlled technical evaluation**

ARAZVERA TECHNOLOGIES develops software building blocks for enterprise data assurance, AI agent authorization and recovery verification. **Level 7** is an internal product category, not a regulator-issued certification or a claim of prior enterprise deployment. These three products are independent of the separate AERON research/infrastructure project; they do **not** connect to its servers, APIs or agents.

## Three focused products

| Product | Current implemented capability | Buyer problem | Maturity |
| --- | --- | --- | --- |
| [Supplier Evidence Network](supplier-evidence-network.md) | Tenant-scoped evidence imports, discrepancy findings, human review and authenticated local FastAPI boundary | Reconcile upstream supplier records before an existing ERP/DPP import | **v0.2.0 LAB_VERIFIED** |
| [AI Agent Security Control](agent-security-control.md) | Deny-by-default policy decisions, usage budget, human approval and audit record | Control whether an agent tool request *should be permitted* | **v0.1.0 LAB_VERIFIED** |
| [Recovery Evidence Orchestrator](recovery-evidence-orchestrator.md) | Transaction-consistent SQLite backup, SHA-256 checks and non-overwriting test restore | Prove that a local database backup can actually be recovered | **v0.1.0 LAB_VERIFIED** |

Each product is a **working, deliberately bounded laboratory module**, not a complete SaaS product, industrial certification solution, managed AI platform or disaster-recovery service.

## Verifiable engineering evidence

- **43 automated local tests** passed across the independent Level 7 workspace on Windows, Python 3.12 (recorded 10 November 2026).
- **Four GitHub Actions jobs passed** on Ubuntu/Windows with Python 3.11/3.12 in the **private** product repository. [View the run](https://github.com/arazvera-technologies/arazvera-level7-enterprise-labs-private/actions/runs/42911572920) (requires permitted private repository access).
- A source-free synthetic demonstration exercises supplier reconciliation, one human authorization decision, deny-by-default, and a verified SQLite restore.
- The supplier API was exercised over **real temporary localhost HTTP**: unknown key → 401, authorized import → 201, tenant B → zero access to tenant A records.
- Each source module was individually ZIP-packaged and run after fresh extraction: supplier v0.2 had **20 passing module tests**, agent and recovery v0.1 had **10 and 9** respectively.
- Signed customer contracts, independent security assessment, production deployment, regulatory conformance and actual market price: **not yet established**.

## Commercial engagement routes

**A. Narrow, paid proof of concept.** Agree synthetic input schemas, independently testable acceptance criteria and a fixed written scope.

**B. Nonexclusive private-source license.** Evaluate existing source under appropriate terms; usage, redistribution and derivative rights are separately negotiated after IP/licensing review.

**C. Bespoke engineering.** Implement the customer's authorised integration, identity, monitoring, security and deployment requirements under a separate agreement. A production SLA is not included in the present laboratory versions.

**D. Subsequent support.** Optional written maintenance/handover after acceptance. No response time or production guarantee is claimed in advance.

No unsupported list price is posted. A historic ambition for high-value enterprise engagements does not establish the value of the current laboratory source. The prospective price depends on source rights, actual deployment obligations, scope, legal eligibility and customer acceptance.

## What an authorised customer provides

A written description of the specific failure or bottleneck; synthetic or legally permitted sample records and interfaces; test acceptance criteria; designated technical reviewer; and any customer-owned production server, API access or paid third-party software required to complete integration. Private customer source and credentials are **not** requested as part of an unsolicited enquiry.

## Delivery and legal conditions

The independent contractor and owner are **genuinely based in Iran**. Any engagement is conditional on both parties confirming applicable sanctions, export, contractual, data/IP and **permitted payment** requirements. No currency or payment service is presented as a way around restrictions.

Collaboration is **asynchronous written English only**, supported by an AI writing assistant and verified source code/test reports. **No telephone, audio/video meetings or spoken interviews.** Human subject-matter experts and qualified regulatory reviewers are separately identified if the customer requires legal/compliance conclusions.

**Contact:** contact.arazvera@gmail.com

[Supplier product brief](supplier-evidence-network.md) · [AI governance brief](agent-security-control.md) · [Recovery brief](recovery-evidence-orchestrator.md) · [Technical capability profile](../../resumes/level-7/ARAZVERA_Level7_Engineering_Profile_EN.md) · [Buyer scoping checklist](engagement-checklist.md)

*Portfolio updated 10 November 2026. No proprietary source is published in this public catalog.*

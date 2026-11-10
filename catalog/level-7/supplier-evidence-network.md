# Supplier Evidence Network — ARAZVERA L7-001

**Version 0.2.0 | LAB_VERIFIED | Private source; public facts only**

## The buyer problem

Data arriving from multiple suppliers can contain missing or conflicting identifiers, missing evidence references, invalid numeric fields or duplicate submissions. The proposed deployment is a **source-record preflight and human review layer** before an already-authorized ERP/DPP workflow—not a competing Battery Passport issuer.

## What runs today

- Bounded, local Python ingestion of four-field supplier records via **CSV/JSON CLI**, persisted in SQLite.
- Cross-field checks for missing identifiers, missing document references, duplicate external identifiers **within an import**, and invalid capacity values.
- Per-tenant request-key deduplication; altered retry payloads are rejected rather than silently replayed.
- Record review workflow: operator submissions; reviewer approval/rejection; approvals blocked while unresolved findings remain.
- Event audit log and local machine-readable reporting.
- Optional **FastAPI v0.2.0** over localhost with server-configured API keys bound to tenant and operator/reviewer roles. The caller cannot change their tenant by adding a request field.
- **20 specific tests passed** after clean extraction of the latest private-source ZIP. Real localhost smoke: no key → HTTP 401; authorized import → 201; other tenant cannot read the submitted record.

## Honest exclusions

Not implemented or verified: SAP/ERP production connectors, real DPP registry integration, formal EU Battery Passport field-conformance, external identity verification/OIDC, enterprise authorization review, end-to-end TLS/reverse-proxy deployment, production PostgreSQL cluster, customer data protection assessment, scale benchmarking, incident response SLA, or buyer acceptance. A shared API key is not a production IAM substitute.

This is **not** merely the same L6-BESS offline CSV engine with a new name: the Level 7 version contains durable import identities, a human review state, tenant scoping, auditable decisions and an authenticated localhost HTTP boundary. Full network-scale enterprise operation is still a subsequent paid engineering phase.

## Example narrowly scoped engagement

A customer supplies a synthetic subset of their existing import schema, an explicit rule and 5–10 agreed failure examples. ARAZVERA implements a schema adapter and deterministic regression report in a self-hosted test environment. The customer reviews output and independently approves acceptance criteria.

Commercial licensing, documentation, deployment effort, legality and payment are quoted **after** confirmation. Contractor based in Iran; written asynchronous English only, no calls.

**Contact:** contact.arazvera@gmail.com

[Back to Level 7 catalog](README.md)

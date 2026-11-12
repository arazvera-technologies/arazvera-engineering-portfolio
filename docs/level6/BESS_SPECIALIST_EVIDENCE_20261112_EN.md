# Level 6 | Battery Supplier Evidence Preflight — Specialist Lab Evidence

**ARAZVERA TECHNOLOGIES · L6-BESS-001 v0.2.0 · 12 November 2026**

[Interactive public overview](https://huggingface.co/spaces/arazvera-technologies/engineering-evidence-showcase) · [Two-page buyer brief (PDF)](https://huggingface.co/spaces/arazvera-technologies/engineering-evidence-showcase/resolve/main/ARAZVERA_L6_BESS_SPECIALIST_PILOT_BRIEF_EN.pdf) · [Synthetic evidence summary (JSON)](https://huggingface.co/spaces/arazvera-technologies/engineering-evidence-showcase/resolve/main/SPECIALIST_EVIDENCE_SUMMARY_20261112.json)

> **Status:** Private-source laboratory candidate. **Not** a certified Battery Passport platform, production deployment, or customer-accepted integration. Proprietary source remains private.

## Buyer problem

A battery manufacturer, importer, or DPP integrator may receive pack, supplier, evidence and event records in different formats. The existing Python preflight tool identifies potential technical inconsistencies before those exports enter an existing data or ERP workflow. It does not authenticate documents or determine legal compliance.

## Reproduced laboratory evidence

| Fictional test case | Tested operation with the separate L6 engine | Findings |
| --- | --- | ---: |
| Valid four-table CSV | Offline supplier evidence preflight | **0** |
| Deliberately defective CSV | Offline scan with discrepancy reports | **14** |
| Vendor-alias JSON | Explicit mapping to canonical CSV, then scan | **0** |
| Local synthetic ERP HTTP response | Actual loopback fetch from `127.0.0.1`, then scan | **0** |

Canonical data tables: `packs`, `suppliers`, `documents`, `events`. The engine produces deterministic CSV/JSON findings, text summaries and SHA-256 receipts.

**Test provenance:** 72/72 automated tests included in the independently extracted private v0.2.0 source ZIP were rerun and passed on Windows Python 3.12 on 12 November 2026. An earlier, wider laboratory workspace had reported 79 tests; seven additional workspace-level tests were not present in the extracted ZIP and **were not rerun in this specialist exercise**. Eight separate source-free packaging/integrity tests also passed and are not part of the 72.

The public Hugging Face browser demonstration contains **five simplified independent illustration rules**. Clicking that demo does not execute the proprietary Level 6 engine. The PDF is a source-free account of an independently rerun synthetic lab, not a copy of private code.

## Proposed synthetic-only buyer pilot (not yet undertaken)

1. Written verification of buyer identity, intended country, civilian end use and ability to contract and pay a real engineering owner **resident in Iran** under all applicable rules.
2. One jointly defined battery category, one synthetic supplier export and an explicit, agreed four-table schema mapping.
3. Agreed positive and negative fixtures, expected findings, deterministic CSV/JSON reports and integrity hashes.
4. Execution in an approved buyer-owned staging environment, human technical review and written buyer PASS/FAIL acceptance.
5. Separate SOW for any production ERP OAuth, hosted service, third-party security review, additional data source or licence.

**Not implemented:** Full EU Battery Passport issuance, complete category/date regulatory data-point applicability, Registry or QR registration, independent certification, real buyer ERP integration, actual customer data handling, a production SLA, or a completed customer acceptance test.

**Commercial scope:** We discuss specific, bounded requirements through written English email. Any fee, delivery date, IP licence or support term is negotiated only after legal eligibility and an agreed statement of work; no price or full-compliance equivalence is claimed by this page. Client-owned paid APIs, cloud, hosting and other services are separately scoped.

**Contact:** contact.arazvera@gmail.com

**Evidence boundaries:** Public profile and PDF share no private engine, customer records, credentials, hidden network endpoints or internal pricing.

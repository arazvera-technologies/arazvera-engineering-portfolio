# ARAZVERA — Verified Engineering Evidence (09 Nov 2026)

## Separate test counts, not a combined certification

- Level 1 historical baseline: **172 passing Python tests**, across four restored, private engineering-kit repositories. These are development environment tests. No production uptime has been verified.
- Level 2 private prototypes (five projects plus safe client generator): **11 passing Python tests**, independently restored and retested from a local private Git recovery bundle.
- Level 2 public synthetic demos: **10 passing built-in `unittest` cases**, two per independent, runnable demo.

These groups are distinct deliverables. The counts do not certify external APIs, SaaS availability, external training, customer integrations or commercial deployment safety.

## Current GitHub Actions

- [Private Level 2 build - PASS](https://github.com/arazvera-technologies/arazvera-level2-private-engineering-portfolio/actions/runs/42532266274): Python tests and dependency review passed. The private source is not shared publicly.
- [Public Level 2 sample build - PASS](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions/runs/42532374737): all five synthetic samples ran, local Python tests passed, and file/history safety scan completed.

## Real local n8n demonstration

A separate, isolated local n8n-to-FastAPI lead-intake demonstration passed five synthetic end-to-end HTTP scenarios (201, 200, 422, 202, 503). The two-minute video has not been verified as publicly accessible; therefore it is deliberately not linked in this public repository.

## Production and licensing boundaries

No Level 2 prototype is production ready. The self-hosted n8n engine release gate remains blocked pending vendor-supported security acceptance. Any client-owned n8n Cloud deployment requires account ownership, authorized live backend access, credentials, real end-to-end tests and a separate license/contract acceptance.

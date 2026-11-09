# ARAZVERA — Verified Engineering Evidence (09 Nov 2026)

**Evidence categories must remain separate. These are not certifications or commercial-production acceptance.**

| Evidence | Locally verified results | Scope |
| --- | --- | --- |
| Level 1 private recovery | 172 tests PASS | Four separately restored engineering-kit repositories (historical) |
| Level 2 private engineering | 16 tests PASS | Five private prototypes / generator; private commit 93607b8 |
| Private Docker runtime CI | 3 jobs PASS in earlier recorded pipeline | Python 3.12 synthetic Docker delivery, local HTTP health and restricted runtime. NOT n8n runtime |
| Original five public examples | 10 tests PASS | Two tests per independent synthetic Python demonstration |
| New public flagship, project 06 | **16 tests PASS** in local Windows Python 3.12 | Actual localhost HTTP, HMAC verification, concurrency, SQLite durable processing, backoff, dead-letter, review and lease failure paths |
| Public combined local tests | **26 tests PASS** (10 original + 16 new) | No external API, paid cloud provider, or customer production environment |

## Evidence and actual commands

Project 06: enter projects/06_resilient_webhook_pipeline and execute:

~~~bash
python demo.py
python -m unittest discover -s tests -v
~~~

Observed local demo: HTTP 201, initial synthetic CRM retry, backoff hold, second successful attempt, process-reopen state complete, auditable transitions; zero failed tests (16 run).

The new public GitHub Actions run [#42571777541](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions/runs/42571777541) completed successfully for **Python 3.11 and Python 3.12**, including six executable demos, all public tests and the full-history secret scan. This is CI evidence for a synthetic reference lab, not an independent security certification.

Earlier verified jobs (prior to this update):
- [Private Level 2 Actions run](https://github.com/arazvera-technologies/arazvera-level2-private-engineering-portfolio/actions/runs/42532266274)
- [Previous public sample Actions run](https://github.com/arazvera-technologies/arazvera-engineering-portfolio/actions/runs/42532374737)

## Material release limits

The new project is a **local synthetic interoperability lab**, not a licensed managed integration or a public Internet-ready API. The HMAC fixture key and demo admin token are fake. Commercial deployment requires an approved identity provider, security/privacy review, customer-owned provider accounts, stable database, load and recovery tests and a separate owner acceptance.

A real, isolated n8n-to-FastAPI execution passed five synthetic HTTP scenarios (201/200/422/202/503), but the full self-hosted n8n runtime remains **BLOCKED** for production pending supported remediation. The two-minute recorded video is not linked until public-access permissions are verified.

Refer to [the Level 2 global services matrix](LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md) for every service's proof status and next development milestone. A job listing is not an engagement, qualification or guaranteed rate.

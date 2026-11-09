# Level 2 — Resilient Webhook & Job Recovery Lab

A **runnable**, open-source-friendly **synthetic reference implementation** of an integration reliability pipeline. This is a new, independently written public example — not a copy of ARAZVERA's private customer templates.

Unlike a happy-path automation demo, this project models failure, concurrency, persistence, and unknown outcomes.

## Run without paid API, cloud, Docker or pip installs

Requires Python 3.11+ standard library only.

~~~shell
python demo.py
python -m unittest discover -s tests -v
~~~

The demo starts an **actual HTTP server bound to 127.0.0.1** on an ephemeral port, POSTs a signed webhook, performs a synthetic failed CRM delivery, honors retry backoff, completes the follow-up, reopens the SQLite database and verifies persistence. The executable self-check exits nonzero if any acceptance condition fails.

## Supported contract (local-only)

| Operation | Contract |
| --- | --- |
| POST /v1/webhooks/{tenant} | HMAC SHA-256 over timestamp, tenant, event ID and exact raw body; returns 201 for new, 200 duplicate, 409 conflicting replay, 401 bad signature |
| GET /v1/events/{tenant}/{event_id} | Synthetic demonstration token checks tenant; exposes status and attempt count but **no original payload** |
| GET /health | Reports explicit production_approved: false |
| Worker run_once(now=...) | Atomic durable SQLite claim, bounded retries, backoff, durable state and audit |
| Review resolve(..., "applied" or "retry") | Operator-confirmed reconciliation of ambiguous or dead-lettered events; does **not** guess if an external action happened |

**State machine:** pending → leased → complete; or leased → retry → leased; or leased → dead_letter; or leased → needs_review (including expired lease). Manual review may resolve a quarantined event as already applied or explicitly clear it for another attempt.

**Atomicity model:** SQLite BEGIN IMMEDIATE plus unique (tenant, event_id) constraint supports concurrent local intake and single-worker claims. No claim of exactly-once side effects across external services: downstream providers must also support idempotency, and a lost acknowledgement must be reconciled.

## Verification scenarios

16 standard-library tests cover HMAC tampering/staleness, replay conflict, tenant boundaries, durable reopen, 8-way concurrent ingest, two concurrent claims, bounded retries, backoff, dead-letter recovery, uncertain-outcome quarantine, expired leases, audit trail, invalid inputs, and real localhost HTTP responses.

## Why this matters to a client

A CRM, ERP, lead funnel or order-integration project usually has to handle retries, dropped network responses, duplicate events and manual recovery. This starter demonstrates reusable mechanisms and a testing pattern, rather than promising a production integration for an unknown customer.

### Explicit limitations

- All credentials and CRM calls are fake; **no commercial provider is connected**.
- Synthetic token access in http_api.py is **not a production authentication scheme**.
- SQLite is a single-node prototype; production requires transaction design, monitored migrations, encrypted credentials, measured throughput, separate worker processes and a supported DB/broker.
- No actual n8n runtime is installed or distributed here; its vendor security gate is a separate issue.
- No customer records, payment systems, public sockets, cloud deployment or live LLM APIs are used.
- A real deployment also needs threat modeling, legal/platform permissions, secret rotation, GDPR/customer data rules, backup, load testing, incident recovery and owner sign-off.

**Business scope:** candidate module for a paid, narrowly scoped Level 2 project after requirements and customer-provided legal infrastructure are established; NOT an off-the-shelf production application.

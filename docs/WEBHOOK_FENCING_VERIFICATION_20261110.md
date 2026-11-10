# Webhook Lease Fencing — Verification Record

**Date:** 2026-11-10
**Status:** Local lab hardening verified; production and PostgreSQL integration acceptance **not complete**.

## Resolved defect
A stale worker could previously finish a job after its lease expired and the event was claimed by a newer worker. The local SQLite event pipeline now issues a unique per-claim `lease_token` and checks both the token and the lease deadline before accepting a completion. Expiration and operator decisions clear the token. Existing SQLite events migrate by adding the token column without discarding pending work.

## Evidence checked
- Project 06 isolated test suite: **19 passed**, including stale-reclaim fencing, expiry-before-sweep and legacy-schema upgrade.
- All 9 public case directories, each in its own Python process: **50 passed, 28 skipped, 0 failures**.
- The 28 skipped cases are PostgreSQL-backed cases 08 and 09. Their real-database behavior was **not revalidated** in this execution.
- Root-level `pytest` is not a supported invocation of these cases because multiple folders use a `demo.py` module and `test_demo.py` filename; importing them in one interpreter causes test collection collisions. Use the isolated runner below.
- Docker Desktop's Linux engine was not responding, and PostgreSQL on local TCP 5432 was unavailable during this check.

## Reproduction
From the repository root:

```powershell
python tools/verify_public_cases.py
python tools/verify_public_cases.py --require-postgres
```

The strict command currently **blocks** unless both `ARAZVERA_PUBLIC_TEST_PG_DSN` and `ARAZVERA_L3_ADMIN_DSN` are explicitly set to disposable PostgreSQL test databases. Never run the destructive RLS fixture against a customer database.

## Remaining acceptance gates
1. Provision authorized disposable PostgreSQL 16, configure the two test DSNs and execute strict verification; record exact pass/skip counts.
2. Confirm GitHub CI on an up-to-date, conflict-free branch and run independent install/replay tests.
3. Conduct customer-specific integration tests and legal/IP/license review before selling a turnkey implementation.
4. Confirm the live provider's idempotency contract and train the operator to reconcile uncertain outcomes.

This record verifies **local lab behavior only**. It does not assert production rollout, a customer deployment, 24/7 availability, exactly-once downstream effects, or a guaranteed fixed sale price.

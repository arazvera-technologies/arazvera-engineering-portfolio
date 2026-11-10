# Webhook Lease Fencing — Verification Record

**Date:** 2026-11-10
**Status:** All nine public synthetic case suites passed in isolated local execution; production acceptance **not complete**.

## Resolved defect
A stale worker could previously finish a job after its lease expired and the event was claimed by a newer worker. The local SQLite event pipeline now issues a unique per-claim `lease_token` and checks both the token and the lease deadline before accepting completion. Expiration and operator decisions clear the token. Existing SQLite events migrate by adding the token column without discarding pending work.

## Current verification evidence
- Project 06 isolated suite: **19 passed**, including stale-reclaim fencing, expiry-before-sweep and legacy-schema upgrade.
- All 9 public case suites: **78 passed, 0 skipped, 0 failed** when run separately in isolated Python processes.
- PostgreSQL-backed cases 08 and 09: **14 + 14 passed** against an actual disposable PostgreSQL 16 Alpine container, using separate synthetic databases `l2public` and `l3proof`. The container was bound to localhost port 55439; no customer database or secrets were used.
- Strict verification exit code **0**. The runner also correctly blocks with code 2 when required PostgreSQL DSNs are missing.
- The root-level `pytest` invocation causes import collisions because multiple folders use module names `demo.py` and `test_demo.py`; the per-project process runner avoids those collisions.
- Public content scan: **125 files scanned, zero findings**. Git history audit was **not completed** in that scan.

## Reproduction
From the repository root:

```powershell
python tools/verify_public_cases.py
python tools/verify_public_cases.py --require-postgres
```

The strict command requires `ARAZVERA_PUBLIC_TEST_PG_DSN` and `ARAZVERA_L3_ADMIN_DSN` pointing explicitly to disposable local PostgreSQL databases. The RLS fixture resets synthetic tables and must never be aimed at a real customer database.

## Remaining acceptance gates
1. Reconcile this local worktree with the latest GitHub main without overwriting parallel work; run independent CI on the reconciled branch.
2. Repeat clean installation and archive/replay checks for the exact deliverable package.
3. Conduct customer-specific authorized integration tests, legal/IP/license review, and contract acceptance before selling a turnkey implementation.
4. Confirm the live provider's idempotency contract and operator procedures for reconciling uncertain external outcomes.

This record verifies **local lab behavior only**. It does not assert production rollout, a customer deployment, 24/7 availability, exactly-once downstream effects, or a guaranteed sale price.

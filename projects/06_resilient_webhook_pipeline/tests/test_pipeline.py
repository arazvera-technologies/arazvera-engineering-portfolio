"""Black-box contract tests for a local-only, durable webhook reliability lab."""
import json
import sqlite3
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import (
    EventPipeline, WebhookSigner, ConflictError, SignatureError,
    RetryableError, UncertainOutcome, TransitionError, Worker,
)
from http_api import make_server


class Adapter:
    def __init__(self, failures=0, unknown=False):
        self.failures = failures
        self.unknown = unknown
        self.calls = []

    def send(self, event):
        self.calls.append((event["tenant"], event["event_id"]))
        if self.unknown:
            raise UncertainOutcome("downstream response lost")
        if len(self.calls) <= self.failures:
            raise RetryableError("temporary mock outage")
        return {"receipt": "synthetic-" + event["event_id"]}


class PipelineContracts(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = str(Path(self.directory.name) / "event-queue.sqlite")
        self.store = EventPipeline(self.path)
        self.payload = {"kind": "demo", "customer": "Example Customer"}

    def ingest(self, tenant="alpha", event_id="evt-001", payload=None):
        return self.store.ingest(tenant, event_id, payload or self.payload)

    def test_hmac_signed_payload_expiry_and_tampering(self):
        signer = WebhookSigner(b"fixture-key-not-a-production-secret")
        body = b'{"kind":"lead"}'
        sig = signer.sign("alpha", "evt-001", 1000, body)
        signer.verify("alpha", "evt-001", 1000, body, sig, now=1001)
        with self.assertRaises(SignatureError):
            signer.verify("alpha", "evt-001", 1000, b'{"kind":"other"}', sig, now=1001)
        with self.assertRaises(SignatureError):
            signer.verify("alpha", "evt-001", 1000, body, sig, now=1400)
        with self.assertRaises(SignatureError):
            signer.verify("beta", "evt-001", 1000, body, sig, now=1001)

    def test_idempotency_and_conflicting_reuse(self):
        first = self.ingest()
        duplicate = self.ingest()
        self.assertTrue(first["created"])
        self.assertFalse(duplicate["created"])
        self.assertEqual(first["id"], duplicate["id"])
        with self.assertRaises(ConflictError):
            self.store.ingest("alpha", "evt-001", {"kind": "other"})
        self.assertEqual(self.store.counts("alpha")["pending"], 1)

    def test_tenant_isolation_and_audit(self):
        self.ingest()
        self.ingest("beta")
        self.assertIsNotNone(self.store.get("alpha", "evt-001"))
        self.assertIsNotNone(self.store.get("beta", "evt-001"))
        self.assertIsNone(self.store.get("alpha", "event-only-in-beta"))
        self.assertEqual(self.store.counts("beta")["pending"], 1)
        self.assertEqual(len(self.store.audit("alpha", "evt-001")), 1)

    def test_persists_across_process_reopen(self):
        self.ingest()
        reopened = EventPipeline(self.path)
        self.assertEqual(reopened.get("alpha", "evt-001")["state"], "pending")
        self.assertEqual(reopened.counts("alpha")["pending"], 1)

    def test_atomic_duplicate_ingress_across_threads(self):
        result = []
        start = threading.Barrier(8)
        def insert():
            start.wait()
            result.append(self.store.ingest("alpha", "concurrent", self.payload))
        threads = [threading.Thread(target=insert) for _ in range(8)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        self.assertEqual(len(result), 8)
        self.assertEqual(sum(v["created"] for v in result), 1)
        self.assertEqual(self.store.counts("alpha")["pending"], 1)

    def test_two_workers_cannot_claim_same_job(self):
        self.ingest()
        results = []
        barrier = threading.Barrier(2)
        def claim():
            barrier.wait()
            results.append(self.store.claim(now=1000))
        t1 = threading.Thread(target=claim)
        t2 = threading.Thread(target=claim)
        t1.start(); t2.start(); t1.join(); t2.join()
        self.assertEqual(sum(v is not None for v in results), 1)
        self.assertEqual(self.store.get("alpha", "evt-001")["attempts"], 1)

    def test_workflow_success_has_receipt_and_no_duplicate_send(self):
        self.ingest()
        adapter = Adapter()
        worker = Worker(self.store, adapter)
        self.assertEqual(worker.run_once(now=1000)["state"], "complete")
        self.assertIsNone(worker.run_once(now=1001))
        self.assertEqual(len(adapter.calls), 1)
        self.assertEqual(self.store.get("alpha", "evt-001")["state"], "complete")

    def test_retry_waits_for_backoff_before_reclaim(self):
        self.ingest()
        adapter = Adapter(failures=1)
        worker = Worker(self.store, adapter)
        self.assertEqual(worker.run_once(now=1000)["state"], "retry")
        self.assertIsNone(worker.run_once(now=1000.5))
        self.assertEqual(worker.run_once(now=1001)["state"], "complete")
        self.assertEqual(len(adapter.calls), 2)

    def test_dead_letter_after_bounded_retries_and_manual_redrive(self):
        self.ingest()
        failing = Worker(self.store, Adapter(failures=10), max_attempts=2)
        self.assertEqual(failing.run_once(now=1000)["state"], "retry")
        self.assertEqual(failing.run_once(now=1001)["state"], "dead_letter")
        self.assertIsNone(failing.run_once(now=10000))
        self.assertEqual(self.store.counts("alpha")["dead_letter"], 1)
        self.assertTrue(self.store.resolve("alpha", "evt-001", "retry", now=10010))
        self.assertEqual(Worker(self.store, Adapter()).run_once(now=10010)["state"], "complete")

    def test_uncertain_outcome_quarantined_not_blindly_retried(self):
        self.ingest()
        worker = Worker(self.store, Adapter(unknown=True))
        self.assertEqual(worker.run_once(now=1000)["state"], "needs_review")
        self.assertIsNone(worker.run_once(now=10000))
        self.assertTrue(self.store.resolve("alpha", "evt-001", "applied", now=10001))
        self.assertEqual(self.store.get("alpha", "evt-001")["state"], "complete")

    def test_expired_worker_lease_moves_to_review_not_duplicate_send(self):
        self.ingest()
        self.assertIsNotNone(self.store.claim(now=1000, lease_seconds=2))
        self.assertEqual(self.store.recover_expired_leases(now=1001), 0)
        self.assertEqual(self.store.recover_expired_leases(now=1003), 1)
        self.assertIsNone(self.store.claim(now=1004))
        self.assertEqual(self.store.get("alpha", "evt-001")["state"], "needs_review")

    def test_stale_worker_cannot_finish_after_reclaim(self):
        self.ingest()
        old_job = self.store.claim(now=1000, lease_seconds=2)
        self.assertEqual(self.store.recover_expired_leases(now=1003), 1)
        self.store.resolve("alpha", "evt-001", "retry", now=1004)
        new_job = self.store.claim(now=1004, lease_seconds=10)
        self.assertIsNotNone(new_job)
        with self.assertRaises(TransitionError):
            self.store._finish(old_job, state="complete", now=1005,
                               receipt={"receipt": "stale"})
        self.assertEqual(self.store.get("alpha", "evt-001")["state"], "leased")
        self.assertEqual(self.store._finish(new_job, state="complete", now=1005,
                                            receipt={"receipt": "fresh"})["state"], "complete")

    def test_expired_worker_cannot_finish_before_recovery_sweep(self):
        self.ingest()
        job = self.store.claim(now=1000, lease_seconds=2)
        with self.assertRaises(TransitionError):
            self.store._finish(job, state="complete", now=1003)
        self.assertEqual(self.store.get("alpha", "evt-001")["state"], "leased")

    def test_legacy_sqlite_schema_upgrades_without_losing_jobs(self):
        legacy = str(Path(self.directory.name) / "legacy.sqlite")
        with sqlite3.connect(legacy) as db:
            db.execute(
                "CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tenant TEXT NOT NULL, event_id TEXT NOT NULL, payload TEXT NOT NULL, "
                "digest TEXT NOT NULL, state TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, "
                "next_attempt REAL NOT NULL DEFAULT 0, lease_until REAL, receipt TEXT, "
                "UNIQUE(tenant,event_id))"
            )
            db.execute(
                "INSERT INTO events(tenant,event_id,payload,digest,state) VALUES(?,?,?,?,?)",
                ("alpha", "legacy-event", '{"kind":"demo"}', "old-digest", "pending")
            )
        db.close()  # sqlite3's context manager commits but does not close on Windows.
        upgraded = EventPipeline(legacy)
        self.assertEqual(upgraded.get("alpha", "legacy-event")["state"], "pending")
        job = upgraded.claim(now=1000)
        self.assertTrue(job["lease_token"])
        self.assertEqual(upgraded._finish(job, state="complete", now=1001)["state"], "complete")
        self.assertEqual(upgraded.get("alpha", "legacy-event")["state"], "complete")

    def test_manual_resolution_requires_review_or_dead_letter(self):
        self.ingest()
        with self.assertRaises(TransitionError):
            self.store.resolve("alpha", "evt-001", "applied", now=1000)
        with self.assertRaises(ValueError):
            self.store.resolve("alpha", "evt-001", "ignored", now=1000)

    def test_validation_rejects_invalid_tenant_and_payload(self):
        with self.assertRaises(ValueError): self.store.ingest("../oops", "evt-001", self.payload)
        with self.assertRaises(ValueError): self.store.ingest("alpha", "", self.payload)
        with self.assertRaises(ValueError): self.store.ingest("alpha", "evt1", ["not", "an", "object"])

    def test_audit_records_transition_history(self):
        self.ingest()
        self.assertEqual(Worker(self.store, Adapter()).run_once(now=1000)["state"], "complete")
        events = [v["action"] for v in self.store.audit("alpha", "evt-001")]
        self.assertEqual(events, ["accepted", "leased", "completed"])


class HttpContracts(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.store = EventPipeline(str(Path(self.directory.name)/"http.sqlite"))
        self.signer = WebhookSigner(b"fixture-key-for-http-synthetic-only")
        self.server = make_server(self.store, {"alpha": self.signer}, {"demo-admin-alpha": "alpha"})
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.root = f"http://127.0.0.1:{self.server.server_address[1]}"

    def send(self, path, body=None, headers=None, method="GET"):
        request = urllib.request.Request(
            self.root + path, data=body, headers=headers or {}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=4) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_real_http_webhook_signing_status_and_tenant_access(self):
        raw = b'{"kind":"synthetic lead","source":"test"}'
        timestamp = 1000
        # The test server accepts an injected deterministic verification clock.
        self.server.verification_clock = lambda: 1000
        headers = {
            "Content-Type": "application/json",
            "X-Event-Id": "external-lead-001",
            "X-Timestamp": str(timestamp),
            "X-Signature": self.signer.sign("alpha", "external-lead-001", timestamp, raw)
        }
        code, result = self.send("/v1/webhooks/alpha", raw, headers, "POST")
        self.assertEqual(code, 201)
        self.assertTrue(result["created"])
        code, repeat = self.send("/v1/webhooks/alpha", raw, headers, "POST")
        self.assertEqual(code, 200)
        self.assertFalse(repeat["created"])
        code, denied = self.send("/v1/events/alpha/external-lead-001")
        self.assertEqual(code, 401)
        code, allowed = self.send("/v1/events/alpha/external-lead-001",
            headers={"X-Demo-Token": "demo-admin-alpha"})
        self.assertEqual(code, 200)
        self.assertEqual(allowed["state"], "pending")
        code, cross = self.send("/v1/events/beta/external-lead-001",
            headers={"X-Demo-Token": "demo-admin-alpha"})
        self.assertEqual(code, 403)
        code, health = self.send("/health")
        self.assertEqual((code, health["mode"]), (200, "local-synthetic"))

    def test_http_tampering_and_invalid_json(self):
        self.server.verification_clock = lambda: 1000
        raw = b'{"kind":"real"}'
        headers = {"Content-Type": "application/json", "X-Event-Id": "id-1",
            "X-Timestamp": "1000",
            "X-Signature": self.signer.sign("alpha", "id-1", 1000, raw)}
        code, _ = self.send("/v1/webhooks/alpha", b'{"kind":"tampered"}', headers, "POST")
        self.assertEqual(code, 401)
        code, _ = self.send("/v1/webhooks/alpha", b"{", headers, "POST")
        self.assertEqual(code, 401)


if __name__ == "__main__":
    unittest.main()

"""Contract-first tests for safe, audit-ready inventory data reconciliation."""
from __future__ import annotations

import tempfile
import threading
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reconcile import DataSync, BatchConflict, parse_inventory_csv


class ReconcileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = str(Path(self.tmp.name) / "inventory.sqlite")
        self.sync = DataSync(self.path)
        self.a = {"external_id": "sku-1", "title": "Synthetic Item", "quantity": 5, "revision": 1}
        self.b = {"external_id": "sku-2", "title": "Sample Item", "quantity": 9, "revision": 1}

    def run_batch(self, rows=None, *, tenant="alpha", source="shop", batch="batch-1", preview=False, fail_after=None):
        fn = self.sync.preview if preview else self.sync.apply
        args = (tenant, source, batch, rows if rows is not None else [self.a])
        if fail_after is not None:
            return fn(*args, fail_after=fail_after)
        return fn(*args)

    def test_initial_insert_counts_and_sorted_snapshot(self):
        report = self.run_batch([self.b, self.a])
        self.assertEqual((report["inserted"], report["updated"], report["rejected"]), (2, 0, 0))
        self.assertEqual([x["external_id"] for x in self.sync.snapshot("alpha", "shop")], ["sku-1", "sku-2"])

    def test_idempotent_batch_replay_no_double_write(self):
        first = self.run_batch()
        second = self.run_batch()
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(second["digest"], first["digest"])
        self.assertEqual(len(self.sync.snapshot("alpha", "shop")), 1)

    def test_batch_id_collision_different_payload_fails(self):
        self.run_batch()
        with self.assertRaises(BatchConflict):
            self.run_batch([{**self.a, "quantity": 500}])
        self.assertEqual(self.sync.snapshot("alpha", "shop")[0]["quantity"], 5)

    def test_tenant_scoping_prevents_leakage(self):
        self.run_batch()
        self.run_batch([{**self.a, "quantity": 77}], tenant="beta")
        self.assertEqual(self.sync.snapshot("alpha", "shop")[0]["quantity"], 5)
        self.assertEqual(self.sync.snapshot("beta", "shop")[0]["quantity"], 77)
        self.assertEqual(self.sync.rejections("beta", "shop", "batch-1"), [])

    def test_source_namespace_scoping(self):
        self.run_batch()
        self.run_batch([{**self.a, "quantity": 8}], source="erp")
        self.assertEqual(self.sync.snapshot("alpha", "shop")[0]["quantity"], 5)
        self.assertEqual(self.sync.snapshot("alpha", "erp")[0]["quantity"], 8)

    def test_dry_run_is_read_only_and_matches_commit_plan(self):
        preview = self.run_batch([self.a, self.b], preview=True)
        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["inserted"], 2)
        self.assertEqual(self.sync.snapshot("alpha", "shop"), [])
        self.assertEqual(self.sync.audit("alpha", "shop", "batch-1"), [])
        result = self.run_batch([self.a, self.b])
        self.assertEqual(result["digest"], preview["digest"])

    def test_mid_batch_failure_rolls_back_all_rows(self):
        with self.assertRaises(RuntimeError):
            self.run_batch([self.a, self.b], fail_after=1)
        self.assertEqual(self.sync.snapshot("alpha", "shop"), [])
        self.assertEqual(self.sync.audit("alpha", "shop", "batch-1"), [])
        self.assertEqual(self.run_batch([self.a, self.b])["inserted"], 2)

    def test_higher_revision_updates_without_duplicate_entity(self):
        self.run_batch()
        updated = {**self.a, "title": "Revised Item", "quantity": 12, "revision": 2}
        report = self.run_batch([updated], batch="batch-2")
        self.assertEqual(report["updated"], 1)
        self.assertEqual(self.sync.snapshot("alpha", "shop")[0]["quantity"], 12)

    def test_older_revision_is_quarantined_not_applied(self):
        self.run_batch([{**self.a, "revision": 3}])
        old = {**self.a, "quantity": 3, "revision": 2}
        report = self.run_batch([old], batch="batch-2")
        self.assertEqual((report["rejected"], report["updated"]), (1, 0))
        self.assertEqual(self.sync.snapshot("alpha", "shop")[0]["quantity"], 5)
        self.assertEqual(self.sync.rejections("alpha", "shop", "batch-2")[0]["reason"], "STALE_REVISION")

    def test_same_revision_conflicting_change_is_quarantined(self):
        self.run_batch()
        report = self.run_batch([{**self.a, "quantity": 20}], batch="batch-2")
        self.assertEqual(report["rejected"], 1)
        self.assertEqual(self.sync.snapshot("alpha", "shop")[0]["quantity"], 5)

    def test_same_revision_same_data_is_unchanged(self):
        self.run_batch()
        self.assertEqual(self.run_batch(batch="batch-2")["unchanged"], 1)
        self.assertEqual(len(self.sync.snapshot("alpha", "shop")), 1)

    def test_duplicate_identifiers_in_one_batch_are_quarantined(self):
        report = self.run_batch([self.a, self.a])
        self.assertEqual((report["inserted"], report["rejected"]), (1, 1))
        self.assertEqual(self.sync.rejections("alpha", "shop", "batch-1")[0]["reason"], "DUPLICATE_BATCH_ID")

    def test_invalid_rows_quarantined_without_raw_pii(self):
        private = {"external_id": "bad", "title": "private@example.test", "quantity": -1, "revision": 1}
        report = self.run_batch([self.a, private])
        self.assertEqual((report["inserted"], report["rejected"]), (1, 1))
        audit = self.sync.rejections("alpha", "shop", "batch-1")
        self.assertEqual(set(audit[0]), {"external_id", "reason"})
        self.assertNotIn("private@example.test", str(audit))

    def test_validation_rejects_invalid_tenant_and_batch(self):
        for tenant in ("../../bad", "", "a", "BAD"):
            with self.assertRaises(ValueError):
                self.run_batch(tenant=tenant)
        with self.assertRaises(ValueError):
            self.run_batch(source="../shop")
        with self.assertRaises(ValueError):
            self.run_batch(batch="x")

    def test_rejects_oversized_batch(self):
        with self.assertRaises(ValueError):
            self.run_batch([self.a] * 501)

    def test_persistent_reopen_keeps_revision_and_batch_ledger(self):
        self.run_batch()
        recovered = DataSync(self.path)
        self.assertEqual(recovered.snapshot("alpha", "shop")[0]["revision"], 1)
        self.assertTrue(recovered.apply("alpha", "shop", "batch-1", [self.a])["replayed"])

    def test_simultaneous_same_batch_only_one_is_applied(self):
        start = threading.Barrier(5)
        results = []
        errors = []
        def task():
            try:
                start.wait()
                results.append(self.sync.apply("alpha", "shop", "batch-z", [self.a]))
            except Exception as exc:
                errors.append(exc)
        threads = [threading.Thread(target=task) for _ in range(5)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        self.assertEqual(errors, [])
        self.assertEqual(sum(not x["replayed"] for x in results), 1)
        self.assertEqual(len(self.sync.snapshot("alpha", "shop")), 1)

    def test_csv_utf8_and_malformed_values(self):
        blob = b"external_id,title,quantity,revision\nsku-1,Example,7,1\nsku-2,Bad,invalid,1\n"
        parsed = parse_inventory_csv(blob)
        result = self.run_batch(parsed)
        self.assertEqual((result["inserted"], result["rejected"]), (1, 1))

    def test_csv_rejects_missing_headers_and_oversize(self):
        with self.assertRaises(ValueError):
            parse_inventory_csv(b"x,y,z\n1,2,3")
        with self.assertRaises(ValueError):
            parse_inventory_csv(b"z" * 200000)

    def test_audit_stores_actions_not_raw_customer_data(self):
        self.run_batch()
        rows = self.sync.audit("alpha", "shop", "batch-1")
        self.assertEqual([x["action"] for x in rows], ["batch_applied"])
        self.assertNotIn("Synthetic Item", str(rows))

    def test_sha_digest_stable_against_mapping_field_order(self):
        self.run_batch(preview=True)
        reordered = dict(reversed(list(self.a.items())))
        a = self.run_batch([self.a], preview=True)["digest"]
        b = self.run_batch([reordered], preview=True)["digest"]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()

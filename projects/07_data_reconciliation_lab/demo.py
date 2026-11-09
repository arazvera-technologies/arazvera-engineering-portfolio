"""Offline, reproducible batch reconciliation with transactional dry-run and rollback."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from reconcile import DataSync, parse_inventory_csv


def main():
    with tempfile.TemporaryDirectory() as directory:
        store = DataSync(Path(directory) / "inventory.sqlite")
        rows = parse_inventory_csv(
            b"external_id,title,quantity,revision\n"
            b"sku-a,Synthetic Book,4,1\n"
            b"sku-b,Sample Pen,20,1\n"
            b"sku-c,Invalid Quantity,-99,1\n"
        )
        preview = store.preview("alpha", "shop", "batch-first", rows)
        no_writes = store.snapshot("alpha", "shop") == []
        committed = store.apply("alpha", "shop", "batch-first", rows)
        replay = store.apply("alpha", "shop", "batch-first", rows)
        update = store.apply(
            "alpha", "shop", "batch-second",
            [{"external_id": "sku-a", "title": "Synthetic Book", "quantity": 7, "revision": 2}]
        )
        before_failed = store.snapshot("alpha", "shop")
        try:
            store.apply(
                "alpha", "shop", "batch-fault",
                [{"external_id": "sku-d", "title": "Fault Demo", "quantity": 10, "revision": 1}],
                fail_after=1,
            )
        except RuntimeError:
            pass
        rolled_back = store.snapshot("alpha", "shop") == before_failed
        result = {
            "demo": "ARAZVERA Level 2 atomic data reconciliation",
            "preview_insertions": preview["inserted"],
            "preview_wrote_nothing": no_writes,
            "committed_insertions": committed["inserted"],
            "quarantined_invalid_rows": committed["rejected"],
            "identical_batch_replayed": replay["replayed"],
            "revision_update_count": update["updated"],
            "fault_injection_rolled_back": rolled_back,
            "persisted_records": DataSync(store.path).snapshot("alpha", "shop"),
            "production_approved": False,
        }
        print(json.dumps(result, indent=2))
        assert (
            result["preview_wrote_nothing"]
            and result["committed_insertions"] == 2
            and result["quarantined_invalid_rows"] == 1
            and result["identical_batch_replayed"]
            and result["revision_update_count"] == 1
            and result["fault_injection_rolled_back"]
        ), "Reconciliation demo acceptance failed"


if __name__ == "__main__":
    main()

"""Atomic CSV-to-SQLite reconciliation demo. Synthetic and local-only.

Demonstrates batch replay safety, revision conflict quarantine, preview
transactions and fault-injection rollback. NOT a production ETL service.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path


IDENT = re.compile(r"^[a-z][a-z0-9-]{1,39}$")
BATCH = re.compile(r"^[a-z][a-z0-9-]{2,99}$")
ITEM = re.compile(r"^[a-zA-Z0-9._:-]{2,100}$")
FIELDS = ("external_id", "title", "quantity", "revision")


class BatchConflict(ValueError):
    pass


def parse_inventory_csv(blob: bytes) -> list[dict]:
    """Read only a bounded, explicitly named inventory fixture."""
    if not isinstance(blob, bytes) or len(blob) > 128 * 1024:
        raise ValueError("CSV bytes must be supplied, maximum 128 KiB")
    try:
        text = blob.decode("utf-8-sig", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV must be UTF-8") from exc
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
        raise ValueError("Required CSV columns missing")
    rows = []
    for row in reader:
        if len(rows) >= 500:
            raise ValueError("Batch exceeds 500 records")
        rows.append({k: row.get(k) for k in FIELDS})
    return rows


def _integer(value, *, min_value, max_value):
    if isinstance(value, bool):
        raise ValueError("Boolean is not numeric")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and re.fullmatch(r"\d{1,10}", value):
        number = int(value)
    else:
        raise ValueError("Invalid numeric field")
    if not min_value <= number <= max_value:
        raise ValueError("Numeric range exceeded")
    return number


def _normalize(raw):
    if not isinstance(raw, dict):
        raise ValueError("Record must be JSON object")
    item_id = raw.get("external_id")
    title = raw.get("title")
    if not isinstance(item_id, str) or not ITEM.fullmatch(item_id):
        raise ValueError("Invalid item identifier")
    if not isinstance(title, str) or not 2 <= len(title) <= 120:
        raise ValueError("Invalid item title")
    if any(ord(c) < 32 for c in title):
        raise ValueError("Control characters in title")
    quantity = _integer(raw.get("quantity"), min_value=0, max_value=1_000_000)
    revision = _integer(raw.get("revision"), min_value=1, max_value=1_000_000)
    return {
        "external_id": item_id, "title": title,
        "quantity": quantity, "revision": revision
    }


class DataSync:
    def __init__(self, path):
        self.path = str(path)
        if self.path == ":memory:":
            raise ValueError("Durable reconciliation requires on-disk SQLite")
        with self._db() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute(
                """CREATE TABLE IF NOT EXISTS entities (
                tenant TEXT NOT NULL, source TEXT NOT NULL,
                external_id TEXT NOT NULL, title TEXT NOT NULL,
                quantity INTEGER NOT NULL, revision INTEGER NOT NULL,
                PRIMARY KEY(tenant,source,external_id))"""
            )
            db.execute(
                """CREATE TABLE IF NOT EXISTS batches (
                tenant TEXT NOT NULL, source TEXT NOT NULL,
                batch_id TEXT NOT NULL, digest TEXT NOT NULL,
                result TEXT NOT NULL,
                PRIMARY KEY(tenant,source,batch_id))"""
            )
            db.execute(
                """CREATE TABLE IF NOT EXISTS rejected (
                tenant TEXT NOT NULL, source TEXT NOT NULL,
                batch_id TEXT NOT NULL, external_id TEXT NOT NULL,
                reason TEXT NOT NULL)"""
            )
            db.execute(
                """CREATE TABLE IF NOT EXISTS audits (
                tenant TEXT NOT NULL, source TEXT NOT NULL,
                batch_id TEXT NOT NULL, action TEXT NOT NULL,
                timestamp REAL NOT NULL)"""
            )

    @contextmanager
    def _db(self):
        connection = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout=10000")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    @staticmethod
    def _scope(tenant, source, batch_id=None):
        for value in (tenant, source):
            if not isinstance(value, str) or not IDENT.fullmatch(value):
                raise ValueError("Invalid tenant/source scope")
        if batch_id is not None and (
            not isinstance(batch_id, str) or not BATCH.fullmatch(batch_id)
        ):
            raise ValueError("Invalid batch identifier")

    @staticmethod
    def _canonical(rows):
        if not isinstance(rows, list) or len(rows) > 500:
            raise ValueError("Records must be list up to 500 items")
        try:
            encoded = json.dumps(rows, sort_keys=True, separators=(",", ":"), allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError("Batch must contain JSON-compatible records") from exc
        if len(encoded.encode("utf-8")) > 128 * 1024:
            raise ValueError("Batch payload too large")
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def preview(self, tenant, source, batch_id, rows):
        return self._process(tenant, source, batch_id, rows, dry_run=True)

    def apply(self, tenant, source, batch_id, rows, *, fail_after=None):
        return self._process(
            tenant, source, batch_id, rows, dry_run=False, fail_after=fail_after
        )

    def _process(self, tenant, source, batch_id, rows, *, dry_run, fail_after=None):
        self._scope(tenant, source, batch_id)
        digest = self._canonical(rows)
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            # Read the durable ledger inside the same transaction as all writes.
            prior = db.execute(
                "SELECT digest,result FROM batches WHERE tenant=? AND source=? AND batch_id=?",
                (tenant, source, batch_id),
            ).fetchone()
            if prior and not dry_run:
                if prior["digest"] != digest:
                    raise BatchConflict("Batch ID already used for different input")
                old = json.loads(prior["result"])
                return {**old, "replayed": True, "dry_run": False}
            seen = set()
            counts = {"inserted": 0, "updated": 0, "unchanged": 0, "rejected": 0}
            processed = 0

            for raw in rows:
                try:
                    rec = _normalize(raw)
                except ValueError:
                    rec = None
                    reason = "INVALID_RECORD"
                if rec is not None:
                    ext_id = rec["external_id"]
                    if ext_id in seen:
                        reason = "DUPLICATE_BATCH_ID"
                    else:
                        seen.add(ext_id)
                        current = db.execute(
                            "SELECT title,quantity,revision FROM entities "
                            "WHERE tenant=? AND source=? AND external_id=?",
                            (tenant, source, ext_id),
                        ).fetchone()
                        if current is None:
                            db.execute(
                                "INSERT INTO entities(tenant,source,external_id,title,quantity,revision) "
                                "VALUES(?,?,?,?,?,?)",
                                (tenant, source, ext_id, rec["title"],
                                 rec["quantity"], rec["revision"]),
                            )
                            counts["inserted"] += 1
                            reason = None
                        elif rec["revision"] > current["revision"]:
                            db.execute(
                                "UPDATE entities SET title=?,quantity=?,revision=? "
                                "WHERE tenant=? AND source=? AND external_id=?",
                                (rec["title"], rec["quantity"], rec["revision"],
                                 tenant, source, ext_id),
                            )
                            counts["updated"] += 1
                            reason = None
                        elif rec["revision"] < current["revision"]:
                            reason = "STALE_REVISION"
                        elif (
                            rec["title"] == current["title"]
                            and rec["quantity"] == current["quantity"]
                        ):
                            counts["unchanged"] += 1
                            reason = None
                        else:
                            reason = "REVISION_CONFLICT"
                if reason is not None:
                    safe_id = (
                        rec["external_id"] if rec is not None
                        else (
                            raw.get("external_id", "<invalid>")
                            if isinstance(raw, dict) else "<invalid>"
                        )
                    )
                    if not isinstance(safe_id, str) or not ITEM.fullmatch(safe_id):
                        safe_id = "<invalid>"
                    db.execute(
                        "INSERT INTO rejected(tenant,source,batch_id,external_id,reason) "
                        "VALUES(?,?,?,?,?)",
                        (tenant, source, batch_id, safe_id, reason),
                    )
                    counts["rejected"] += 1
                processed += 1
                if not dry_run and fail_after is not None and processed == fail_after:
                    raise RuntimeError("Injected failure: testing transaction rollback")

            result = {
                "batch_id": batch_id, "digest": digest,
                **counts, "replayed": False, "dry_run": dry_run,
            }
            if dry_run:
                # A preview runs real checks but has absolutely no permanent writes.
                db.execute("ROLLBACK")
                return result
            db.execute(
                "INSERT INTO batches(tenant,source,batch_id,digest,result) "
                "VALUES(?,?,?,?,?)",
                (tenant, source, batch_id, digest, json.dumps(result, sort_keys=True)),
            )
            db.execute(
                "INSERT INTO audits(tenant,source,batch_id,action,timestamp) "
                "VALUES(?,?,?,?,?)",
                (tenant, source, batch_id, "batch_applied", time.time())
            )
            return result

    def snapshot(self, tenant, source):
        self._scope(tenant, source)
        with self._db() as db:
            rows = db.execute(
                "SELECT external_id,title,quantity,revision FROM entities "
                "WHERE tenant=? AND source=? ORDER BY external_id",
                (tenant, source),
            )
            return [dict(row) for row in rows]

    def rejections(self, tenant, source, batch_id):
        self._scope(tenant, source, batch_id)
        with self._db() as db:
            rows = db.execute(
                "SELECT external_id,reason FROM rejected "
                "WHERE tenant=? AND source=? AND batch_id=? ORDER BY rowid",
                (tenant, source, batch_id),
            )
            return [dict(row) for row in rows]

    def audit(self, tenant, source, batch_id):
        self._scope(tenant, source, batch_id)
        with self._db() as db:
            rows = db.execute(
                "SELECT action,timestamp FROM audits "
                "WHERE tenant=? AND source=? AND batch_id=? ORDER BY rowid",
                (tenant, source, batch_id),
            )
            return [dict(row) for row in rows]

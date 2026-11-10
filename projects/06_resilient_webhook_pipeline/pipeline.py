"""Durable, local-only reference pipeline. Synthetic only; NOT production approved.

Demonstrates at-least-once worker behavior with idempotent intake and
explicit quarantine for uncertain downstream outcomes. SQLite is a demo backend.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
import time
from uuid import uuid4
from contextlib import contextmanager
from pathlib import Path


TENANT = re.compile(r"^[a-z][a-z0-9-]{1,39}$")
EVENT = re.compile(r"^[a-zA-Z0-9._:-]{2,100}$")
STATES = ("pending", "leased", "retry", "needs_review", "complete", "dead_letter")


class ConflictError(ValueError):
    pass


class SignatureError(ValueError):
    pass


class TransitionError(ValueError):
    pass


class RetryableError(Exception):
    pass


class UncertainOutcome(Exception):
    pass


class WebhookSigner:
    """HMAC signs tenant, event ID, timestamp and *exact* raw bytes."""

    def __init__(self, secret: bytes):
        if not isinstance(secret, bytes) or len(secret) < 16:
            raise ValueError("A separate, high-entropy webhook secret is required")
        self._secret = secret

    def sign(self, tenant: str, event_id: str, timestamp: int, body: bytes) -> str:
        if not isinstance(body, bytes) or not isinstance(timestamp, int):
            raise ValueError("Signing requires integer timestamp and byte payload")
        message = b"\n".join(
            (str(timestamp).encode(), tenant.encode(), event_id.encode(), body)
        )
        return "sha256=" + hmac.new(self._secret, message, hashlib.sha256).hexdigest()

    def verify(
        self, tenant: str, event_id: str, timestamp: int, body: bytes,
        signature: str, *, now: int | None = None, max_age: int = 300,
    ) -> None:
        if now is None:
            now = int(time.time())
        if not isinstance(timestamp, int) or abs(now - timestamp) > max_age:
            raise SignatureError("Expired or invalid webhook timestamp")
        if not isinstance(signature, str) or not hmac.compare_digest(
            self.sign(tenant, event_id, timestamp, body), signature
        ):
            raise SignatureError("Invalid signature")


class EventPipeline:
    """Persistent SQLite inbox, durable job leases, and auditable transitions."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path == ":memory:":
            raise ValueError("Use an on-disk database for durable queue semantics")
        with self._db() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute(
                """CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant TEXT NOT NULL, event_id TEXT NOT NULL,
                payload TEXT NOT NULL, digest TEXT NOT NULL,
                state TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
                next_attempt REAL NOT NULL DEFAULT 0,
                lease_until REAL, receipt TEXT, lease_token TEXT,
                UNIQUE(tenant,event_id))"""
            )
            # Existing local demo DBs are upgraded without deleting queued events.
            columns = {row[1] for row in connection.execute("PRAGMA table_info(events)")}
            if "lease_token" not in columns:
                connection.execute("ALTER TABLE events ADD COLUMN lease_token TEXT")
            connection.execute(
                """CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant TEXT NOT NULL, event_id TEXT NOT NULL,
                action TEXT NOT NULL, occurred_at REAL NOT NULL
                )"""
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS ix_events_queue ON events(state,next_attempt,id)"
            )

    @contextmanager
    def _db(self):
        conn = sqlite3.connect(self.path, isolation_level=None, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=10000")
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    @staticmethod
    def _validate(tenant, event_id):
        if not isinstance(tenant, str) or not TENANT.fullmatch(tenant):
            raise ValueError("Invalid tenant identifier")
        if not isinstance(event_id, str) or not EVENT.fullmatch(event_id):
            raise ValueError("Invalid event identifier")

    @staticmethod
    def _audit(conn, tenant, event_id, action):
        conn.execute(
            "INSERT INTO audit(tenant,event_id,action,occurred_at) VALUES(?,?,?,?)",
            (tenant, event_id, action, time.time()),
        )

    def ingest(self, tenant: str, event_id: str, payload: dict) -> dict:
        self._validate(tenant, event_id)
        if not isinstance(payload, dict):
            raise ValueError("JSON object required")
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        if len(encoded.encode("utf-8")) > 8192:
            raise ValueError("Payload exceeds local demo limit")
        digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute(
                "SELECT id,digest,state FROM events WHERE tenant=? AND event_id=?",
                (tenant, event_id),
            ).fetchone()
            if old:
                if old["digest"] != digest:
                    raise ConflictError("Event ID reused with different data")
                return {"id": old["id"], "created": False, "state": old["state"]}
            cursor = db.execute(
                "INSERT INTO events(tenant,event_id,payload,digest,state) VALUES(?,?,?,?,?)",
                (tenant, event_id, encoded, digest, "pending"),
            )
            self._audit(db, tenant, event_id, "accepted")
            return {"id": cursor.lastrowid, "created": True, "state": "pending"}

    def get(self, tenant: str, event_id: str) -> dict | None:
        self._validate(tenant, event_id)
        with self._db() as db:
            row = db.execute(
                "SELECT id,tenant,event_id,state,attempts,receipt FROM events "
                "WHERE tenant=? AND event_id=?",
                (tenant, event_id),
            ).fetchone()
        return dict(row) if row else None

    def counts(self, tenant: str) -> dict:
        self._validate(tenant, "count")
        with self._db() as db:
            rows = db.execute(
                "SELECT state, COUNT(*) AS n FROM events WHERE tenant=? GROUP BY state",
                (tenant,),
            )
            count = {row["state"]: row["n"] for row in rows}
        return {state: count.get(state, 0) for state in STATES}

    def audit(self, tenant: str, event_id: str) -> list:
        self._validate(tenant, event_id)
        with self._db() as db:
            rows = db.execute(
                "SELECT action,occurred_at FROM audit WHERE tenant=? AND event_id=? "
                "ORDER BY id",
                (tenant, event_id),
            )
            return [dict(row) for row in rows]

    def claim(self, *, now: float | None = None, lease_seconds: float = 30) -> dict | None:
        if now is None:
            now = time.time()
        if not 0 < lease_seconds <= 3600:
            raise ValueError("Lease must be positive and bounded")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT * FROM events WHERE state IN ('pending','retry') "
                "AND next_attempt <= ? ORDER BY id LIMIT 1",
                (now,),
            ).fetchone()
            if row is None:
                return None
            token = uuid4().hex
            db.execute(
                "UPDATE events SET state='leased',attempts=attempts+1,lease_until=?,lease_token=? "
                "WHERE id=?", (now + lease_seconds, token, row["id"])
            )
            self._audit(db, row["tenant"], row["event_id"], "leased")
            return {
                "id": row["id"], "tenant": row["tenant"], "event_id": row["event_id"],
                "payload": json.loads(row["payload"]), "attempts": row["attempts"] + 1,
                "lease_token": token
            }

    def recover_expired_leases(self, *, now: float | None = None) -> int:
        """Unknown external side effects require human verification; never blind retry."""
        if now is None:
            now = time.time()
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            rows = list(db.execute(
                "SELECT id,tenant,event_id FROM events "
                "WHERE state='leased' AND lease_until <= ?", (now,)
            ))
            for row in rows:
                db.execute(
                    "UPDATE events SET state='needs_review',lease_until=NULL,lease_token=NULL WHERE id=?",
                    (row["id"],)
                )
                self._audit(db, row["tenant"], row["event_id"], "lease_expired_review")
            return len(rows)

    def _finish(self, job: dict, *, state: str, now: float, receipt=None, backoff=None):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT state,lease_until,lease_token FROM events WHERE id=? AND tenant=? AND event_id=?",
                (job["id"], job["tenant"], job["event_id"]),
            ).fetchone()
            if (row is None or row["state"] != "leased"
                    or row["lease_token"] is None
                    or row["lease_token"] != job.get("lease_token")
                    or row["lease_until"] is None or row["lease_until"] <= now):
                raise TransitionError("Job lease is missing, expired or superseded")
            db.execute(
                "UPDATE events SET state=?, lease_until=NULL, lease_token=NULL, "
                "next_attempt=?,receipt=? WHERE id=?",
                (
                    state, now + backoff if backoff is not None else 0,
                    json.dumps(receipt, sort_keys=True) if receipt is not None else None,
                    job["id"],
                )
            )
            action = {
                "complete": "completed", "retry": "retry_scheduled",
                "dead_letter": "dead_lettered", "needs_review": "uncertain_review"
            }[state]
            self._audit(db, job["tenant"], job["event_id"], action)
            return {"event_id": job["event_id"], "state": state, "attempt": job["attempts"]}

    def resolve(self, tenant: str, event_id: str, decision: str, *, now: float) -> bool:
        """Requires external confirmation before choosing applied vs retry."""
        self._validate(tenant, event_id)
        if decision not in ("retry", "applied"):
            raise ValueError("Decision must be retry or applied")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT id,state FROM events WHERE tenant=? AND event_id=?",
                (tenant, event_id),
            ).fetchone()
            if row is None or row["state"] not in ("needs_review", "dead_letter"):
                raise TransitionError("Not a reviewable item")
            state = "pending" if decision == "retry" else "complete"
            db.execute(
                "UPDATE events SET state=?,attempts=0,next_attempt=?,lease_until=NULL,lease_token=NULL "
                "WHERE id=?", (state, now if state == "pending" else 0, row["id"])
            )
            self._audit(db, tenant, event_id, "manual_" + decision)
            return True


class Worker:
    def __init__(self, pipeline: EventPipeline, adapter, max_attempts: int = 3):
        if not 1 <= max_attempts <= 8:
            raise ValueError("Bounded retries required")
        self.pipeline = pipeline
        self.adapter = adapter
        self.max_attempts = max_attempts

    def run_once(self, *, now: float | None = None) -> dict | None:
        if now is None:
            now = time.time()
        self.pipeline.recover_expired_leases(now=now)
        job = self.pipeline.claim(now=now)
        if job is None:
            return None
        try:
            receipt = self.adapter.send(job)
        except UncertainOutcome:
            return self.pipeline._finish(job, state="needs_review", now=now)
        except RetryableError:
            terminal = job["attempts"] >= self.max_attempts
            return self.pipeline._finish(
                job, state="dead_letter" if terminal else "retry",
                now=now, backoff=None if terminal else 2 ** (job["attempts"] - 1)
            )
        except Exception:
            # Unknown exception => unknown downstream outcome. No automatic repetition.
            return self.pipeline._finish(job, state="needs_review", now=now)
        return self.pipeline._finish(job, state="complete", now=now, receipt=receipt)

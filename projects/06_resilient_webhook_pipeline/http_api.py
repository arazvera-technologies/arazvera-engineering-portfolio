"""Local-only HTTP façade for the durable webhook reference demo.

Uses a deliberately fake admin token. Do NOT expose to the Internet.
"""
from __future__ import annotations

import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

from pipeline import ConflictError, SignatureError


def make_server(pipeline, signers: dict, tokens: dict, *, host="127.0.0.1", port=0):
    if host != "127.0.0.1":
        raise ValueError("Demo must bind localhost only")

    class Handler(BaseHTTPRequestHandler):
        server_version = "ARAZVERA-LocalDemo/0.1"

        def log_message(self, format, *args):
            # Avoid logging synthetic payloads/tokens in shared console.
            return

        def _respond(self, code, payload):
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _parts(self):
            path = urlsplit(self.path).path
            return [unquote(part) for part in path.split("/") if part]

        def do_GET(self):
            parts = self._parts()
            if parts == ["health"]:
                return self._respond(200, {"status": "ok", "mode": "local-synthetic",
                                           "production_approved": False})
            if len(parts) != 4 or parts[:2] != ["v1", "events"]:
                return self._respond(404, {"error": "NOT_FOUND"})
            _, _, tenant, event_id = parts
            token = self.headers.get("X-Demo-Token", "")
            if not token or token not in tokens:
                return self._respond(401, {"error": "AUTH_REQUIRED"})
            if tokens[token] != tenant:
                return self._respond(403, {"error": "TENANT_DENIED"})
            try:
                event = pipeline.get(tenant, event_id)
            except ValueError:
                return self._respond(422, {"error": "INVALID_IDENTIFIER"})
            if event is None:
                return self._respond(404, {"error": "NOT_FOUND"})
            return self._respond(200, event)

        def do_POST(self):
            parts = self._parts()
            if len(parts) != 3 or parts[:2] != ["v1", "webhooks"]:
                return self._respond(404, {"error": "NOT_FOUND"})
            tenant = parts[2]
            signer = signers.get(tenant)
            if not signer:
                return self._respond(404, {"error": "UNKNOWN_TENANT"})
            raw_size = self.headers.get("Content-Length", "")
            try:
                size = int(raw_size)
                if not 1 <= size <= 8192:
                    raise ValueError()
            except ValueError:
                return self._respond(413, {"error": "PAYLOAD_SIZE"})
            raw = self.rfile.read(size)
            event_id = self.headers.get("X-Event-Id", "")
            try:
                timestamp = int(self.headers.get("X-Timestamp", ""))
                signer.verify(
                    tenant, event_id, timestamp, raw,
                    self.headers.get("X-Signature", ""),
                    now=int(self.server.verification_clock())
                )
            except (ValueError, SignatureError):
                return self._respond(401, {"error": "INVALID_SIGNATURE_OR_TIME"})
            try:
                payload = json.loads(raw)
                result = pipeline.ingest(tenant, event_id, payload)
            except ConflictError:
                return self._respond(409, {"error": "IDEMPOTENCY_CONFLICT"})
            except (ValueError, TypeError, json.JSONDecodeError):
                return self._respond(422, {"error": "INVALID_JSON_OR_EVENT"})
            return self._respond(201 if result["created"] else 200, result)

    server = ThreadingHTTPServer((host, port), Handler)
    server.verification_clock = time.time
    return server

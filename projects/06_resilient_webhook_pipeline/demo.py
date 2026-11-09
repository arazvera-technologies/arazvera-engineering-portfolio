"""One-command, real localhost HTTP and SQLite recovery demonstration."""
import json
import tempfile
import threading
import urllib.request
from pathlib import Path
from pipeline import EventPipeline, WebhookSigner, RetryableError, Worker
from http_api import make_server


class SimulatedCRM:
    def __init__(self):
        self.calls = 0

    def send(self, event):
        self.calls += 1
        if self.calls == 1:
            raise RetryableError("Synthetic temporary outage")
        return {"receipt": "demo-crm-" + event["event_id"]}


def main():
    with tempfile.TemporaryDirectory() as directory:
        db = EventPipeline(Path(directory) / "events.sqlite")
        signer = WebhookSigner(b"demo-only-key-not-for-production")
        server = make_server(db, {"alpha": signer}, {"demo-admin-alpha": "alpha"})
        server.verification_clock = lambda: 1000
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            payload = b'{"source":"synthetic-contact-form","kind":"lead"}'
            headers = {
                "Content-Type": "application/json",
                "X-Event-Id": "lead-demo-123",
                "X-Timestamp": "1000",
                "X-Signature": signer.sign("alpha", "lead-demo-123", 1000, payload)
            }
            request = urllib.request.Request(
                f"http://127.0.0.1:{server.server_address[1]}/v1/webhooks/alpha",
                data=payload, headers=headers, method="POST"
            )
            with urllib.request.urlopen(request, timeout=4) as response:
                intake_status = response.status
                intake = json.loads(response.read())
            adapter = SimulatedCRM()
            worker = Worker(db, adapter)
            first = worker.run_once(now=1000)
            too_early = worker.run_once(now=1000.5)
            retry_result = worker.run_once(now=1001)
            result = {
                "demo": "ARAZVERA Level 2 reliable webhook processing",
                "http_intake_status": intake_status,
                "first_intake_created": intake["created"],
                "first_attempt": first["state"],
                "early_retry_blocked": too_early is None,
                "second_attempt": retry_result["state"],
                "mock_calls": adapter.calls,
                "queue_counts": db.counts("alpha"),
                "audit_actions": [v["action"] for v in db.audit("alpha", "lead-demo-123")],
                "persistence_verified": EventPipeline(db.path).get("alpha", "lead-demo-123")["state"] == "complete",
                "production_approved": False
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            if not (intake_status == 201 and result["second_attempt"] == "complete"
                    and result["early_retry_blocked"] and result["persistence_verified"]):
                raise SystemExit("Demo acceptance failed")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    main()

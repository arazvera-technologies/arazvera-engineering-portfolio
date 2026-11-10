"""Build and independently test a public-only tenant boundary / RLS buyer pack.

The explicit allowlist excludes proprietary kits, client files and credentials.
Requires locally available Python dependencies, Docker, and cached PostgreSQL 16.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "projects/08_postgres_auth_contract/demo.py": "projects/08_postgres_auth_contract/demo.py",
    "projects/08_postgres_auth_contract/README.md": "projects/08_postgres_auth_contract/README.md",
    "projects/08_postgres_auth_contract/requirements.txt": "projects/08_postgres_auth_contract/requirements.txt",
    "projects/08_postgres_auth_contract/service.py": "projects/08_postgres_auth_contract/service.py",
    "projects/08_postgres_auth_contract/storage.py": "projects/08_postgres_auth_contract/storage.py",
    "projects/08_postgres_auth_contract/token_verify.py": "projects/08_postgres_auth_contract/token_verify.py",
    "projects/08_postgres_auth_contract/tests/test_contract.py": "projects/08_postgres_auth_contract/tests/test_contract.py",
    "projects/09_postgres_rls_recovery/README.md": "projects/09_postgres_rls_recovery/README.md",
    "projects/09_postgres_rls_recovery/requirements.txt": "projects/09_postgres_rls_recovery/requirements.txt",
    "projects/09_postgres_rls_recovery/proof_db.py": "projects/09_postgres_rls_recovery/proof_db.py",
    "projects/09_postgres_rls_recovery/verify_restore.py": "projects/09_postgres_rls_recovery/verify_restore.py",
    "projects/09_postgres_rls_recovery/tests/test_rls.py": "projects/09_postgres_rls_recovery/tests/test_rls.py",
    "projects/09_postgres_rls_recovery/EVIDENCE_RESTORE_SYNTHETIC.json": "projects/09_postgres_rls_recovery/EVIDENCE_RESTORE_SYNTHETIC.json",
    "tools/verify_tenant_rls_docker.py": "tools/verify_tenant_rls_docker.py",
    "docs/TENANT_RLS_PRODUCT_CARD_EN_20261110.md": "docs/product_offer.md",
    "docs/TENANT_RLS_BUYER_ACCEPTANCE_IP_DRAFT_EN_20261110.md": "docs/acceptance_and_ip_draft.md",
}
ROOT_NOTICE = """# ARAZVERA — Tenant Boundary & Restore Public Review

**Evidence/reference only**. The software is synthetic and not production-ready.
No customer data, private engineering kits, valid production credentials or
permission to redistribute proprietary components is included.

## Prerequisites

Python 3.11+, Docker Desktop with cached postgres:16-alpine, and Python
dependencies listed in projects/08_postgres_auth_contract/requirements.txt.

From this archive's root, run:
    python tools/verify_tenant_rls_docker.py

This creates a separate localhost-only PostgreSQL 16 container, runs 28
actual database tests and a same-cluster schema backup/restore check, then
automatically stops and removes the container. Never point these fixture tests
at a customer database.

For the proposed paid scope, risks and licensing options, read:
- docs/product_offer.md
- docs/acceptance_and_ip_draft.md

Contract terms and IP rights are not granted by this review document.
"""

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.out.resolve()
    try:
        output.relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise SystemExit("Refusing to place the buyer ZIP inside the public repository.")
    output.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, bytes] = {}
    for source, target in FILES.items():
        file = ROOT / source
        if not file.is_file():
            raise SystemExit(f"Missing allowlisted file: {source}")
        payload = file.read_bytes()
        if target.endswith("/README.md"):
            text = payload.decode("utf-8")
            repo = "https://github.com/arazvera-technologies/arazvera-engineering-portfolio"
            text = text.replace("../../docs/LEVEL2_VERIFIED_RESULTS.md",
                                repo + "/blob/main/docs/LEVEL2_VERIFIED_RESULTS.md")
            text = text.replace("../../docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md",
                                repo + "/blob/main/docs/LEVEL2_GLOBAL_SERVICE_MATRIX_20261109.md")
            text = text.replace("../../docs/LEVEL3_SPECIALIST_READINESS_20261109.md",
                                repo + "/blob/main/docs/LEVEL3_SPECIALIST_READINESS_20261109.md")
            text = text.replace("../../README.md", repo)
            payload = text.encode("utf-8")
        data[target] = payload
    data["README_REVIEW.md"] = ROOT_NOTICE.encode()
    manifest = {name: hashlib.sha256(payload).hexdigest()
                for name, payload in sorted(data.items())}
    data["SHA256_MANIFEST.json"] = json.dumps(manifest, indent=2).encode()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        for name, payload in sorted(data.items()):
            z.writestr(name, payload)
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        with zipfile.ZipFile(output) as z:
            if z.testzip() is not None:
                raise SystemExit("Archive integrity check failed.")
            z.extractall(root)
        for name, expected in manifest.items():
            actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
            if actual != expected:
                raise SystemExit("Extracted file hash mismatch: " + name)
        checked = subprocess.run(
            [sys.executable, "tools/verify_tenant_rls_docker.py"],
            cwd=root, capture_output=True, text=True)
        if checked.returncode:
            print(checked.stdout, checked.stderr)
            raise SystemExit(checked.returncode)
        print(checked.stdout.strip())
        if '"contract_tests_passed": 28' not in checked.stdout:
            raise SystemExit("Expected passing database verification not detected.")
    print(json.dumps({"status": "PASS", "archive": str(output),
                      "files": len(manifest),
                      "archive_bytes": output.stat().st_size,
                      "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

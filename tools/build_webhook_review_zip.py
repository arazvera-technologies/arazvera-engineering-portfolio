"""Build a self-tested public-only ARAZVERA webhook buyer review archive.

Use only the explicit allowlist below. No private starter libraries, credentials,
database files, customer material or system-specific paths are packaged.

Usage:
    python tools/build_webhook_review_zip.py --out D:/safe-output/webhook-review.zip
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
    "projects/06_resilient_webhook_pipeline/pipeline.py": "src/pipeline.py",
    "projects/06_resilient_webhook_pipeline/http_api.py": "src/http_api.py",
    "projects/06_resilient_webhook_pipeline/demo.py": "src/demo.py",
    "projects/06_resilient_webhook_pipeline/tests/test_pipeline.py": "src/tests/test_pipeline.py",
    "projects/06_resilient_webhook_pipeline/README.md": "src/README.md",
    "docs/WEBHOOK_FENCING_VERIFICATION_20261110.md": "docs/verification.md",
    "docs/WEBHOOK_RECOVERY_PRODUCT_CARD_EN_20261110.md": "docs/product_offer.md",
    "docs/WEBHOOK_BUYER_ACCEPTANCE_IP_DRAFT_EN_20261110.md": "docs/acceptance_and_ip_draft.md",
}
README = """# ARAZVERA — Webhook/API Recovery: Public Buyer Review

This is a **synthetic reference and engineering-sprint proposal**, NOT a
production-ready service or a license to redistribute proprietary code.

Quick check (Python 3.11+; no paid API or external services):
    cd src
    python demo.py
    python -m unittest discover -s tests -v

See docs/product_offer.md for the paid scope and exclusions, docs/verification.md
for evidence, and docs/acceptance_and_ip_draft.md for proposed commercial
options and buyer-specific acceptance gates. The draft terms are not executed.

The source in src/ is a public laboratory demonstration. No private kit or
customer code is included. The buyer must negotiate exact contractual
deliverables and permitted commercial use separately.
"""

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path,
                        help="Destination ZIP; keep it outside the public repository")
    args = parser.parse_args()
    dest = args.out.resolve()
    try:
        dest.relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise SystemExit("Refusing to package inside the public repository.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    archive_contents: dict[str, bytes] = {}
    for source, target in FILES.items():
        p = ROOT / source
        if not p.is_file():
            raise SystemExit("Missing allowlisted source: " + source)
        data = p.read_bytes()
        if target == "src/README.md":
            data = data.replace(
                b"../../docs/WEBHOOK_RECOVERY_CLIENT_OFFER_20261110.md",
                b"../docs/product_offer.md"
            )
        archive_contents[target] = data
    archive_contents["README_REVIEW.md"] = README.encode()
    manifest = {
        name: hashlib.sha256(data).hexdigest()
        for name, data in sorted(archive_contents.items())
    }
    archive_contents["SHA256_MANIFEST.json"] = json.dumps(
        manifest, indent=2
    ).encode()
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(archive_contents.items()):
            archive.writestr(name, data)
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(dest) as archive:
            assert archive.testzip() is None, "Archive integrity check failed"
            archive.extractall(tmp)
        temp = Path(tmp)
        for name, expected in manifest.items():
            found = hashlib.sha256((temp / name).read_bytes()).hexdigest()
            assert found == expected, f"Hash mismatch: {name}"
        for arguments in (["demo.py"], ["-m", "unittest", "discover",
                                         "-s", "tests", "-q"]):
            proc = subprocess.run([sys.executable, *arguments],
                                  cwd=temp / "src", capture_output=True, text=True)
            if proc.returncode:
                print(proc.stdout, proc.stderr)
                return proc.returncode
    print(json.dumps({"status": "PASS", "file_count": len(manifest),
                      "bytes": dest.stat().st_size, "archive": str(dest),
                      "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

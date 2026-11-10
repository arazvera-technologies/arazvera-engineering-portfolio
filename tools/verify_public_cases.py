"""Run each public case in an isolated Python process to avoid demo.py collisions.

Usage:
    python tools/verify_public_cases.py
    python tools/verify_public_cases.py --require-postgres

The stricter mode requires explicit disposable PostgreSQL DSNs so skipped DB
tests cannot be mistaken for a completed integration acceptance run.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = sorted(path for path in (ROOT / "projects").iterdir()
               if path.is_dir() and (path / "tests").is_dir())
PG_ENVS = ("ARAZVERA_PUBLIC_TEST_PG_DSN", "ARAZVERA_L3_ADMIN_DSN")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-postgres", action="store_true",
                        help="Fail if required PostgreSQL DSNs are missing or tests skip")
    args = parser.parse_args()
    if args.require_postgres:
        missing = [name for name in PG_ENVS if not os.getenv(name)]
        if missing:
            print("BLOCKED: provide disposable PostgreSQL configuration: "
                  + ", ".join(missing), flush=True)
            return 2
    total_passed = total_skipped = failures = 0
    for project in CASES:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "--disable-warnings"],
            cwd=project, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180,
        )
        summary = " | ".join(line.strip() for line in result.stdout.splitlines()[-3:])
        passed = re.search(r"(\d+) passed", result.stdout)
        skipped = re.search(r"(\d+) skipped", result.stdout)
        total_passed += int(passed.group(1)) if passed else 0
        total_skipped += int(skipped.group(1)) if skipped else 0
        failures += result.returncode != 0
        print(f"{project.name}: exit={result.returncode} {summary}", flush=True)
    print(f"TOTAL: passed={total_passed}; skipped={total_skipped}; "
          f"failed_projects={failures}; tested_cases={len(CASES)}", flush=True)
    if failures or (args.require_postgres and total_skipped):
        return 1
    if total_skipped:
        print("INCOMPLETE INTEGRATION EVIDENCE: PostgreSQL tests were skipped.",
              flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

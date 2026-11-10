"""Isolated public Level 2 auth + Level 3 RLS and restore verification.

Runs 28 contract tests against a unique disposable PostgreSQL 16 container
and verifies a same-container schema backup/restore. Never touches client data.

Requires Docker Desktop, cached postgres:16-alpine and Python dependencies
listed in projects/08_postgres_auth_contract/requirements.txt.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "postgres:16-alpine"
USER, PASSWORD = "l3admin", "synthetic_local_fixture"

def invoke(args: list[str], check: bool = True, **kwargs):
    return subprocess.run(args, text=True, capture_output=True, check=check, **kwargs)

def main() -> int:
    name = "av-tenant-audit-" + uuid.uuid4().hex[:12]
    created = False
    try:
        if invoke(["docker", "image", "inspect", IMAGE], check=False).returncode:
            print("BLOCKED: postgres:16-alpine not cached. No network pull attempted.")
            return 2
        invoke(["docker", "run", "--rm", "-d", "--name", name,
                "-e", f"POSTGRES_USER={USER}",
                "-e", f"POSTGRES_PASSWORD={PASSWORD}",
                "-e", "POSTGRES_DB=l3proof", "-p", "127.0.0.1::5432", IMAGE])
        created = True
        published = invoke(["docker", "port", name, "5432/tcp"]).stdout.strip()
        match = re.fullmatch(r"127\.0\.0\.1:(\d+)", published)
        if match is None:
            print("BLOCKED: database is not limited to localhost.")
            return 2
        for _ in range(40):
            if invoke(["docker", "exec", name, "pg_isready", "-U", USER,
                       "-d", "l3proof"], check=False).returncode == 0:
                break
            time.sleep(0.5)
        else:
            print("BLOCKED: disposable PostgreSQL failed readiness checks.")
            return 2
        invoke(["docker", "exec", name, "createdb", "-U", USER, "l2public"])
        env = os.environ.copy()
        env["ARAZVERA_PUBLIC_TEST_PG_DSN"] = (
            f"postgresql://{USER}:{PASSWORD}@127.0.0.1:{match.group(1)}/l2public"
        )
        env["ARAZVERA_L3_ADMIN_DSN"] = (
            f"host=127.0.0.1 port={match.group(1)} dbname=l3proof "
            f"user={USER} password={PASSWORD}"
        )
        tests_total = 0
        with tempfile.TemporaryDirectory() as directory:
            staged = Path(directory)
            for code in ("08_postgres_auth_contract", "09_postgres_rls_recovery"):
                source = ROOT / "projects" / code
                target = staged / code
                shutil.copytree(source, target, ignore=shutil.ignore_patterns(
                    "__pycache__", ".pytest_cache", "*.pyc"))
                result = invoke([sys.executable, "-m", "unittest", "discover",
                                 "-s", "tests", "-v"],
                                cwd=target, env=env, check=False)
                if result.returncode:
                    print(result.stdout, result.stderr)
                    print("FAIL: " + code)
                    return 1
                count = re.search(r"Ran\s+(\d+)\s+tests?", result.stderr)
                if count is None or "OK" not in result.stderr:
                    print("FAIL: unverifiable unit-test count:", result.stderr)
                    return 1
                tests_total += int(count.group(1))
                print(f"{code}: {count.group(1)} passed", flush=True)
            dump = "/tmp/av_tenant_restore_lab.dump"
            invoke(["docker", "exec", name, "pg_dump", "-U", USER,
                    "-d", "l3proof", "-Fc", "-n", "level3", "-f", dump])
            invoke(["docker", "exec", name, "createdb", "-U", USER,
                    "l3proof_restore"])
            invoke(["docker", "exec", name, "pg_restore", "-U", USER,
                    "-d", "l3proof_restore", "--exit-on-error", dump])
            restored = invoke([sys.executable, "verify_restore.py"],
                              cwd=staged / "09_postgres_rls_recovery",
                              env=env, check=False)
            if restored.returncode:
                print(restored.stdout, restored.stderr)
                print("FAIL: synthetic restoration rehearsal")
                return 1
            proof = json.loads(restored.stdout.strip())
            assert proof["status"] == "PASS"
            assert proof["rows_equal"] and proof["independent_logins_isolated_after_restore"]
        if tests_total != 28:
            print(f"FAIL: expected 28 tests, observed {tests_total}")
            return 1
        print(json.dumps({"status": "PASS", "contract_tests_passed": tests_total,
                          "skipped": 0, "synthetic_restore": "PASS",
                          "customer_production_approved": False}))
        return 0
    except (OSError, subprocess.CalledProcessError, AssertionError,
            ValueError, json.JSONDecodeError) as error:
        print("BLOCKED:", type(error).__name__, str(error)[:450])
        return 2
    finally:
        if created:
            result = invoke(["docker", "stop", "--time", "5", name], check=False)
            if result.returncode:
                print("WARNING: inspect/stop disposable container:", name)

if __name__ == "__main__":
    raise SystemExit(main())

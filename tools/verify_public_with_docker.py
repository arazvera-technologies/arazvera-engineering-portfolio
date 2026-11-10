"""Run all public engineering acceptance tests against disposable PostgreSQL 16.

Requires: Docker Desktop running; locally cached postgres:16-alpine image.
Never supplies production/customer database connections. Creates a unique local
container, selects a free loopback-only TCP port, and removes it in finally.

Usage:
    python tools/verify_public_with_docker.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "postgres:16-alpine"
USER = "l3admin"
PASSWORD = "synthetic_local_fixture"
DB = "l3proof"


def run(args: list[str], *, check: bool = True, **kwargs):
    return subprocess.run(args, check=check, text=True,
                          capture_output=True, **kwargs)


def main() -> int:
    name = "av-disposable-public-verify-" + uuid.uuid4().hex[:12]
    created = False
    try:
        result = run(["docker", "image", "inspect", IMAGE], check=False)
        if result.returncode:
            print(f"BLOCKED: {IMAGE} not available locally; no image pulled.")
            return 2
        result = run(["docker", "run", "--rm", "--detach", "--name", name,
                      "-e", f"POSTGRES_USER={USER}",
                      "-e", f"POSTGRES_PASSWORD={PASSWORD}",
                      "-e", f"POSTGRES_DB={DB}",
                      "-p", "127.0.0.1::5432", IMAGE])
        created = True
        port = run(["docker", "port", name, "5432/tcp"]).stdout.strip()
        match = re.fullmatch(r"127\.0\.0\.1:(\d+)", port)
        if match is None:
            print("BLOCKED: container was not bound exclusively to localhost.")
            return 2
        ready = False
        for _ in range(40):
            check = run(["docker", "exec", name, "pg_isready", "-U", USER, "-d", DB],
                        check=False)
            if check.returncode == 0:
                ready = True
                break
            time.sleep(0.5)
        if not ready:
            print("BLOCKED: disposable PostgreSQL did not start.")
            return 2
        run(["docker", "exec", name, "createdb", "-U", USER, "l2public"])
        env = os.environ.copy()
        # Explicitly replace any inherited credentials, never reusing client DSNs.
        env["ARAZVERA_PUBLIC_TEST_PG_DSN"] = (
            f"postgresql://{USER}:{PASSWORD}@127.0.0.1:{match.group(1)}/l2public"
        )
        env["ARAZVERA_L3_ADMIN_DSN"] = (
            f"host=127.0.0.1 port={match.group(1)} dbname=l3proof "
            f"user={USER} password={PASSWORD}"
        )
        print("Running isolated synthetic PostgreSQL 16 acceptance tests.", flush=True)
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "verify_public_cases.py"),
             "--require-postgres"],
            cwd=ROOT, env=env,
        )
        return completed.returncode
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"BLOCKED: disposable verification could not complete: {exc}")
        return 2
    finally:
        if created:
            stopped = run(["docker", "stop", "--time", "5", name], check=False)
            if stopped.returncode:
                print("WARNING: automatic container cleanup failed; inspect name:", name)


if __name__ == "__main__":
    raise SystemExit(main())

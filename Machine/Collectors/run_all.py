#!/usr/bin/env python3
"""Run every collector and append one line per collector to today's agent log.

Each collector runs in its own process, so one failing never stops the others.
Exit code is 1 if any collector failed, 0 otherwise.
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import common

HERE = Path(__file__).resolve().parent
COLLECTORS = ["github", "vault_stats"]
TIMEOUT_SECONDS = 120


def run_one(name: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            [sys.executable, str(HERE / f"{name}.py")],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
    except Exception as exc:
        return False, f"did not start: {exc}"
    out = (proc.stderr if proc.returncode else proc.stdout).strip().splitlines()
    return proc.returncode == 0, out[-1] if out else "no output"


def log_line(name: str, ok: bool, detail: str, now: datetime) -> str:
    return f"- {now:%H:%M} [collector:{name}] {'ok' if ok else 'failed'} → {detail}\n"


def main() -> int:
    common.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    failures = 0
    for name in COLLECTORS:
        ok, detail = run_one(name)
        failures += not ok
        now = datetime.now()
        with open(common.LOGS_DIR / f"{now:%Y-%m-%d}.md", "a", encoding="utf-8") as f:
            f.write(log_line(name, ok, detail, now))
        print(f"{name}: {'ok' if ok else 'FAILED'} — {detail}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

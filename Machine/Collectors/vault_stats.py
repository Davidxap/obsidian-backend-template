#!/usr/bin/env python3
"""Collect vault statistics from the filesystem (counts, mtimes, open tasks)."""
import os
import sys
from datetime import date, datetime

import common
from common import mark_failed, today_note, update_frontmatter

SKIP_DIRS = {".git", ".obsidian", "Templates", "node_modules"}
KEYS = ["vault_notes_human", "vault_notes_machine", "vault_modified_today_human", "vault_open_tasks"]


def walk_notes(root, skip=frozenset(SKIP_DIRS)):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in files:
            if name.endswith(".md"):
                yield os.path.join(base, name)


def modified_today(path: str, today: date) -> bool:
    return datetime.fromtimestamp(os.stat(path).st_mtime).date() == today


def count_open_tasks(paths) -> int:
    total = 0
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as f:
            total += sum(1 for line in f if line.lstrip().startswith("- [ ]"))
    return total


def collect(today: date) -> dict:
    human_dir, machine_dir = common.VAULT_DIR / "Human", common.VAULT_DIR / "Machine"
    if not human_dir.is_dir() or not machine_dir.is_dir():
        raise FileNotFoundError("Human/ or Machine/ not found")
    human = [p for p in walk_notes(human_dir) if os.path.basename(p) != "AGENTS.md"]
    machine = list(walk_notes(machine_dir, frozenset({".git"})))
    return {
        "type": "metrics",
        "vault_notes_human": len(human),
        "vault_notes_machine": len(machine),
        "vault_modified_today_human": sum(modified_today(p, today) for p in human),
        "vault_open_tasks": count_open_tasks(human),
    }


def main() -> int:
    try:
        props = collect(date.today())
    except Exception as exc:
        mark_failed(today_note(), KEYS)
        print(f"cannot read vault: {exc}", file=sys.stderr)
        return 1
    update_frontmatter(today_note(), props)
    print(f"updated {today_note()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

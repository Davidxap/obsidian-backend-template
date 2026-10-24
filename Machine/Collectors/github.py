#!/usr/bin/env python3
"""Collect GitHub metrics into today's metrics note.

Uses the authenticated `gh` CLI. The account is taken from $GITHUB_USER, or from
`gh api user` when unset. Writes only frontmatter properties (idempotent).
"""
import json
import os
import subprocess
import sys

from common import mark_failed, today_note, update_frontmatter

KEYS = ["github_followers", "github_public_repos", "github_stars", "github_contributions_year"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection { contributionCalendar { totalContributions } }
  }
}
"""


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def login() -> str:
    return os.environ.get("GITHUB_USER") or gh("api", "user", "--jq", ".login").strip()


def fetch(user: str) -> dict:
    out = gh("api", "graphql", "-f", f"query={QUERY}", "-F", f"login={user}")
    return json.loads(out)["data"]["user"]


def to_props(user: dict) -> dict:
    repos = user["repositories"]
    return {
        "type": "metrics",
        "github_followers": user["followers"]["totalCount"],
        "github_public_repos": repos["totalCount"],
        "github_stars": sum(n["stargazerCount"] for n in repos["nodes"]),
        "github_contributions_year": user["contributionsCollection"]["contributionCalendar"]["totalContributions"],
    }


def main() -> int:
    try:
        props = to_props(fetch(login()))
    except Exception as exc:  # any failure: leave properties empty, never invent numbers
        mark_failed(today_note(), KEYS)
        print(f"gh unavailable or not authenticated: {exc}", file=sys.stderr)
        return 1
    update_frontmatter(today_note(), props)
    print(f"updated {today_note()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

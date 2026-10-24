# AGENTS.md — Collectors

Scripts that fill `Metrics/YYYY-MM-DD.md`. They are the only writers of metrics.

1. One collector = one `.py` file. No new credentials: use an already-authenticated CLI or the filesystem.
2. Write only the day note's frontmatter via `common.update_frontmatter` (idempotent). Do not duplicate that helper.
3. On failure call `common.mark_failed`, exit 1 and print the reason to stderr. Never estimate a number.
4. To add one: create the script, then add its name to `COLLECTORS` in `run_all.py`.
5. Metric keys use a source prefix (`github_`, `vault_`); values are numbers or `YYYY-MM-DD` dates.

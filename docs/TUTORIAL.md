# Tutorial

## 1. Mental model

The vault is a database made of Markdown. A daily note is a **column**, each frontmatter property a **row**. Dataview reads them; nothing else is required.

```
collector scripts ──► Machine/Metrics/2026-01-31.md  (frontmatter)
agents            ──► Machine/Logs/2026-01-31.md     (one line per task)
you               ──► Human/**                       (ideas, tasks)
Dashboard.md      ◄── reads all of the above
```

## 2. Daily routine

1. **Morning**: open `Dashboard.md`. "Needs you" lists overdue and high-priority tasks; metrics and agent activity are below.
2. **Capture**: drop anything into `Human/Inbox/`. Tasks go in project notes: `- [ ] Send proposal 📅 2026-02-01 ⏫`
3. **Daily note**: run *Daily notes: Open today's note*. The "Machine today" section is filled for you.
4. **With an agent**: open your agent (Claude Code, Codex, ...) in the vault folder. It reads `AGENTS.md`, works, and appends a line to `Machine/Logs/`.
5. **Weekly**: empty the inbox, skim the Findings table, prune stale tasks.

## 3. Add a metric collector

Example: a collector that records the number of open pull requests.

1. Create `Machine/Collectors/open_prs.py`:

```python
import json, subprocess, sys
from common import mark_failed, today_note, update_frontmatter

KEYS = ["github_open_prs"]

def main() -> int:
    try:
        out = subprocess.run(["gh", "search", "prs", "--author", "@me", "--state", "open",
                              "--json", "number"], capture_output=True, text=True, check=True).stdout
        props = {"type": "metrics", "github_open_prs": len(json.loads(out))}
    except Exception as exc:
        mark_failed(today_note(), KEYS)
        print(f"failed: {exc}", file=sys.stderr)
        return 1
    update_frontmatter(today_note(), props)
    print(f"updated {today_note()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

2. Add `"open_prs"` to `COLLECTORS` in `run_all.py`.
3. Add a column to the metrics table in `Dashboard.md`: `github_open_prs AS "Open PRs"`.
4. Write a test next to the others (see `tests/test_github.py`): success path, and failure leaves the value empty.

Rules every collector follows: idempotent writes, no new credentials, on failure leave the value empty and exit 1. **A model never writes a metric.**

## 4. Build a workflow that learns

1. Copy `Machine/Findings/example-workflow.md` to `Machine/Findings/<workflow>.md`.
2. Tell your agent: "Do X. First read `Machine/Findings/<workflow>.md`; afterwards update it with what you learned."
3. Over time the file captures what works, what failed and what is still unverified, so each run starts smarter than the last.

## 5. Writing good `AGENTS.md` files

- Say what the folder is for, who may write, and the naming format.
- Keep it under ~25 lines. If it needs more, split the folder.
- Rules are testable ("append one line `- HH:MM [agent] what → result`"), not vague ("be careful").

## 6. Common mistakes

| Mistake | Fix |
|---|---|
| Hand-editing `Machine/Metrics/` | The next collector run overwrites it. Put your own notes in the daily note. |
| "Read the whole vault" prompts | Name the folder; the agent reads its `AGENTS.md`. |
| Tasks without date or priority | They will not appear in "Needs you". Add `📅` or `⏫`. |
| Raw `<% tp... %>` in new notes | Enable *Trigger Templater on new file creation*. |
| Dataview shows nothing | Check the folder path in `FROM` and that the day note has `type: metrics`. |

## 7. Scheduling

Linux: `./install-timer.sh` installs a systemd user timer (08:00 daily, `Persistent=true` so a missed run fires at next boot). macOS/Windows: schedule `python3 Machine/Collectors/run_all.py` with launchd / Task Scheduler.

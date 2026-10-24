# AGENTS.md — Machine zone

Agents may read, write and edit here without asking.

| Folder | Content | Who writes |
|---|---|---|
| `Collectors/` | Scripts that fill metrics from real sources | scripts + agents |
| `Metrics/` | One note per day; metrics live in the frontmatter | collectors only |
| `Logs/` | One note per day with what each agent did | agents |
| `Findings/` | What was learned per workflow | agents |

## Rules

1. Log every task to `Logs/YYYY-MM-DD.md` as `- HH:MM [agent] what → result`.
2. Metrics are written by collectors, never by a model: the number comes from the source, not from an estimate.
3. Read `Findings/<workflow>.md` before repeating a workflow; update it afterwards.
4. If a collector fails, leave the property empty and log it. Never invent a value.

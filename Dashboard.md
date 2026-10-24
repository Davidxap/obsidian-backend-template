---
type: dashboard
---

# Dashboard — what needs you today

## Needs you

```tasks
not done
(due before tomorrow) OR (priority is above medium)
path does not include Templates
sort by due
sort by priority
limit 15
```

## Unprocessed inbox

```dataview
LIST
FROM "Human/Inbox"
SORT file.ctime ASC
```

## Metrics (last 14 days)

```dataview
TABLE WITHOUT ID file.link AS "Day", github_contributions_year AS "Contrib/yr", github_stars AS "Stars", vault_notes_human AS "Notes", vault_open_tasks AS "Tasks"
FROM "Machine/Metrics"
WHERE type = "metrics"
SORT file.name DESC
LIMIT 14
```

## What the agents did

```dataview
LIST
FROM "Machine/Logs"
WHERE file.name != "AGENTS"
SORT file.name DESC
LIMIT 7
```

## Findings

```dataview
TABLE WITHOUT ID file.link AS "Workflow", file.mtime AS "Updated"
FROM "Machine/Findings"
WHERE file.name != "AGENTS"
SORT file.mtime DESC
```

---
type: daily
created: <% tp.date.now("YYYY-MM-DD") %>
---

# <% tp.date.now("YYYY-MM-DD") %>

## Machine today (read-only)

```dataview
TABLE WITHOUT ID github_contributions_year AS "Contributions/yr", github_stars AS "Stars", vault_open_tasks AS "Open tasks"
FROM "Machine/Metrics"
WHERE file.name = this.file.name
```

```tasks
not done
due before tomorrow
path does not include Templates
short mode
```

![[Machine/Logs/<% tp.date.now("YYYY-MM-DD") %>]]

## Brain dump

## Tomorrow

- 

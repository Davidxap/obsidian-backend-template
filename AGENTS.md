# AGENTS.md — Vault map

This vault is split into a **human zone** and a **machine zone**.

| Folder | Zone | Agent rule |
|---|---|---|
| `Human/` | Human | Read and copy freely. Write only when the user asks (a slash command or direct order counts). |
| `Machine/` | Machine | Read, write, edit without asking. |
| `Dashboard.md` | Front end | Read-only for agents. |

## Rules

1. Read **only** the `AGENTS.md` of the folder you work in. Do not load the whole vault.
2. After any task, append one line to `Machine/Logs/YYYY-MM-DD.md`: `- HH:MM [agent] what you did → result`.
3. Never write numbers into `Machine/Metrics/`; only collectors do. Never invent a number.
4. Before repeating a workflow, read its file in `Machine/Findings/`; afterwards, add what you learned.

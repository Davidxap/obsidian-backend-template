@AGENTS.md

## Claude Code notes

- Run `pytest -q` after touching anything in `Machine/Collectors/`; every collector change needs a test.
- Collectors must stay idempotent and must never write an estimated value: on failure call `common.mark_failed`.
- Keep `AGENTS.md` files short (under ~25 lines) and rules testable.
- All repository content is written in English.

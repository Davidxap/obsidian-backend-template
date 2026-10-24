"""Shared helpers for collectors: today's metrics note and frontmatter updates."""
from datetime import date
from pathlib import Path

VAULT_DIR = Path(__file__).resolve().parent.parent.parent
METRICS_DIR = VAULT_DIR / "Machine" / "Metrics"
LOGS_DIR = VAULT_DIR / "Machine" / "Logs"


def today_note() -> Path:
    return METRICS_DIR / f"{date.today().isoformat()}.md"


def read_note(path: Path) -> tuple[dict, str]:
    """Return (frontmatter as dict of strings, body); empty if the note is missing."""
    if not path.exists():
        return {}, ""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        return {}, text
    current = {}
    for line in head.splitlines():
        key, colon, value = line.partition(":")
        if colon and key.strip():
            current[key.strip()] = value.strip()
    return current, body


def update_frontmatter(path: Path, props: dict) -> None:
    """Merge props into the note's frontmatter (idempotent). None becomes an empty value."""
    path.parent.mkdir(parents=True, exist_ok=True)
    current, body = read_note(path)
    current.update({k: "" if v is None else str(v) for k, v in props.items()})
    front = "\n".join(f"{k}: {v}".rstrip() for k, v in current.items())
    path.write_text(f"---\n{front}\n---\n{body}", encoding="utf-8")


def mark_failed(path: Path, keys: list[str]) -> None:
    """On failure: create the keys empty, but never overwrite a real value written earlier."""
    current, _ = read_note(path)
    props = {"type": "metrics"}
    props.update({k: None for k in keys if k not in current})
    update_frontmatter(path, props)

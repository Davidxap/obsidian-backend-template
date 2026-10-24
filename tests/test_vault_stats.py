from datetime import date

import common
import vault_stats


def test_collect_counts_notes_and_open_tasks(vault):
    (vault / "Human" / "Projects" / "a.md").write_text("- [ ] one\n- [x] done\n- [ ] two\n")
    (vault / "Human" / "AGENTS.md").write_text("- [ ] must be ignored\n")
    props = vault_stats.collect(date.today())
    assert props["vault_notes_human"] == 1
    assert props["vault_open_tasks"] == 2
    assert props["vault_modified_today_human"] == 1


def test_missing_zone_marks_failed_and_exits_1(tmp_path, monkeypatch):
    monkeypatch.setattr(common, "VAULT_DIR", tmp_path)
    monkeypatch.setattr(common, "METRICS_DIR", tmp_path / "Machine" / "Metrics")
    monkeypatch.setattr(vault_stats, "today_note", lambda: tmp_path / "day.md")
    assert vault_stats.main() == 1
    props, _ = common.read_note(tmp_path / "day.md")
    assert props["vault_open_tasks"] == ""

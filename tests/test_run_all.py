from datetime import datetime

import run_all


def test_log_line_format():
    line = run_all.log_line("github", True, "updated x", datetime(2026, 1, 1, 8, 5))
    assert line == "- 08:05 [collector:github] ok → updated x\n"
    assert "failed" in run_all.log_line("github", False, "boom", datetime(2026, 1, 1, 8, 5))


def test_one_failing_collector_does_not_stop_the_rest(vault, monkeypatch):
    calls = []
    def fake(name):
        calls.append(name)
        return name != "github", "detail"
    monkeypatch.setattr(run_all, "run_one", fake)
    assert run_all.main() == 1
    assert calls == run_all.COLLECTORS
    log = next((vault / "Machine" / "Logs").glob("*.md")).read_text()
    assert "[collector:github] failed" in log and "[collector:vault_stats] ok" in log

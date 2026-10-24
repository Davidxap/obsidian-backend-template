import sys
from pathlib import Path

import pytest

COLLECTORS = Path(__file__).resolve().parent.parent / "Machine" / "Collectors"
sys.path.insert(0, str(COLLECTORS))

import common  # noqa: E402


@pytest.fixture
def vault(tmp_path, monkeypatch):
    """A throwaway vault; collectors are pointed at it instead of the real one."""
    (tmp_path / "Human" / "Projects").mkdir(parents=True)
    (tmp_path / "Machine" / "Metrics").mkdir(parents=True)
    (tmp_path / "Machine" / "Logs").mkdir(parents=True)
    monkeypatch.setattr(common, "VAULT_DIR", tmp_path)
    monkeypatch.setattr(common, "METRICS_DIR", tmp_path / "Machine" / "Metrics")
    monkeypatch.setattr(common, "LOGS_DIR", tmp_path / "Machine" / "Logs")
    return tmp_path

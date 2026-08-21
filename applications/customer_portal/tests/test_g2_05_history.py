"""G2-05 History store harness + snapshot isolation."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from applications.customer_portal.config import PORTAL_ROOT

FLOW_HARNESS = Path(__file__).parent / "js" / "result_store_flow.js"
STORE_JS = PORTAL_ROOT / "static" / "js" / "result_store.js"


def test_result_store_keeps_history_as_snapshot() -> None:
    source = STORE_JS.read_text(encoding="utf-8")
    assert "Explicit History never falls back to current" in source
    assert "findHistoryById" in source
    assert "HISTORY_LIMIT" in source


def test_g2_05_history_store_flow() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is required to execute the ResultStore harness")
    completed = subprocess.run(
        [node, str(FLOW_HARNESS)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "FAILED 0" in completed.stdout
    assert "PASS g205.save_once" in completed.stdout
    assert "PASS g205.missing_id_not_current" in completed.stdout
    assert "PASS g205.old_not_overwritten" in completed.stdout

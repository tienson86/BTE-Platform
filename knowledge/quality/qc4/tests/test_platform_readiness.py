"""QC-4 platform readiness and LTS flags."""
from __future__ import annotations

import json
from pathlib import Path

QC4 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
QC1 = REPO / "knowledge" / "quality" / "qc1"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_readiness_flags_match_gates() -> None:
    ready = _load(QC4 / "reports" / "platform_readiness.json")
    qc1_ready = _load(QC1 / "reports" / "release_readiness.json")
    by_gate = {item["gate"]: item for item in ready["gates"]}

    assert ready["architecture_ready"] is True
    assert ready["knowledge_ready"] is True
    assert ready["integration_ready"] is True
    assert ready["engine_complete"] is False
    assert ready["commercial_publication_ready"] is False
    assert ready["release_candidate_ready"] is True
    assert ready["lts_eligible"] is True
    assert qc1_ready["engine_complete"] is False
    assert by_gate["engine_complete"]["pass"] is False
    assert by_gate["golden_dataset_wired"]["pass"] is False
    assert by_gate["af1_package_index_covers_ecosystem"]["pass"] is False
    assert by_gate["architecture_freeze_intact"]["pass"] is True
    assert by_gate["no_runtime_changes"]["pass"] is True
    assert by_gate["qc1_zero_errors"]["pass"] is True
    assert by_gate["qc2_zero_errors"]["pass"] is True
    assert by_gate["qc3_zero_errors"]["pass"] is True
    assert ready["passed"] + ready["failed"] == len(ready["gates"])
    assert ready["failed"] == 3


def test_lts_line_is_v1x() -> None:
    lifecycle = _load(QC4 / "reports" / "lifecycle.json")
    assert lifecycle["line"] == "1.x"
    assert lifecycle["platform_version"] == "1.0.0"
    assert lifecycle["lts"]["eligible"] is True
    assert "Foundation 1.0.0" in lifecycle["lts"]["in_scope"][0]
    assert any("bz_16" in item for item in lifecycle["lts"]["out_of_scope"])

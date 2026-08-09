"""QC-3 audit continuity: no render artifacts, no audit breaks."""
from __future__ import annotations

import json
from pathlib import Path

QC3 = Path(__file__).resolve().parents[1]


def test_audit_flow_forbids_render_and_has_no_breaks() -> None:
    audit = json.loads((QC3 / "reports" / "audit_flow.json").read_text(encoding="utf-8"))
    assert audit["continuity"] is True
    assert audit["breaks"] == []
    assert len(audit["stages"]) == 5
    for stage in audit["stages"]:
        assert stage["html"] is False
        assert stage["pdf"] is False
        assert stage["docx"] is False
        assert stage["binary_artifacts"] is False
        assert stage["audit_fields"]


def test_rx1_audit_keeps_publisher_disabled() -> None:
    matrix = json.loads((QC3 / "reports" / "integration_matrix.json").read_text(encoding="utf-8"))
    rx1 = next(item for item in matrix["pipelines"] if item["sprint_id"] == "RX-1")
    assert "publisher" in rx1["inactive_stages"]
    assert "delivery" in rx1["inactive_stages"]
    assert "print" in rx1["inactive_stages"]
    assert "no_filesystem_persist" in rx1["audit_fields"]

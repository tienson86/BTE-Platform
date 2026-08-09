"""QC-3 end-to-end ordering and serialization."""
from __future__ import annotations

import json
from pathlib import Path

QC3 = Path(__file__).resolve().parents[1]
ORDER = ["AX-2", "AX-3", "AX-4", "IX-1", "RX-1"]


def test_end_to_end_order_and_inactive_slots() -> None:
    matrix = json.loads((QC3 / "reports" / "integration_matrix.json").read_text(encoding="utf-8"))
    pipelines = {item["sprint_id"]: item for item in matrix["pipelines"]}
    assert matrix["order"] == ORDER
    assert "luck_cycle" in pipelines["AX-2"]["inactive_stages"]
    assert "interpretation" in pipelines["AX-2"]["inactive_stages"]
    assert "report" in pipelines["AX-2"]["inactive_stages"]
    assert "interpretation" in pipelines["AX-3"]["inactive_stages"]
    assert "interpretation" in pipelines["AX-4"]["inactive_stages"]
    assert "report" in pipelines["AX-4"]["inactive_stages"]
    assert "ai_rewrite" in pipelines["IX-1"]["inactive_stages"]
    assert pipelines["AX-2"]["active_stages"][-1] == "useful_god"
    assert pipelines["AX-3"]["active_stages"] == [
        "useful_god_foundation",
        "useful_god_priority",
        "useful_god_override",
    ]


def test_report_serialization() -> None:
    for name in (
        "integration_matrix.json",
        "handoff_matrix.json",
        "contract_flow.json",
        "trace_flow.json",
        "audit_flow.json",
        "pipeline_status.json",
        "quality_metrics.json",
    ):
        payload = json.loads((QC3 / "reports" / name).read_text(encoding="utf-8"))
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        assert json.loads(encoded)
    validation = json.loads((QC3 / "validation" / "VALIDATION.json").read_text(encoding="utf-8"))
    assert validation["counts"]["errors"] == 0
    assert validation["status"] == "pass_with_warnings"

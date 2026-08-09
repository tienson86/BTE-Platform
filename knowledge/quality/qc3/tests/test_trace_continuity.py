"""QC-3 trace continuity across pipeline graph and QC-2 snapshots (read-only)."""
from __future__ import annotations

import json
from pathlib import Path

QC3 = Path(__file__).resolve().parents[1]
QC2 = Path(__file__).resolve().parents[2] / "qc2"
LAYERS = ("analysis", "decision", "luck", "interpretation", "report")


def test_trace_flow_has_no_breaks() -> None:
    trace = json.loads((QC3 / "reports" / "trace_flow.json").read_text(encoding="utf-8"))
    assert trace["continuity"] is True
    assert trace["breaks"] == []
    assert [item["sprint_id"] for item in trace["stages"]] == ["AX-2", "AX-3", "AX-4", "IX-1", "RX-1"]
    assert trace["stages"][0]["consumes_upstream_trace"] is False
    assert all(item["consumes_upstream_trace"] for item in trace["stages"][1:])
    assert all(item["trace_fields"] for item in trace["stages"])


def test_qc2_layer_snapshots_exist_for_trace_evidence() -> None:
    catalog = json.loads((QC2 / "datasets" / "scenario_catalog.json").read_text(encoding="utf-8"))
    assert catalog["scenarios"]
    for scenario in catalog["scenarios"]:
        for snapshot_id, layer in zip(scenario["snapshot_ids"], LAYERS, strict=True):
            path = QC2 / "snapshots" / layer / f"{snapshot_id}.json"
            item = json.loads(path.read_text(encoding="utf-8"))
            assert item["trace"]["package_ids"]
            assert item["scenario_id"] == scenario["scenario_id"]

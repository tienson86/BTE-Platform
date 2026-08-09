"""QC-2 snapshot integrity: ids, layers, no render artifacts."""
from __future__ import annotations

import json
from pathlib import Path

QC2 = Path(__file__).resolve().parents[1]
LAYERS = ("analysis", "decision", "luck", "interpretation", "report")


def _snapshots() -> list[dict]:
    items = []
    for layer in LAYERS:
        for path in sorted((QC2 / "snapshots" / layer).glob("*.json")):
            items.append(json.loads(path.read_text(encoding="utf-8")))
    return items


def test_one_snapshot_per_scenario_layer() -> None:
    catalog = json.loads((QC2 / "datasets" / "scenario_catalog.json").read_text(encoding="utf-8"))
    snapshots = _snapshots()
    assert len(snapshots) == 65
    ids = [item["snapshot_id"] for item in snapshots]
    assert len(set(ids)) == 65
    by_scenario = {item["scenario_id"]: item["snapshot_ids"] for item in catalog["scenarios"]}
    present = {item["snapshot_id"] for item in snapshots}
    for snapshot_ids in by_scenario.values():
        assert len(snapshot_ids) == 5
        assert set(snapshot_ids) <= present


def test_audit_forbids_render_artifacts() -> None:
    for item in _snapshots():
        audit = item["audit"]
        assert audit["html"] is False
        assert audit["css"] is False
        assert audit["pdf"] is False
        assert audit["docx"] is False
        assert audit["binary_artifacts"] is False
        assert audit["renderer"] is None
        assert audit["prose_embedded"] is False
        blob = json.dumps(item, ensure_ascii=False).lower()
        assert "<html" not in blob
        assert "%pdf" not in blob

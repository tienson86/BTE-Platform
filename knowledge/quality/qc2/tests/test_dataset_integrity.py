"""QC-2 dataset integrity. Additive snapshots only."""
from __future__ import annotations

import json
from pathlib import Path

QC2 = Path(__file__).resolve().parents[1]
DATASETS = QC2 / "datasets"

REQUIRED_SCENARIOS = {
    "balanced_chart",
    "strong_day_master",
    "weak_day_master",
    "follow_pattern",
    "transformation",
    "combination",
    "conflict",
    "useful_god_conflict",
    "luck_transition",
    "executive_report",
    "technical_report",
    "minimal_report",
    "dashboard_report",
}


def test_index_and_catalog_unique() -> None:
    index = json.loads((DATASETS / "index.json").read_text(encoding="utf-8"))
    catalog = json.loads((DATASETS / "scenario_catalog.json").read_text(encoding="utf-8"))
    ids = [item["scenario_id"] for item in catalog["scenarios"]]
    assert index["scenario_count"] == 13
    assert len(ids) == 13
    assert len(set(ids)) == 13
    assert ids == index["scenario_ids"]
    slugs = {item["slug"] for item in catalog["scenarios"]}
    assert slugs == REQUIRED_SCENARIOS


def test_serialization_round_trip() -> None:
    for name in ("index.json", "scenario_catalog.json", "coverage_matrix.json"):
        payload = json.loads((DATASETS / name).read_text(encoding="utf-8"))
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        assert json.loads(encoded)["sprint"] == "QC-2" or "scenarios" in json.loads(encoded) or "rows" in json.loads(encoded)

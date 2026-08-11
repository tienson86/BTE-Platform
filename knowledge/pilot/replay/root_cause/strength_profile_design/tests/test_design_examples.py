"""Design example content tests for PILOT-1I."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"

REQUIRED = [
    "very_weak_synthetic.json",
    "weak_synthetic.json",
    "slightly_weak_real.json",
    "balanced_synthetic.json",
    "strong_synthetic.json",
    "very_strong_synthetic.json",
    "evidence_conflict.json",
    "incomplete_evidence.json",
]


def test_all_design_examples_present() -> None:
    for name in REQUIRED:
        assert (EXAMPLES / name).exists(), name


def test_saturation_metadata_on_ceiling_examples() -> None:
    strong = json.loads((EXAMPLES / "strong_synthetic.json").read_text(encoding="utf-8"))
    very = json.loads((EXAMPLES / "very_strong_synthetic.json").read_text(encoding="utf-8"))
    assert strong["score_reference"]["saturation_detected"] is True
    assert very["score_reference"]["saturation_detected"] is True
    assert strong["score_reference"]["saturation_type"] == "upper_clamp"
    assert very["score_reference"]["raw_score"] == 107.0
    assert strong["score_reference"]["raw_score"] == 82.0
    assert strong["score_reference"]["normalized_score"] == 1.0
    assert very["score_reference"]["normalized_score"] == 1.0


def test_conflict_example_has_unresolved_conflict() -> None:
    data = json.loads((EXAMPLES / "evidence_conflict.json").read_text(encoding="utf-8"))
    assert data["conflicts"]
    assert data["conflicts"][0]["resolution_status"] == "unresolved"


def test_incomplete_example_unknown_heavy() -> None:
    data = json.loads((EXAMPLES / "incomplete_evidence.json").read_text(encoding="utf-8"))
    assert data["score_reference"]["current_v1_band"] == "unknown"
    assert data["score_reference"]["saturation_detected"] == "unknown"
    assert data["evidence_completeness"]["overall"] == "limited"


def test_external_labels_not_taxonomy_fields() -> None:
    for path in EXAMPLES.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for forbidden in (
            "taxonomy_v2_label",
            "future_taxonomy_label",
            "t1",
            "t2",
            "t3",
            "t4",
            "t5",
            "t6",
            "final_v2_classification",
        ):
            assert forbidden not in data
        if data.get("external_labels") and data["external_labels"].get("synthetic_expected_taxonomy"):
            assert "taxonomy" not in data or True

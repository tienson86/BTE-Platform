"""Population separation tests for PILOT-1I."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
CAL_DIR = ROOT.parents[0] / "strength_taxonomy_v2" / "calibration" / "cases"
SYN_DIR = ROOT.parents[1] / "synthetic_strength" / "datasets"


def test_no_new_cal_ids() -> None:
    cal_ids = sorted(p.stem for p in CAL_DIR.glob("CAL-*.json"))
    assert cal_ids == [f"CAL-{n:06d}" for n in range(1, 8)]


def test_synthetic_unchanged_count() -> None:
    syn_ids = sorted(p.stem for p in SYN_DIR.glob("SYN-STR-*.json"))
    assert len(syn_ids) == 21


def test_design_examples_marked() -> None:
    for path in EXAMPLES.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["design_marker"] == "design_example"
        assert data["population"] == "design_example"
        assert data["identity"]["population"] == "design_example"


def test_synthetic_flags_on_synthetic_examples() -> None:
    for name in (
        "very_weak_synthetic.json",
        "weak_synthetic.json",
        "balanced_synthetic.json",
        "strong_synthetic.json",
        "very_strong_synthetic.json",
        "evidence_conflict.json",
        "incomplete_evidence.json",
    ):
        data = json.loads((EXAMPLES / name).read_text(encoding="utf-8"))
        flags = data["synthetic_flags"]
        assert flags["synthetic"] is True
        assert flags["calibration_eligible"] is False
        assert flags["golden_eligible"] is False
        assert flags["expert_calibration_eligible"] is False


def test_real_example_keeps_expert_external() -> None:
    data = json.loads((EXAMPLES / "slightly_weak_real.json").read_text(encoding="utf-8"))
    assert data["source_case_ref"] if False else data["identity"]["source_case_ref"] == "CAL-000001"
    assert data.get("taxonomy_v2_label") is None
    assert "taxonomy_v2_label" not in data
    assert data["external_labels"]["expert_taxonomy_candidate"] == "slightly_weak"
    assert data["synthetic_flags"] is None

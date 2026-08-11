"""Population separation tests for PILOT-1H."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CAL_DIR = ROOT.parents[0] / "strength_taxonomy_v2" / "calibration" / "cases"
SYN_DIR = ROOT.parents[1] / "synthetic_strength" / "datasets"


def test_real_and_synthetic_ids_not_mixed_in_trace() -> None:
    trace = json.loads((REPORTS / "score_trace.json").read_text(encoding="utf-8"))
    for case in trace["cases"]:
        pop = case["population"]
        cid = case["case_id"]
        if pop == "REAL_CALIBRATION":
            assert cid.startswith("CAL-")
            assert "synthetic_expected" not in case or case.get("synthetic_expected") in (None, "N/A")
        elif pop == "SYNTHETIC_STRESS":
            assert cid.startswith("SYN-STR-")
            assert "expert" not in case or case.get("expert") in (None, "N/A")
        else:
            raise AssertionError(f"unexpected population {pop}")


def test_no_new_cal_ids_created_by_this_sprint() -> None:
    """Diagnostic sprint must not add CAL case files."""
    cal_ids = sorted(p.stem for p in CAL_DIR.glob("CAL-*.json"))
    assert cal_ids == [
        "CAL-000001",
        "CAL-000002",
        "CAL-000003",
        "CAL-000004",
        "CAL-000005",
        "CAL-000006",
        "CAL-000007",
    ]


def test_synthetic_dataset_count_unchanged() -> None:
    syn_ids = sorted(p.stem for p in SYN_DIR.glob("SYN-STR-*.json"))
    assert len(syn_ids) == 21
    assert syn_ids[0] == "SYN-STR-000001"
    assert syn_ids[-1] == "SYN-STR-000021"


def test_dual_reviewed_n_documented() -> None:
    text = (ROOT / "REAL_CALIBRATION_DIAGNOSTIC.md").read_text(encoding="utf-8")
    assert "n = 2 dual-reviewed" in text
    assert "CAL-000001" in text
    assert "CAL-000006" in text


def test_collision_keeps_population_labels() -> None:
    text = (ROOT / "SCORE_COLLISION_ANALYSIS.md").read_text(encoding="utf-8")
    assert "REAL_CALIBRATION" in text
    assert "SYNTHETIC_STRESS" in text
    assert "Never merge" not in text  # soft
    collision = json.loads((REPORTS / "collision_analysis.json").read_text(encoding="utf-8"))
    assert collision["score_only_sufficient"] is False

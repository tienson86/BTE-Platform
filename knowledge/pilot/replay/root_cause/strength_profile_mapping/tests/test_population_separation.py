"""Population separation tests for PILOT-1J."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CAL_DIR = ROOT.parents[0] / "strength_taxonomy_v2" / "calibration" / "cases"
SYN_DIR = ROOT.parents[1] / "synthetic_strength" / "datasets"


def test_cal_ids_unchanged() -> None:
    cal_ids = sorted(p.stem for p in CAL_DIR.glob("CAL-*.json"))
    assert cal_ids == [f"CAL-{n:06d}" for n in range(1, 8)]


def test_syn_ids_unchanged() -> None:
    assert len(list(SYN_DIR.glob("SYN-STR-*.json"))) == 21


def test_result_populations() -> None:
    real = []
    syn = []
    for path in RESULTS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["population"] == "real_calibration":
            real.append(data["case_id"])
            assert data["profile"]["population"] == "real_calibration"
            assert data["profile"]["synthetic_flags"] is None
            assert data["expert_review_reference"] is not None
        elif data["population"] == "synthetic_stress":
            syn.append(data["case_id"])
            flags = data["profile"]["synthetic_flags"]
            assert flags["synthetic"] is True
            assert flags["calibration_eligible"] is False
            assert flags["golden_eligible"] is False
            assert flags["expert_calibration_eligible"] is False
            assert data["expert_review_reference"] is None
        else:
            raise AssertionError(data["population"])
    assert sorted(real) == ["CAL-000001", "CAL-000006"]
    assert len(syn) == 21

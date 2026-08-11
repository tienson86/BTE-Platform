"""Population separation: REAL / SYN / design / runtime stay separate."""

from __future__ import annotations

import json

from .helpers import CAL_DIR, CASES, REPORTS, ROOT, SYN_DIR, VALIDATION


def test_existing_cal_ids_unchanged_count() -> None:
    cal_ids = sorted(p.stem for p in CAL_DIR.glob("CAL-*.json"))
    assert cal_ids == [f"CAL-{n:06d}" for n in range(1, 8)]


def test_synthetic_unchanged_count() -> None:
    syn_ids = sorted(p.stem for p in SYN_DIR.glob("SYN-STR-*.json"))
    assert len(syn_ids) == 21


def test_round3_cases_dir_has_no_new_cal_or_syn() -> None:
    assert list(CASES.glob("CAL-*.json")) == []
    assert list(CASES.glob("SYN-*.json")) == []
    assert list(CASES.rglob("**/CAL-*")) == []


def test_coverage_references_only_existing_dual() -> None:
    data = json.loads((REPORTS / "coverage_matrix.json").read_text(encoding="utf-8"))
    assert data["existing_dual_reviewed"] == ["CAL-000001", "CAL-000006"]
    assert data["new_cal_ids_created"] == []
    assert data["next_free_calibration_id"] == "CAL-000008"


def test_summary_keeps_populations_separated() -> None:
    text = (ROOT / "PILOT_1L_SUMMARY.md").read_text(encoding="utf-8")
    assert "CALIBRATION_DATA_CHANGED: NO" in text
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    data = json.loads((VALIDATION / "VALIDATION.json").read_text(encoding="utf-8"))
    assert data["cal_000001_unchanged"] is True
    assert data["cal_000006_unchanged"] is True
    assert data["syn_unchanged"] is True

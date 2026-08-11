"""Population separation and existing case protection."""

from __future__ import annotations

from .helpers import CAL_DIR, REPORTS, ROOT, SYN_DIR, VALIDATION, load_json


def test_existing_cal_ids_unchanged() -> None:
    cal_ids = sorted(p.stem for p in CAL_DIR.glob("CAL-*.json"))
    assert cal_ids == [f"CAL-{n:06d}" for n in range(1, 8)]


def test_synthetic_unchanged() -> None:
    syn_ids = sorted(p.stem for p in SYN_DIR.glob("SYN-STR-*.json"))
    assert len(syn_ids) == 21


def test_coverage_references_existing_dual_only() -> None:
    data = load_json(REPORTS / "current_coverage.json")
    assert data["existing_dual_reviewed"] == {
        "CAL-000001": "slightly_weak",
        "CAL-000006": "slightly_weak",
    }
    assert data["dual_reviewed_by_level"]["slightly_weak"] == 2
    assert data["cal_ids_allocated_this_sprint"] == []
    assert data["next_free_calibration_id"] == "CAL-000008"


def test_validation_protection_flags() -> None:
    data = load_json(VALIDATION / "VALIDATION.json")
    assert data["cal_000001_unchanged"] is True
    assert data["cal_000006_unchanged"] is True
    assert data["syn_unchanged"] is True
    assert data["existing_dual_reviewed_cases"] == 2


def test_queue_p0_gaps() -> None:
    text = (ROOT / "queue" / "P0_GAPS.md").read_text(encoding="utf-8")
    assert "very_weak" in text
    assert "weak" in text
    assert "balanced" in text

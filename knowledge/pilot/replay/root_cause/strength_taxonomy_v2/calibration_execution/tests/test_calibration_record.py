"""Calibration record specification tests."""

from __future__ import annotations

from .helpers import ROOT, TEMPLATES, load_json


def test_calibration_record_required_fields() -> None:
    data = load_json(TEMPLATES / "calibration_record.json")
    for field in (
        "case_id",
        "acquisition_id",
        "verified_birth_data",
        "calendar_verification",
        "expert_a",
        "expert_b",
        "agreement",
        "adjudication",
        "runtime_reference",
        "calibration_status",
        "provenance",
    ):
        assert field in data
    assert data["layers_separate"] is True


def test_calibration_spec_separates_layers() -> None:
    text = (ROOT / "CALIBRATION_RECORD_SPEC.md").read_text(encoding="utf-8")
    assert "runtime" in text.lower()
    assert "expert" in text.lower()
    assert "separate" in text.lower()

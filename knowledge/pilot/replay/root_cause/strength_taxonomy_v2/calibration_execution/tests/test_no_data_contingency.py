"""No-data contingency honesty tests."""

from __future__ import annotations

from .helpers import EXECUTION, PACKETS, REPORTS, ROOT, VALIDATION, load_json


def test_execution_status_is_no_data() -> None:
    data = load_json(REPORTS / "execution_status.json")
    assert data["execution_status"] == "no_data"
    assert data["new_real_cases"] == 0
    assert data["new_verified_cases"] == 0
    assert data["new_dual_reviewed_cases"] == 0
    assert data["final_decision"] == "CALIBRATION_PARTIAL"
    assert data["premature_cal_allocation_prevented"] is True
    assert data["active_cases"] == []


def test_readiness_data_gap() -> None:
    data = load_json(REPORTS / "readiness.json")
    assert data["readiness"] == "data_gap"
    assert data["final_decision"] == "CALIBRATION_PARTIAL"


def test_no_packets_or_execution_artifacts() -> None:
    assert list(PACKETS.glob("*.json")) == []
    assert list(EXECUTION.glob("*.json")) == []


def test_no_data_contingency_doc() -> None:
    text = (ROOT / "NO_DATA_CONTINGENCY.md").read_text(encoding="utf-8")
    assert "CAL-000008" in text
    assert "no_data" in text
    assert "CALIBRATION_PARTIAL" in text
    assert "fake" in text.lower()


def test_validation_no_data_flags() -> None:
    data = load_json(VALIDATION / "VALIDATION.json")
    assert data["cal_000008_created"] is False
    assert data["no_data_contingency_validated"] is True
    assert data["new_real_cases_acquired"] == 0

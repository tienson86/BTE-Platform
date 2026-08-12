"""Active-case contingency honesty tests."""

from __future__ import annotations

from .helpers import EXECUTION, PACKETS, REPORTS, ROOT, VALIDATION, load_json


def test_execution_status_ready_for_expert_a() -> None:
    data = load_json(REPORTS / "execution_status.json")
    assert data["execution_status"] == "active_case_ready_for_expert_a"
    assert data["new_real_cases"] == 1
    assert data["new_verified_cases"] == 1
    assert data["new_dual_reviewed_cases"] == 0
    assert data["final_decision"] == "CALIBRATION_PARTIAL"
    assert data["premature_cal_allocation_prevented"] is True
    assert data["active_cases"] == ["CAL-000008"]
    assert data["expert_a_review_status"] == "pending_independent_expert_a"
    assert data["expert_b_status"] == "blocked_pending_expert_a"


def test_readiness_ready_for_expert_a() -> None:
    data = load_json(REPORTS / "readiness.json")
    assert data["readiness"] == "ready_for_expert_a"
    assert data["final_decision"] == "CALIBRATION_PARTIAL"
    assert data["active_cases"] == ["CAL-000008"]


def test_only_expert_a_packet_and_execution_artifacts_exist() -> None:
    assert (PACKETS / "CAL-000008" / "expert_a_packet.json").is_file()
    assert not (PACKETS / "CAL-000008" / "expert_b_packet.json").exists()
    assert (EXECUTION / "CAL-000008" / "intake_record.json").is_file()
    assert not (EXECUTION / "CAL-000008" / "expert_a_review.json").exists()


def test_no_data_contingency_doc() -> None:
    text = (ROOT / "NO_DATA_CONTINGENCY.md").read_text(encoding="utf-8")
    assert "CAL-000008" in text
    assert "no_data" in text
    assert "CALIBRATION_PARTIAL" in text
    assert "fake" in text.lower()


def test_validation_no_fabrication_flags() -> None:
    data = load_json(VALIDATION / "VALIDATION.json")
    assert data["cal_000008_created"] is True
    assert data["cal_000008_ready_for_expert_a"] is True
    assert data["cal_000008_expert_a_review_created"] is False
    assert data["cal_000008_expert_b_created"] is False
    assert data["no_data_contingency_validated"] is True
    assert data["new_real_cases_acquired"] == 1
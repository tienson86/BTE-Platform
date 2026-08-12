"""CAL-000008 active intake and Expert-A readiness tests."""

from __future__ import annotations

from .helpers import EXECUTION, PACKETS, load_json


CASE_EXECUTION = EXECUTION / "CAL-000008"
CASE_PACKET = PACKETS / "CAL-000008" / "expert_a_packet.json"


def test_cal_000008_intake_verified_and_allocated_after_eligibility() -> None:
    intake = load_json(CASE_EXECUTION / "intake_record.json")
    eligibility = load_json(CASE_EXECUTION / "eligibility_report.json")

    assert intake["cal_id"] == "CAL-000008"
    assert intake["case_status"] == "ready_for_expert_a"
    assert intake["verification_status"] == "verified_by_source"
    assert eligibility["eligible_for_expert_a"] is True
    assert eligibility["cal_id_allocation"]["allocation_reason"] == (
        "real_authorized_chart_passed_intake_eligibility"
    )


def test_cal_000008_calendar_uses_user_verified_pillars_without_rederivation() -> None:
    calendar = load_json(CASE_EXECUTION / "calendar_verification.json")

    assert calendar["pillar_source"] == "user_verified"
    assert calendar["year_pillar"] == "dinh_suu"
    assert calendar["month_pillar"] == "quy_suu"
    assert calendar["day_pillar"] == "at_mao"
    assert calendar["hour_pillar"] == "giap_than"
    assert calendar["calendar_status"] == "verified"
    assert "not_rederived" in calendar["local_time_interpretation"]


def test_expert_a_packet_has_no_runtime_or_prelabel_leaks() -> None:
    packet = load_json(CASE_PACKET)
    text = CASE_PACKET.read_text(encoding="utf-8").lower()

    assert packet["review_status"] == "pending_independent_expert_a"
    assert "strength_level" in packet["review_instructions"]["required_output_fields"]
    assert "runtime_score" not in text
    assert "runtime_band" not in text
    assert "expected_classification" in packet["review_instructions"]["must_not_use"]
    assert "slightly_weak" in packet["review_instructions"]["candidate_strength_levels"]


def test_no_expert_judgment_or_expert_b_created() -> None:
    status = load_json(CASE_EXECUTION / "ready_for_expert_a.json")

    assert status["expert_a_review_created"] is False
    assert status["expert_b_packet_created"] is False
    assert status["expert_b_review_created"] is False
    assert not (CASE_EXECUTION / "expert_a_review.json").exists()
    assert not (PACKETS / "CAL-000008" / "expert_b_packet.json").exists()
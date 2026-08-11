"""Source classification and acceptable/forbidden source rules."""

from __future__ import annotations

from .helpers import ROOT


def test_source_log_lists_acceptable_categories() -> None:
    text = (ROOT / "ROUND_3_SOURCE_LOG.md").read_text(encoding="utf-8")
    for token in (
        "user_provided_birth_data",
        "authorized_consultant_records",
        "authorized_historical_case_records",
        "authorized_anonymized_client_records",
        "public_case_material_lawful_and_verifiable",
    ):
        assert token in text


def test_source_log_forbids_fabrication_sources() -> None:
    text = (ROOT / "ROUND_3_SOURCE_LOG.md").read_text(encoding="utf-8")
    for token in (
        "random invented dates",
        "synthetic charts as real",
        "ai_generated_charts_as_real",
        "unverified social claims",
    ):
        assert token in text


def test_source_verification_guide_present() -> None:
    text = (ROOT / "SOURCE_VERIFICATION_GUIDE.md").read_text(encoding="utf-8")
    assert "source_precision" in text
    assert "timezone_verified" in text
    assert "birth_time_verified" in text


def test_requirements_list_eligibility() -> None:
    text = (ROOT / "ROUND_3_REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "calendar_verified" in text
    assert "not synthetic" in text
    assert "intake_pending" in text
    assert "eligible_for_expert_a" in text
    assert "eligible_for_expert_b" in text

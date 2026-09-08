"""Stable version tokens for TV1-B05 Report Profile."""

from __future__ import annotations

from typing import Final

REPORT_PROFILE_ID: Final[str] = "marriage.report.profile.v1"
REPORT_PROFILE_VERSION: Final[str] = "1.1.0"
REPORT_MODEL_VERSION: Final[str] = "marriage.report.model.v1@1.1.0"

CUSTOMER_STORY_ORDER: Final[tuple[str, ...]] = (
    "identity",
    "executive_summary",
    "compatibility_hero",
    "strengths",
    "risks",
    "comparison_a_to_b",
    "comparison_b_to_a",
    "comparison_harmony",
    "comparison_conflict",
    "comparison_rescue",
    "cung_phi",
    "timing",
    "domain_analysis",
    "action_plan",
    "confidence_limitations",
    "conclusion",
    "appendix",
)

REQUIRED_CUSTOMER_SECTIONS: Final[tuple[str, ...]] = (
    "identity",
    "executive_summary",
    "compatibility_hero",
    "strengths",
    "risks",
    "action_plan",
    "confidence_limitations",
    "conclusion",
    "appendix",
)


def report_profile_token() -> str:
    """Return the bound report profile identity."""
    return f"{REPORT_PROFILE_ID}@{REPORT_PROFILE_VERSION}"

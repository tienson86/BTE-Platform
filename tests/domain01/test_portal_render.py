"""Portal-facing projection for Career Selection Assessment (no layout change)."""

from __future__ import annotations

from applications.api.services.narrative_result_truth import build_narrative_result_dict
from engines.commercial_knowledge import CAREER_SELECTION_ALLOW_LIST

from .conftest import CAREER_SELECTION_FIELDS, baseline_interpretation, strong_employee_chart


def _portal_project(narrative: dict) -> dict[str, str]:
    """
    Mirror customer_portal careerFieldText preference for existing Result slots.

    Does not invent UI — only maps assessment fields into existing content roles.
    """
    assessment = narrative.get("career_selection_assessment") or {}
    bundle = narrative.get("commercial_knowledge_bundle") or {}
    if not assessment:
        assessment = bundle.get("career_selection_assessment") or {}

    def _text(key: str) -> str:
        item = assessment.get(key) or {}
        return str(item.get("text") or "").strip()

    return {
        "executive": _text("career_direction"),
        "strengths": _text("career_strengths"),
        "warnings": _text("career_risks"),
        "mitigation": _text("career_mitigation"),
        "actions": _text("action_plan_90d"),
        "role": _text("preferred_role"),
        "environment": _text("working_environment"),
    }


def test_portal_receives_career_selection_on_narrative_result() -> None:
    """Production narrative_result attaches Career Selection for Portal slots."""
    result = build_narrative_result_dict(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        run_id="portal-1",
        include_commercial_knowledge=True,
    )
    assessment = result["career_selection_assessment"]
    assert assessment["capability_id"] == "CAP-D1-CA-SEL"
    for field_name in CAREER_SELECTION_FIELDS:
        assert assessment[field_name]["text"]
        assert assessment[field_name]["knowledge_unit_id"] in CAREER_SELECTION_ALLOW_LIST

    projected = _portal_project(result)
    assert "Họ nghề hợp bạn" in projected["executive"]
    assert projected["actions"].startswith("Kế hoạch 90 ngày")
    assert projected["strengths"]
    assert projected["warnings"]
    assert projected["role"]
    assert projected["environment"]
    assert result["career_selection_label"] == "Career Selection Assessment"
    assert result["promotion_readiness_label"] == "Promotion Readiness Assessment"
    assert result["primary_recommendation"]["what"]
    assert "What:" in result["primary_recommendation"]["composed_text"]
    assert "Promotion Readiness Assessment" in result["secondary_career_milestone"][
        "composed_text"
    ]
    executive = result["commercial_executive_summary"]
    assert executive["central_message"]
    assert len(executive["supporting_points"]) <= 3
    assert executive["conclusion"]
    assert "Dụng thần" not in executive["composed_text"]


def test_portal_projection_does_not_require_new_route() -> None:
    """Career content rides existing narrative_result contract fields only."""
    result = build_narrative_result_dict(
        analysis=strong_employee_chart(),
        interpretation=baseline_interpretation(),
        run_id="portal-2",
    )
    assert result.get("contract") == "pack05_narrative_result_v1"
    assert "career_selection_assessment" in result
    assert "commercial_knowledge_bundle" in result
    # No alternate screen/route payload keys.
    assert "career_selection_page" not in result
    assert "new_route" not in result

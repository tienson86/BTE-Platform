"""Commercial Bundle mapping for Career Selection Assessment."""

from __future__ import annotations

from engines.commercial_knowledge import (
    CAREER_SELECTION_ALLOW_LIST,
    PRODUCTION_ALLOW_LIST,
    CommercialKnowledgeAdapter,
    bundle_to_dict,
)

from .conftest import (
    CAREER_SELECTION_FIELDS,
    assert_career_selection_complete,
    strong_employee_chart,
)


def test_bundle_maps_all_career_selection_fields() -> None:
    """Bundle exposes the eleven Career Selection Assessment fields."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
        run_id="bundle-1",
    )
    assert_career_selection_complete(bundle.career_selection)
    assert bundle.career_selection is not None
    assert bundle.career_selection.career_direction.evidence_kind == "career_direction"
    assert bundle.career_selection.working_environment.evidence_kind == "career_environment"
    assert bundle.career_selection.preferred_role.evidence_kind == "career_org_role"
    assert bundle.career_selection.leadership_posture.evidence_kind == "career_lead_vs_spec"
    assert bundle.career_selection.employment_posture.evidence_kind == "career_path_mode"
    assert bundle.career_selection.career_strengths.evidence_kind == "career_advantage"
    assert bundle.career_selection.career_risks.evidence_kind == "career_risk"
    assert bundle.career_selection.career_mitigation.evidence_kind == "career_mitigation"
    assert bundle.career_selection.development_focus.evidence_kind == "career_development"
    assert bundle.career_selection.timing_guidance.evidence_kind == "career_timing"
    assert bundle.career_selection.action_plan_90d.evidence_kind == "action"
    assert bundle.career_selection.action_plan_90d.knowledge_unit_id == "KU-AC-CA-000001"


def test_bundle_dict_exposes_assessment_not_raw_units() -> None:
    """Serialized bundle carries assessment projection without raw KU rows."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(
        analysis=strong_employee_chart(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
    )
    payload = bundle_to_dict(bundle)
    assessment = payload["career_selection_assessment"]
    assert assessment["capability_id"] == "CAP-D1-CA-SEL"
    for field_name in CAREER_SELECTION_FIELDS:
        assert assessment[field_name]["text"]
        assert assessment[field_name]["knowledge_unit_id"] in CAREER_SELECTION_ALLOW_LIST
    assert "modern_interpretation" not in payload
    assert "classical_text" not in str(payload)

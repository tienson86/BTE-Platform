"""Career Golden Cases — Career Selection Assessment production path."""

from __future__ import annotations

import pytest

from applications.api.services.narrative_result_truth import build_narrative_result_dict
from engines.commercial_knowledge import (
    PRODUCTION_ALLOW_LIST,
    CommercialKnowledgeAdapter,
)

from .conftest import (
    CAREER_SELECTION_FIELDS,
    assert_career_selection_complete,
    baseline_interpretation,
    mixed_employee_chart,
    strong_employee_chart,
    weak_employee_chart,
)

GOLDEN_CASES = (
    ("D1-GC-STRONG-EMP", strong_employee_chart),
    ("D1-GC-WEAK-EMP", weak_employee_chart),
    ("D1-GC-MIXED-EMP", mixed_employee_chart),
)


@pytest.mark.parametrize("case_id,factory", GOLDEN_CASES)
def test_golden_case_career_selection_complete(case_id: str, factory) -> None:
    """Each P0 Career Golden Case fills all SEL assessment fields."""
    adapter = CommercialKnowledgeAdapter()
    bundle, _payload = adapter.adapt(
        analysis=factory(),
        allow_list_ids=PRODUCTION_ALLOW_LIST,
        run_id=case_id,
        scenario_id="default",
    )
    assert_career_selection_complete(bundle.career_selection)
    assert "CAP-D1-CA-SEL" in bundle.metadata["capabilities"]
    assert "CAP-D1-CA-PRO" in bundle.metadata["capabilities"]


@pytest.mark.parametrize("case_id,factory", GOLDEN_CASES)
def test_golden_case_acceptance_checklist(case_id: str, factory) -> None:
    """Acceptance checklist: direction, environment, role, postures, risks, 90d."""
    result = build_narrative_result_dict(
        analysis=factory(),
        interpretation=baseline_interpretation(),
        run_id=case_id,
        include_commercial_knowledge=True,
    )
    assessment = result["career_selection_assessment"]
    assert assessment["status"] in {"complete", "partial"}
    for field_name in CAREER_SELECTION_FIELDS:
        text = assessment[field_name]["text"]
        assert text.strip(), f"{case_id} missing {field_name}"
        assert "kích hoạt khi" not in text.lower()
        assert "(mock)" not in text.lower()

    assert "Họ nghề" in assessment["career_direction"]["text"]
    assert "Môi trường" in assessment["working_environment"]["text"]
    assert "Vai trò" in assessment["preferred_role"]["text"]
    assert "Lãnh đạo hay chuyên gia" in assessment["leadership_posture"]["text"]
    assert "Làm thuê hay độc lập" in assessment["employment_posture"]["text"]
    assert "Lợi thế nghề" in assessment["career_strengths"]["text"]
    assert "Rủi ro nghề" in assessment["career_risks"]["text"]
    assert "Giảm rủi ro" in assessment["career_mitigation"]["text"]
    assert "Ưu tiên phát triển" in assessment["development_focus"]["text"]
    assert "Nhịp quyết định" in assessment["timing_guidance"]["text"]
    assert "Kế hoạch 90 ngày" in assessment["action_plan_90d"]["text"]

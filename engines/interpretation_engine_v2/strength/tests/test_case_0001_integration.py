"""Integration test for CASE-0001."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.runtime.service import StrengthInterpretationService
from engines.interpretation_engine_v2.strength.tests.test_reasoner import GOLDEN_SELECTED


def test_case_0001_integration() -> None:
    service = StrengthInterpretationService()
    result = service.run_case_0001()
    assert result.meta.case_id == "CASE-0001"
    assert result.narrative_plan.primary_conclusion["class_id"] == "strong"
    assert result.validation_mode
    assert result.customer_mode
    assert result.validation_mode[0].section_id == "CONCLUSION"
    assert any(section.section_id == "EVIDENCE" for section in result.validation_mode)
    assert not any(section.section_id == "EVIDENCE" for section in result.customer_mode)

    by_section = {section.section_id: section for section in result.narrative_plan.sections}
    for section_id, expected_ids in GOLDEN_SELECTED.items():
        selected = {item.knowledge_id for item in by_section[section_id].selected_units}
        assert selected == expected_ids

    customer_text = "\n".join(
        paragraph
        for section in result.customer_mode
        for paragraph in section.paragraphs
    )
    assert "Strong" in customer_text
    assert "luck" in customer_text.lower() or "timing" in customer_text.lower()

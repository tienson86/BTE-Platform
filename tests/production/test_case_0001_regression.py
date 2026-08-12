"""CASE-0001 golden regression through generic pipeline."""

from __future__ import annotations

from applications.production.fixtures.case_0001 import (
    CASE_0001_EXPECTED_PILLARS,
    CASE_0001_EXPECTED_STRENGTH,
    CASE_0001_REQUEST,
)
from applications.production.orchestrator import ProductionEndToEndOrchestrator
from engines.interpretation_engine_v2.strength.runtime.published_facts_adapter import (
    build_published_strength_facts,
)
from engines.interpretation_engine_v2.strength.runtime.service import (
    StrengthInterpretationService,
)
from engines.interpretation_engine_v2.strength.tests.test_reasoner import GOLDEN_SELECTED


def test_case_0001_pillars_regression(case_0001_generic_result) -> None:
    """Generic pipeline preserves canonical CASE-0001 pillars."""
    analysis = case_0001_generic_result.diagnostics["engine_analysis"]
    pillars = analysis["pillars"]
    for key, expected in CASE_0001_EXPECTED_PILLARS.items():
        assert pillars[key] == expected


def test_case_0001_strength_regression(case_0001_generic_result) -> None:
    """Generic pipeline preserves canonical strength classification."""
    strength = case_0001_generic_result.diagnostics["engine_analysis"]["strength"]
    assert strength["strength_level"] == CASE_0001_EXPECTED_STRENGTH["strength_level"]
    assert abs(
        strength["strength_score"] - CASE_0001_EXPECTED_STRENGTH["strength_score"]
    ) < 0.01


def test_case_0001_narrative_plan_regression() -> None:
    """Live adapter yields frozen CASE-0001 NarrativePlan selection."""
    from applications.production.engine_runner import ProductionEngineRunner

    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    published = build_published_strength_facts(
        case_id=CASE_0001_REQUEST.case_id,
        strength_result=output.strength_result,
        strength_context=output.strength_context,
    )
    service = StrengthInterpretationService()
    result = service.interpret(published=published)
    by_section = {
        section.section_id: section for section in result.narrative_plan.sections
    }
    for section_id, expected_ids in GOLDEN_SELECTED.items():
        selected = {item.knowledge_id for item in by_section[section_id].selected_units}
        assert selected == expected_ids


def test_case_0001_pattern_and_useful_god_present(case_0001_generic_result) -> None:
    """Pattern and Useful God engines produce output for CASE-0001."""
    analysis = case_0001_generic_result.diagnostics["engine_analysis"]
    assert analysis["pattern"]
    assert analysis["useful_god"]


def test_case_0001_ten_gods_present(case_0001_generic_result) -> None:
    """Ten Gods engine produces output for CASE-0001."""
    ten_gods = case_0001_generic_result.diagnostics["engine_analysis"]["ten_gods"]
    assert ten_gods["day_master"]["stem"] == "Canh"
    assert len(ten_gods["visible"]) >= 4

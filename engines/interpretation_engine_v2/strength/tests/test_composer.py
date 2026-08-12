"""Tests for sentence composer."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.composer.composer import SentenceComposer
from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader
from engines.interpretation_engine_v2.strength.narrative.planner import NarrativePlanner
from engines.interpretation_engine_v2.strength.reasoner.engine import StrengthReasoner
from engines.interpretation_engine_v2.strength.tests.test_reasoner import _build_input


def test_compose_customer_and_validation_modes() -> None:
    loader = KnowledgeCatalogLoader()
    units_by_id = {unit.knowledge_id: unit for unit in loader.load_all()}
    plan = NarrativePlanner().finalize(
        StrengthReasoner().build_plan(_build_input()),
        units_by_id,
    )
    composer = SentenceComposer()
    customer = composer.compose_customer(plan, units_by_id)
    validation = composer.compose_validation(plan, units_by_id)
    assert customer[0].section_id == "CONCLUSION"
    assert "Strong" in customer[0].paragraphs[0]
    assert any(section.section_id == "WHY" for section in customer)
    assert any(section.section_id == "EVIDENCE" for section in validation)
    assert len(validation) > len(customer)


def test_customer_mode_has_no_rule_ids() -> None:
    loader = KnowledgeCatalogLoader()
    units_by_id = {unit.knowledge_id: unit for unit in loader.load_all()}
    plan = NarrativePlanner().finalize(
        StrengthReasoner().build_plan(_build_input()),
        units_by_id,
    )
    customer = SentenceComposer().compose_customer(plan, units_by_id)
    joined = "\n".join(paragraph for section in customer for paragraph in section.paragraphs)
    assert "sea_002" not in joined
    assert "0.87" not in joined

"""Tests for strength reasoner."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import AudienceMode, ReasoningInput
from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader
from engines.interpretation_engine_v2.strength.reasoner.engine import StrengthReasoner
from engines.interpretation_engine_v2.strength.runtime.case_0001 import load_case_0001_facts
from engines.interpretation_engine_v2.strength.selector.selector import KnowledgeSelector


GOLDEN_SELECTED = {
    "WHY": {
        "IK-STR-CAUS-0002",
        "IK-STR-CAUS-0007",
        "IK-STR-CAUS-0010",
        "IK-STR-CAUS-0016",
    },
    "MEANING": {"IK-STR-MEAN-0006"},
    "ADVANTAGE": {"IK-STR-ADV-0013", "IK-STR-ADV-0009"},
    "CHALLENGE": {"IK-STR-CHAL-0010", "IK-STR-CHAL-0014"},
    "CAREER": {"IK-STR-CAR-0012"},
    "MARRIAGE": {"IK-STR-MAR-0007"},
    "HEALTH": {"IK-STR-HEA-0010"},
    "RECOMMENDATION": {"IK-STR-REC-0036", "IK-STR-REC-0037", "IK-STR-REC-0038"},
}


def _build_input() -> ReasoningInput:
    loader = KnowledgeCatalogLoader()
    published = load_case_0001_facts()
    candidates = KnowledgeSelector().select_candidates(
        loader.load_all(),
        published,
        AudienceMode.CUSTOMER,
    )
    return ReasoningInput(published=published, candidates=candidates, audience=AudienceMode.CUSTOMER)


def test_reasoner_produces_qualified_conclusion() -> None:
    plan = StrengthReasoner().build_plan(_build_input())
    assert plan.primary_conclusion["class_id"] == "strong"
    assert plan.primary_conclusion["language_strength"] == "qualified"


def test_reasoner_case_0001_golden_units() -> None:
    plan = StrengthReasoner().build_plan(_build_input())
    by_section = {section.section_id: section for section in plan.sections}
    for section_id, expected_ids in GOLDEN_SELECTED.items():
        selected = {item.knowledge_id for item in by_section[section_id].selected_units}
        assert selected == expected_ids


def test_luck_section_insufficient() -> None:
    plan = StrengthReasoner().build_plan(_build_input())
    luck = next(section for section in plan.sections if section.section_id == "LUCK")
    assert luck.insufficient_data is True
    assert luck.insufficient_reason == "INSUFFICIENT_DATA_LUCK"
    assert luck.selected_units == []

"""Sprint K2.1 — Useful God role knowledge tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.concepts import ConceptRegistry
from engines.interpretation_engine.foundation.facts.useful_god import (
    UsefulGodCandidateFact,
    UsefulGodInterpretationFacts,
)
from engines.interpretation_engine.foundation.knowledge import (
    KnowledgeQualityGate,
    KnowledgeRegistry,
    KnowledgeValidator,
    USEFUL_GOD_KNOWLEDGE_MISSING,
    UsefulGodKnowledgeBundle,
    build_useful_god_knowledge_bundle,
    build_useful_god_quality_report,
)
from engines.interpretation_engine.foundation.knowledge.entity import (
    KnowledgeEntity,
    KnowledgeMetadata,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    ENGINE_CANDIDATE_TYPES,
    KNOWLEDGE_READINESS_READY,
    USEFUL_GOD_ROLE_KEYS,
    USEFUL_GOD_STEM_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus
from engines.interpretation_engine.foundation.status import DataAvailability

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
)

_RULE_DIR = Path("database/13_useful_god")
_RULE_FILES = (
    "01_strength_rules.csv",
    "02_season_rules.csv",
    "03_temperature_rules.csv",
    "04_flow_rules.csv",
    "06_special_rules.csv",
)


def test_engine_inventory_is_stem_and_ten_god() -> None:
    """Engine candidate values are stems or ten-god roles; no element selected."""
    selected, favorable, unfavorable = _engine_rule_values()
    all_values = selected | favorable | unfavorable
    assert all_values
    unexpected = all_values - set(USEFUL_GOD_STEM_KEYS) - set(USEFUL_GOD_ROLE_KEYS)
    assert unexpected == set()
    assert selected & set(USEFUL_GOD_STEM_KEYS)
    assert selected & set(USEFUL_GOD_ROLE_KEYS)
    assert "Mộc" not in all_values
    assert "Hỏa" not in all_values
    assert ENGINE_CANDIDATE_TYPES == ("stem", "ten_god")


def test_stem_lookup(knowledge_registry: KnowledgeRegistry) -> None:
    """Stem lookup still works after role population."""
    entity = knowledge_registry.get("UsefulGod", "Đinh")
    assert entity is not None
    assert entity.entity_type == "stem"
    assert entity.concept_ids


def test_role_lookup(knowledge_registry: KnowledgeRegistry) -> None:
    """Every engine role key loads as a role entity."""
    for key in USEFUL_GOD_ROLE_KEYS:
        entity = knowledge_registry.get("UsefulGod", key)
        assert entity is not None, key
        assert entity.entity_type == "role"
        assert entity.concept_ids
        assert entity.meaning
        assert "Hỏa âm" not in entity.meaning
        assert "mộc dương" not in entity.meaning.lower()


def test_mixed_lookup(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Bundle retrieves stem and role keys through the same lookup path."""
    facts = _facts(
        selected="Đinh",
        favorable=("Đinh", "Thực Thần"),
        unfavorable=("Tỷ Kiên", "Canh"),
    )
    bundle = build_useful_god_knowledge_bundle(
        facts,
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert bundle.selected_entity is not None
    assert bundle.selected_entity.entity_type == "stem"
    types = {entity.entity_type for entity in bundle.favorable_entities}
    assert types == {"stem", "role"}
    assert {entity.key for entity in bundle.unfavorable_entities} == {"Tỷ Kiên", "Canh"}
    assert bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert bundle.status == DataAvailability.AVAILABLE


def test_bundle_retrieval_ignores_narrative_type(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Stem or role selected uses the same bundle contract."""
    stem_bundle = build_useful_god_knowledge_bundle(
        _facts(selected="Đinh", favorable=("Đinh",), unfavorable=("Canh",)),
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    role_bundle = build_useful_god_knowledge_bundle(
        _facts(
            selected="Thực Thần",
            favorable=("Thực Thần", "Thương Quan"),
            unfavorable=("Tỷ Kiên", "Kiếp Tài"),
        ),
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert isinstance(stem_bundle, UsefulGodKnowledgeBundle)
    assert isinstance(role_bundle, UsefulGodKnowledgeBundle)
    assert stem_bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert role_bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert stem_bundle.coverage.selected_entity_type == "stem"
    assert role_bundle.coverage.selected_entity_type == "role"


def test_case0001_ready(case0001_explanation) -> None:
    """CASE-0001 retrieves role knowledge with READY coverage."""
    bundle = build_useful_god_knowledge_bundle(case0001_explanation)
    assert bundle.selected_key == "Chính Quan"
    assert bundle.selected_entity is not None
    assert bundle.selected_entity.entity_type == "role"
    assert bundle.selected_entity.key == "Chính Quan"
    assert set(bundle.favorable_keys) == {"Chính Quan", "Thực Thần"}
    assert set(bundle.unfavorable_keys) == {"Tỷ Kiên", "Kiếp Tài"}
    assert bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert bundle.status == DataAvailability.AVAILABLE
    assert USEFUL_GOD_KNOWLEDGE_MISSING not in bundle.diagnostics
    payload = str(bundle.to_dict())
    assert "Lương Ngọc Huỳnh" not in payload
    assert "1966" not in payload


def test_huynh_ready(huynh_explanation) -> None:
    """Huỳnh stem retrieval remains READY."""
    bundle = build_useful_god_knowledge_bundle(huynh_explanation)
    assert bundle.selected_key == "Chính Tài"
    assert bundle.selected_entity is not None
    assert bundle.selected_entity.entity_type == "role"
    assert bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert bundle.status == DataAvailability.AVAILABLE
    assert USEFUL_GOD_KNOWLEDGE_MISSING not in bundle.diagnostics


def test_no_hardcoding(knowledge_registry: KnowledgeRegistry) -> None:
    """Role entities contain no Huỳnh-specific or chart-specific content."""
    for key in USEFUL_GOD_ROLE_KEYS:
        entity = knowledge_registry.get("UsefulGod", key)
        assert entity is not None
        blob = " ".join(
            [
                entity.meaning,
                entity.positive_meaning,
                entity.negative_meaning,
                entity.evidence_notes,
                *entity.applications.values(),
            ]
        )
        assert "Lương Ngọc Huỳnh" not in blob
        assert "1966" not in blob
        assert "Nguyễn Tiến Sơn" not in blob


def test_no_ui_dependency() -> None:
    """K2.1 retrieval has no UI dependency."""
    import engines.interpretation_engine.foundation.knowledge.retrieval as retrieval

    source = Path(retrieval.__file__ or "").read_text(encoding="utf-8")
    assert "customer_portal" not in source
    assert "portal" not in Path(retrieval.__file__ or "").parts


def test_entity_type_validation_codes() -> None:
    """Validator flags type mismatch, unknown type, missing concepts, duplicate roles."""
    meta = KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
    mismatch = KnowledgeEntity(
        id="test.mismatch",
        domain="UsefulGod",
        key="Thực Thần",
        title="T",
        metadata=meta,
        entity_type="stem",
        concept_ids=("output_role",),
    )
    unknown = KnowledgeEntity(
        id="test.unknown",
        domain="UsefulGod",
        key="X",
        title="T",
        metadata=meta,
        entity_type="planet",
    )
    role_no_concept = KnowledgeEntity(
        id="test.role_nc",
        domain="UsefulGod",
        key="Thương Quan",
        title="T",
        metadata=meta,
        entity_type="role",
    )
    stem_no_concept = KnowledgeEntity(
        id="test.stem_nc",
        domain="UsefulGod",
        key="Giáp",
        title="T",
        metadata=meta,
        entity_type="stem",
    )
    dup_a = KnowledgeEntity(
        id="test.dup_a",
        domain="UsefulGod",
        key="Chính Ấn",
        title="A",
        metadata=meta,
        entity_type="role",
        concept_ids=("resource_role",),
    )
    dup_b = KnowledgeEntity(
        id="test.dup_b",
        domain="UsefulGod",
        key="Chính Ấn",
        title="B",
        metadata=meta,
        entity_type="role",
        concept_ids=("resource_role",),
    )
    result = KnowledgeValidator().validate(
        [mismatch, unknown, role_no_concept, stem_no_concept, dup_a, dup_b]
    )
    codes = {issue.code for issue in result.issues}
    assert "entity_type_mismatch" in codes
    assert "unknown_entity_type" in codes
    assert "role_missing_concept" in codes
    assert "stem_missing_concept" in codes
    assert "duplicate_role_entity" in codes


def test_role_quality_and_coverage(knowledge_registry: KnowledgeRegistry) -> None:
    """Approved role entities meet quality gates; coverage lists all roles."""
    roles = [
        entity
        for entity in knowledge_registry.list("UsefulGod")
        if entity.entity_type == "role"
    ]
    assert {entity.key for entity in roles} == set(USEFUL_GOD_ROLE_KEYS)
    result = KnowledgeQualityGate().evaluate_approved(roles)
    assert result.passed, [issue.to_dict() for issue in result.issues]
    report = build_useful_god_quality_report(knowledge_registry=knowledge_registry)
    assert all(status == "APPROVED" for status in report.role_status.values())
    assert report.entity_count == 20


def test_default_registry_still_validates(knowledge_registry: KnowledgeRegistry) -> None:
    """Default Useful God inventory passes structural validation."""
    result = knowledge_registry.validate()
    assert result.passed, [issue.to_dict() for issue in result.issues]


def test_huynh_explanation_fixture(huynh_explanation) -> None:
    """Huỳnh explanation fixture is available for READY assertion."""
    assert huynh_explanation.decision is not None
    assert huynh_explanation.decision.selected == "Chính Tài"


def test_case0001_explanation_fixture(case0001_explanation) -> None:
    """CASE-0001 explanation fixture selects Chính Quan."""
    assert case0001_explanation.decision is not None
    assert case0001_explanation.decision.selected == "Chính Quan"


@pytest.fixture(scope="module")
def knowledge_registry() -> KnowledgeRegistry:
    """Default knowledge registry."""
    return KnowledgeRegistry.default()


@pytest.fixture(scope="module")
def concept_registry() -> ConceptRegistry:
    """Default concept registry."""
    return ConceptRegistry.default()


@pytest.fixture(scope="module")
def huynh_explanation():
    """Decision Explanation for Lương Ngọc Huỳnh."""
    output = ProductionEngineRunner().run(HUYNH)
    foundation = output.interpretation_foundation
    assert foundation is not None
    assert foundation.useful_god_explanation is not None
    return foundation.useful_god_explanation


@pytest.fixture(scope="module")
def case0001_explanation():
    """Decision Explanation for CASE-0001."""
    output = ProductionEngineRunner().run(CASE_0001_REQUEST)
    foundation = output.interpretation_foundation
    assert foundation is not None
    assert foundation.useful_god_explanation is not None
    return foundation.useful_god_explanation


def _engine_rule_values() -> tuple[set[str], set[str], set[str]]:
    """Read actual Useful God Engine rule CSVs."""
    import csv

    selected: set[str] = set()
    favorable: set[str] = set()
    unfavorable: set[str] = set()
    for filename in _RULE_FILES:
        path = _RULE_DIR / filename
        with path.open(encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                god = str(row.get("useful_god") or "").strip()
                if god:
                    selected.add(god)
                favorable.update(_parse_list(row.get("favorable_gods")))
                unfavorable.update(_parse_list(row.get("unfavorable_gods")))
    return selected, favorable, unfavorable


def _parse_list(raw: object) -> set[str]:
    """Parse a JSON list cell from a Useful God rule CSV."""
    text = str(raw or "").strip()
    if not text:
        return set()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {text}
    if isinstance(parsed, list):
        return {str(item) for item in parsed if str(item)}
    return {str(parsed)}


def _facts(
    *,
    selected: str,
    favorable: tuple[str, ...],
    unfavorable: tuple[str, ...],
) -> UsefulGodInterpretationFacts:
    """Build structured facts for mixed stem/role retrieval."""
    return UsefulGodInterpretationFacts(
        selected=selected,
        candidate_type="strength",
        confidence=0.8,
        reason="test",
        favorable_gods=favorable,
        unfavorable_gods=unfavorable,
        candidates=(
            UsefulGodCandidateFact(
                useful_god=selected,
                rule_id="test_selected",
                confidence=0.8,
                reason="test",
                rule_group="strength",
            ),
        ),
        rule_ids=("test_selected",),
        presence=DataAvailability.AVAILABLE,
        status=DataAvailability.AVAILABLE,
        day_master="Canh",
        day_master_element="Kim",
        month_branch="Sửu",
        season="Đông",
        strength_level="strong",
        strength_score=0.8,
        temperature_level="cool",
        five_elements={"wood": 2, "fire": 2, "earth": 2, "metal": 3, "water": 1},
    )

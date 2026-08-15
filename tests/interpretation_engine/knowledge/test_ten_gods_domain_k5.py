"""Sprint K5 — Ten Gods domain tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.concepts import ConceptRegistry
from engines.interpretation_engine.foundation.interpreters.ten_gods import (
    TenGodFacts,
    TenGodInterpretationBundle,
    build_ten_god_facts,
    build_ten_god_interpretation_bundle,
    explain_ten_god_relationships,
)
from engines.interpretation_engine.foundation.knowledge import (
    DUPLICATE_ROLE,
    DuplicateContentDetector,
    INVALID_POSITION,
    INVALID_TEN_GOD,
    KnowledgeQualityGate,
    KnowledgeRegistry,
    KnowledgeValidator,
    MISSING_NARRATIVE_MAPPING,
    TEN_GOD_KNOWLEDGE_MISSING,
    TenGodKnowledgeBundle,
    build_ten_god_knowledge_bundle,
    build_ten_god_quality_report,
    write_ten_god_reports,
)
from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    INTERPRETATION_CLASS_RELATIONSHIP,
    interpretation_class_for,
)
from engines.interpretation_engine.foundation.knowledge.entity import (
    KnowledgeEntity,
    KnowledgeMetadata,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_ENTITY_TYPE_TEN_GOD,
    KNOWLEDGE_READINESS_READY,
    TEN_GOD_KEYS,
    TEN_GOD_PILLAR_KEYS,
    TEN_GOD_ROLE_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus
from engines.interpretation_engine.foundation.relationship.types import (
    CANONICAL_RELATIONSHIP_TYPES,
)
from engines.interpretation_engine.foundation.status import DataAvailability
from engines.ten_gods_engine.constants import DAY_MASTER_LABEL, TEN_GOD_LABELS

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
)

_TEN_GODS_ENGINE = Path("engines/ten_gods_engine")


def test_engine_inventory_matches_ten_gods_constants() -> None:
    """Knowledge inventory is engine labels, not guessed aliases."""
    assert TEN_GOD_ROLE_KEYS == TEN_GOD_LABELS
    assert DAY_MASTER_LABEL in TEN_GOD_KEYS
    assert set(TEN_GOD_KEYS) == set(TEN_GOD_LABELS) | {DAY_MASTER_LABEL}
    assert len(TEN_GOD_KEYS) == 11


def test_ten_gods_is_relationship_domain() -> None:
    """Ten Gods uses Relationship Reasoning, not Decision or State."""
    assert interpretation_class_for("TenGods") == INTERPRETATION_CLASS_RELATIONSHIP


def test_ten_god_entities_are_production_quality(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Every engine Ten God has an approved entity with required content."""
    entities = list(knowledge_registry.list("TenGods"))
    assert {entity.key for entity in entities} == set(TEN_GOD_KEYS)
    for entity in entities:
        assert entity.entity_type == KNOWLEDGE_ENTITY_TYPE_TEN_GOD
        assert entity.metadata.status == KnowledgeStatus.APPROVED
        assert entity.meaning
        assert entity.positive_meaning
        assert entity.negative_meaning
        assert entity.concept_ids
        for concept_id in entity.concept_ids:
            assert concept_registry.get(concept_id) is not None
    result = KnowledgeQualityGate().evaluate_approved(entities)
    assert result.passed, [issue.to_dict() for issue in result.issues]
    warnings = DuplicateContentDetector().detect(entities)
    assert warnings == ()


def test_knowledge_retrieval_by_engine_label(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Lookup is by engine Vietnamese label such as Kiếp Tài."""
    entity = knowledge_registry.get("TenGods", "Kiếp Tài")
    assert entity is not None
    assert entity.key == "Kiếp Tài"
    day_master = knowledge_registry.get("TenGods", "Nhật Chủ")
    assert day_master is not None
    assert day_master.key == "Nhật Chủ"


def test_facts_copy_upstream_without_recalculation(huynh_output) -> None:
    """TenGodFacts copies engine fields; it does not rerun TenGodsEngine."""
    facts = _facts_from(huynh_output)
    assert isinstance(facts, TenGodFacts)
    visible = tuple(item.ten_god for item in huynh_output.ten_gods.visible)
    hidden = tuple(item.ten_god for item in huynh_output.ten_gods.hidden)
    assert facts.visible_roles == tuple(dict.fromkeys(visible))
    assert facts.hidden_roles == tuple(dict.fromkeys(hidden))
    assert facts.selected_roles == facts.visible_roles
    assert facts.day_master == huynh_output.ten_gods.day_master.stem
    assert {item.pillar for item in facts.positions if item.visibility == "visible"} <= set(
        TEN_GOD_PILLAR_KEYS
    )
    assert facts.counts
    assert facts.rule_ids


def test_position_preservation(huynh_output) -> None:
    """Year/month/day/hour stay on position facts; no extra entities per pillar."""
    facts = _facts_from(huynh_output)
    visible = [item for item in facts.positions if item.visibility == "visible"]
    assert [item.pillar for item in visible] == ["year", "month", "day", "hour"]
    registry = KnowledgeRegistry.default()
    assert len(list(registry.list("TenGods"))) == 11


def test_relationship_assessment_uses_generic_types(huynh_output) -> None:
    """Ten Gods graph uses canonical relationship types and requested node kinds."""
    facts = _facts_from(huynh_output)
    assessment = explain_ten_god_relationships(facts)
    assert assessment.domain == "TenGods"
    assert {node.kind for node in assessment.graph.nodes} <= {
        "day_master",
        "ten_god",
        "pillar",
        "stem",
        "branch",
    }
    for edge in assessment.graph.edges:
        assert edge.relationship_type in CANONICAL_RELATIONSHIP_TYPES
    kinds = {node.kind for node in assessment.graph.nodes}
    assert "day_master" in kinds
    assert "ten_god" in kinds
    assert "pillar" in kinds


def test_bundle_retrieves_multiple_roles(huynh_output) -> None:
    """Knowledge bundle retrieves every visible and hidden role present."""
    facts = _facts_from(huynh_output)
    bundle = build_ten_god_knowledge_bundle(facts)
    assert isinstance(bundle, TenGodKnowledgeBundle)
    requested = set(facts.visible_roles) | set(facts.hidden_roles)
    assert set(bundle.coverage.requested_keys) == requested
    assert set(bundle.coverage.found_keys) == requested
    assert bundle.coverage.missing_keys == ()
    assert {entity.key for entity in bundle.entities} == requested
    assert len(bundle.entities) >= 2


def test_interpretation_bundle_is_structured(huynh_output) -> None:
    """Interpretation exposes structured slots, not prose pages."""
    facts = _facts_from(huynh_output)
    domain = build_ten_god_interpretation_bundle(facts)
    assert isinstance(domain, TenGodInterpretationBundle)
    assert domain.interpretation.roles
    for role in domain.interpretation.roles:
        assert role.role_meaning
        assert role.strengths
        assert role.risks
        assert role.activation
        assert role.interaction_with_day_master
        assert role.interaction_with_pattern
        assert role.interaction_with_useful_god
        assert role.positions
    assert domain.interpretation.creating_relationships
    assert domain.narrative.summary
    assert domain.narrative.reasoning
    assert "winner" not in domain.to_dict()


def test_missing_entity_and_invalid_role(
    concept_registry: ConceptRegistry,
) -> None:
    """Missing and unknown Ten God labels are reported, not remapped."""
    empty = KnowledgeRegistry([])
    facts = TenGodFacts(
        selected_roles=("Kiếp Tài",),
        visible_roles=("Kiếp Tài",),
        hidden_roles=(),
        positions=(),
        related_stems=(),
        related_branches=(),
        counts=(),
        strength_context="strong",
        rule_ids=("visible:month:Đinh",),
        day_master="Bính",
        pattern_label="Chính Tài",
        useful_god_selected="Đinh",
        engine_relationships=(),
        status=DataAvailability.AVAILABLE,
    )
    missing = build_ten_god_knowledge_bundle(
        facts,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert missing.entities == ()
    assert TEN_GOD_KNOWLEDGE_MISSING in missing.diagnostics
    invalid_facts = TenGodFacts(
        selected_roles=("Not A God",),
        visible_roles=("Not A God",),
        hidden_roles=(),
        positions=(),
        related_stems=(),
        related_branches=(),
        counts=(),
        strength_context="",
        rule_ids=(),
        day_master="",
        pattern_label="",
        useful_god_selected="",
        engine_relationships=(),
        status=DataAvailability.AVAILABLE,
    )
    invalid = build_ten_god_knowledge_bundle(
        invalid_facts,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert INVALID_TEN_GOD in invalid.diagnostics
    assert invalid.status == DataAvailability.INVALID


def test_validation_codes() -> None:
    """Validator detects invalid ten god, duplicate role, missing concepts."""
    meta = KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
    invalid = KnowledgeEntity(
        id="test.invalid",
        domain="TenGods",
        key="not_a_god",
        title="T",
        metadata=meta,
        entity_type="ten_god",
        concept_ids=("ten_god_relation",),
    )
    missing_concept = KnowledgeEntity(
        id="test.no_concept",
        domain="TenGods",
        key="Tỷ Kiên",
        title="T",
        metadata=meta,
        entity_type="ten_god",
    )
    dup_a = KnowledgeEntity(
        id="test.dup_a",
        domain="TenGods",
        key="Kiếp Tài",
        title="A",
        metadata=meta,
        entity_type="ten_god",
        concept_ids=("ten_god_relation",),
    )
    dup_b = KnowledgeEntity(
        id="test.dup_b",
        domain="TenGods",
        key="Kiếp Tài",
        title="B",
        metadata=meta,
        entity_type="ten_god",
        concept_ids=("ten_god_relation",),
    )
    result = KnowledgeValidator().validate(
        [invalid, missing_concept, dup_a, dup_b],
        known_concept_ids=frozenset({"ten_god_relation"}),
    )
    codes = {issue.code for issue in result.issues}
    assert "invalid_ten_god" in codes
    assert DUPLICATE_ROLE in codes
    assert "ten_god_missing_concept" in codes


def test_invalid_position_is_detected() -> None:
    """Pillar values outside year/month/day/hour are invalid positions."""
    from engines.interpretation_engine.foundation.facts.ten_gods import (
        TenGodInterpretationFacts,
        TenGodPositionFact,
    )

    upstream = TenGodInterpretationFacts(
        visible=(
            TenGodPositionFact(
                name="Kiếp Tài",
                pillar="luck",
                stem="Đinh",
                branch="",
                visibility="visible",
                relation_to_day_master="Kiếp Tài",
            ),
        ),
        hidden=(),
        distribution=(),
        day_master="Bính",
        day_master_element="Hỏa",
        status=DataAvailability.AVAILABLE,
    )
    facts = build_ten_god_facts(upstream)
    assert INVALID_POSITION in facts.diagnostics
    domain = build_ten_god_interpretation_bundle(facts)
    assert domain.status == DataAvailability.INVALID


def test_quality_and_coverage(knowledge_registry: KnowledgeRegistry) -> None:
    """Coverage lists all engine Ten Gods as approved."""
    report = build_ten_god_quality_report(knowledge_registry=knowledge_registry)
    assert report.entity_count == 11
    assert report.approved_count == 11
    assert report.broken_references == ()
    assert report.missing_required_content == ()
    assert all(status == "APPROVED" for status in report.ten_god_status.values())
    coverage_path, quality_path = write_ten_god_reports(report=report)
    assert coverage_path.is_file()
    assert quality_path.is_file()


def test_default_registry_still_validates(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Default registry including Ten Gods still validates."""
    result = knowledge_registry.validate()
    assert result.passed, [issue.to_dict() for issue in result.issues]


def test_huynh_ten_gods_domain_is_ready(huynh_output) -> None:
    """Lương Ngọc Huỳnh retrieves knowledge for every present role."""
    facts = _facts_from(huynh_output)
    visible = set(facts.visible_roles)
    assert "Kiếp Tài" in visible
    assert "Nhật Chủ" in visible
    assert "Thiên Tài" in visible
    domain = build_ten_god_interpretation_bundle(facts)
    found = {entity.key for entity in domain.knowledge.entities}
    assert visible <= found
    assert set(facts.hidden_roles) <= found
    assert domain.knowledge.concepts
    assert domain.relationship.graph.edges
    assert domain.narrative.summary
    assert domain.readiness == KNOWLEDGE_READINESS_READY
    assert domain.status == DataAvailability.AVAILABLE
    assert MISSING_NARRATIVE_MAPPING not in domain.diagnostics


def test_case_0001_same_framework_no_hardcoding(case0001_output) -> None:
    """CASE-0001 uses generic lookup; no person-specific knowledge."""
    facts = _facts_from(case0001_output)
    for key in (*facts.visible_roles, *facts.hidden_roles):
        assert key in TEN_GOD_KEYS
    domain = build_ten_god_interpretation_bundle(facts)
    assert domain.knowledge.entities
    assert {entity.key for entity in domain.knowledge.entities} == set(
        facts.visible_roles
    ) | set(facts.hidden_roles)
    assert domain.readiness == KNOWLEDGE_READINESS_READY
    for entity in domain.knowledge.entities:
        blob = " ".join(
            [
                entity.meaning,
                entity.evidence_notes,
                *entity.applications.values(),
            ]
        )
        assert "Nguyễn Tiến Sơn" not in blob
        assert "Lương Ngọc Huỳnh" not in blob
        assert "1987" not in blob


def test_no_ui_dependency() -> None:
    """Ten Gods domain retrieval has no UI dependency."""
    import engines.interpretation_engine.foundation.knowledge.ten_god_retrieval as retrieval
    import engines.interpretation_engine.foundation.interpreters.ten_gods.interpretation as interp

    for module in (retrieval, interp):
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        assert "customer_portal" not in source
        assert "portal" not in Path(module.__file__ or "").parts
        assert "NarrativeEngine" not in source


def test_no_engine_changes() -> None:
    """K5 does not change Ten Gods calculation."""
    engine_source = (_TEN_GODS_ENGINE / "engine.py").read_text(encoding="utf-8")
    assert "TenGodKnowledgeBundle" not in engine_source
    assert "knowledge.interpretation" not in engine_source
    calculator = (_TEN_GODS_ENGINE / "calculator.py").read_text(encoding="utf-8")
    assert "TenGodInterpretationBundle" not in calculator


def test_entities_are_not_person_specific(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Ten Gods knowledge has no person-specific content."""
    for entity in knowledge_registry.list("TenGods"):
        blob = " ".join(
            [
                entity.meaning,
                entity.positive_meaning,
                entity.negative_meaning,
                *entity.applications.values(),
            ]
        )
        assert "Lương Ngọc Huỳnh" not in blob
        assert "Nguyễn Tiến Sơn" not in blob
        assert "1966" not in blob


@pytest.fixture(scope="module")
def knowledge_registry() -> KnowledgeRegistry:
    """Default knowledge registry."""
    return KnowledgeRegistry.default()


@pytest.fixture(scope="module")
def concept_registry() -> ConceptRegistry:
    """Default concept registry."""
    return ConceptRegistry.default()


@pytest.fixture(scope="module")
def huynh_output():
    """Production pipeline output for Lương Ngọc Huỳnh."""
    return ProductionEngineRunner().run(HUYNH)


@pytest.fixture(scope="module")
def case0001_output():
    """Production pipeline output for CASE-0001."""
    return ProductionEngineRunner().run(CASE_0001_REQUEST)


def _facts_from(output) -> TenGodFacts:
    """Build TenGodFacts from production output without recalculating."""
    foundation = output.interpretation_foundation
    assert foundation is not None
    bazi = foundation.context.bazi
    branches: dict[str, str] = {}
    for pillar in TEN_GOD_PILLAR_KEYS:
        text = str(getattr(bazi, pillar) or "")
        parts = text.split()
        if len(parts) >= 2:
            branches[pillar] = parts[-1]
    return build_ten_god_facts(
        foundation.facts.ten_gods,
        ten_gods_result=output.ten_gods,
        strength_level=foundation.facts.strength.level,
        pattern_label=foundation.facts.pattern.label,
        useful_god_selected=foundation.facts.useful_god.selected,
        pillar_branches=branches,
    )

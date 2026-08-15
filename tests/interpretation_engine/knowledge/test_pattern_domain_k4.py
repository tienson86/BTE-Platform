"""Sprint K4 — Pattern domain tests."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.concepts import ConceptRegistry
from engines.interpretation_engine.foundation.interpreters.pattern import (
    PatternFacts,
    PatternInterpretationBundle,
    build_pattern_facts,
    build_pattern_interpretation_bundle,
    explain_pattern_relationships,
)
from engines.interpretation_engine.foundation.knowledge import (
    DuplicateContentDetector,
    INVALID_PATTERN,
    KnowledgeQualityGate,
    KnowledgeRegistry,
    KnowledgeValidator,
    MISSING_NARRATIVE_MAPPING,
    PATTERN_KNOWLEDGE_MISSING,
    PatternKnowledgeBundle,
    build_pattern_knowledge_bundle,
    build_pattern_quality_report,
    write_pattern_reports,
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
    KNOWLEDGE_ENTITY_TYPE_PATTERN,
    KNOWLEDGE_READINESS_READY,
    PATTERN_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus
from engines.interpretation_engine.foundation.relationship.types import (
    CANONICAL_RELATIONSHIP_TYPES,
)
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

_RULE_DIR = Path("database/14_pattern")
_RULE_FILES = (
    "01_main_pattern.csv",
    "02_special_pattern.csv",
    "03_follow_pattern.csv",
    "04_combination_pattern.csv",
)
_PATTERN_ENGINE = Path("engines/pattern_engine")


def test_engine_inventory_matches_rule_csvs() -> None:
    """Knowledge inventory is the Pattern Engine rule codes, not guessed labels."""
    codes = _engine_pattern_codes()
    assert codes == set(PATTERN_KEYS)
    assert "chinh_tai" in codes
    assert len(codes) == 26


def test_pattern_is_relationship_domain() -> None:
    """Pattern uses Relationship Reasoning, not Decision or State."""
    assert interpretation_class_for("Pattern") == INTERPRETATION_CLASS_RELATIONSHIP


def test_pattern_entities_are_production_quality(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Every engine pattern has an approved entity with required content."""
    entities = list(knowledge_registry.list("Pattern"))
    assert {entity.key for entity in entities} == set(PATTERN_KEYS)
    for entity in entities:
        assert entity.entity_type == KNOWLEDGE_ENTITY_TYPE_PATTERN
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


def test_knowledge_retrieval_by_engine_code(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Lookup is by engine code such as chinh_tai."""
    entity = knowledge_registry.get("Pattern", "chinh_tai")
    assert entity is not None
    assert entity.key == "chinh_tai"
    assert "Chính Tài" in entity.title


def test_facts_copy_upstream_without_recalculation(huynh_output) -> None:
    """PatternFacts copies engine fields; it does not rerun Pattern Engine."""
    foundation = huynh_output.interpretation_foundation
    assert foundation is not None
    facts = build_pattern_facts(
        foundation.facts.pattern,
        pattern_context=huynh_output.pattern_context,
        pattern_result=huynh_output.pattern_result,
    )
    assert isinstance(facts, PatternFacts)
    assert facts.selected == huynh_output.pattern_result.pattern
    assert facts.label == huynh_output.pattern_result.cach_cuc
    assert facts.candidate_patterns == tuple(huynh_output.pattern_result.candidate_patterns)
    assert facts.rule_ids == tuple(huynh_output.pattern_result.matched_rules)
    assert facts.month_command == (huynh_output.pattern_context.month_branch_ten_god or "")
    assert facts.day_master == (huynh_output.pattern_context.day_master or "")
    assert facts.confidence == pytest.approx(huynh_output.pattern_result.confidence)


def test_relationship_assessment_uses_generic_types(huynh_output) -> None:
    """Pattern graph uses canonical relationship types only."""
    facts = _facts_from(huynh_output)
    assessment = explain_pattern_relationships(facts)
    assert assessment.domain == "Pattern"
    assert {node.kind for node in assessment.graph.nodes} <= {
        "month_command",
        "day_master",
        "ten_god",
        "pattern",
    }
    for edge in assessment.graph.edges:
        assert edge.relationship_type in CANONICAL_RELATIONSHIP_TYPES
    sources = {edge.source.split(":", 1)[0] for edge in assessment.graph.edges}
    targets = {edge.target.split(":", 1)[0] for edge in assessment.graph.edges}
    assert "month_command" in sources or "day_master" in sources
    assert "pattern" in targets


def test_bundle_and_interpretation(huynh_output) -> None:
    """Knowledge bundle plus interpretation expose structured slots, not prose pages."""
    facts = _facts_from(huynh_output)
    bundle = build_pattern_knowledge_bundle(facts)
    assert isinstance(bundle, PatternKnowledgeBundle)
    domain = build_pattern_interpretation_bundle(facts)
    assert isinstance(domain, PatternInterpretationBundle)
    assert domain.interpretation.why_exists
    assert domain.interpretation.creating_relationships
    assert domain.interpretation.structural_meaning
    assert domain.interpretation.strengths
    assert domain.interpretation.risks
    assert domain.interpretation.applications
    assert domain.narrative.summary
    assert domain.narrative.reasoning
    assert "winner" not in domain.to_dict()


def test_missing_entity_and_invalid_pattern(
    concept_registry: ConceptRegistry,
) -> None:
    """Missing and unknown pattern codes are reported, not remapped."""
    empty = KnowledgeRegistry([])
    facts = PatternFacts(
        selected="chinh_tai",
        label="Chính Tài",
        candidate_patterns=(),
        month_command="Chính Tài",
        supporting_relationships=("Chính Tài",),
        rule_ids=("pat_ct_01",),
        confidence=0.7,
        reason="test",
        related_pillars=(),
        day_master="Mậu",
        ten_gods=("Chính Tài",),
        status=DataAvailability.AVAILABLE,
    )
    missing = build_pattern_knowledge_bundle(
        facts,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert missing.pattern_entity is None
    assert PATTERN_KNOWLEDGE_MISSING in missing.diagnostics
    invalid_facts = PatternFacts(
        selected="not_a_pattern",
        label="X",
        candidate_patterns=(),
        month_command="",
        supporting_relationships=(),
        rule_ids=(),
        confidence=0.1,
        reason="",
        related_pillars=(),
        day_master="",
        ten_gods=(),
        status=DataAvailability.AVAILABLE,
    )
    invalid = build_pattern_knowledge_bundle(
        invalid_facts,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert INVALID_PATTERN in invalid.diagnostics
    assert invalid.status == DataAvailability.INVALID


def test_validation_codes() -> None:
    """Validator detects invalid pattern, duplicate entity, missing concepts."""
    meta = KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
    invalid = KnowledgeEntity(
        id="test.invalid",
        domain="Pattern",
        key="not_a_pattern",
        title="T",
        metadata=meta,
        entity_type="pattern",
        concept_ids=("month_command",),
    )
    missing_concept = KnowledgeEntity(
        id="test.no_concept",
        domain="Pattern",
        key="chinh_quan",
        title="T",
        metadata=meta,
        entity_type="pattern",
    )
    dup_a = KnowledgeEntity(
        id="test.dup_a",
        domain="Pattern",
        key="chinh_tai",
        title="A",
        metadata=meta,
        entity_type="pattern",
        concept_ids=("month_command",),
    )
    dup_b = KnowledgeEntity(
        id="test.dup_b",
        domain="Pattern",
        key="chinh_tai",
        title="B",
        metadata=meta,
        entity_type="pattern",
        concept_ids=("month_command",),
    )
    result = KnowledgeValidator().validate(
        [invalid, missing_concept, dup_a, dup_b],
        known_concept_ids=frozenset({"month_command"}),
    )
    codes = {issue.code for issue in result.issues}
    assert "invalid_pattern" in codes
    assert "duplicate_entity" in codes
    assert "pattern_missing_concept" in codes


def test_quality_and_coverage(knowledge_registry: KnowledgeRegistry) -> None:
    """Coverage lists all engine patterns as approved."""
    report = build_pattern_quality_report(knowledge_registry=knowledge_registry)
    assert report.entity_count == 26
    assert report.approved_count == 26
    assert report.broken_references == ()
    assert report.missing_required_content == ()
    assert all(status == "APPROVED" for status in report.pattern_status.values())
    coverage_path, quality_path = write_pattern_reports(report=report)
    assert coverage_path.is_file()
    assert quality_path.is_file()


def test_default_registry_still_validates(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Default registry including Pattern still validates."""
    result = knowledge_registry.validate()
    assert result.passed, [issue.to_dict() for issue in result.issues]


def test_huynh_pattern_domain_is_ready(huynh_output) -> None:
    """Lương Ngọc Huỳnh retrieves Chính Tài knowledge with relationship assessment."""
    facts = _facts_from(huynh_output)
    assert facts.selected == "chinh_tai"
    assert facts.label == "Chính Tài"
    domain = build_pattern_interpretation_bundle(facts)
    assert domain.knowledge.pattern_entity is not None
    assert domain.knowledge.pattern_entity.key == "chinh_tai"
    assert domain.knowledge.concepts
    assert domain.relationship.graph.edges
    assert domain.narrative.summary
    assert domain.readiness == KNOWLEDGE_READINESS_READY
    assert domain.status == DataAvailability.AVAILABLE
    assert MISSING_NARRATIVE_MAPPING not in domain.diagnostics


def test_case_0001_same_framework_no_hardcoding(case0001_output) -> None:
    """CASE-0001 uses generic lookup; no person-specific knowledge."""
    facts = _facts_from(case0001_output)
    assert facts.selected in PATTERN_KEYS
    domain = build_pattern_interpretation_bundle(facts)
    assert domain.knowledge.pattern_entity is not None
    assert domain.knowledge.pattern_entity.key == facts.selected
    assert domain.readiness == KNOWLEDGE_READINESS_READY
    blob = " ".join(
        [
            domain.knowledge.pattern_entity.meaning,
            domain.knowledge.pattern_entity.evidence_notes,
            *domain.knowledge.pattern_entity.applications.values(),
        ]
    )
    assert "Nguyễn Tiến Sơn" not in blob
    assert "Lương Ngọc Huỳnh" not in blob
    assert "1987" not in blob


def test_no_ui_dependency() -> None:
    """Pattern domain retrieval has no UI dependency."""
    import engines.interpretation_engine.foundation.knowledge.pattern_retrieval as retrieval
    import engines.interpretation_engine.foundation.interpreters.pattern.interpretation as interp

    for module in (retrieval, interp):
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        assert "customer_portal" not in source
        assert "portal" not in Path(module.__file__ or "").parts
        assert "NarrativeEngine" not in source


def test_no_engine_changes() -> None:
    """K4 does not change Pattern calculation."""
    engine_source = (_PATTERN_ENGINE / "engine.py").read_text(encoding="utf-8")
    assert "PatternKnowledgeBundle" not in engine_source
    assert "knowledge.interpretation" not in engine_source
    calculator = (_PATTERN_ENGINE / "calculator.py").read_text(encoding="utf-8")
    assert "PatternInterpretationBundle" not in calculator


def test_entities_are_not_person_specific(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Pattern knowledge has no person-specific content."""
    for entity in knowledge_registry.list("Pattern"):
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


def _facts_from(output) -> PatternFacts:
    """Build PatternFacts from production output without recalculating."""
    foundation = output.interpretation_foundation
    assert foundation is not None
    return build_pattern_facts(
        foundation.facts.pattern,
        pattern_context=output.pattern_context,
        pattern_result=output.pattern_result,
    )


def _engine_pattern_codes() -> set[str]:
    """Read actual Pattern Engine rule CSVs."""
    codes: set[str] = set()
    for filename in _RULE_FILES:
        path = _RULE_DIR / filename
        with path.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                code = str(row.get("pattern") or "").strip()
                if code:
                    codes.add(code)
    return codes

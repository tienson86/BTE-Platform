"""Sprint K3 — Strength state knowledge tests."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import (
    CASE_0001_EXPECTED_STRENGTH,
    CASE_0001_REQUEST,
)
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.assessment import (
    STRENGTH_ASSESSMENT_PATH,
    build_strength_assessment,
)
from engines.interpretation_engine.foundation.concepts import ConceptRegistry
from engines.interpretation_engine.foundation.facts.strength import (
    StrengthInterpretationFacts,
)
from engines.interpretation_engine.foundation.knowledge import (
    DuplicateContentDetector,
    INVALID_STRENGTH_STATE,
    KnowledgeQualityGate,
    KnowledgeRegistry,
    KnowledgeValidator,
    STRENGTH_CONCEPTS_MISSING,
    STRENGTH_KNOWLEDGE_MISSING,
    StrengthKnowledgeBundle,
    build_strength_knowledge_bundle,
    build_strength_quality_report,
    write_strength_reports,
)
from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    DECISION_KNOWLEDGE_DOMAINS,
    INTERPRETATION_CLASS_DECISION,
    INTERPRETATION_CLASS_STATE,
    STATE_KNOWLEDGE_DOMAINS,
    interpretation_class_for,
)
from engines.interpretation_engine.foundation.knowledge.entity import (
    KnowledgeEntity,
    KnowledgeMetadata,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_ENTITY_TYPE_STATE,
    KNOWLEDGE_READINESS_READY,
    STRENGTH_STATE_KEYS,
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

_LEVEL_RULES = Path("database/12_strength/06_priority_rules.csv")
_STRENGTH_ENGINE_ROOT = Path("engines/strength_engine")
_REQUIRED_APPLICATIONS = (
    "career",
    "wealth",
    "relationships",
    "health",
    "learning",
    "decision_making",
)


def test_decision_and_state_classes_are_not_merged() -> None:
    """Useful God is decision; Strength is state."""
    assert interpretation_class_for("UsefulGod") == INTERPRETATION_CLASS_DECISION
    assert interpretation_class_for("Strength") == INTERPRETATION_CLASS_STATE
    assert "UsefulGod" in DECISION_KNOWLEDGE_DOMAINS
    assert "Strength" in STATE_KNOWLEDGE_DOMAINS
    assert not set(DECISION_KNOWLEDGE_DOMAINS) & set(STATE_KNOWLEDGE_DOMAINS)


def test_engine_state_inventory_from_level_rules() -> None:
    """Knowledge inventory matches Strength Engine level rules, not guessed labels."""
    levels = _engine_level_inventory()
    assert levels == set(STRENGTH_STATE_KEYS)
    assert "very_strong" not in levels
    assert "very_weak" not in levels


def test_knowledge_does_not_populate_non_engine_states(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """very_strong and very_weak are absent because the engine does not emit them."""
    keys = {entity.key for entity in knowledge_registry.list("Strength")}
    assert keys == set(STRENGTH_STATE_KEYS)
    assert knowledge_registry.get("Strength", "very_strong") is None
    assert knowledge_registry.get("Strength", "very_weak") is None


def test_strength_entities_are_production_states(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Each Strength entity is an approved state with required content."""
    entities = list(knowledge_registry.list("Strength"))
    assert len(entities) == 3
    for entity in entities:
        assert entity.entity_type == KNOWLEDGE_ENTITY_TYPE_STATE
        assert entity.metadata.status == KnowledgeStatus.APPROVED
        assert entity.meaning
        assert entity.positive_meaning
        assert entity.negative_meaning
        assert entity.evidence_notes
        assert entity.concept_ids
        for key in _REQUIRED_APPLICATIONS:
            assert str(entity.applications.get(key) or "").strip()
        assert len(entity.recommendations) >= 2
        assert len(entity.warnings) >= 1
        for concept_id in entity.concept_ids:
            assert concept_registry.get(concept_id) is not None


def test_assessment_path_has_no_winner() -> None:
    """Assessment path is Season → ... → Strength with no alternatives."""
    assert STRENGTH_ASSESSMENT_PATH == (
        "season",
        "roots",
        "support",
        "drain",
        "control",
        "balance",
        "strength",
    )
    assessment = build_strength_assessment(_facts(level="strong", score=0.66))
    assert [step.step_id for step in assessment.assessment_path] == list(
        STRENGTH_ASSESSMENT_PATH
    )
    assert not hasattr(assessment, "decision")
    assert not hasattr(assessment, "alternatives")
    assert assessment.interpretation_class == INTERPRETATION_CLASS_STATE
    blob = str(assessment.to_dict())
    assert "winner" not in blob.lower()


def test_assessment_reuses_facts_without_recalculation() -> None:
    """Assessment copies facts and optional engine component scores."""
    facts = _facts(level="strong", score=0.66, label="Thân vượng", confidence=0.8)
    result = _component_source(
        season=0.1,
        root=0.2,
        support=0.05,
        drain=-0.04,
        control=-0.03,
    )
    assessment = build_strength_assessment(facts, strength_result=result)
    assert assessment.state == "strong"
    assert assessment.label == "Thân vượng"
    assert assessment.score == 0.66
    assert assessment.balance == 0.66
    assert assessment.season == 0.1
    assert assessment.roots == 0.2
    assert assessment.support == 0.05
    assert assessment.drain == -0.04
    assert assessment.control == -0.03
    assert assessment.confidence == 0.8
    assert assessment.evidence == ("season",)
    assert [step.status for step in assessment.assessment_path] == ["passed"] * 7


def test_knowledge_retrieval_by_state(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Registry lookup is by engine state key."""
    for key in STRENGTH_STATE_KEYS:
        entity = knowledge_registry.get("Strength", key)
        assert entity is not None
        assert entity.key == key
        assert entity.entity_type == "state"


def test_bundle_retrieves_state_knowledge(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Bundle returns state entity, concepts, status, and coverage."""
    assessment = build_strength_assessment(_facts(level="strong", score=0.66))
    bundle = build_strength_knowledge_bundle(
        assessment,
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert isinstance(bundle, StrengthKnowledgeBundle)
    assert bundle.state_entity is not None
    assert bundle.state_entity.key == "strong"
    assert bundle.concepts
    assert bundle.status == DataAvailability.AVAILABLE
    assert bundle.coverage.state_found is True
    assert bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert STRENGTH_KNOWLEDGE_MISSING not in bundle.diagnostics


def test_missing_entity_is_partial(
    concept_registry: ConceptRegistry,
) -> None:
    """Missing state knowledge is reported; no silent fallback entity."""
    empty = KnowledgeRegistry([])
    assessment = build_strength_assessment(_facts(level="strong", score=0.7))
    bundle = build_strength_knowledge_bundle(
        assessment,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert bundle.state_entity is None
    assert bundle.status == DataAvailability.PARTIAL
    assert STRENGTH_KNOWLEDGE_MISSING in bundle.diagnostics
    assert bundle.coverage.state_found is False


def test_invalid_state_is_flagged(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """States outside engine inventory are invalid, not remapped."""
    assessment = build_strength_assessment(_facts(level="very_strong", score=0.9))
    bundle = build_strength_knowledge_bundle(
        assessment,
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert assessment.state == "very_strong"
    assert INVALID_STRENGTH_STATE in bundle.diagnostics
    assert bundle.status == DataAvailability.INVALID
    assert bundle.state_entity is None
    assert knowledge_registry.get("Strength", "very_strong") is None


def test_missing_concepts_are_flagged(concept_registry: ConceptRegistry) -> None:
    """Entity without concepts is reported as partial coverage."""
    meta = KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
    entity = KnowledgeEntity(
        id="test.strength.no_concepts",
        domain="Strength",
        key="strong",
        title="T",
        metadata=meta,
        entity_type="state",
    )
    registry = KnowledgeRegistry([entity])
    assessment = build_strength_assessment(_facts(level="strong", score=0.7))
    bundle = build_strength_knowledge_bundle(
        assessment,
        knowledge_registry=registry,
        concept_registry=concept_registry,
    )
    assert STRENGTH_CONCEPTS_MISSING in bundle.diagnostics
    assert bundle.status == DataAvailability.PARTIAL


def test_validation_codes() -> None:
    """Validator detects invalid state, duplicate state, missing concepts, broken refs."""
    meta = KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
    invalid = KnowledgeEntity(
        id="test.invalid",
        domain="Strength",
        key="very_strong",
        title="T",
        metadata=meta,
        entity_type="state",
        concept_ids=("strength_balance",),
    )
    missing_concept = KnowledgeEntity(
        id="test.no_concept",
        domain="Strength",
        key="weak",
        title="T",
        metadata=meta,
        entity_type="state",
    )
    dup_a = KnowledgeEntity(
        id="test.dup_a",
        domain="Strength",
        key="balanced",
        title="A",
        metadata=meta,
        entity_type="state",
        concept_ids=("strength_balance",),
    )
    dup_b = KnowledgeEntity(
        id="test.dup_b",
        domain="Strength",
        key="balanced",
        title="B",
        metadata=meta,
        entity_type="state",
        concept_ids=("strength_balance",),
    )
    broken = KnowledgeEntity(
        id="test.broken",
        domain="Strength",
        key="strong",
        title="T",
        metadata=meta,
        entity_type="state",
        concept_ids=("strength_balance", "missing_concept_id"),
        related_entities=(),
    )
    from engines.interpretation_engine.foundation.references import (
        KnowledgeEntityReference,
    )

    broken_ref = KnowledgeEntity(
        id="test.broken_ref",
        domain="Strength",
        key="strong",
        title="T",
        metadata=meta,
        entity_type="state",
        concept_ids=("strength_balance",),
        related_entities=(KnowledgeEntityReference(domain="Strength", key="missing"),),
    )
    result = KnowledgeValidator().validate(
        [invalid, missing_concept, dup_a, dup_b, broken, broken_ref],
        known_concept_ids=frozenset({"strength_balance"}),
    )
    codes = {issue.code for issue in result.issues}
    assert "invalid_state" in codes
    assert "duplicate_state" in codes
    assert "strength_missing_concept" in codes
    assert "broken_concept_reference" in codes
    assert "broken_reference" in codes


def test_quality_and_coverage(knowledge_registry: KnowledgeRegistry) -> None:
    """Approved Strength entities pass quality gates; coverage lists engine states."""
    entities = list(knowledge_registry.list("Strength"))
    result = KnowledgeQualityGate().evaluate_approved(entities)
    assert result.passed, [issue.to_dict() for issue in result.issues]
    warnings = DuplicateContentDetector().detect(entities)
    assert warnings == ()
    report = build_strength_quality_report(knowledge_registry=knowledge_registry)
    assert report.entity_count == 3
    assert report.approved_count == 3
    assert report.draft_count == 0
    assert report.broken_references == ()
    assert report.missing_required_content == ()
    assert all(status == "APPROVED" for status in report.state_status.values())
    coverage_path, quality_path = write_strength_reports(report=report)
    assert coverage_path.is_file()
    assert quality_path.is_file()
    markdown = coverage_path.read_text(encoding="utf-8")
    assert "strong" in markdown
    assert "very_strong: not emitted" in markdown


def test_default_registry_still_validates(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Default registry including Strength still validates."""
    result = knowledge_registry.validate()
    assert result.passed, [issue.to_dict() for issue in result.issues]


def test_huynh_retrieves_strong_knowledge(huynh_output) -> None:
    """Lương Ngọc Huỳnh is balanced / 0.64 / Trung hòa and retrieves that entity."""
    foundation = huynh_output.interpretation_foundation
    assert foundation is not None
    facts = foundation.facts.strength
    assert facts.level == "balanced"
    assert facts.score == pytest.approx(0.64, abs=0.02)
    assert facts.label == "Trung hòa"
    assessment = build_strength_assessment(
        facts,
        strength_result=huynh_output.strength_result,
    )
    assert assessment.state == "balanced"
    assert assessment.score == pytest.approx(0.64, abs=0.02)
    bundle = build_strength_knowledge_bundle(assessment)
    assert bundle.state_entity is not None
    assert bundle.state_entity.key == "balanced"
    assert bundle.coverage.readiness == KNOWLEDGE_READINESS_READY
    assert bundle.status == DataAvailability.AVAILABLE


def test_case_0001_uses_same_framework_without_hardcoding(case0001_output) -> None:
    """CASE-0001 uses generic state lookup; no person-specific knowledge."""
    foundation = case0001_output.interpretation_foundation
    assert foundation is not None
    facts = foundation.facts.strength
    expected_level = CASE_0001_EXPECTED_STRENGTH["strength_level"]
    assert facts.level == expected_level
    assert facts.score == pytest.approx(
        CASE_0001_EXPECTED_STRENGTH["strength_score"], abs=0.02
    )
    assessment = build_strength_assessment(
        facts,
        strength_result=case0001_output.strength_result,
    )
    bundle = build_strength_knowledge_bundle(assessment)
    assert assessment.state == expected_level
    assert bundle.state_entity is not None
    assert bundle.state_entity.key == expected_level
    blob = " ".join(
        [
            bundle.state_entity.meaning,
            bundle.state_entity.evidence_notes,
            *bundle.state_entity.applications.values(),
        ]
    )
    assert "Nguyễn Tiến Sơn" not in blob
    assert "Lương Ngọc Huỳnh" not in blob
    assert "1987" not in blob
    assert "CASE-0001" not in bundle.state_entity.meaning


def test_no_ui_dependency() -> None:
    """Strength knowledge retrieval has no UI dependency."""
    import engines.interpretation_engine.foundation.knowledge.strength_retrieval as retrieval
    import engines.interpretation_engine.foundation.assessment.strength as assessment

    for module in (retrieval, assessment):
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        assert "customer_portal" not in source
        assert "portal" not in Path(module.__file__ or "").parts
        assert "NarrativeEngine" not in source


def test_no_engine_or_decision_changes() -> None:
    """K3 does not import analytical engines or Decision Explanation."""
    import engines.interpretation_engine.foundation.knowledge.strength_retrieval as retrieval
    import engines.interpretation_engine.foundation.assessment.strength as assessment

    for module in (retrieval, assessment):
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        assert "engines.strength_engine" not in source
        assert "DecisionExplainer" not in source
        assert "DecisionExplanationResult" not in source
    engine_source = (_STRENGTH_ENGINE_ROOT / "engine.py").read_text(encoding="utf-8")
    assert "StrengthKnowledgeBundle" not in engine_source
    assert "knowledge.interpretation" not in engine_source


def test_entities_are_not_person_specific(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Strength knowledge has no person-specific content."""
    for entity in knowledge_registry.list("Strength"):
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


def _engine_level_inventory() -> set[str]:
    """Read actual Strength Engine level-classification keys."""
    levels: set[str] = set()
    with _LEVEL_RULES.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("score_target") or "") != "level":
                continue
            level = str(row.get("strength_level") or "").strip()
            if level:
                levels.add(level)
    return levels


def _facts(
    *,
    level: str,
    score: float,
    label: str = "",
    confidence: float = 0.7,
) -> StrengthInterpretationFacts:
    """Build Strength facts without recalculating engine truth."""
    return StrengthInterpretationFacts(
        level=level,
        score=score,
        label=label,
        confidence=confidence,
        evidence=("season",),
        rule_ids=("pri_level_strong",),
        status=DataAvailability.AVAILABLE,
    )


def _component_source(
    *,
    season: float,
    root: float,
    support: float,
    drain: float,
    control: float,
) -> object:
    """Duck-typed StrengthResult component scores."""

    class _Scores:
        season_score = season
        root_score = root
        support_score = support
        drain_score = drain
        control_score = control

    return _Scores()

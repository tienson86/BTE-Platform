"""Sprint K6 — Shen Sha Expert Domain tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.bazi_engine.core.constants import EARTHLY_BRANCHES, HEAVENLY_STEMS
from engines.bazi_engine.shensha.service import ShenShaService
from engines.interpretation_engine.foundation.concepts import ConceptRegistry
from engines.interpretation_engine.foundation.interpreters.shensha import (
    ShenShaFacts,
    ShenShaInterpretationBundle,
    build_shensha_facts,
    build_shensha_interpretation_bundle,
    explain_shensha_relationships,
)
from engines.interpretation_engine.foundation.knowledge import (
    DuplicateContentDetector,
    INVALID_SHENSHA,
    KnowledgeQualityGate,
    KnowledgeRegistry,
    KnowledgeValidator,
    MISSING_ACTIVATION,
    MISSING_MECHANISM,
    MISSING_NARRATIVE_MAPPING,
    SHENSHA_KNOWLEDGE_MISSING,
    ShenShaKnowledgeBundle,
    build_shensha_knowledge_bundle,
    build_shensha_quality_report,
    write_shensha_reports,
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
    KNOWLEDGE_ENTITY_TYPE_SHEN_SHA,
    KNOWLEDGE_READINESS_READY,
    SHEN_SHA_KEYS,
    SHEN_SHA_PUBLISHED_KEYS,
    TEN_GOD_PILLAR_KEYS,
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

_BAZI_SHENSHA = Path("engines/bazi_engine/shensha")


def _runtime_catalog() -> set[str]:
    """Generate production inventory by running ShenShaService, not CSV lists."""
    service = ShenShaService()
    names: set[str] = set()
    stems = list(HEAVENLY_STEMS)
    branches = list(EARTHLY_BRANCHES)
    for day_master in stems:
        for year_branch in branches:
            for month_branch in branches:
                names.update(
                    service.calculate(
                        year_branch=year_branch,
                        day_master=day_master,
                        month_branch=month_branch,
                        day_branch=year_branch,
                        hour_branch=month_branch,
                        stems=stems,
                        branches=[year_branch, month_branch, year_branch, month_branch],
                    )
                )
    return names


def test_engine_inventory_from_runtime() -> None:
    """Knowledge catalog is the closed production service emit list."""
    runtime = _runtime_catalog()
    assert runtime == set(SHEN_SHA_PUBLISHED_KEYS)
    assert "Thiên Ất" not in runtime
    assert "Thiên Đức" not in runtime
    assert "Nguyệt Đức" not in runtime
    assert "Văn Khúc" not in runtime
    assert "Đào Hoa" not in runtime
    assert "Dịch Mã" not in runtime
    assert len(SHEN_SHA_PUBLISHED_KEYS) == 9
    assert len(SHEN_SHA_KEYS) == 12


def test_shensha_is_relationship_domain() -> None:
    """Shen Sha uses Relationship Reasoning."""
    assert interpretation_class_for("ShenSha") == INTERPRETATION_CLASS_RELATIONSHIP


def test_shensha_entities_are_expert_ready(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Every production Shen Sha is approved Expert Ready with required fields."""
    entities = list(knowledge_registry.list("ShenSha"))
    assert {entity.key for entity in entities} == set(SHEN_SHA_KEYS)
    for entity in entities:
        assert entity.entity_type == KNOWLEDGE_ENTITY_TYPE_SHEN_SHA
        assert entity.metadata.status == KnowledgeStatus.APPROVED
        assert entity.meaning
        assert entity.mechanism
        assert entity.manifestation
        assert entity.activation_conditions
        assert entity.typical_triggers
        assert entity.contraindications
        assert entity.luck_relationship
        assert entity.pattern_relationship
        assert entity.ten_gods_relationship
        assert entity.suppression or entity.suppression_conditions
        assert entity.base_influence
        assert entity.applications
        assert entity.recommendations
        assert entity.warnings
        assert entity.evidence_notes
        assert entity.concept_ids
        for concept_id in entity.concept_ids:
            assert concept_registry.get(concept_id) is not None
        assert "TODO" not in entity.meaning
        assert "placeholder" not in entity.meaning.lower()
        assert "lorem" not in entity.meaning.lower()
    gate = KnowledgeQualityGate()
    assert gate.evaluate_approved(entities).passed
    assert gate.evaluate_expert_ready(entities).passed
    assert DuplicateContentDetector().detect(entities) == ()


def test_knowledge_retrieval_by_engine_label(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Lookup is by production Vietnamese name."""
    entity = knowledge_registry.get("ShenSha", "Thiên Ất Quý Nhân")
    assert entity is not None
    assert entity.mechanism
    assert entity.activation_conditions


def test_facts_copy_upstream_without_recalculation(huynh_output) -> None:
    """ShenShaFacts copies production names; it does not rematch stars."""
    facts = _facts_from(huynh_output)
    assert isinstance(facts, ShenShaFacts)
    production = tuple(huynh_output.analysis.bazi.shensha)
    assert facts.matched_shensha == tuple(dict.fromkeys(production))
    assert {item.name for item in facts.matches} == set(facts.matched_shensha)
    for item in facts.matches:
        assert item.match_reason
        assert item.evidence
        assert item.confidence == pytest.approx(1.0)


def test_relationship_assessment_uses_generic_types(huynh_output) -> None:
    """Shen Sha graph uses canonical types only — no activates/suppresses types."""
    facts = _facts_from(huynh_output)
    assessment = explain_shensha_relationships(facts)
    assert assessment.domain == "ShenSha"
    assert {node.kind for node in assessment.graph.nodes} <= {
        "day_master",
        "shensha",
        "pillar",
        "stem",
        "branch",
    }
    for edge in assessment.graph.edges:
        assert edge.relationship_type in CANONICAL_RELATIONSHIP_TYPES
        assert edge.relationship_type not in {"activates", "suppresses"}
    kinds = {node.kind for node in assessment.graph.nodes}
    assert "day_master" in kinds
    assert "shensha" in kinds


def test_bundle_retrieves_all_matched_stars(huynh_output) -> None:
    """Knowledge bundle retrieves every matched production star."""
    facts = _facts_from(huynh_output)
    bundle = build_shensha_knowledge_bundle(facts)
    assert isinstance(bundle, ShenShaKnowledgeBundle)
    assert set(bundle.coverage.found_keys) == set(facts.matched_shensha)
    assert bundle.coverage.missing_keys == ()


def test_interpretation_exposes_activation_and_strength(huynh_output) -> None:
    """Interpretation carries activation, strength, and chart-interaction slots."""
    facts = _facts_from(huynh_output)
    domain = build_shensha_interpretation_bundle(facts)
    assert isinstance(domain, ShenShaInterpretationBundle)
    assert domain.interpretation.stars
    for star in domain.interpretation.stars:
        assert star.mechanism
        assert star.activation
        assert star.base_influence
        assert star.luck_relationship
        assert star.pattern_relationship
        assert star.ten_gods_relationship
        assert star.suppression
    assert domain.narrative.summary
    assert domain.narrative.reasoning
    assert "winner" not in domain.to_dict()


def test_missing_entity_and_invalid_star(
    concept_registry: ConceptRegistry,
) -> None:
    """Missing and unknown stars are reported, not remapped."""
    empty = KnowledgeRegistry([])
    facts = ShenShaFacts(
        matched_shensha=("Thiên Ất Quý Nhân",),
        matches=(),
        related_stems=(),
        related_branches=(),
        related_pillars=(),
        day_master="Bính",
        pattern_label="Chính Tài",
        ten_god_roles=(),
        strength_context="strong",
        status=DataAvailability.AVAILABLE,
    )
    missing = build_shensha_knowledge_bundle(
        facts,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert missing.entities == ()
    assert SHENSHA_KNOWLEDGE_MISSING in missing.diagnostics
    invalid_facts = ShenShaFacts(
        matched_shensha=("Đào Hoa",),
        matches=(),
        related_stems=(),
        related_branches=(),
        related_pillars=(),
        day_master="",
        pattern_label="",
        ten_god_roles=(),
        strength_context="",
        status=DataAvailability.AVAILABLE,
    )
    invalid = build_shensha_knowledge_bundle(
        invalid_facts,
        knowledge_registry=empty,
        concept_registry=concept_registry,
    )
    assert INVALID_SHENSHA in invalid.diagnostics
    assert invalid.status == DataAvailability.INVALID


def test_validation_codes() -> None:
    """Validator detects invalid star, duplicate, missing mechanism/activation."""
    meta = KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
    invalid = KnowledgeEntity(
        id="test.invalid",
        domain="ShenSha",
        key="Đào Hoa",
        title="T",
        metadata=meta,
        entity_type="shen_sha",
        concept_ids=("shensha_presence",),
        mechanism="x",
        activation_conditions=("y",),
        applications={"career": "z"},
    )
    missing_mech = KnowledgeEntity(
        id="test.no_mech",
        domain="ShenSha",
        key="Văn Xương",
        title="T",
        metadata=meta,
        entity_type="shen_sha",
        concept_ids=("shensha_presence",),
        activation_conditions=("y",),
        applications={"career": "z"},
    )
    missing_act = KnowledgeEntity(
        id="test.no_act",
        domain="ShenSha",
        key="Lộc Thần",
        title="T",
        metadata=meta,
        entity_type="shen_sha",
        concept_ids=("shensha_presence",),
        mechanism="x",
        applications={"career": "z"},
    )
    dup_a = KnowledgeEntity(
        id="test.dup_a",
        domain="ShenSha",
        key="Hoa Cái",
        title="A",
        metadata=meta,
        entity_type="shen_sha",
        concept_ids=("shensha_presence",),
        mechanism="x",
        activation_conditions=("y",),
        applications={"career": "z"},
    )
    dup_b = KnowledgeEntity(
        id="test.dup_b",
        domain="ShenSha",
        key="Hoa Cái",
        title="B",
        metadata=meta,
        entity_type="shen_sha",
        concept_ids=("shensha_presence",),
        mechanism="x",
        activation_conditions=("y",),
        applications={"career": "z"},
    )
    result = KnowledgeValidator().validate(
        [invalid, missing_mech, missing_act, dup_a, dup_b],
        known_concept_ids=frozenset({"shensha_presence"}),
    )
    codes = {issue.code for issue in result.issues}
    assert "invalid_shensha" in codes
    assert "duplicate_entity" in codes
    assert MISSING_MECHANISM in codes
    assert MISSING_ACTIVATION in codes


def test_quality_and_coverage(knowledge_registry: KnowledgeRegistry) -> None:
    """Coverage lists all production Shen Sha as expert ready."""
    report = build_shensha_quality_report(knowledge_registry=knowledge_registry)
    assert report.entity_count == 12
    assert report.approved_count == 12
    assert report.expert_ready_count == 12
    assert report.broken_references == ()
    assert report.missing_required_content == ()
    assert all(status == "EXPERT_READY" for status in report.shensha_status.values())
    coverage_path, quality_path = write_shensha_reports(report=report)
    assert coverage_path.is_file()
    assert quality_path.is_file()


def test_default_registry_still_validates(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Default registry including Shen Sha still validates."""
    result = knowledge_registry.validate()
    assert result.passed, [issue.to_dict() for issue in result.issues]


def test_huynh_shensha_domain_is_ready(huynh_output) -> None:
    """Lương Ngọc Huỳnh retrieves every matched star with empty diagnostics."""
    facts = _facts_from(huynh_output)
    assert facts.matched_shensha
    assert "Thiên Ất Quý Nhân" in facts.matched_shensha
    domain = build_shensha_interpretation_bundle(facts)
    found = {entity.key for entity in domain.knowledge.entities}
    assert set(facts.matched_shensha) <= found
    assert domain.knowledge.concepts
    assert domain.relationship.graph.edges
    assert domain.readiness == KNOWLEDGE_READINESS_READY
    assert domain.status == DataAvailability.AVAILABLE
    assert domain.diagnostics == ()
    assert MISSING_NARRATIVE_MAPPING not in domain.diagnostics


def test_case_0001_same_framework_no_hardcoding(case0001_output) -> None:
    """CASE-0001 uses generic lookup; no person-specific knowledge."""
    facts = _facts_from(case0001_output)
    for key in facts.matched_shensha:
        assert key in SHEN_SHA_KEYS
    domain = build_shensha_interpretation_bundle(facts)
    assert {entity.key for entity in domain.knowledge.entities} == set(facts.matched_shensha)
    assert domain.readiness == KNOWLEDGE_READINESS_READY
    assert domain.diagnostics == ()
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
    """Shen Sha domain retrieval has no UI dependency."""
    import engines.interpretation_engine.foundation.knowledge.shensha_retrieval as retrieval
    import engines.interpretation_engine.foundation.interpreters.shensha.interpretation as interp

    for module in (retrieval, interp):
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        assert "customer_portal" not in source
        assert "portal" not in Path(module.__file__ or "").parts
        assert "NarrativeEngine" not in source


def test_no_engine_changes() -> None:
    """K6 does not own Shen Sha matching; production service stays engine-owned."""
    service = (_BAZI_SHENSHA / "service.py").read_text(encoding="utf-8")
    assert "ShenShaKnowledgeBundle" not in service
    assert "knowledge.interpretation" not in service
    assert "def evaluate(" in service
    assert 'stars.append("Thiên Ất")' not in service


def test_entities_are_not_person_specific(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Shen Sha knowledge has no person-specific content."""
    for entity in knowledge_registry.list("ShenSha"):
        blob = " ".join(
            [
                entity.meaning,
                entity.positive_meaning,
                entity.negative_meaning,
                entity.mechanism,
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


def _facts_from(output) -> ShenShaFacts:
    """Build ShenShaFacts from production output without rematching."""
    foundation = output.interpretation_foundation
    assert foundation is not None
    bazi = foundation.context.bazi
    pillars = {slot: str(getattr(bazi, slot) or "") for slot in TEN_GOD_PILLAR_KEYS}
    stems: list[str] = []
    branches: list[str] = []
    for text in pillars.values():
        parts = str(text).split()
        if parts:
            stems.append(parts[0])
        if len(parts) >= 2:
            branches.append(parts[-1])
    production_names = tuple(output.analysis.bazi.shensha or ())
    ten_god_roles = tuple(
        dict.fromkeys(item.ten_god for item in output.ten_gods.visible)
    )
    return build_shensha_facts(
        foundation.facts.shensha,
        matched_names=production_names,
        day_master=bazi.day_master,
        stems=stems,
        branches=branches,
        pillars=pillars,
        pattern_label=foundation.facts.pattern.label,
        ten_god_roles=ten_god_roles,
        strength_level=foundation.facts.strength.level,
    )

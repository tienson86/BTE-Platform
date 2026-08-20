"""Sprint K2 — Useful God knowledge population tests."""

from __future__ import annotations

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
    DuplicateContentDetector,
    KnowledgeQualityGate,
    KnowledgeRegistry,
    USEFUL_GOD_KNOWLEDGE_MISSING,
    USEFUL_GOD_ROLE_CONFLICT,
    UsefulGodKnowledgeBundle,
    build_useful_god_knowledge_bundle,
    build_useful_god_quality_report,
    write_useful_god_reports,
)
from engines.interpretation_engine.foundation.knowledge.coverage import USEFUL_GOD_STEM_ORDER
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

_STEMS = USEFUL_GOD_STEM_ORDER


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


def test_a_all_ten_stem_entities_load(knowledge_registry: KnowledgeRegistry) -> None:
    """A. All 10 Heavenly Stem Useful God entities load."""
    keys = {entity.key for entity in knowledge_registry.list("UsefulGod")}
    assert keys >= set(_STEMS)
    for stem in _STEMS:
        entity = knowledge_registry.get("UsefulGod", stem)
        assert entity is not None
        assert entity.domain == "UsefulGod"
        assert entity.key == stem


def test_b_approved_entities_meet_quality(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """B. All approved entities satisfy minimum quality requirements."""
    entities = list(knowledge_registry.list("UsefulGod"))
    approved = [
        entity
        for entity in entities
        if entity.metadata.status == KnowledgeStatus.APPROVED
    ]
    stems = [entity for entity in approved if entity.entity_type == "stem"]
    assert len(stems) == 10
    result = KnowledgeQualityGate().evaluate_approved(entities)
    assert result.passed, [issue.to_dict() for issue in result.issues]


def test_c_each_entity_has_concept_mapping(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """C. Each entity has concept mapping."""
    for entity in knowledge_registry.list("UsefulGod"):
        assert entity.concept_ids, entity.key


def test_d_concept_references_resolve(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """D. Concept references resolve."""
    for entity in knowledge_registry.list("UsefulGod"):
        for concept_id in entity.concept_ids:
            assert concept_registry.exists(concept_id), concept_id


def test_e_no_broken_concept_references(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """E. No broken concept references."""
    result = knowledge_registry.validate()
    broken = [issue for issue in result.issues if "broken" in issue.code]
    assert broken == []
    assert result.passed


def test_f_knowledge_bundle_builds(huynh_explanation) -> None:
    """F. UsefulGodKnowledgeBundle builds."""
    bundle = build_useful_god_knowledge_bundle(huynh_explanation)
    assert isinstance(bundle, UsefulGodKnowledgeBundle)
    assert bundle.selected_entity is not None
    assert bundle.to_dict()["selected_key"] == bundle.selected_key


def test_g_selected_separate_from_hy_ky(huynh_explanation) -> None:
    """G. Selected Useful God knowledge is separate from Hỷ/Kỵ knowledge."""
    bundle = build_useful_god_knowledge_bundle(huynh_explanation)
    assert bundle.selected_entity is not None
    assert bundle.selected_entity.key == bundle.selected_key
    favorable_keys = [entity.key for entity in bundle.favorable_entities]
    unfavorable_keys = [entity.key for entity in bundle.unfavorable_entities]
    assert favorable_keys == list(bundle.favorable_keys)
    assert unfavorable_keys == list(bundle.unfavorable_keys)
    assert bundle.favorable_keys != bundle.unfavorable_keys
    assert "selected_entity" in bundle.to_dict()
    assert "favorable_entities" in bundle.to_dict()
    assert "unfavorable_entities" in bundle.to_dict()


def test_h_hy_and_ky_roles_preserved(huynh_explanation) -> None:
    """H. Hỷ and Kỵ roles are preserved."""
    bundle = build_useful_god_knowledge_bundle(huynh_explanation)
    assert "Chính Tài" in bundle.favorable_keys
    assert "Thực Thần" in bundle.favorable_keys
    assert "Kiếp Tài" in bundle.unfavorable_keys
    assert set(bundle.favorable_keys).isdisjoint(bundle.unfavorable_keys)


def test_i_missing_entity_partial_status(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """I. Missing entity produces partial status, not fake fallback."""
    facts = _facts(selected="NotAStem", favorable=("Đinh",), unfavorable=("Canh",))
    bundle = build_useful_god_knowledge_bundle(
        facts,
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert bundle.status == DataAvailability.PARTIAL
    assert USEFUL_GOD_KNOWLEDGE_MISSING in bundle.diagnostics
    assert bundle.selected_entity is None
    payload = str(bundle.to_dict())
    assert "generic fallback" not in payload.lower()
    assert bundle.selected_key == "NotAStem"


def test_j_role_conflict_detected(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """J. Role conflict is detected."""
    facts = _facts(
        selected="Đinh",
        favorable=("Đinh", "Canh"),
        unfavorable=("Canh", "Tân"),
    )
    bundle = build_useful_god_knowledge_bundle(
        facts,
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert USEFUL_GOD_ROLE_CONFLICT in bundle.diagnostics
    assert bundle.selected_key == "Đinh"
    assert "Canh" in bundle.favorable_keys
    assert "Canh" in bundle.unfavorable_keys


def test_k_huynh_retrieves_required_entities(huynh_explanation) -> None:
    """K. Lương Ngọc Huỳnh retrieves Chính Tài selected (UG-R2 Frozen)."""
    bundle = build_useful_god_knowledge_bundle(huynh_explanation)
    assert bundle.selected_key == "Chính Tài"
    assert bundle.selected_entity is not None
    assert bundle.selected_entity.key == "Chính Tài"
    assert set(bundle.favorable_keys) == {"Chính Tài", "Thực Thần"}
    assert set(bundle.unfavorable_keys) == {"Kiếp Tài"}
    assert {entity.key for entity in bundle.favorable_entities} == {
        "Chính Tài",
        "Thực Thần",
    }
    assert {entity.key for entity in bundle.unfavorable_entities} == {"Kiếp Tài"}
    selected_concept_ids = {item.id for item in bundle.selected_concepts}
    assert selected_concept_ids
    assert bundle.status == DataAvailability.AVAILABLE
    assert USEFUL_GOD_KNOWLEDGE_MISSING not in bundle.diagnostics


def test_l_case0001_uses_generic_knowledge(case0001_explanation) -> None:
    """L. CASE-0001 uses generic knowledge with no Huỳnh-specific content."""
    bundle = build_useful_god_knowledge_bundle(case0001_explanation)
    assert bundle.selected_key == case0001_explanation.decision.selected
    payload = str(bundle.to_dict())
    assert "Lương Ngọc Huỳnh" not in payload
    assert "1966" not in payload
    for entity in (
        *(() if bundle.selected_entity is None else (bundle.selected_entity,)),
        *bundle.favorable_entities,
        *bundle.unfavorable_entities,
    ):
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
        assert "Huỳnh" not in blob


def test_m_knowledge_cannot_alter_decision(huynh_explanation) -> None:
    """M. Knowledge cannot alter Decision selected value."""
    selected_before = huynh_explanation.decision.selected
    favorable_before = [
        item.value for item in huynh_explanation.evidence if item.fact == "favorable_god"
    ]
    unfavorable_before = [
        item.value
        for item in huynh_explanation.evidence
        if item.fact == "unfavorable_god"
    ]
    bundle = build_useful_god_knowledge_bundle(huynh_explanation)
    assert huynh_explanation.decision.selected == selected_before
    assert bundle.selected_key == selected_before
    assert list(bundle.favorable_keys) == favorable_before
    assert list(bundle.unfavorable_keys) == unfavorable_before


def test_n_no_ui_dependency() -> None:
    """N. No UI dependency."""
    import engines.interpretation_engine.foundation.knowledge.retrieval as retrieval
    import engines.interpretation_engine.foundation.knowledge.bundle as bundle_mod

    for mod in (retrieval, bundle_mod):
        source = Path(mod.__file__ or "").read_text(encoding="utf-8")
        assert "customer_portal" not in source
        assert "portal" not in Path(mod.__file__ or "").parts


def test_o_no_narrative_dependency() -> None:
    """O. No Narrative dependency."""
    import engines.interpretation_engine.foundation.knowledge.retrieval as retrieval

    source = Path(retrieval.__file__ or "").read_text(encoding="utf-8")
    assert "narrative_engine" not in source
    assert "NarrativeEngine" not in source
    assert "customer paragraph" not in source.lower()


def test_duplicate_content_not_copied(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Duplicate-content detector finds no copy-paste across stems."""
    warnings = DuplicateContentDetector().detect(list(knowledge_registry.list("UsefulGod")))
    assert warnings == ()


def test_quality_report_and_coverage_index(
    knowledge_registry: KnowledgeRegistry,
) -> None:
    """Coverage index and quality report are generated from live knowledge."""
    report = build_useful_god_quality_report(knowledge_registry=knowledge_registry)
    assert report.entity_count >= 10
    assert report.approved_count >= 10
    assert report.draft_count == 0
    assert report.broken_references == ()
    assert report.missing_required_content == ()
    assert report.duplicate_content_warnings == ()
    assert all(status == "APPROVED" for status in report.stem_status.values())
    markdown = report.to_markdown()
    assert "UsefulGod Knowledge V1" in markdown
    assert "Giáp" in markdown
    coverage_path, quality_path = write_useful_god_reports(report=report)
    assert coverage_path.is_file()
    assert quality_path.is_file()
    assert "APPROVED" in coverage_path.read_text(encoding="utf-8")


def test_bundle_from_facts_matches_keys(
    knowledge_registry: KnowledgeRegistry,
    concept_registry: ConceptRegistry,
) -> None:
    """Facts input builds the same structured lookup as explanation keys."""
    facts = _facts(
        selected="Đinh",
        favorable=("Đinh", "Bính", "Ất"),
        unfavorable=("Canh", "Tân"),
        rejected=("Bính", "Nhâm"),
    )
    bundle = build_useful_god_knowledge_bundle(
        facts,
        knowledge_registry=knowledge_registry,
        concept_registry=concept_registry,
    )
    assert bundle.selected_entity is not None
    assert bundle.selected_entity.key == "Đinh"
    assert {entity.key for entity in bundle.rejected_entities} >= {"Nhâm"}
    assert bundle.status == DataAvailability.AVAILABLE


def _facts(
    *,
    selected: str,
    favorable: tuple[str, ...],
    unfavorable: tuple[str, ...],
    rejected: tuple[str, ...] = (),
) -> UsefulGodInterpretationFacts:
    """Build structured Useful God facts for retrieval tests."""
    candidates = [
        UsefulGodCandidateFact(
            useful_god=selected,
            rule_id="test_selected",
            confidence=0.9,
            reason="test",
            rule_group="season",
        )
    ]
    for key in rejected:
        candidates.append(
            UsefulGodCandidateFact(
                useful_god=key,
                rule_id=f"test_{key}",
                confidence=0.4,
                reason="rejected test",
                rule_group="temperature",
            )
        )
    return UsefulGodInterpretationFacts(
        selected=selected,
        candidate_type="season",
        confidence=0.9,
        reason="test reason",
        favorable_gods=favorable,
        unfavorable_gods=unfavorable,
        candidates=tuple(candidates),
        rule_ids=("test_selected",),
        presence=DataAvailability.AVAILABLE,
        status=DataAvailability.AVAILABLE,
        day_master="Bính",
        day_master_element="Hỏa",
        month_branch="Dậu",
        season="Thu",
        strength_level="strong",
        strength_score=0.66,
        temperature_level="cool",
        five_elements={"wood": 2, "fire": 7, "earth": 4, "metal": 4, "water": 0},
    )

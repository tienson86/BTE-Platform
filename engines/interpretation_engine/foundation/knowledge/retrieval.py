"""Retrieve Useful God knowledge from Decision Explanation / facts."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry
from engines.interpretation_engine.foundation.explanation.models import DecisionExplanationResult
from engines.interpretation_engine.foundation.facts.useful_god import UsefulGodInterpretationFacts
from engines.interpretation_engine.foundation.knowledge.bundle import (
    UsefulGodKnowledgeBundle,
    UsefulGodKnowledgeCoverage,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    USEFUL_GOD_KNOWLEDGE_MISSING,
    USEFUL_GOD_ROLE_CONFLICT,
)
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.registry import KnowledgeRegistry
from engines.interpretation_engine.foundation.knowledge.service import get_knowledge_registry
from engines.interpretation_engine.foundation.concepts.service import get_concept_registry
from engines.interpretation_engine.foundation.status import DataAvailability

_USEFUL_GOD_DOMAIN = "UsefulGod"


def build_useful_god_knowledge_bundle(
    source: DecisionExplanationResult | UsefulGodInterpretationFacts,
    *,
    knowledge_registry: KnowledgeRegistry | None = None,
    concept_registry: ConceptRegistry | None = None,
) -> UsefulGodKnowledgeBundle:
    """Build a structured Useful God knowledge bundle from analytical input.

    Input must be Decision Explanation or Useful God facts — not customer prose.
    Lookup never changes ``selected`` / Hỷ / Kỵ values supplied by the source.
    """
    knowledge = knowledge_registry or get_knowledge_registry()
    concepts = concept_registry or get_concept_registry()
    selected, favorable, unfavorable, rejected = _extract_keys(source)
    return _assemble_bundle(
        selected=selected,
        favorable=favorable,
        unfavorable=unfavorable,
        rejected=rejected,
        knowledge=knowledge,
        concepts=concepts,
    )


def _extract_keys(
    source: DecisionExplanationResult | UsefulGodInterpretationFacts,
) -> tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Read Dụng / Hỷ / Kỵ / rejected keys from structured analytical input."""
    if isinstance(source, UsefulGodInterpretationFacts):
        selected = source.selected
        favorable = _unique(source.favorable_gods)
        unfavorable = _unique(source.unfavorable_gods)
        rejected = _unique(
            candidate.useful_god
            for candidate in source.candidates
            if candidate.useful_god and candidate.useful_god != selected
        )
        return selected, favorable, unfavorable, rejected

    selected = source.decision.selected if source.decision is not None else ""
    favorable = _keys_from_evidence(source, "favorable_god")
    unfavorable = _keys_from_evidence(source, "unfavorable_god")
    if not favorable:
        favorable = _keys_from_analysis(source, "favorable_gods")
    if not unfavorable:
        unfavorable = _keys_from_analysis(source, "unfavorable_gods")
    rejected = _unique(
        alternative.candidate
        for alternative in source.alternatives
        if alternative.status == "rejected" and alternative.candidate
    )
    return selected, favorable, unfavorable, rejected


def _keys_from_evidence(
    explanation: DecisionExplanationResult,
    fact_name: str,
) -> tuple[str, ...]:
    """Read stem keys from structured evidence items."""
    return _unique(
        item.value
        for item in explanation.evidence
        if item.fact == fact_name and item.value
    )


def _keys_from_analysis(
    explanation: DecisionExplanationResult,
    fact_name: str,
) -> tuple[str, ...]:
    """Read comma-separated stem keys from analysis facts."""
    for item in explanation.analysis:
        if item.fact != fact_name:
            continue
        if not item.value or item.value == "none":
            return ()
        return _unique(part.strip() for part in item.value.split(",") if part.strip())
    return ()


def _assemble_bundle(
    *,
    selected: str,
    favorable: tuple[str, ...],
    unfavorable: tuple[str, ...],
    rejected: tuple[str, ...],
    knowledge: KnowledgeRegistry,
    concepts: ConceptRegistry,
) -> UsefulGodKnowledgeBundle:
    """Lookup entities/concepts and flag missing data or role conflicts."""
    diagnostics: list[str] = []

    overlap = sorted(set(favorable) & set(unfavorable))
    if overlap:
        diagnostics.append(USEFUL_GOD_ROLE_CONFLICT)

    selected_entity = _lookup(knowledge, selected) if selected else None
    favorable_entities, favorable_found, favorable_missing = _lookup_many(
        knowledge, favorable
    )
    unfavorable_entities, unfavorable_found, unfavorable_missing = _lookup_many(
        knowledge, unfavorable
    )
    rejected_entities, rejected_found, rejected_missing = _lookup_many(
        knowledge, rejected
    )

    missing_requested = False
    if selected and selected_entity is None:
        missing_requested = True
    if favorable_missing or unfavorable_missing:
        missing_requested = True
    if missing_requested:
        diagnostics.append(USEFUL_GOD_KNOWLEDGE_MISSING)

    selected_concepts = _concepts_for(selected_entity, concepts)
    favorable_concepts = _concepts_for_many(favorable_entities, concepts)
    unfavorable_concepts = _concepts_for_many(unfavorable_entities, concepts)
    rejected_concepts = _concepts_for_many(rejected_entities, concepts)

    status = DataAvailability.PARTIAL if missing_requested else DataAvailability.AVAILABLE
    concept_count = len(
        {
            item.id
            for item in (
                *selected_concepts,
                *favorable_concepts,
                *unfavorable_concepts,
                *rejected_concepts,
            )
        }
    )
    coverage = UsefulGodKnowledgeCoverage(
        selected_found=selected_entity is not None,
        favorable_found=favorable_found,
        favorable_missing=favorable_missing,
        unfavorable_found=unfavorable_found,
        unfavorable_missing=unfavorable_missing,
        rejected_found=rejected_found,
        rejected_missing=rejected_missing,
        concept_count=concept_count,
    )
    return UsefulGodKnowledgeBundle(
        selected_entity=selected_entity,
        favorable_entities=favorable_entities,
        unfavorable_entities=unfavorable_entities,
        rejected_entities=rejected_entities,
        selected_concepts=selected_concepts,
        favorable_concepts=favorable_concepts,
        unfavorable_concepts=unfavorable_concepts,
        rejected_concepts=rejected_concepts,
        status=status,
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        coverage=coverage,
        selected_key=selected,
        favorable_keys=favorable,
        unfavorable_keys=unfavorable,
        rejected_keys=rejected,
    )


def _lookup(registry: KnowledgeRegistry, key: str) -> KnowledgeEntity | None:
    """Lookup one Useful God entity by key."""
    if not key:
        return None
    return registry.get(_USEFUL_GOD_DOMAIN, key)


def _lookup_many(
    registry: KnowledgeRegistry,
    keys: tuple[str, ...],
) -> tuple[tuple[KnowledgeEntity, ...], tuple[str, ...], tuple[str, ...]]:
    """Lookup many keys; preserve request order; do not invent fallback entities."""
    found_entities: list[KnowledgeEntity] = []
    found_keys: list[str] = []
    missing_keys: list[str] = []
    for key in keys:
        entity = _lookup(registry, key)
        if entity is None:
            missing_keys.append(key)
            continue
        found_entities.append(entity)
        found_keys.append(key)
    return tuple(found_entities), tuple(found_keys), tuple(missing_keys)


def _concepts_for(
    entity: KnowledgeEntity | None,
    registry: ConceptRegistry,
) -> tuple[ConceptEntity, ...]:
    """Resolve concept_ids for one entity."""
    if entity is None:
        return ()
    results: list[ConceptEntity] = []
    for concept_id in entity.concept_ids:
        concept = registry.get(concept_id)
        if concept is not None:
            results.append(concept)
    return tuple(results)


def _concepts_for_many(
    entities: tuple[KnowledgeEntity, ...],
    registry: ConceptRegistry,
) -> tuple[ConceptEntity, ...]:
    """Resolve concepts for many entities, de-duplicating by id."""
    seen: set[str] = set()
    results: list[ConceptEntity] = []
    for entity in entities:
        for concept in _concepts_for(entity, registry):
            if concept.id in seen:
                continue
            seen.add(concept.id)
            results.append(concept)
    return tuple(results)


def _unique(values: Any) -> tuple[str, ...]:
    """Preserve order while dropping empty duplicates."""
    return tuple(dict.fromkeys(str(item) for item in values if str(item)))

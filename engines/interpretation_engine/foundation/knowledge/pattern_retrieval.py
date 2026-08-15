"""Retrieve Pattern knowledge from PatternFacts."""

from __future__ import annotations

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry
from engines.interpretation_engine.foundation.concepts.service import get_concept_registry
from engines.interpretation_engine.foundation.interpreters.pattern.facts import PatternFacts
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    INVALID_PATTERN,
    PATTERN_CONCEPTS_MISSING,
    PATTERN_KNOWLEDGE_MISSING,
)
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_READINESS_PARTIAL,
    KNOWLEDGE_READINESS_READY,
    PATTERN_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.pattern_bundle import (
    PatternKnowledgeBundle,
    PatternKnowledgeCoverage,
)
from engines.interpretation_engine.foundation.knowledge.registry import KnowledgeRegistry
from engines.interpretation_engine.foundation.knowledge.service import get_knowledge_registry
from engines.interpretation_engine.foundation.status import DataAvailability

_PATTERN_DOMAIN = "Pattern"


def build_pattern_knowledge_bundle(
    facts: PatternFacts,
    *,
    knowledge_registry: KnowledgeRegistry | None = None,
    concept_registry: ConceptRegistry | None = None,
) -> PatternKnowledgeBundle:
    """Lookup Pattern knowledge by engine code. Do not change selected pattern."""
    knowledge = knowledge_registry or get_knowledge_registry()
    concepts = concept_registry or get_concept_registry()
    selected = str(facts.selected or "").strip()
    diagnostics: list[str] = list(facts.diagnostics)
    invalid = bool(selected) and selected not in PATTERN_KEYS
    if invalid:
        diagnostics.append(INVALID_PATTERN)

    entity: KnowledgeEntity | None = None
    if selected and not invalid:
        entity = knowledge.get(_PATTERN_DOMAIN, selected)
        if entity is None:
            diagnostics.append(PATTERN_KNOWLEDGE_MISSING)
    elif not selected:
        diagnostics.append(PATTERN_KNOWLEDGE_MISSING)

    resolved, missing_concept_ids = _concepts_for(entity, concepts)
    if entity is not None and (not entity.concept_ids or missing_concept_ids):
        diagnostics.append(PATTERN_CONCEPTS_MISSING)

    missing_entity = PATTERN_KNOWLEDGE_MISSING in diagnostics
    missing_concepts = PATTERN_CONCEPTS_MISSING in diagnostics
    if invalid:
        status = DataAvailability.INVALID
        readiness = KNOWLEDGE_READINESS_PARTIAL
    elif missing_entity or missing_concepts:
        status = DataAvailability.PARTIAL
        readiness = KNOWLEDGE_READINESS_PARTIAL
    else:
        status = DataAvailability.AVAILABLE
        readiness = KNOWLEDGE_READINESS_READY

    coverage = PatternKnowledgeCoverage(
        pattern_found=entity is not None,
        pattern_key=selected,
        concept_count=len(resolved),
        missing_concept_ids=missing_concept_ids,
        readiness=readiness,
        entity_type=entity.entity_type if entity is not None else "",
    )
    return PatternKnowledgeBundle(
        facts=facts,
        pattern_entity=entity,
        concepts=resolved,
        status=status,
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        coverage=coverage,
    )


def _concepts_for(
    entity: KnowledgeEntity | None,
    registry: ConceptRegistry,
) -> tuple[tuple[ConceptEntity, ...], tuple[str, ...]]:
    """Resolve concept_ids; report unresolved ids."""
    if entity is None:
        return (), ()
    results: list[ConceptEntity] = []
    missing: list[str] = []
    for concept_id in entity.concept_ids:
        concept = registry.get(concept_id)
        if concept is None:
            missing.append(concept_id)
            continue
        results.append(concept)
    return tuple(results), tuple(missing)

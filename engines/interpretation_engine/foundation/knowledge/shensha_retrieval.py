"""Retrieve Shen Sha knowledge from ShenShaFacts — all matched stars."""

from __future__ import annotations

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry
from engines.interpretation_engine.foundation.concepts.service import get_concept_registry
from engines.interpretation_engine.foundation.interpreters.shensha.facts import ShenShaFacts
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    INVALID_SHENSHA,
    SHENSHA_CONCEPTS_MISSING,
    SHENSHA_KNOWLEDGE_MISSING,
)
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_READINESS_PARTIAL,
    KNOWLEDGE_READINESS_READY,
    SHEN_SHA_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.registry import KnowledgeRegistry
from engines.interpretation_engine.foundation.knowledge.service import get_knowledge_registry
from engines.interpretation_engine.foundation.knowledge.shensha_bundle import (
    ShenShaKnowledgeBundle,
    ShenShaKnowledgeCoverage,
)
from engines.interpretation_engine.foundation.status import DataAvailability

_SHENSHA_DOMAIN = "ShenSha"


def build_shensha_knowledge_bundle(
    facts: ShenShaFacts,
    *,
    knowledge_registry: KnowledgeRegistry | None = None,
    concept_registry: ConceptRegistry | None = None,
) -> ShenShaKnowledgeBundle:
    """Lookup knowledge for every matched star. Do not remap labels."""
    knowledge = knowledge_registry or get_knowledge_registry()
    concepts = concept_registry or get_concept_registry()
    requested = tuple(facts.matched_shensha)
    diagnostics: list[str] = list(facts.diagnostics)
    entities: list[KnowledgeEntity] = []
    missing_keys: list[str] = []
    invalid = False
    for key in requested:
        if key not in SHEN_SHA_KEYS:
            invalid = True
            continue
        entity = knowledge.get(_SHENSHA_DOMAIN, key)
        if entity is None:
            missing_keys.append(key)
            continue
        entities.append(entity)
    if invalid:
        diagnostics.append(INVALID_SHENSHA)
    if missing_keys or (requested and not entities):
        diagnostics.append(SHENSHA_KNOWLEDGE_MISSING)

    resolved, missing_concept_ids = _concepts_for(entities, concepts)
    if entities and (
        any(not entity.concept_ids for entity in entities) or missing_concept_ids
    ):
        diagnostics.append(SHENSHA_CONCEPTS_MISSING)

    missing_entity = SHENSHA_KNOWLEDGE_MISSING in diagnostics
    missing_concepts = SHENSHA_CONCEPTS_MISSING in diagnostics
    if INVALID_SHENSHA in diagnostics:
        status = DataAvailability.INVALID
        readiness = KNOWLEDGE_READINESS_PARTIAL
    elif missing_entity or missing_concepts:
        status = DataAvailability.PARTIAL
        readiness = KNOWLEDGE_READINESS_PARTIAL
    else:
        status = DataAvailability.AVAILABLE
        readiness = KNOWLEDGE_READINESS_READY

    coverage = ShenShaKnowledgeCoverage(
        requested_keys=requested,
        found_keys=tuple(entity.key for entity in entities),
        missing_keys=tuple(missing_keys),
        concept_count=len(resolved),
        missing_concept_ids=missing_concept_ids,
        readiness=readiness,
    )
    return ShenShaKnowledgeBundle(
        facts=facts,
        entities=tuple(entities),
        concepts=resolved,
        status=status,
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        coverage=coverage,
    )


def _concepts_for(
    entities: list[KnowledgeEntity],
    registry: ConceptRegistry,
) -> tuple[tuple[ConceptEntity, ...], tuple[str, ...]]:
    """Resolve concept_ids across retrieved entities; report unresolved ids."""
    results: list[ConceptEntity] = []
    missing: list[str] = []
    seen: set[str] = set()
    for entity in entities:
        for concept_id in entity.concept_ids:
            if concept_id in seen:
                continue
            seen.add(concept_id)
            concept = registry.get(concept_id)
            if concept is None:
                missing.append(concept_id)
                continue
            results.append(concept)
    return tuple(results), tuple(missing)

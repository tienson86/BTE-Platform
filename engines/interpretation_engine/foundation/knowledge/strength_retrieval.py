"""Retrieve Strength knowledge from StrengthAssessment."""

from __future__ import annotations

from engines.interpretation_engine.foundation.assessment.strength import (
    StrengthAssessment,
)
from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry
from engines.interpretation_engine.foundation.concepts.service import get_concept_registry
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    INVALID_STRENGTH_STATE,
    STRENGTH_CONCEPTS_MISSING,
    STRENGTH_KNOWLEDGE_MISSING,
)
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_READINESS_PARTIAL,
    KNOWLEDGE_READINESS_READY,
    STRENGTH_STATE_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.registry import KnowledgeRegistry
from engines.interpretation_engine.foundation.knowledge.service import get_knowledge_registry
from engines.interpretation_engine.foundation.knowledge.strength_bundle import (
    StrengthKnowledgeBundle,
    StrengthKnowledgeCoverage,
)
from engines.interpretation_engine.foundation.status import DataAvailability

_STRENGTH_DOMAIN = "Strength"


def build_strength_knowledge_bundle(
    assessment: StrengthAssessment,
    *,
    knowledge_registry: KnowledgeRegistry | None = None,
    concept_registry: ConceptRegistry | None = None,
) -> StrengthKnowledgeBundle:
    """Build a structured Strength knowledge bundle from assessment.

    Lookup never changes the assessed state supplied by StrengthAssessment.
    Missing knowledge is reported; no silent fallback entity is invented.
    """
    knowledge = knowledge_registry or get_knowledge_registry()
    concepts = concept_registry or get_concept_registry()
    state = str(assessment.state or "").strip()
    diagnostics: list[str] = list(assessment.diagnostics)
    invalid_state = bool(state) and state not in STRENGTH_STATE_KEYS
    if invalid_state and INVALID_STRENGTH_STATE not in diagnostics:
        diagnostics.append(INVALID_STRENGTH_STATE)

    entity: KnowledgeEntity | None = None
    if state and not invalid_state:
        entity = knowledge.get(_STRENGTH_DOMAIN, state)
        if entity is None:
            diagnostics.append(STRENGTH_KNOWLEDGE_MISSING)
    elif not state:
        diagnostics.append(STRENGTH_KNOWLEDGE_MISSING)

    resolved, missing_concept_ids = _concepts_for(entity, concepts)
    if entity is not None and (not entity.concept_ids or missing_concept_ids):
        diagnostics.append(STRENGTH_CONCEPTS_MISSING)

    missing_requested = STRENGTH_KNOWLEDGE_MISSING in diagnostics
    missing_concepts = STRENGTH_CONCEPTS_MISSING in diagnostics
    if invalid_state:
        status = DataAvailability.INVALID
        readiness = KNOWLEDGE_READINESS_PARTIAL
    elif missing_requested or missing_concepts:
        status = DataAvailability.PARTIAL
        readiness = KNOWLEDGE_READINESS_PARTIAL
    else:
        status = DataAvailability.AVAILABLE
        readiness = KNOWLEDGE_READINESS_READY

    coverage = StrengthKnowledgeCoverage(
        state_found=entity is not None,
        state_key=state,
        concept_count=len(resolved),
        missing_concept_ids=missing_concept_ids,
        readiness=readiness,
        entity_type=entity.entity_type if entity is not None else "",
    )
    return StrengthKnowledgeBundle(
        assessment=assessment,
        state_entity=entity,
        concepts=resolved,
        status=status,
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        coverage=coverage,
    )


def _concepts_for(
    entity: KnowledgeEntity | None,
    registry: ConceptRegistry,
) -> tuple[tuple[ConceptEntity, ...], tuple[str, ...]]:
    """Resolve concept_ids; report unresolved ids without inventing concepts."""
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

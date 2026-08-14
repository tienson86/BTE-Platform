"""Retrieve interpretation concepts for knowledge entities."""

from __future__ import annotations

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.service import retrieve_knowledge

_default_registry: ConceptRegistry | None = None


def get_concept_registry() -> ConceptRegistry:
    """Return shared default concept registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = ConceptRegistry.default()
    return _default_registry


def retrieve_concept(concept_id: str) -> ConceptEntity | None:
    """Lookup one concept by id."""
    return get_concept_registry().get(concept_id)


def retrieve_concepts(concept_ids: tuple[str, ...] | list[str]) -> tuple[ConceptEntity, ...]:
    """Lookup multiple concepts preserving order."""
    registry = get_concept_registry()
    results: list[ConceptEntity] = []
    for concept_id in concept_ids:
        concept = registry.get(concept_id)
        if concept is not None:
            results.append(concept)
    return tuple(results)


def retrieve_concepts_for_knowledge(domain: str, key: str) -> tuple[ConceptEntity, ...]:
    """Resolve concept_ids from a knowledge entity lookup."""
    entity = retrieve_knowledge(domain, key)
    if entity is None:
        return ()
    return retrieve_concepts(entity.concept_ids)


def retrieve_concepts_for_entity(entity: KnowledgeEntity) -> tuple[ConceptEntity, ...]:
    """Resolve concept_ids from a loaded knowledge entity."""
    return retrieve_concepts(entity.concept_ids)

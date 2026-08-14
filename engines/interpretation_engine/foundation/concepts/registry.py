"""Concept registry — opaque lookup API for semantic graph."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engines.interpretation_engine.foundation.concepts.categories import (
    CANONICAL_CONCEPT_CATEGORIES,
)
from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.concepts.loader import JsonConceptLoader
from engines.interpretation_engine.foundation.concepts.relationships import (
    ConceptRelationshipType,
)
from engines.interpretation_engine.foundation.concepts.validator import (
    ConceptValidationResult,
    ConceptValidator,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONCEPT_ROOT = _REPO_ROOT / "knowledge" / "interpretation" / "concepts"


class ConceptRegistry:
    """Registry for concept id lookup and graph navigation."""

    def __init__(self, concepts: list[ConceptEntity]) -> None:
        """Index concepts by id and category."""
        self._by_id: dict[str, ConceptEntity] = {}
        self._by_category: dict[str, list[ConceptEntity]] = {}
        for concept in concepts:
            self._by_id[concept.id] = concept
            self._by_category.setdefault(concept.category, []).append(concept)

    @classmethod
    def default(cls, *, root: Path | None = None) -> ConceptRegistry:
        """Load default registry from knowledge/interpretation/concepts."""
        loader = JsonConceptLoader(root or DEFAULT_CONCEPT_ROOT)
        concepts = loader.load_all()
        return cls(concepts)

    @classmethod
    def from_loader(cls, loader: JsonConceptLoader) -> ConceptRegistry:
        """Build registry from a configured loader."""
        return cls(loader.load_all())

    def get(self, concept_id: str) -> ConceptEntity | None:
        """Return concept by id, or None."""
        return self._by_id.get(concept_id)

    def exists(self, concept_id: str) -> bool:
        """Return True when concept exists."""
        return concept_id in self._by_id

    def list(self, category: str) -> tuple[ConceptEntity, ...]:
        """List all concepts in a category."""
        return tuple(self._by_category.get(category, ()))

    def list_categories(self) -> tuple[str, ...]:
        """Return categories that have at least one concept."""
        return tuple(sorted(self._by_category))

    def related(
        self,
        concept_id: str,
        relationship: ConceptRelationshipType | None = None,
    ) -> tuple[ConceptEntity, ...]:
        """Return concepts linked from concept_id via graph edges."""
        concept = self.get(concept_id)
        if concept is None:
            return ()
        results: list[ConceptEntity] = []
        for edge in concept.related_concepts:
            if relationship is not None and edge.relationship != relationship:
                continue
            target = self.get(edge.target_id)
            if target is not None:
                results.append(target)
        return tuple(results)

    def validate(self) -> ConceptValidationResult:
        """Validate all indexed concepts."""
        return ConceptValidator().validate(list(self._by_id.values()))

    def known_ids(self) -> frozenset[str]:
        """Return all known concept ids."""
        return frozenset(self._by_id)

    def canonical_categories(self) -> tuple[str, ...]:
        """Return frozen canonical category list."""
        return CANONICAL_CONCEPT_CATEGORIES

    def to_dict(self) -> dict[str, Any]:
        """Serialize registry summary."""
        return {
            "concept_count": len(self._by_id),
            "categories": {
                category: [concept.id for concept in items]
                for category, items in sorted(self._by_category.items())
            },
        }

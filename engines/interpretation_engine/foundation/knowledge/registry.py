"""Knowledge registry — opaque lookup API for interpreters."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engines.interpretation_engine.foundation.knowledge.domains import CANONICAL_KNOWLEDGE_DOMAINS
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.loader import JsonKnowledgeLoader
from engines.interpretation_engine.foundation.knowledge.validator import (
    KnowledgeValidationResult,
    KnowledgeValidator,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_KNOWLEDGE_ROOT = _REPO_ROOT / "knowledge" / "interpretation"


class KnowledgeRegistry:
    """Registry for domain/key knowledge lookup."""

    def __init__(self, entities: list[KnowledgeEntity]) -> None:
        """Index entities by domain and key."""
        self._by_domain_key: dict[tuple[str, str], KnowledgeEntity] = {}
        self._by_domain: dict[str, list[KnowledgeEntity]] = {}
        for entity in entities:
            self._by_domain_key[(entity.domain, entity.key)] = entity
            self._by_domain.setdefault(entity.domain, []).append(entity)

    @classmethod
    def default(cls, *, root: Path | None = None) -> KnowledgeRegistry:
        """Load default registry from knowledge/interpretation."""
        loader = JsonKnowledgeLoader(root or DEFAULT_KNOWLEDGE_ROOT)
        entities = loader.load_all()
        return cls(entities)

    @classmethod
    def from_loader(cls, loader: JsonKnowledgeLoader) -> KnowledgeRegistry:
        """Build registry from a configured loader."""
        return cls(loader.load_all())

    def get(self, domain: str, key: str) -> KnowledgeEntity | None:
        """Return knowledge entity for domain/key, or None."""
        return self._by_domain_key.get((domain, key))

    def exists(self, domain: str, key: str) -> bool:
        """Return True when entity exists."""
        return (domain, key) in self._by_domain_key

    def list(self, domain: str) -> tuple[KnowledgeEntity, ...]:
        """List all entities in a domain."""
        return tuple(self._by_domain.get(domain, ()))

    def list_domains(self) -> tuple[str, ...]:
        """Return domains that have at least one entity."""
        return tuple(sorted(self._by_domain))

    def validate(self) -> KnowledgeValidationResult:
        """Validate all indexed entities and concept references."""
        from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry

        entities = list(self._by_domain_key.values())
        known_concept_ids = ConceptRegistry.default().known_ids()
        return KnowledgeValidator().validate(
            entities,
            known_concept_ids=known_concept_ids,
        )

    def canonical_domains(self) -> tuple[str, ...]:
        """Return frozen canonical domain list."""
        return CANONICAL_KNOWLEDGE_DOMAINS

    def to_dict(self) -> dict[str, Any]:
        """Serialize registry summary."""
        return {
            "entity_count": len(self._by_domain_key),
            "domains": {
                domain: [entity.key for entity in items]
                for domain, items in sorted(self._by_domain.items())
            },
        }

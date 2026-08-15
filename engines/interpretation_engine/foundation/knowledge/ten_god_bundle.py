"""Ten God knowledge bundle — retrieval of multiple roles, not narrative."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.interpreters.ten_gods.facts import TenGodFacts
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class TenGodKnowledgeCoverage:
    """Lookup coverage for one Ten Gods knowledge retrieval."""

    requested_keys: tuple[str, ...]
    found_keys: tuple[str, ...]
    missing_keys: tuple[str, ...]
    concept_count: int
    missing_concept_ids: tuple[str, ...]
    readiness: str = "PARTIAL"

    def to_dict(self) -> dict[str, Any]:
        """Serialize coverage."""
        return {
            "requested_keys": list(self.requested_keys),
            "found_keys": list(self.found_keys),
            "missing_keys": list(self.missing_keys),
            "concept_count": self.concept_count,
            "missing_concept_ids": list(self.missing_concept_ids),
            "readiness": self.readiness,
        }


@dataclass(frozen=True, slots=True)
class TenGodKnowledgeBundle:
    """Structured Ten Gods knowledge for all visible and hidden roles."""

    facts: TenGodFacts
    entities: tuple[KnowledgeEntity, ...]
    concepts: tuple[ConceptEntity, ...]
    status: DataAvailability
    diagnostics: tuple[str, ...]
    coverage: TenGodKnowledgeCoverage

    def to_dict(self) -> dict[str, Any]:
        """Serialize bundle without generating customer prose."""
        return {
            "facts": self.facts.to_dict(),
            "entities": [item.to_dict() for item in self.entities],
            "concepts": [item.to_dict() for item in self.concepts],
            "status": self.status.value,
            "diagnostics": list(self.diagnostics),
            "coverage": self.coverage.to_dict(),
        }

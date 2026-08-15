"""Pattern knowledge bundle — retrieval, not narrative."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.interpreters.pattern.facts import PatternFacts
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class PatternKnowledgeCoverage:
    """Lookup coverage for one Pattern knowledge retrieval."""

    pattern_found: bool
    pattern_key: str
    concept_count: int
    missing_concept_ids: tuple[str, ...]
    readiness: str = "PARTIAL"
    entity_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize coverage."""
        return {
            "pattern_found": self.pattern_found,
            "pattern_key": self.pattern_key,
            "concept_count": self.concept_count,
            "missing_concept_ids": list(self.missing_concept_ids),
            "readiness": self.readiness,
            "entity_type": self.entity_type,
        }


@dataclass(frozen=True, slots=True)
class PatternKnowledgeBundle:
    """Structured Pattern knowledge for one PatternFacts lookup."""

    facts: PatternFacts
    pattern_entity: KnowledgeEntity | None
    concepts: tuple[ConceptEntity, ...]
    status: DataAvailability
    diagnostics: tuple[str, ...]
    coverage: PatternKnowledgeCoverage

    def to_dict(self) -> dict[str, Any]:
        """Serialize bundle without generating customer prose."""
        return {
            "facts": self.facts.to_dict(),
            "pattern_entity": (
                self.pattern_entity.to_dict() if self.pattern_entity else None
            ),
            "concepts": [item.to_dict() for item in self.concepts],
            "status": self.status.value,
            "diagnostics": list(self.diagnostics),
            "coverage": self.coverage.to_dict(),
        }

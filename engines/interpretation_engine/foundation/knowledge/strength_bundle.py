"""Strength knowledge bundle — state retrieval, not decision, not narrative."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.assessment.strength import (
    StrengthAssessment,
)
from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class StrengthKnowledgeCoverage:
    """Lookup coverage for one Strength knowledge retrieval."""

    state_found: bool
    state_key: str
    concept_count: int
    missing_concept_ids: tuple[str, ...]
    readiness: str = "PARTIAL"
    entity_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize coverage."""
        return {
            "state_found": self.state_found,
            "state_key": self.state_key,
            "concept_count": self.concept_count,
            "missing_concept_ids": list(self.missing_concept_ids),
            "readiness": self.readiness,
            "entity_type": self.entity_type,
        }


@dataclass(frozen=True, slots=True)
class StrengthKnowledgeBundle:
    """Structured Strength knowledge for one StrengthAssessment.

    Knowledge explains the assessed state. It does not reclassify strength
    and does not generate customer prose.
    """

    assessment: StrengthAssessment
    state_entity: KnowledgeEntity | None
    concepts: tuple[ConceptEntity, ...]
    status: DataAvailability
    diagnostics: tuple[str, ...]
    coverage: StrengthKnowledgeCoverage

    def to_dict(self) -> dict[str, Any]:
        """Serialize bundle without generating customer prose."""
        return {
            "assessment": self.assessment.to_dict(),
            "state_entity": (
                self.state_entity.to_dict() if self.state_entity else None
            ),
            "concepts": [item.to_dict() for item in self.concepts],
            "status": self.status.value,
            "diagnostics": list(self.diagnostics),
            "coverage": self.coverage.to_dict(),
        }

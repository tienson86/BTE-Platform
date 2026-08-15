"""Useful God knowledge bundle — structured retrieval, not narrative."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.concepts.entity import ConceptEntity
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class UsefulGodKnowledgeCoverage:
    """Lookup coverage for one Useful God knowledge retrieval."""

    selected_found: bool
    favorable_found: tuple[str, ...]
    favorable_missing: tuple[str, ...]
    unfavorable_found: tuple[str, ...]
    unfavorable_missing: tuple[str, ...]
    rejected_found: tuple[str, ...]
    rejected_missing: tuple[str, ...]
    concept_count: int
    readiness: str = "PARTIAL"
    selected_entity_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize coverage."""
        return {
            "selected_found": self.selected_found,
            "favorable_found": list(self.favorable_found),
            "favorable_missing": list(self.favorable_missing),
            "unfavorable_found": list(self.unfavorable_found),
            "unfavorable_missing": list(self.unfavorable_missing),
            "rejected_found": list(self.rejected_found),
            "rejected_missing": list(self.rejected_missing),
            "concept_count": self.concept_count,
            "readiness": self.readiness,
            "selected_entity_type": self.selected_entity_type,
        }


@dataclass(frozen=True, slots=True)
class UsefulGodKnowledgeBundle:
    """Structured Useful God knowledge for one Decision Explanation.

    Knowledge explains roles already assigned upstream. It does not
    recalculate Dụng / Hỷ / Kỵ and does not generate customer prose.
    """

    selected_entity: KnowledgeEntity | None
    favorable_entities: tuple[KnowledgeEntity, ...]
    unfavorable_entities: tuple[KnowledgeEntity, ...]
    rejected_entities: tuple[KnowledgeEntity, ...]
    selected_concepts: tuple[ConceptEntity, ...]
    favorable_concepts: tuple[ConceptEntity, ...]
    unfavorable_concepts: tuple[ConceptEntity, ...]
    rejected_concepts: tuple[ConceptEntity, ...]
    status: DataAvailability
    diagnostics: tuple[str, ...]
    coverage: UsefulGodKnowledgeCoverage
    selected_key: str
    favorable_keys: tuple[str, ...]
    unfavorable_keys: tuple[str, ...]
    rejected_keys: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize bundle without generating customer prose."""
        return {
            "selected_key": self.selected_key,
            "favorable_keys": list(self.favorable_keys),
            "unfavorable_keys": list(self.unfavorable_keys),
            "rejected_keys": list(self.rejected_keys),
            "selected_entity": (
                self.selected_entity.to_dict() if self.selected_entity else None
            ),
            "favorable_entities": [item.to_dict() for item in self.favorable_entities],
            "unfavorable_entities": [
                item.to_dict() for item in self.unfavorable_entities
            ],
            "rejected_entities": [item.to_dict() for item in self.rejected_entities],
            "selected_concepts": [item.to_dict() for item in self.selected_concepts],
            "favorable_concepts": [item.to_dict() for item in self.favorable_concepts],
            "unfavorable_concepts": [
                item.to_dict() for item in self.unfavorable_concepts
            ],
            "rejected_concepts": [item.to_dict() for item in self.rejected_concepts],
            "status": self.status.value,
            "diagnostics": list(self.diagnostics),
            "coverage": self.coverage.to_dict(),
        }

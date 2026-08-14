"""ConceptEntity contract — reusable semantic meaning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.foundation.references import KnowledgeEntityReference
from engines.interpretation_engine.foundation.concepts.relationships import (
    ConceptRelationshipType,
)
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus


@dataclass(frozen=True, slots=True)
class ConceptRelationship:
    """Directed edge in the concept graph."""

    target_id: str
    relationship: ConceptRelationshipType

    def to_dict(self) -> dict[str, str]:
        """Serialize relationship."""
        return {
            "target_id": self.target_id,
            "relationship": self.relationship.value,
        }


@dataclass(frozen=True, slots=True)
class ConceptMetadata:
    """Concept lifecycle metadata."""

    author: str
    version: str
    status: KnowledgeStatus
    source: str
    created: str = ""
    updated: str = ""
    quality: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata."""
        return {
            "author": self.author,
            "version": self.version,
            "created": self.created,
            "updated": self.updated,
            "status": self.status.value,
            "source": self.source,
            "quality": self.quality,
        }


@dataclass(frozen=True, slots=True)
class ConceptEntity:
    """Reusable semantic concept for interpretation knowledge."""

    id: str
    category: str
    title: str
    metadata: ConceptMetadata
    summary: str = ""
    meaning: str = ""
    conditions: tuple[str, ...] = ()
    applications: Mapping[str, str] = field(default_factory=dict)
    related_concepts: tuple[ConceptRelationship, ...] = ()
    related_entities: tuple[KnowledgeEntityReference, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize concept entity."""
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "summary": self.summary,
            "meaning": self.meaning,
            "conditions": list(self.conditions),
            "applications": dict(self.applications),
            "related_concepts": [item.to_dict() for item in self.related_concepts],
            "related_entities": [item.to_dict() for item in self.related_entities],
            "metadata": self.metadata.to_dict(),
        }

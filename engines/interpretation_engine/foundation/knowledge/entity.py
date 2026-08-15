"""KnowledgeEntity contract — expert meaning, not calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.foundation.references import KnowledgeEntityReference
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus

__all__ = ["KnowledgeEntity", "KnowledgeEntityReference", "KnowledgeMetadata"]


@dataclass(frozen=True, slots=True)
class KnowledgeMetadata:
    """Entity metadata — author, version, lifecycle."""

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
class KnowledgeEntity:
    """Generic expert knowledge item for one domain key."""

    id: str
    domain: str
    key: str
    title: str
    metadata: KnowledgeMetadata
    meaning: str = ""
    positive_meaning: str = ""
    negative_meaning: str = ""
    applications: Mapping[str, str] = field(default_factory=dict)
    recommendations: tuple[Mapping[str, Any], ...] = ()
    warnings: tuple[Mapping[str, Any], ...] = ()
    related_entities: tuple[KnowledgeEntityReference, ...] = ()
    concept_ids: tuple[str, ...] = ()
    evidence_notes: str = ""
    entity_type: str = ""
    mechanism: str = ""
    manifestation: str = ""
    contraindications: tuple[Mapping[str, Any], ...] = ()
    activation_conditions: tuple[str, ...] = ()
    typical_triggers: tuple[str, ...] = ()
    luck_relationship: str = ""
    pattern_relationship: str = ""
    ten_gods_relationship: str = ""
    suppression: str = ""
    base_influence: str = ""
    conditional_influence: str = ""
    activation_dependency: str = ""
    suppression_conditions: tuple[str, ...] = ()
    interaction_conditions: tuple[str, ...] = ()
    relationship_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize knowledge entity."""
        return {
            "id": self.id,
            "domain": self.domain,
            "key": self.key,
            "entity_type": self.entity_type,
            "title": self.title,
            "meaning": self.meaning,
            "positive_meaning": self.positive_meaning,
            "negative_meaning": self.negative_meaning,
            "applications": dict(self.applications),
            "recommendations": [dict(item) for item in self.recommendations],
            "warnings": [dict(item) for item in self.warnings],
            "related_entities": [item.to_dict() for item in self.related_entities],
            "concept_ids": list(self.concept_ids),
            "evidence_notes": self.evidence_notes,
            "mechanism": self.mechanism,
            "manifestation": self.manifestation,
            "contraindications": [dict(item) for item in self.contraindications],
            "activation_conditions": list(self.activation_conditions),
            "typical_triggers": list(self.typical_triggers),
            "luck_relationship": self.luck_relationship,
            "pattern_relationship": self.pattern_relationship,
            "ten_gods_relationship": self.ten_gods_relationship,
            "suppression": self.suppression,
            "base_influence": self.base_influence,
            "conditional_influence": self.conditional_influence,
            "activation_dependency": self.activation_dependency,
            "suppression_conditions": list(self.suppression_conditions),
            "interaction_conditions": list(self.interaction_conditions),
            "relationship_notes": self.relationship_notes,
            "metadata": self.metadata.to_dict(),
        }

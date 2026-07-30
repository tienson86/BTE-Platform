"""Relationship index for typed relationship edges."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from services.knowledge.models import KnowledgeRecord


class RelationshipIndex:
    """Index relationship edges by type and endpoint."""

    def __init__(self) -> None:
        """Initialize empty relationship index."""
        self.by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
        self.by_source: dict[str, list[dict[str, str]]] = defaultdict(list)

    def build(self, records: list[KnowledgeRecord]) -> RelationshipIndex:
        """Rebuild relationship indexes."""
        self.by_type.clear()
        self.by_source.clear()
        for record in records:
            if not record.knowledge_id:
                continue
            relationships = record.data.get("relationships", {})
            if not isinstance(relationships, dict):
                continue
            for rel_key, value in relationships.items():
                for link in self._iter_links(value):
                    target = str(link.get("knowledge_id", "")).strip()
                    rel_type = str(
                        link.get("relationship_type") or rel_key
                    ).strip()
                    if not target:
                        continue
                    edge = {
                        "source": record.knowledge_id,
                        "target": target,
                        "type": rel_type,
                        "slot": rel_key,
                    }
                    self.by_type[rel_type].append(edge)
                    self.by_source[record.knowledge_id].append(edge)
        return self

    def edges_for(self, knowledge_id: str) -> list[dict[str, str]]:
        """Return outgoing edges for a knowledge id."""
        return list(self.by_source.get(knowledge_id, []))

    def edges_of_type(self, relationship_type: str) -> list[dict[str, str]]:
        """Return all edges of a given relationship type."""
        return list(self.by_type.get(relationship_type, []))

    def _iter_links(self, value: Any) -> list[dict[str, Any]]:
        if isinstance(value, dict):
            return [value]
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        return []

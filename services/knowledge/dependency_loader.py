"""Extract dependency edges from Knowledge Records."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from services.knowledge.models import KnowledgeRecord


class DependencyLoader:
    """Build dependency maps from record relationship sections."""

    def load_edges(
        self,
        records: list[KnowledgeRecord],
    ) -> dict[str, list[str]]:
        """Return adjacency map: knowledge_id -> dependency ids."""
        edges: dict[str, list[str]] = defaultdict(list)
        for record in records:
            src = record.knowledge_id
            if not src:
                continue
            for dep_id in self._extract_dependency_ids(record.data):
                if dep_id and dep_id not in edges[src]:
                    edges[src].append(dep_id)
        return dict(edges)

    def load_reverse_edges(
        self,
        records: list[KnowledgeRecord],
    ) -> dict[str, list[str]]:
        """Return reverse adjacency map: dependency id -> dependents."""
        reverse: dict[str, list[str]] = defaultdict(list)
        for src, deps in self.load_edges(records).items():
            for dep in deps:
                if src not in reverse[dep]:
                    reverse[dep].append(src)
        return dict(reverse)

    def _extract_dependency_ids(self, data: dict[str, Any]) -> list[str]:
        relationships = data.get("relationships", {})
        if not isinstance(relationships, dict):
            return []
        ids: list[str] = []
        depends_on = relationships.get("depends_on", [])
        if isinstance(depends_on, list):
            for item in depends_on:
                if isinstance(item, dict):
                    kid = str(item.get("knowledge_id", "")).strip()
                    if kid:
                        ids.append(kid)
        return ids

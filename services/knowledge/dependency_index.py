"""Dependency index for Knowledge Records."""

from __future__ import annotations

from services.knowledge.dependency_loader import DependencyLoader
from services.knowledge.models import KnowledgeRecord


class DependencyIndex:
    """Forward and reverse dependency indexes."""

    def __init__(self) -> None:
        """Initialize empty dependency index."""
        self.forward: dict[str, list[str]] = {}
        self.reverse: dict[str, list[str]] = {}
        self._loader = DependencyLoader()

    def build(self, records: list[KnowledgeRecord]) -> DependencyIndex:
        """Rebuild dependency indexes."""
        self.forward = self._loader.load_edges(records)
        self.reverse = self._loader.load_reverse_edges(records)
        return self

    def dependents_of(self, knowledge_id: str) -> list[str]:
        """Return records that depend on the given id."""
        return list(self.reverse.get(knowledge_id, []))

    def dependencies_of(self, knowledge_id: str) -> list[str]:
        """Return dependencies of the given id."""
        return list(self.forward.get(knowledge_id, []))

    def graph(self) -> dict[str, list[str]]:
        """Return forward dependency graph."""
        return dict(self.forward)

"""Interpreter registry dependency graph."""

from __future__ import annotations

from collections import defaultdict, deque

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry.metadata import InterpreterRegistryEntry


class DependencyGraph:
    """Directed dependency graph over interpreter registry entries.

    Models interpreter load-order relationships structurally only.
    Does not generate sentences or interpret BaZi content.
    """

    def __init__(self) -> None:
        """Initialize an empty dependency graph."""
        self._nodes: set[str] = set()
        self._outgoing: dict[str, set[str]] = defaultdict(set)
        self._incoming: dict[str, set[str]] = defaultdict(set)
        self._missing: set[str] = set()

    def clear(self) -> None:
        """Remove all nodes and edges."""
        self._nodes.clear()
        self._outgoing.clear()
        self._incoming.clear()
        self._missing.clear()

    def add_node(self, node_id: str) -> None:
        """Ensure a registered node exists in the graph."""
        self._nodes.add(node_id)
        self._missing.discard(node_id)

    def add_edge(self, source_id: str, target_id: str) -> None:
        """Add a dependency edge ``source → target`` (source depends on target)."""
        self.add_node(source_id)
        self._outgoing[source_id].add(target_id)
        self._incoming[target_id].add(source_id)
        if target_id not in self._nodes:
            self._missing.add(target_id)

    def build_from_entries(self, entries: tuple[InterpreterRegistryEntry, ...]) -> None:
        """Rebuild the graph from interpreter registry entry dependencies."""
        self.clear()
        known = {entry.entry_id for entry in entries}
        for entry_id in known:
            self.add_node(entry_id)
        for entry in entries:
            for dependency_id in entry.dependencies:
                self.add_edge(entry.entry_id, dependency_id)

    def nodes(self) -> tuple[str, ...]:
        """Return sorted registered node identifiers."""
        return tuple(sorted(self._nodes))

    def dependencies_of(self, entry_id: str) -> tuple[str, ...]:
        """Return direct dependency identifiers for an entry."""
        return tuple(sorted(self._outgoing.get(entry_id, set())))

    def dependents_of(self, entry_id: str) -> tuple[str, ...]:
        """Return identifiers that directly depend on an entry."""
        return tuple(sorted(self._incoming.get(entry_id, set())))

    def missing_dependencies(
        self,
        entries: tuple[InterpreterRegistryEntry, ...] | None = None,
    ) -> tuple[str, ...]:
        """Return referenced identifiers that are not registered entries."""
        if entries is not None:
            present = {entry.entry_id for entry in entries}
            missing: set[str] = set()
            for entry in entries:
                for dependency_id in entry.dependencies:
                    if dependency_id not in present:
                        missing.add(dependency_id)
            return tuple(sorted(missing))
        return tuple(sorted(self._missing))

    def has_cycle(self) -> bool:
        """Return True when the registered subgraph contains a directed cycle."""
        try:
            self.topological_order()
        except InterpretationRegistryError:
            return True
        return False

    def topological_order(self) -> tuple[str, ...]:
        """Return a deterministic topological order of registered nodes.

        Missing external references are ignored for ordering.
        Raises:
            InterpretationRegistryError: if a circular dependency is detected.
        """
        indegree: dict[str, int] = {node: 0 for node in self._nodes}
        adjacency: dict[str, set[str]] = defaultdict(set)

        for source, targets in self._outgoing.items():
            if source not in self._nodes:
                continue
            for target in targets:
                if target not in self._nodes:
                    continue
                adjacency[target].add(source)
                indegree[source] += 1

        queue: deque[str] = deque(
            sorted(node for node, degree in indegree.items() if degree == 0)
        )
        ordered: list[str] = []
        while queue:
            node = queue.popleft()
            ordered.append(node)
            for dependent in sorted(adjacency.get(node, set())):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(ordered) != len(self._nodes):
            raise InterpretationRegistryError("circular_dependency_detected")
        return tuple(ordered)

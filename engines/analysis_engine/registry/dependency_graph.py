"""Registry dependency graph runtime service."""

from __future__ import annotations

from collections import defaultdict, deque

from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.registry.registry_models import RegistryEntry


class DependencyGraph:
    """Directed dependency graph over registry entry references.

    Models Pack 01 registry relationships structurally only.
    Does not interpret academic meaning of references.
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
        if target_id in self._nodes:
            self._outgoing[source_id].add(target_id)
            self._incoming[target_id].add(source_id)
            return
        self._outgoing[source_id].add(target_id)
        self._incoming[target_id].add(source_id)
        self._missing.add(target_id)

    def build_from_entries(self, entries: tuple[RegistryEntry, ...]) -> None:
        """Rebuild the graph from registry entry references."""
        self.clear()
        known = {entry.entry_id for entry in entries}
        for entry_id in known:
            self.add_node(entry_id)
        for entry in entries:
            for reference_id in entry.references:
                self.add_edge(entry.entry_id, reference_id)

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
        entries: tuple[RegistryEntry, ...] | None = None,
    ) -> tuple[str, ...]:
        """Return referenced identifiers that are not registered entries."""
        if entries is not None:
            present = {entry.entry_id for entry in entries}
            missing: set[str] = set()
            for entry in entries:
                for reference_id in entry.references:
                    if reference_id not in present:
                        missing.add(reference_id)
            return tuple(sorted(missing))
        return tuple(sorted(self._missing))

    def has_cycle(self) -> bool:
        """Return True when the registered subgraph contains a directed cycle."""
        try:
            self.topological_order()
        except RegistryError:
            return True
        return False

    def topological_order(self) -> tuple[str, ...]:
        """Return a deterministic topological order of registered nodes.

        Missing external references are ignored for ordering.
        Raises:
            RegistryError: if a circular dependency is detected among registered nodes.
        """
        # Restrict edges to registered nodes for cycle detection / load order.
        indegree: dict[str, int] = {node: 0 for node in self._nodes}
        adjacency: dict[str, set[str]] = defaultdict(set)
        reverse: dict[str, set[str]] = defaultdict(set)

        for source, targets in self._outgoing.items():
            if source not in self._nodes:
                continue
            for target in targets:
                if target not in self._nodes:
                    continue
                # source depends on target → target precedes source
                adjacency[target].add(source)
                reverse[source].add(target)
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
            raise RegistryError("circular_dependency_detected")
        return tuple(ordered)

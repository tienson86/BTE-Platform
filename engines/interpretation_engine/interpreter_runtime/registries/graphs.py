"""Registry graph primitives for Pack 03 interpreter integration.

Infrastructure only. Dependency Injection only. No singleton globals.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Mapping

from engines.interpretation_engine.runtime.registry_base import RegistryError


@dataclass(frozen=True, slots=True)
class GraphNode:
    """Immutable registry graph node descriptor."""

    node_id: str
    priority: int = 100
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate node structural integrity."""
        return bool(self.node_id)


class DependencyGraph:
    """Directed dependency graph over registry node identifiers."""

    def __init__(self) -> None:
        """Initialize an empty dependency graph."""
        self._nodes: dict[str, GraphNode] = {}

    def clear(self) -> None:
        """Remove all nodes."""
        self._nodes.clear()

    def add_node(self, node: GraphNode) -> None:
        """Add or replace a graph node."""
        if not node.validate():
            raise RegistryError("graph_node_invalid")
        self._nodes[node.node_id] = node

    def remove_node(self, node_id: str) -> None:
        """Remove a node if present."""
        self._nodes.pop(node_id, None)

    def nodes(self) -> tuple[str, ...]:
        """Return sorted node identifiers."""
        return tuple(sorted(self._nodes.keys()))

    def get(self, node_id: str) -> GraphNode | None:
        """Lookup a node by identifier."""
        return self._nodes.get(node_id)

    def dependencies_of(self, node_id: str) -> tuple[str, ...]:
        """Return direct dependencies for a node."""
        node = self._nodes.get(node_id)
        if node is None:
            return ()
        return tuple(node.dependencies)

    def missing_dependencies(self) -> tuple[str, ...]:
        """Return dependency ids that are not registered nodes."""
        known = set(self._nodes)
        missing: set[str] = set()
        for node in self._nodes.values():
            for dep in node.dependencies:
                if dep not in known:
                    missing.add(dep)
        return tuple(sorted(missing))

    def topological_order(self) -> tuple[str, ...]:
        """Return deterministic topological order; raise on cycles."""
        indegree: dict[str, int] = {node_id: 0 for node_id in self._nodes}
        adjacency: dict[str, set[str]] = defaultdict(set)
        for node_id, node in self._nodes.items():
            for dep in node.dependencies:
                if dep in self._nodes:
                    adjacency[dep].add(node_id)
                    indegree[node_id] += 1

        ready = sorted(
            [node_id for node_id, degree in indegree.items() if degree == 0],
            key=lambda item: (self._nodes[item].priority, item),
        )
        ordered: list[str] = []
        while ready:
            current = ready.pop(0)
            ordered.append(current)
            nxt: list[str] = []
            for dependent in sorted(
                adjacency[current],
                key=lambda item: (self._nodes[item].priority, item),
            ):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    nxt.append(dependent)
            ready.extend(nxt)
            ready.sort(key=lambda item: (self._nodes[item].priority, item))

        if len(ordered) != len(self._nodes):
            raise RegistryError("dependency_graph_cycle")
        return tuple(ordered)

    def has_cycle(self) -> bool:
        """Return True when the graph contains a cycle."""
        try:
            self.topological_order()
        except RegistryError:
            return True
        return False

    def validate(self) -> bool:
        """Validate graph has no cycles and no missing dependencies."""
        if self.missing_dependencies():
            return False
        return not self.has_cycle()


class PriorityGraph:
    """Priority ordering graph (lower priority value executes first)."""

    def __init__(self) -> None:
        """Initialize empty priority graph."""
        self._priorities: dict[str, int] = {}

    def clear(self) -> None:
        """Remove all priorities."""
        self._priorities.clear()

    def set_priority(self, node_id: str, priority: int) -> None:
        """Set priority for a node."""
        if not node_id:
            raise RegistryError("priority_node_id_required")
        self._priorities[node_id] = priority

    def remove(self, node_id: str) -> None:
        """Remove a node priority."""
        self._priorities.pop(node_id, None)

    def priority_of(self, node_id: str) -> int | None:
        """Return priority for a node if known."""
        return self._priorities.get(node_id)

    def ordered(self) -> tuple[str, ...]:
        """Return nodes ordered by priority then id."""
        return tuple(
            sorted(self._priorities.keys(), key=lambda item: (self._priorities[item], item))
        )

    def validate(self) -> bool:
        """Validate all priorities are assigned to non-empty ids."""
        return all(bool(node_id) for node_id in self._priorities)


class ExecutionGraph:
    """Execution graph combining dependency topology and priority order."""

    def __init__(
        self,
        *,
        dependency_graph: DependencyGraph | None = None,
        priority_graph: PriorityGraph | None = None,
    ) -> None:
        """Initialize with injected dependency and priority graphs."""
        self._dependency_graph = dependency_graph or DependencyGraph()
        self._priority_graph = priority_graph or PriorityGraph()

    @property
    def dependency_graph(self) -> DependencyGraph:
        """Return dependency graph collaborator."""
        return self._dependency_graph

    @property
    def priority_graph(self) -> PriorityGraph:
        """Return priority graph collaborator."""
        return self._priority_graph

    def rebuild_from_nodes(self, nodes: tuple[GraphNode, ...]) -> None:
        """Rebuild both graphs from node descriptors."""
        self._dependency_graph.clear()
        self._priority_graph.clear()
        for node in nodes:
            self._dependency_graph.add_node(node)
            self._priority_graph.set_priority(node.node_id, node.priority)

    def execution_order(self) -> tuple[str, ...]:
        """Return execution order (dependency-aware, priority-stable)."""
        return self._dependency_graph.topological_order()

    def priority_order(self) -> tuple[str, ...]:
        """Return pure priority order."""
        return self._priority_graph.ordered()

    def validate(self) -> bool:
        """Validate dependency and priority graphs."""
        return self._dependency_graph.validate() and self._priority_graph.validate()

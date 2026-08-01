"""Graph algorithms used by dependency and knowledge-graph builders."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable


def detect_cycles(edges: Iterable[tuple[str, str]]) -> list[list[str]]:
    """Detect directed cycles. Returns list of cycle node-id lists."""
    adjacency: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for source, target in edges:
        adjacency[source].append(target)
        nodes.add(source)
        nodes.add(target)

    visited: set[str] = set()
    stack: set[str] = set()
    path: list[str] = []
    cycles: list[list[str]] = []

    def dfs(node: str) -> None:
        visited.add(node)
        stack.add(node)
        path.append(node)
        for neighbor in sorted(adjacency.get(node, [])):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in stack:
                idx = path.index(neighbor)
                cycles.append(path[idx:] + [neighbor])
        path.pop()
        stack.remove(node)

    for node in sorted(nodes):
        if node not in visited:
            dfs(node)
    return cycles


def topological_sort(
    nodes: Iterable[str],
    edges: Iterable[tuple[str, str]],
) -> list[str]:
    """Kahn topological sort. Edge (u, v) means u depends on v (v before u)."""
    node_set = set(nodes)
    indegree: dict[str, int] = {n: 0 for n in node_set}
    dependents: dict[str, list[str]] = defaultdict(list)

    for source, target in edges:
        if source not in node_set or target not in node_set:
            continue
        # target must precede source → edge target -> source in Kahn graph
        dependents[target].append(source)
        indegree[source] = indegree.get(source, 0) + 1
        indegree.setdefault(target, indegree.get(target, 0))

    queue = deque(sorted(n for n, d in indegree.items() if d == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dependent in sorted(dependents.get(node, [])):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(node_set):
        remaining = sorted(node_set - set(order))
        order.extend(remaining)
    return order


def orphan_nodes(
    nodes: Iterable[str],
    edges: Iterable[tuple[str, str]],
) -> list[str]:
    """Return nodes with no incident edges."""
    connected: set[str] = set()
    for source, target in edges:
        connected.add(source)
        connected.add(target)
    return sorted(set(nodes) - connected)


def connected_components(
    nodes: Iterable[str],
    edges: Iterable[tuple[str, str]],
) -> list[list[str]]:
    """Undirected connected components over the edge set."""
    adjacency: dict[str, set[str]] = defaultdict(set)
    node_set = set(nodes)
    for source, target in edges:
        adjacency[source].add(target)
        adjacency[target].add(source)
        node_set.add(source)
        node_set.add(target)

    seen: set[str] = set()
    components: list[list[str]] = []
    for start in sorted(node_set):
        if start in seen:
            continue
        queue = deque([start])
        component: list[str] = []
        seen.add(start)
        while queue:
            node = queue.popleft()
            component.append(node)
            for neighbor in sorted(adjacency.get(node, [])):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    return components

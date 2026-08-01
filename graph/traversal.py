"""Graph traversal helpers for Graph Builder V2."""

from __future__ import annotations

from collections import defaultdict, deque

from graph.models import KnowledgeGraph


def adjacency(graph: KnowledgeGraph) -> dict[str, list[str]]:
    """Build outgoing adjacency lists sorted for determinism."""
    adj: dict[str, list[str]] = defaultdict(list)
    for edge in graph.edges:
        adj[edge.source].append(edge.target)
    return {key: sorted(set(values)) for key, values in sorted(adj.items())}


def bfs(graph: KnowledgeGraph, start: str) -> list[str]:
    """Breadth-first traversal from start node."""
    adj = adjacency(graph)
    if start not in {node.node_id for node in graph.nodes}:
        return []
    visited: set[str] = set()
    order: list[str] = []
    queue: deque[str] = deque([start])
    visited.add(start)
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs(graph: KnowledgeGraph, start: str) -> list[str]:
    """Depth-first traversal from start node."""
    adj = adjacency(graph)
    if start not in {node.node_id for node in graph.nodes}:
        return []
    visited: set[str] = set()
    order: list[str] = []

    def _walk(node: str) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                _walk(neighbor)

    _walk(start)
    return order


def reachable(graph: KnowledgeGraph, start: str) -> set[str]:
    """Return the reachable node set from start."""
    return set(bfs(graph, start))

"""Graph optimization utilities (deterministic, non-destructive)."""

from __future__ import annotations

import logging
from collections import Counter

from graph.models import GraphEdge, GraphNode, KnowledgeGraph

logger = logging.getLogger(__name__)


class GraphOptimizer:
    """Optimize graphs by removing duplicate nodes/edges and sorting canonically."""

    def optimize(self, graph: KnowledgeGraph) -> KnowledgeGraph:
        """Return an optimized copy of the graph."""
        nodes = self.deduplicate_nodes(graph.nodes)
        edges = self.deduplicate_edges(graph.edges)
        nodes = self.sort_nodes(nodes)
        edges = self.sort_edges(edges)
        edges = self.drop_dangling_edges(nodes, edges)
        optimized = KnowledgeGraph(
            graph_id=graph.graph_id,
            graph_type=graph.graph_type,
            title=graph.title,
            nodes=nodes,
            edges=edges,
            schema_version=graph.schema_version,
            status=graph.status,
            timestamp=graph.timestamp,
            metadata={
                **graph.metadata,
                "optimized": True,
                "optimizer": "GraphOptimizerV2",
            },
        )
        logger.debug(
            "Optimized %s: nodes %s->%s edges %s->%s",
            graph.graph_type,
            len(graph.nodes),
            len(nodes),
            len(graph.edges),
            len(edges),
        )
        return optimized

    def deduplicate_nodes(self, nodes: list[GraphNode]) -> list[GraphNode]:
        """Keep first occurrence of each node_id."""
        seen: set[str] = set()
        result: list[GraphNode] = []
        for node in nodes:
            if node.node_id in seen:
                continue
            seen.add(node.node_id)
            result.append(node)
        return result

    def deduplicate_edges(self, edges: list[GraphEdge]) -> list[GraphEdge]:
        """Deduplicate by edge_id, then by (source, target, edge_type)."""
        by_id: set[str] = set()
        by_triple: set[tuple[str, str, str]] = set()
        result: list[GraphEdge] = []
        for edge in edges:
            triple = (edge.source, edge.target, edge.edge_type)
            if edge.edge_id in by_id or triple in by_triple:
                continue
            by_id.add(edge.edge_id)
            by_triple.add(triple)
            result.append(edge)
        return result

    def sort_nodes(self, nodes: list[GraphNode]) -> list[GraphNode]:
        """Canonical node order by node_id."""
        return sorted(nodes, key=lambda node: node.node_id)

    def sort_edges(self, edges: list[GraphEdge]) -> list[GraphEdge]:
        """Canonical edge order by edge_id."""
        return sorted(edges, key=lambda edge: edge.edge_id)

    def drop_dangling_edges(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
    ) -> list[GraphEdge]:
        """Remove edges whose endpoints are not in the node set."""
        node_ids = {node.node_id for node in nodes}
        return [
            edge
            for edge in edges
            if edge.source in node_ids and edge.target in node_ids
        ]

    def compression_stats(
        self,
        before: KnowledgeGraph,
        after: KnowledgeGraph,
    ) -> dict[str, int]:
        """Return before/after node and edge counts."""
        return {
            "nodes_before": len(before.nodes),
            "nodes_after": len(after.nodes),
            "edges_before": len(before.edges),
            "edges_after": len(after.edges),
            "duplicate_node_candidates": sum(
                1 for _, count in Counter(n.node_id for n in before.nodes).items() if count > 1
            ),
            "duplicate_edge_candidates": sum(
                1 for _, count in Counter(e.edge_id for e in before.edges).items() if count > 1
            ),
        }

"""Graph validation for Graph Builder V2 outputs."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from graph.models import KnowledgeGraph


@dataclass(slots=True)
class GraphValidationResult:
    """Validation outcome for one graph."""

    ok: bool
    graph_type: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation result."""
        return {
            "ok": self.ok,
            "graph_type": self.graph_type,
            "findings": self.findings,
            "statistics": self.statistics,
        }


class GraphValidator:
    """Validate graph integrity: IDs, dangling edges, duplicates, cycles (optional)."""

    def validate(self, graph: KnowledgeGraph, *, check_cycles: bool = False) -> GraphValidationResult:
        """Validate a single knowledge graph."""
        findings: list[dict[str, Any]] = []
        node_ids = [node.node_id for node in graph.nodes]
        node_set = set(node_ids)

        for node_id, count in Counter(node_ids).items():
            if count > 1:
                findings.append(
                    {
                        "code": "DUPLICATE_NODE",
                        "severity": "ERROR",
                        "message": f"Duplicate node_id '{node_id}'",
                    }
                )

        edge_ids = [edge.edge_id for edge in graph.edges]
        for edge_id, count in Counter(edge_ids).items():
            if count > 1:
                findings.append(
                    {
                        "code": "DUPLICATE_EDGE",
                        "severity": "ERROR",
                        "message": f"Duplicate edge_id '{edge_id}'",
                    }
                )

        for edge in graph.edges:
            if edge.source not in node_set:
                findings.append(
                    {
                        "code": "DANGLING_SOURCE",
                        "severity": "ERROR",
                        "message": f"Edge '{edge.edge_id}' source missing",
                    }
                )
            if edge.target not in node_set:
                findings.append(
                    {
                        "code": "DANGLING_TARGET",
                        "severity": "ERROR",
                        "message": f"Edge '{edge.edge_id}' target missing",
                    }
                )

        cycle_count = 0
        if check_cycles:
            cycle_count = len(self._detect_cycles(graph))
            if cycle_count:
                findings.append(
                    {
                        "code": "CYCLE",
                        "severity": "WARNING",
                        "message": f"Detected {cycle_count} cycle(s)",
                    }
                )

        ok = not any(item["severity"] == "ERROR" for item in findings)
        return GraphValidationResult(
            ok=ok,
            graph_type=graph.graph_type,
            findings=findings,
            statistics={
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges),
                "finding_count": len(findings),
                "cycle_count": cycle_count,
            },
        )

    def _detect_cycles(self, graph: KnowledgeGraph) -> list[list[str]]:
        adj: dict[str, list[str]] = {node.node_id: [] for node in graph.nodes}
        for edge in graph.edges:
            adj.setdefault(edge.source, []).append(edge.target)
        visited: set[str] = set()
        stack: set[str] = set()
        path: list[str] = []
        cycles: list[list[str]] = []

        def dfs(node: str) -> None:
            visited.add(node)
            stack.add(node)
            path.append(node)
            for neighbor in sorted(adj.get(node, [])):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in stack:
                    idx = path.index(neighbor)
                    cycles.append(path[idx:] + [neighbor])
            path.pop()
            stack.remove(node)

        for node_id in sorted(adj):
            if node_id not in visited:
                dfs(node_id)
        return cycles

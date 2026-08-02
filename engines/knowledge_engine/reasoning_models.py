"""Reasoning graph models for explainable knowledge conclusions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

NodeKind = Literal["evidence", "intermediate_rule", "reasoning", "conclusion"]


@dataclass(slots=True)
class ReasoningNode:
    """One node in the explainable reasoning graph."""

    id: str
    label: str
    kind: NodeKind
    domain: str = ""
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize node."""
        return {
            "id": self.id,
            "label": self.label,
            "kind": self.kind,
            "domain": self.domain,
            "payload": dict(self.payload),
        }


@dataclass(slots=True)
class ReasoningEdge:
    """Directed edge Evidence/Rule → next step.

    Every edge stores reason, priority, confidence, and source.
    """

    id: str
    source_id: str
    target_id: str
    reason: str
    priority: int
    confidence: float
    source: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize edge."""
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "reason": self.reason,
            "priority": self.priority,
            "confidence": self.confidence,
            "source": self.source,
        }


@dataclass(slots=True)
class ReasoningGraph:
    """Full reasoning graph with metadata.trace."""

    nodes: list[ReasoningNode]
    edges: list[ReasoningEdge]
    conclusions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def node_map(self) -> dict[str, ReasoningNode]:
        """Return nodes keyed by id."""
        return {node.id: node for node in self.nodes}

    def edges_from(self, node_id: str) -> list[ReasoningEdge]:
        """Return outgoing edges from a node."""
        return [edge for edge in self.edges if edge.source_id == node_id]

    def path_labels(self, start_id: str) -> list[list[str]]:
        """Return label paths reachable from ``start_id`` (DFS, cycle-safe)."""
        nodes = self.node_map()
        adjacency: dict[str, list[str]] = {}
        for edge in self.edges:
            adjacency.setdefault(edge.source_id, []).append(edge.target_id)

        paths: list[list[str]] = []

        def walk(current: str, trail: list[str], seen: set[str]) -> None:
            label = nodes[current].label if current in nodes else current
            next_trail = trail + [label]
            targets = adjacency.get(current, [])
            if not targets:
                paths.append(next_trail)
                return
            for target in targets:
                if target in seen:
                    paths.append(next_trail + [nodes.get(target, ReasoningNode(target, target, "reasoning")).label])
                    continue
                walk(target, next_trail, seen | {target})

        if start_id in nodes:
            walk(start_id, [], {start_id})
        return paths

    @property
    def trace(self) -> list[dict[str, Any]]:
        """Return serialized reasoning trace from metadata."""
        raw = self.metadata.get("trace") if self.metadata else None
        return list(raw) if isinstance(raw, list) else []

    def to_dict(self) -> dict[str, Any]:
        """Serialize graph for reports / future AI prompt builders."""
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "conclusions": list(self.conclusions),
            "metadata": dict(self.metadata),
        }

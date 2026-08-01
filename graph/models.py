"""Typed graph models for Graph Builder V2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GraphNode:
    """Knowledge graph node."""

    node_id: str
    node_type: str
    label: str
    status: str = "official"
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize node."""
        payload = {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "status": self.status,
        }
        if self.properties:
            payload["properties"] = self.properties
        return payload


@dataclass(slots=True)
class GraphEdge:
    """Knowledge graph edge."""

    edge_id: str
    source: str
    target: str
    edge_type: str
    relationship: str = ""
    status: str = "official"
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize edge."""
        payload = {
            "edge_id": self.edge_id,
            "source": self.source,
            "target": self.target,
            "edge_type": self.edge_type,
            "relationship": self.relationship or self.edge_type,
            "status": self.status,
        }
        if self.properties:
            payload["properties"] = self.properties
        return payload


@dataclass(slots=True)
class KnowledgeGraph:
    """In-memory knowledge graph document."""

    graph_id: str
    graph_type: str
    title: str
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    schema_version: str = "1.0.0"
    status: str = "official"
    timestamp: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize graph document."""
        return {
            "graph_id": self.graph_id,
            "graph_type": self.graph_type,
            "schema_version": self.schema_version,
            "status": self.status,
            "title": self.title,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "statistics": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
            },
        }

    @staticmethod
    def from_dict(payload: dict[str, Any]) -> "KnowledgeGraph":
        """Deserialize graph document."""
        nodes = [
            GraphNode(
                node_id=str(item["node_id"]),
                node_type=str(item.get("node_type", "")),
                label=str(item.get("label", "")),
                status=str(item.get("status", "official")),
                properties=dict(item.get("properties") or {}),
            )
            for item in payload.get("nodes", [])
        ]
        edges = [
            GraphEdge(
                edge_id=str(item["edge_id"]),
                source=str(item["source"]),
                target=str(item["target"]),
                edge_type=str(item.get("edge_type", "")),
                relationship=str(item.get("relationship") or item.get("edge_type") or ""),
                status=str(item.get("status", "official")),
                properties=dict(item.get("properties") or {}),
            )
            for item in payload.get("edges", [])
        ]
        return KnowledgeGraph(
            graph_id=str(payload.get("graph_id", "")),
            graph_type=str(payload.get("graph_type", "")),
            title=str(payload.get("title", "")),
            nodes=nodes,
            edges=edges,
            schema_version=str(payload.get("schema_version", "1.0.0")),
            status=str(payload.get("status", "official")),
            timestamp=str(payload.get("timestamp", "")),
            metadata=dict(payload.get("metadata") or {}),
        )

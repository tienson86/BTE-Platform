"""Multi-format deterministic graph exporters."""

from __future__ import annotations

import json
from typing import Any
from xml.sax.saxutils import escape

from graph.models import KnowledgeGraph


class GraphExporter:
    """Export KnowledgeGraph documents to GraphML, DOT, JSON, Mermaid, JSON-LD."""

    def export_all(self, graph: KnowledgeGraph) -> dict[str, str]:
        """Return mapping of format -> serialized text."""
        payload = graph.to_dict()
        return {
            "json": self.to_json(payload),
            "graphml": self.to_graphml(payload),
            "dot": self.to_dot(payload),
            "mmd": self.to_mermaid(payload),
            "jsonld": self.to_jsonld(payload),
        }

    def to_json(self, graph: dict[str, Any]) -> str:
        """Export JSON."""
        return json.dumps(
            graph,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        ) + "\n"

    def to_graphml(self, graph: dict[str, Any]) -> str:
        """Export GraphML."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
            '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
            '  <key id="node_type" for="node" attr.name="node_type" attr.type="string"/>',
            '  <key id="edge_type" for="edge" attr.name="edge_type" attr.type="string"/>',
            f'  <graph id="{escape(str(graph.get("graph_id", "G")))}" edgedefault="directed">',
        ]
        for node in graph.get("nodes", []):
            node_id = escape(str(node["node_id"]))
            label = escape(str(node.get("label", node_id)))
            node_type = escape(str(node.get("node_type", "")))
            lines.append(f'    <node id="{node_id}">')
            lines.append(f'      <data key="label">{label}</data>')
            lines.append(f'      <data key="node_type">{node_type}</data>')
            lines.append("    </node>")
        for edge in graph.get("edges", []):
            edge_id = escape(str(edge["edge_id"]))
            source = escape(str(edge["source"]))
            target = escape(str(edge["target"]))
            edge_type = escape(str(edge.get("edge_type", "")))
            lines.append(
                f'    <edge id="{edge_id}" source="{source}" target="{target}">'
            )
            lines.append(f'      <data key="edge_type">{edge_type}</data>')
            lines.append("    </edge>")
        lines.append("  </graph>")
        lines.append("</graphml>")
        return "\n".join(lines) + "\n"

    def to_dot(self, graph: dict[str, Any]) -> str:
        """Export Graphviz DOT."""
        graph_id = _safe_id(str(graph.get("graph_id", "Graph")))
        lines = [
            f"digraph {graph_id} {{",
            "  rankdir=LR;",
            '  node [shape=box, fontname="Helvetica"];',
        ]
        for node in graph.get("nodes", []):
            node_id = _safe_id(str(node["node_id"]))
            label = str(node.get("label", node["node_id"])).replace('"', '\\"')
            node_type = str(node.get("node_type", "")).replace('"', '\\"')
            lines.append(f'  {node_id} [label="{label}\\n({node_type})"];')
        for edge in graph.get("edges", []):
            source = _safe_id(str(edge["source"]))
            target = _safe_id(str(edge["target"]))
            edge_type = str(edge.get("edge_type", "")).replace('"', '\\"')
            lines.append(f'  {source} -> {target} [label="{edge_type}"];')
        lines.append("}")
        return "\n".join(lines) + "\n"

    def to_mermaid(self, graph: dict[str, Any]) -> str:
        """Export Mermaid flowchart."""
        lines = ["flowchart LR"]
        for node in graph.get("nodes", []):
            node_id = _safe_id(str(node["node_id"]))
            label = str(node.get("label", node["node_id"])).replace('"', "'")
            lines.append(f'  {node_id}["{label}"]')
        for edge in graph.get("edges", []):
            source = _safe_id(str(edge["source"]))
            target = _safe_id(str(edge["target"]))
            edge_type = str(edge.get("edge_type", "")).replace("|", "/")
            lines.append(f"  {source} -->|{edge_type}| {target}")
        return "\n".join(lines) + "\n"

    def to_jsonld(self, graph: dict[str, Any]) -> str:
        """Export JSON-LD representation."""
        context = {
            "@vocab": "https://bte-platform.org/graph#",
            "node_id": "@id",
            "label": "https://schema.org/name",
            "node_type": "@type",
            "edge_type": "https://bte-platform.org/graph#edgeType",
            "source": {"@id": "https://bte-platform.org/graph#source", "@type": "@id"},
            "target": {"@id": "https://bte-platform.org/graph#target", "@type": "@id"},
        }
        nodes = []
        for node in graph.get("nodes", []):
            nodes.append(
                {
                    "@id": str(node["node_id"]),
                    "@type": str(node.get("node_type", "Node")),
                    "label": node.get("label"),
                    "status": node.get("status"),
                }
            )
        edges = []
        for edge in graph.get("edges", []):
            edges.append(
                {
                    "@id": str(edge["edge_id"]),
                    "@type": "Edge",
                    "edge_type": edge.get("edge_type"),
                    "source": str(edge["source"]),
                    "target": str(edge["target"]),
                }
            )
        payload = {
            "@context": context,
            "@id": str(graph.get("graph_id")),
            "@type": "KnowledgeGraph",
            "graph_type": graph.get("graph_type"),
            "title": graph.get("title"),
            "timestamp": graph.get("timestamp"),
            "nodes": nodes,
            "edges": edges,
        }
        return json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        ) + "\n"


def _safe_id(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in value)
    if cleaned and cleaned[0].isdigit():
        cleaned = f"n_{cleaned}"
    return cleaned or "node"

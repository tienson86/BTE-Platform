"""Knowledge graph generator and multi-format exporters."""

from __future__ import annotations

from typing import Any
from xml.sax.saxutils import escape

from baseline.constants import (
    PACK01_ACADEMIC_HARD_DEPS,
    PACK01_SEMANTIC_DEPS,
    SCHEMA_VERSION,
)
from baseline.models import BuildContext, GraphEdge, GraphNode


def build_knowledge_graph(
    context: BuildContext,
    knowledge_records: list[dict[str, Any]],
    ontology: dict[str, Any],
    dependency_snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Build the Pack 01 knowledge graph with nodes, edges, and mappings."""
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    pack_node = GraphNode(
        node_id=context.pack_id,
        node_type="Pack",
        label="Pack 01 — Fundamental Theory",
        properties={"version": context.version},
    )
    nodes.append(pack_node)

    for record in knowledge_records:
        nodes.append(
            GraphNode(
                node_id=record["record_id"],
                node_type="Concept",
                label=record["canonical_name"],
                properties={
                    "pattern": record["pattern"],
                    "layer": record["layer"],
                    "path": record["path"],
                },
            )
        )
        edges.append(
            GraphEdge(
                edge_id=f"BELONGS-{record['record_id']}",
                source=record["record_id"],
                target=context.pack_id,
                edge_type="BELONGS_TO",
                relationship="belongs_to_pack",
            )
        )

    for class_item in ontology.get("classes", []):
        class_id = str(class_item.get("id") or "")
        if not class_id:
            continue
        nodes.append(
            GraphNode(
                node_id=class_id,
                node_type="OntologyClass",
                label=str(class_item.get("canonical_name") or class_id),
                properties={
                    "parent_class": class_item.get("parent_class"),
                    "namespace": class_item.get("namespace"),
                },
            )
        )
        parent = class_item.get("parent_class")
        if parent:
            edges.append(
                GraphEdge(
                    edge_id=f"OPARENT-{class_id}",
                    source=class_id,
                    target=str(parent),
                    edge_type="SUBCLASS_OF",
                    relationship="ontology_hierarchy",
                )
            )

    for idx, (source, target) in enumerate(PACK01_ACADEMIC_HARD_DEPS, start=1):
        edges.append(
            GraphEdge(
                edge_id=f"DEP-H-{idx:06d}",
                source=source,
                target=target,
                edge_type="DEPENDS_ON",
                relationship="academic_hard_dependency",
                properties={"level_id": "hard_dependency"},
            )
        )
    for idx, (source, target) in enumerate(PACK01_SEMANTIC_DEPS, start=1):
        edges.append(
            GraphEdge(
                edge_id=f"DEP-S-{idx:06d}",
                source=source,
                target=target,
                edge_type="RELATED_TO",
                relationship="semantic_dependency",
                properties={"level_id": "semantic_dependency"},
            )
        )

    # Link ontology root to pack for single connectivity component.
    edges.append(
        GraphEdge(
            edge_id="ONT-PACK-ROOT",
            source="OCL-000001",
            target=context.pack_id,
            edge_type="DESCRIBES",
            relationship="ontology_describes_pack",
        )
    )

    # Context and mapping edges from analytical foundations.
    context_edges = (
        ("KR-000015", "KR-000005", "CONTEXTUALIZES"),
        ("KR-000015", "KR-000003", "CONTEXTUALIZES"),
        ("KR-000010", "KR-000007", "MAPS"),
        ("KR-000010", "KR-000004", "MAPS"),
        ("KR-000010", "KR-000005", "MAPS"),
        ("KR-000014", "KR-000004", "RELATES"),
        ("KR-000014", "KR-000005", "RELATES"),
    )
    for idx, (source, target, edge_type) in enumerate(context_edges, start=1):
        edges.append(
            GraphEdge(
                edge_id=f"CTX-{idx:06d}",
                source=source,
                target=target,
                edge_type=edge_type,
                relationship="context_or_mapping",
            )
        )

    node_dicts = [node.to_dict() for node in nodes]
    edge_dicts = [edge.to_dict() for edge in edges]
    return {
        "graph_id": "GRAPH-000001",
        "schema_version": SCHEMA_VERSION,
        "status": "official",
        "title": "Pack 01 Knowledge Graph",
        "description": (
            "Deterministic knowledge graph for Pack 01 Fundamental Theory "
            "covering records, ontology classes, dependencies, contexts, "
            "and mappings."
        ),
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "nodes": node_dicts,
        "edges": edge_dicts,
        "dependencies": dependency_snapshot.get("academic_dependency_graph", {}),
        "relationships": {
            "types": sorted({edge.edge_type for edge in edges}),
            "count": len(edges),
        },
        "contexts": [
            edge.to_dict()
            for edge in edges
            if edge.edge_type == "CONTEXTUALIZES"
        ],
        "mappings": [
            edge.to_dict() for edge in edges if edge.edge_type == "MAPS"
        ],
        "statistics": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "concept_nodes": sum(
                1 for node in nodes if node.node_type == "Concept"
            ),
            "ontology_nodes": sum(
                1 for node in nodes if node.node_type == "OntologyClass"
            ),
        },
    }


def export_graphml(graph: dict[str, Any]) -> str:
    """Export knowledge graph to GraphML."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
        '  <key id="label" for="node" attr.name="label" attr.type="string"/>',
        '  <key id="node_type" for="node" attr.name="node_type" attr.type="string"/>',
        '  <key id="edge_type" for="edge" attr.name="edge_type" attr.type="string"/>',
        '  <graph id="Pack01" edgedefault="directed">',
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


def export_dot(graph: dict[str, Any]) -> str:
    """Export knowledge graph to Graphviz DOT."""
    lines = [
        "digraph Pack01KnowledgeGraph {",
        "  rankdir=LR;",
        '  node [shape=box, fontname="Helvetica"];',
    ]
    for node in graph.get("nodes", []):
        node_id = _dot_id(str(node["node_id"]))
        label = str(node.get("label", node["node_id"])).replace('"', '\\"')
        node_type = str(node.get("node_type", ""))
        lines.append(
            f'  {node_id} [label="{label}\\n({node_type})"];'
        )
    for edge in graph.get("edges", []):
        source = _dot_id(str(edge["source"]))
        target = _dot_id(str(edge["target"]))
        edge_type = str(edge.get("edge_type", "")).replace('"', '\\"')
        lines.append(f'  {source} -> {target} [label="{edge_type}"];')
    lines.append("}")
    return "\n".join(lines) + "\n"


def export_mermaid(graph: dict[str, Any]) -> str:
    """Export knowledge graph to Mermaid flowchart syntax."""
    lines = ["flowchart LR"]
    for node in graph.get("nodes", []):
        node_id = _mmd_id(str(node["node_id"]))
        label = str(node.get("label", node["node_id"])).replace('"', "'")
        lines.append(f'  {node_id}["{label}"]')
    for edge in graph.get("edges", []):
        source = _mmd_id(str(edge["source"]))
        target = _mmd_id(str(edge["target"]))
        edge_type = str(edge.get("edge_type", "")).replace("|", "/")
        lines.append(f"  {source} -->|{edge_type}| {target}")
    return "\n".join(lines) + "\n"


def _dot_id(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in value)
    if cleaned and cleaned[0].isdigit():
        cleaned = f"n_{cleaned}"
    return cleaned or "node"


def _mmd_id(value: str) -> str:
    return _dot_id(value)

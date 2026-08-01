"""Knowledge graph validation report generator."""

from __future__ import annotations

from collections import Counter
from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.graph_algo import (
    connected_components,
    detect_cycles,
    orphan_nodes,
)
from baseline.models import BuildContext, ValidationFinding, ValidationReport


def validate_graph(
    context: BuildContext,
    graph: dict[str, Any],
) -> ValidationReport:
    """Validate cycles, orphans, duplicate edges, and connectivity."""
    findings: list[ValidationFinding] = []
    nodes = [str(n["node_id"]) for n in graph.get("nodes", [])]
    edges = graph.get("edges", [])
    edge_pairs = [(str(e["source"]), str(e["target"])) for e in edges]
    node_set = set(nodes)

    node_counts = Counter(nodes)
    for node_id, count in sorted(node_counts.items()):
        if count > 1:
            findings.append(
                ValidationFinding(
                    code="GRAPH-DUPLICATE-NODE",
                    severity="ERROR",
                    message=f"Duplicate graph node '{node_id}'",
                    object_id=node_id,
                )
            )

    edge_id_counts = Counter(str(e.get("edge_id") or "") for e in edges)
    for edge_id, count in sorted(edge_id_counts.items()):
        if edge_id and count > 1:
            findings.append(
                ValidationFinding(
                    code="GRAPH-DUPLICATE-EDGE",
                    severity="ERROR",
                    message=f"Duplicate edge ID '{edge_id}'",
                    object_id=edge_id,
                )
            )

    pair_counts = Counter(
        (
            str(e.get("source") or ""),
            str(e.get("target") or ""),
            str(e.get("edge_type") or ""),
        )
        for e in edges
    )
    for pair, count in sorted(pair_counts.items()):
        if count > 1:
            findings.append(
                ValidationFinding(
                    code="GRAPH-DUPLICATE-PAIR",
                    severity="WARNING",
                    message=(
                        f"Duplicate edge {pair[0]} -[{pair[2]}]-> {pair[1]} ({count})"
                    ),
                    object_id=f"{pair[0]}-{pair[2]}->{pair[1]}",
                )
            )

    for edge in edges:
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        if source not in node_set:
            findings.append(
                ValidationFinding(
                    code="GRAPH-BROKEN-SOURCE",
                    severity="ERROR",
                    message=f"Edge source '{source}' not in node set",
                    object_id=str(edge.get("edge_id") or ""),
                )
            )
        if target not in node_set:
            findings.append(
                ValidationFinding(
                    code="GRAPH-BROKEN-TARGET",
                    severity="ERROR",
                    message=f"Edge target '{target}' not in node set",
                    object_id=str(edge.get("edge_id") or ""),
                )
            )

    # Cycle check on hard dependency edges only.
    hard_pairs = [
        (str(e["source"]), str(e["target"]))
        for e in edges
        if e.get("edge_type") == "DEPENDS_ON"
    ]
    cycles = detect_cycles(hard_pairs)
    if cycles:
        findings.append(
            ValidationFinding(
                code="GRAPH-CYCLE",
                severity="CRITICAL",
                message=f"Detected {len(cycles)} dependency cycle(s)",
            )
        )

    orphans = orphan_nodes(nodes, edge_pairs)
    for node_id in orphans:
        findings.append(
            ValidationFinding(
                code="GRAPH-ORPHAN",
                severity="WARNING",
                message=f"Orphan graph node '{node_id}'",
                object_id=node_id,
            )
        )

    components = connected_components(nodes, edge_pairs)
    if len(components) > 1:
        findings.append(
            ValidationFinding(
                code="GRAPH-DISCONNECTED",
                severity="WARNING",
                message=(
                    f"Graph has {len(components)} connected components"
                ),
            )
        )

    status = "PASS" if not any(
        f.severity in {"ERROR", "CRITICAL"} for f in findings
    ) else "FAIL"
    return ValidationReport(
        report_id="VAL-GRAPH-BASELINE-001",
        domain="graph",
        status=status,
        schema_version=SCHEMA_VERSION,
        findings=findings,
        statistics={
            "node_count": len(nodes),
            "edge_count": len(edges),
            "cycle_count": len(cycles),
            "orphan_count": len(orphans),
            "component_count": len(components),
            "duplicate_edge_count": sum(
                1 for f in findings if f.code in {
                    "GRAPH-DUPLICATE-EDGE",
                    "GRAPH-DUPLICATE-PAIR",
                }
            ),
            "relationship_integrity_errors": sum(
                1
                for f in findings
                if f.code in {"GRAPH-BROKEN-SOURCE", "GRAPH-BROKEN-TARGET"}
            ),
        },
        metadata={
            "pack_id": context.pack_id,
            "version": context.version,
            "timestamp": context.timestamp,
            "cycles": cycles,
            "checks": [
                "cycles",
                "disconnected_nodes",
                "duplicate_edges",
                "relationship_integrity",
            ],
        },
    )

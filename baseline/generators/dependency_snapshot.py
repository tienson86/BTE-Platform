"""Dependency snapshot generator."""

from __future__ import annotations

from typing import Any

from baseline.constants import (
    PACK01_ACADEMIC_HARD_DEPS,
    PACK01_SEMANTIC_DEPS,
    SCHEMA_VERSION,
)
from baseline.graph_algo import detect_cycles, topological_sort
from baseline.models import BuildContext


def generate_dependency_snapshot(
    context: BuildContext,
    knowledge_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate academic and implementation dependency graphs."""
    nodes = [item["record_id"] for item in knowledge_records]

    academic_edges = [
        {
            "edge_id": f"ADEP-{idx:06d}",
            "source": source,
            "target": target,
            "level_id": "hard_dependency",
            "edge_type": "DEPENDS_ON",
            "graph": "academic",
        }
        for idx, (source, target) in enumerate(PACK01_ACADEMIC_HARD_DEPS, start=1)
    ]
    for idx, (source, target) in enumerate(PACK01_SEMANTIC_DEPS, start=1):
        academic_edges.append(
            {
                "edge_id": f"SDEP-{idx:06d}",
                "source": source,
                "target": target,
                "level_id": "semantic_dependency",
                "edge_type": "RELATED_TO",
                "graph": "academic",
            }
        )

    # Implementation dependency graph: sequential load order (KR-N depends on KR-(N-1)).
    implementation_pairs = [
        (nodes[i], nodes[i - 1]) for i in range(1, len(nodes))
    ]
    implementation_edges = [
        {
            "edge_id": f"IDEP-{idx:06d}",
            "source": source,
            "target": target,
            "level_id": "hard_dependency",
            "edge_type": "LOADS_AFTER",
            "graph": "implementation",
        }
        for idx, (source, target) in enumerate(implementation_pairs, start=1)
    ]

    hard_pairs = list(PACK01_ACADEMIC_HARD_DEPS)
    cycles = detect_cycles(hard_pairs)
    topo = topological_sort(nodes, hard_pairs)
    load_order = list(nodes)

    dependency_levels = [
        {
            "level": 0,
            "records": [rid for rid in topo if rid == "KR-000001"],
        },
        {
            "level": 1,
            "records": [rid for rid in topo if rid in {"KR-000002", "KR-000003"}],
        },
        {
            "level": 2,
            "records": [
                rid for rid in topo if rid in {"KR-000004", "KR-000005"}
            ],
        },
        {
            "level": 3,
            "records": [
                rid for rid in topo if rid in {"KR-000006", "KR-000007"}
            ],
        },
        {
            "level": 4,
            "records": [
                rid
                for rid in topo
                if rid in {"KR-000008", "KR-000009", "KR-000010"}
            ],
        },
        {
            "level": 5,
            "records": [
                rid
                for rid in topo
                if rid
                in {
                    "KR-000011",
                    "KR-000012",
                    "KR-000013",
                    "KR-000014",
                    "KR-000015",
                }
            ],
        },
    ]

    return {
        "artifact": "dependency_snapshot",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "nodes": nodes,
        "academic_dependency_graph": {
            "edge_count": len(academic_edges),
            "edges": academic_edges,
        },
        "implementation_dependency_graph": {
            "edge_count": len(implementation_edges),
            "edges": implementation_edges,
        },
        "topological_order": topo,
        "load_order": load_order,
        "dependency_levels": dependency_levels,
        "cycle_detection": {
            "has_cycles": bool(cycles),
            "cycle_count": len(cycles),
            "cycles": cycles,
            "scope": "hard_dependency",
        },
        "statistics": {
            "node_count": len(nodes),
            "academic_edge_count": len(academic_edges),
            "implementation_edge_count": len(implementation_edges),
            "hard_dependency_count": len(hard_pairs),
            "semantic_dependency_count": len(PACK01_SEMANTIC_DEPS),
        },
    }

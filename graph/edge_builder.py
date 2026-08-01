"""Edge builders for each Pack 01 graph type."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graph.constants import (
    ACADEMIC_HARD_DEPS,
    ACADEMIC_SEMANTIC_DEPS,
    PACK01_RECORDS,
    PACK_ID,
    REGISTRY_DOMAINS,
    RUNTIME_STAGES,
)
from graph.io_utils import read_json
from graph.models import GraphEdge


class EdgeBuilder:
    """Build typed edges for the five graph families."""

    def __init__(self, project_root: Path) -> None:
        """Initialize with project root for ontology parent links."""
        self.project_root = project_root.resolve()

    def academic_edges(self) -> list[GraphEdge]:
        """Pack membership + academic hard/semantic dependencies."""
        edges: list[GraphEdge] = []
        for record in PACK01_RECORDS:
            rid = record["record_id"]
            edges.append(
                GraphEdge(
                    edge_id=f"BELONGS-{rid}",
                    source=rid,
                    target=PACK_ID,
                    edge_type="BELONGS_TO",
                    relationship="belongs_to_pack",
                )
            )
        for idx, (source, target) in enumerate(ACADEMIC_HARD_DEPS, start=1):
            edges.append(
                GraphEdge(
                    edge_id=f"ADEP-H-{idx:06d}",
                    source=source,
                    target=target,
                    edge_type="DEPENDS_ON",
                    relationship="academic_hard_dependency",
                    properties={"level_id": "hard_dependency"},
                )
            )
        for idx, (source, target) in enumerate(ACADEMIC_SEMANTIC_DEPS, start=1):
            edges.append(
                GraphEdge(
                    edge_id=f"ADEP-S-{idx:06d}",
                    source=source,
                    target=target,
                    edge_type="RELATED_TO",
                    relationship="semantic_dependency",
                    properties={"level_id": "semantic_dependency"},
                )
            )
        return edges

    def ontology_edges(self) -> list[GraphEdge]:
        """Ontology subclass hierarchy edges."""
        path = self.project_root / "knowledge" / "ontology" / "ontology_classes.json"
        edges: list[GraphEdge] = []
        if not path.is_file():
            return edges
        for item in read_json(path).get("classes", []):
            class_id = str(item.get("id") or "")
            parent = item.get("parent_class")
            if class_id and parent:
                edges.append(
                    GraphEdge(
                        edge_id=f"OPARENT-{class_id}",
                        source=class_id,
                        target=str(parent),
                        edge_type="SUBCLASS_OF",
                        relationship="ontology_hierarchy",
                    )
                )
        return edges

    def dependency_edges(self) -> list[GraphEdge]:
        """Hard + semantic + sequential load-order dependency edges."""
        edges: list[GraphEdge] = []
        for idx, (source, target) in enumerate(ACADEMIC_HARD_DEPS, start=1):
            edges.append(
                GraphEdge(
                    edge_id=f"DEP-H-{idx:06d}",
                    source=source,
                    target=target,
                    edge_type="DEPENDS_ON",
                    relationship="hard_dependency",
                )
            )
        for idx, (source, target) in enumerate(ACADEMIC_SEMANTIC_DEPS, start=1):
            edges.append(
                GraphEdge(
                    edge_id=f"DEP-S-{idx:06d}",
                    source=source,
                    target=target,
                    edge_type="RELATED_TO",
                    relationship="semantic_dependency",
                )
            )
        record_ids = [item["record_id"] for item in PACK01_RECORDS]
        for idx in range(1, len(record_ids)):
            edges.append(
                GraphEdge(
                    edge_id=f"DEP-L-{idx:06d}",
                    source=record_ids[idx],
                    target=record_ids[idx - 1],
                    edge_type="LOADS_AFTER",
                    relationship="implementation_load_order",
                )
            )
        return edges

    def registry_edges(self) -> list[GraphEdge]:
        """Registry domain membership and namespace/object-type links."""
        edges: list[GraphEdge] = []
        for domain in REGISTRY_DOMAINS:
            edges.append(
                GraphEdge(
                    edge_id=f"REG-BELONGS-{domain}",
                    source=f"REGDOM-{domain}",
                    target="REGISTRY-ROOT",
                    edge_type="BELONGS_TO",
                    relationship="registry_domain_membership",
                )
            )

        ns_path = (
            self.project_root
            / "knowledge"
            / "registry"
            / "global_registry"
            / "namespace_registry.json"
        )
        if ns_path.is_file():
            for record in read_json(ns_path).get("records", []):
                namespace = str(record.get("namespace") or "")
                if namespace:
                    edges.append(
                        GraphEdge(
                            edge_id=f"NS-BELONGS-{namespace}",
                            source=f"NS-{namespace}",
                            target="REGISTRY-ROOT",
                            edge_type="BELONGS_TO",
                            relationship="namespace_membership",
                        )
                    )

        ot_path = (
            self.project_root
            / "knowledge"
            / "registry"
            / "global_registry"
            / "object_type_registry.json"
        )
        if ot_path.is_file():
            for record in read_json(ot_path).get("records", []):
                object_type = str(record.get("object_type") or "")
                namespace = str(record.get("namespace") or "")
                if object_type and namespace:
                    edges.append(
                        GraphEdge(
                            edge_id=f"OTYPE-NS-{object_type}",
                            source=f"OTYPE-{object_type}",
                            target=f"NS-{namespace}",
                            edge_type="IN_NAMESPACE",
                            relationship="object_type_namespace",
                        )
                    )
                if object_type:
                    edges.append(
                        GraphEdge(
                            edge_id=f"OTYPE-ROOT-{object_type}",
                            source=f"OTYPE-{object_type}",
                            target="REGISTRY-ROOT",
                            edge_type="BELONGS_TO",
                            relationship="object_type_membership",
                        )
                    )
        return edges

    def runtime_edges(self) -> list[GraphEdge]:
        """Compiler stage pipeline + runtime KR load-order edges."""
        edges: list[GraphEdge] = []
        for stage_id in RUNTIME_STAGES:
            edges.append(
                GraphEdge(
                    edge_id=f"RT-STAGE-{stage_id}",
                    source=stage_id,
                    target="RUNTIME-ROOT",
                    edge_type="BELONGS_TO",
                    relationship="runtime_stage_membership",
                )
            )
        for idx in range(1, len(RUNTIME_STAGES)):
            edges.append(
                GraphEdge(
                    edge_id=f"RT-NEXT-{idx:06d}",
                    source=RUNTIME_STAGES[idx],
                    target=RUNTIME_STAGES[idx - 1],
                    edge_type="FOLLOWS",
                    relationship="pipeline_order",
                )
            )
        record_ids = [item["record_id"] for item in PACK01_RECORDS]
        for rid in record_ids:
            edges.append(
                GraphEdge(
                    edge_id=f"RT-LOAD-{rid}",
                    source=f"RT-{rid}",
                    target="STAGE-LOAD",
                    edge_type="LOADED_BY",
                    relationship="runtime_load",
                )
            )
        for idx in range(1, len(record_ids)):
            edges.append(
                GraphEdge(
                    edge_id=f"RT-SEQ-{idx:06d}",
                    source=f"RT-{record_ids[idx]}",
                    target=f"RT-{record_ids[idx - 1]}",
                    edge_type="LOADS_AFTER",
                    relationship="runtime_sequence",
                )
            )
        return edges

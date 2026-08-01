"""Node builders for each Pack 01 graph type."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graph.constants import (
    PACK01_RECORDS,
    PACK_ID,
    REGISTRY_DOMAINS,
    RUNTIME_STAGES,
)
from graph.io_utils import read_json
from graph.models import GraphNode


class NodeBuilder:
    """Build typed nodes for academic, ontology, dependency, registry, runtime graphs."""

    def __init__(self, project_root: Path) -> None:
        """Initialize with project root for ontology/registry reads."""
        self.project_root = project_root.resolve()

    def academic_nodes(self) -> list[GraphNode]:
        """Build Pack + Knowledge Record concept nodes."""
        nodes = [
            GraphNode(
                node_id=PACK_ID,
                node_type="Pack",
                label="Pack 01 — Fundamental Theory",
                properties={"layer": "pack"},
            )
        ]
        for record in PACK01_RECORDS:
            nodes.append(
                GraphNode(
                    node_id=record["record_id"],
                    node_type="Concept",
                    label=record["canonical_name"],
                    properties={
                        "layer": record["layer"],
                        "filename": record["filename"],
                    },
                )
            )
        return nodes

    def ontology_nodes(self) -> list[GraphNode]:
        """Build ontology class nodes from ontology_classes.json."""
        path = self.project_root / "knowledge" / "ontology" / "ontology_classes.json"
        nodes: list[GraphNode] = []
        if not path.is_file():
            return nodes
        payload = read_json(path)
        for item in payload.get("classes", []):
            class_id = str(item.get("id") or "")
            if not class_id:
                continue
            nodes.append(
                GraphNode(
                    node_id=class_id,
                    node_type="OntologyClass",
                    label=str(item.get("canonical_name") or class_id),
                    properties={
                        "parent_class": item.get("parent_class"),
                        "namespace": item.get("namespace"),
                    },
                )
            )
        return nodes

    def dependency_nodes(self) -> list[GraphNode]:
        """Dependency graph reuses academic KR concept nodes."""
        return [
            GraphNode(
                node_id=record["record_id"],
                node_type="Concept",
                label=record["canonical_name"],
                properties={"layer": record["layer"]},
            )
            for record in PACK01_RECORDS
        ]

    def registry_nodes(self) -> list[GraphNode]:
        """Build registry domain, namespace, and object-type nodes."""
        nodes: list[GraphNode] = [
            GraphNode(
                node_id="REGISTRY-ROOT",
                node_type="RegistryRoot",
                label="BTE Registry Root",
            )
        ]
        for domain in REGISTRY_DOMAINS:
            nodes.append(
                GraphNode(
                    node_id=f"REGDOM-{domain}",
                    node_type="RegistryDomain",
                    label=domain,
                    properties={"domain": domain},
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
                if not namespace:
                    continue
                nodes.append(
                    GraphNode(
                        node_id=f"NS-{namespace}",
                        node_type="Namespace",
                        label=namespace,
                        properties={"prefix": record.get("prefix")},
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
                if not object_type:
                    continue
                nodes.append(
                    GraphNode(
                        node_id=f"OTYPE-{object_type}",
                        node_type="ObjectType",
                        label=object_type,
                        properties={
                            "namespace": record.get("namespace"),
                            "object_id_prefix": record.get("object_id_prefix"),
                        },
                    )
                )
        return nodes

    def runtime_nodes(self) -> list[GraphNode]:
        """Build compiler pipeline stage + KR runtime load nodes."""
        nodes = [
            GraphNode(
                node_id="RUNTIME-ROOT",
                node_type="RuntimeRoot",
                label="Pack 01 Runtime Pipeline",
            )
        ]
        for stage_id in RUNTIME_STAGES:
            nodes.append(
                GraphNode(
                    node_id=stage_id,
                    node_type="CompilerStage",
                    label=stage_id.replace("STAGE-", ""),
                    properties={"stage_id": stage_id},
                )
            )
        for record in PACK01_RECORDS:
            nodes.append(
                GraphNode(
                    node_id=f"RT-{record['record_id']}",
                    node_type="RuntimeRecord",
                    label=record["canonical_name"],
                    properties={"record_id": record["record_id"]},
                )
            )
        return nodes

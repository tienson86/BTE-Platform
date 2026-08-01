"""Checksum and statistics helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from baseline.io_utils import relative_posix, sha256_file


def build_checksums(
    project_root: Path,
    knowledge_records: list[dict[str, Any]],
    registries: list[dict[str, Any]],
    ontology_files: list[dict[str, Any]],
    generated_files: dict[str, Path],
) -> dict[str, Any]:
    """Build checksums.json payload for sources and generated artifacts."""
    entries: dict[str, str] = {}
    categories: dict[str, list[str]] = {
        "knowledge_records": [],
        "registries": [],
        "snapshots": [],
        "reports": [],
        "graphs": [],
        "other": [],
    }

    for record in knowledge_records:
        if record.get("sha256"):
            entries[record["path"]] = record["sha256"]
            categories["knowledge_records"].append(record["path"])

    for registry in registries:
        for file_entry in registry.get("files", []):
            entries[file_entry["path"]] = file_entry["sha256"]
            categories["registries"].append(file_entry["path"])

    for file_entry in ontology_files:
        if file_entry.get("sha256"):
            entries[file_entry["path"]] = file_entry["sha256"]
            categories["other"].append(file_entry["path"])

    for _name, path in sorted(generated_files.items()):
        if path.is_file():
            rel = relative_posix(path, project_root)
            entries[rel] = sha256_file(path)
            lowered = path.name.lower()
            if "snapshot" in lowered or lowered in {
                "baseline_manifest.json",
                "statistics.json",
                "checksums.json",
                "release_manifest.json",
                "release_metadata.json",
                "release_artifacts.json",
                "release_inventory.json",
                "freeze_inventory.json",
                "governance_metadata.json",
                "known_issues.json",
                "build_summary.json",
            }:
                categories["snapshots"].append(rel)
            elif lowered.endswith(".md") or "report" in lowered:
                categories["reports"].append(rel)
            elif "knowledge_graph" in lowered:
                categories["graphs"].append(rel)
            else:
                categories["other"].append(rel)

    return {
        "artifact": "checksums",
        "algorithm": "SHA256",
        "encoding": "utf-8",
        "count": len(entries),
        "categories": {
            key: {"count": len(paths), "files": sorted(paths)}
            for key, paths in sorted(categories.items())
        },
        "files": dict(sorted(entries.items())),
    }


def build_statistics(
    knowledge_records: list[dict[str, Any]],
    registries: list[dict[str, Any]],
    ontology: dict[str, Any],
    validation: dict[str, Any],
    compiler: dict[str, Any],
    dependency: dict[str, Any],
    graph: dict[str, Any],
    coverage: dict[str, Any],
) -> dict[str, Any]:
    """Build statistics.json payload for Sprint 3 release artifacts."""
    ontology_count = ontology.get("statistics", {}).get("class_count", 0)
    return {
        "artifact": "statistics",
        "knowledge_records": len(knowledge_records),
        "registry_count": len(registries),
        "ontology_count": ontology_count,
        "ontology_classes": ontology_count,
        "relationship_count": ontology.get("statistics", {}).get(
            "relationship_type_count", 0
        ),
        "rule_count": validation.get("statistics", {}).get("rule_count", 0),
        "context_count": len(graph.get("contexts", [])),
        "compiler_stages": compiler.get("statistics", {}).get("stage_count", 0),
        "validation_stages": validation.get("statistics", {}).get("stage_count", 0),
        "graph_nodes": graph.get("statistics", {}).get("node_count", 0),
        "graph_edges": graph.get("statistics", {}).get("edge_count", 0),
        "dependency_academic_edges": dependency.get("statistics", {}).get(
            "academic_edge_count", 0
        ),
        "dependency_implementation_edges": dependency.get("statistics", {}).get(
            "implementation_edge_count", 0
        ),
        "coverage": coverage,
        "compiler_statistics": {
            "stage_count": compiler.get("statistics", {}).get("stage_count", 0),
            "file_count": compiler.get("statistics", {}).get("file_count", 0),
            "pipeline_id": (compiler.get("pipeline") or {}).get("pipeline_id"),
        },
        "validation_statistics": {
            "stage_count": validation.get("statistics", {}).get("stage_count", 0),
            "rule_count": validation.get("statistics", {}).get("rule_count", 0),
            "validator_count": validation.get("statistics", {}).get(
                "validator_count", 0
            ),
            "coverage": coverage,
        },
        "graph_statistics": {
            "node_count": graph.get("statistics", {}).get("node_count", 0),
            "edge_count": graph.get("statistics", {}).get("edge_count", 0),
            "concept_nodes": graph.get("statistics", {}).get("concept_nodes", 0),
            "ontology_nodes": graph.get("statistics", {}).get("ontology_nodes", 0),
            "context_count": len(graph.get("contexts", [])),
            "mapping_count": len(graph.get("mappings", [])),
            "relationship_types": graph.get("relationships", {}).get("types", []),
        },
    }

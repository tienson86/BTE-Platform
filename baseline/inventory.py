"""Inventory discovery for Pack 01 baseline generation."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

from baseline.constants import (
    COMPILER_DATA_FILES,
    ONTOLOGY_DATA_FILES,
    PACK01_KR_INVENTORY,
    REGISTRY_DOMAINS,
    VALIDATION_DATA_FILES,
)
from baseline.io_utils import read_json, relative_posix, sha256_file
from baseline.paths import BaselinePaths

logger = logging.getLogger(__name__)

_KR_ID_RE = re.compile(r"^KR-\d{6}$")
_ID_FIELDS = (
    "id",
    "record_id",
    "stage_id",
    "pipeline_id",
    "validator_id",
    "rule_id",
    "code",
    "document_id",
)


def discover_knowledge_records(paths: BaselinePaths) -> list[dict[str, Any]]:
    """Discover Pack 01 KR files and attach checksums/metadata."""
    records: list[dict[str, Any]] = []
    for entry in PACK01_KR_INVENTORY:
        filename = entry["filename"]
        file_path = paths.records_dir / filename
        item: dict[str, Any] = {
            "record_id": entry["record_id"],
            "canonical_name": entry["canonical_name"],
            "pattern": entry["pattern"],
            "layer": entry["layer"],
            "filename": filename,
            "path": relative_posix(file_path, paths.project_root),
            "exists": file_path.is_file(),
        }
        if file_path.is_file():
            item["size_bytes"] = file_path.stat().st_size
            item["sha256"] = sha256_file(file_path)
        else:
            item["size_bytes"] = 0
            item["sha256"] = ""
            logger.warning("Missing Knowledge Record file: %s", file_path)
        records.append(item)
    return records


def discover_extra_kr_files(paths: BaselinePaths) -> list[str]:
    """Return unexpected KR-* filenames not in the canonical inventory."""
    expected = {entry["filename"] for entry in PACK01_KR_INVENTORY}
    extras: list[str] = []
    if not paths.records_dir.is_dir():
        return extras
    for path in sorted(paths.records_dir.glob("KR-*.md")):
        if path.name not in expected:
            extras.append(path.name)
    return extras


def discover_registries(paths: BaselinePaths) -> list[dict[str, Any]]:
    """Discover registry containers and compute checksums."""
    registries: list[dict[str, Any]] = []
    for domain in REGISTRY_DOMAINS:
        domain_dir = paths.registry_dir / domain
        primary = domain_dir / f"{domain}.json"
        files: list[dict[str, Any]] = []
        record_count = 0
        schema_version = "1.0.0"
        if domain_dir.is_dir():
            for json_path in sorted(domain_dir.glob("*.json")):
                checksum = sha256_file(json_path)
                payload: dict[str, Any] = {}
                try:
                    loaded = read_json(json_path)
                    if isinstance(loaded, dict):
                        payload = loaded
                except (OSError, ValueError) as exc:
                    logger.warning("Failed reading %s: %s", json_path, exc)
                count = _count_records(payload)
                if json_path.name == primary.name:
                    record_count = count
                    schema_version = str(
                        payload.get("version")
                        or payload.get("schema_version")
                        or "1.0.0"
                    )
                files.append(
                    {
                        "filename": json_path.name,
                        "path": relative_posix(json_path, paths.project_root),
                        "sha256": checksum,
                        "record_count": count,
                        "size_bytes": json_path.stat().st_size,
                    }
                )
        registries.append(
            {
                "registry_id": domain,
                "domain": domain,
                "path": relative_posix(domain_dir, paths.project_root),
                "primary_file": relative_posix(primary, paths.project_root)
                if primary.is_file()
                else "",
                "exists": domain_dir.is_dir(),
                "schema_version": schema_version,
                "record_count": record_count,
                "file_count": len(files),
                "files": files,
                "checksum": files[0]["sha256"] if files else "",
            }
        )
    return registries


def discover_ontology(paths: BaselinePaths) -> dict[str, Any]:
    """Discover ontology inventory files and extract class hierarchy."""
    files: list[dict[str, Any]] = []
    classes: list[dict[str, Any]] = []
    entity_types: list[dict[str, Any]] = []
    relationship_types: list[dict[str, Any]] = []
    semantic_levels: list[dict[str, Any]] = []
    node_types: list[dict[str, Any]] = []
    edge_types: list[dict[str, Any]] = []

    for filename in ONTOLOGY_DATA_FILES:
        path = paths.ontology_dir / filename
        entry: dict[str, Any] = {
            "filename": filename,
            "path": relative_posix(path, paths.project_root),
            "exists": path.is_file(),
        }
        if path.is_file():
            entry["sha256"] = sha256_file(path)
            entry["size_bytes"] = path.stat().st_size
            payload = read_json(path)
            if filename == "ontology_classes.json":
                classes = list(payload.get("classes", []))
            elif filename == "entity_types.json":
                entity_types = list(payload.get("entity_types", []))
            elif filename == "relationship_types.json":
                relationship_types = list(
                    payload.get("relationship_types", [])
                )
            elif filename == "semantic_levels.json":
                semantic_levels = list(payload.get("levels", []))
                if not semantic_levels:
                    semantic_levels = list(payload.get("semantic_levels", []))
            elif filename == "node_types.json":
                node_types = list(payload.get("node_types", []))
            elif filename == "edge_types.json":
                edge_types = list(payload.get("edge_types", []))
        files.append(entry)

    hierarchy = [
        {
            "id": item.get("id"),
            "canonical_name": item.get("canonical_name"),
            "parent_class": item.get("parent_class"),
        }
        for item in classes
    ]
    return {
        "files": files,
        "classes": classes,
        "hierarchy": hierarchy,
        "entity_types": entity_types,
        "relationship_types": relationship_types,
        "semantic_levels": semantic_levels,
        "node_types": node_types,
        "edge_types": edge_types,
        "statistics": {
            "class_count": len(classes),
            "entity_type_count": len(entity_types),
            "relationship_type_count": len(relationship_types),
            "semantic_level_count": len(semantic_levels),
            "node_type_count": len(node_types),
            "edge_type_count": len(edge_types),
            "file_count": len(files),
        },
    }


def discover_compiler(paths: BaselinePaths) -> dict[str, Any]:
    """Discover compiler contracts and pipeline definition."""
    files: list[dict[str, Any]] = []
    pipeline: dict[str, Any] = {}
    stages: list[dict[str, Any]] = []
    for filename in COMPILER_DATA_FILES:
        path = paths.compiler_dir / filename
        entry: dict[str, Any] = {
            "filename": filename,
            "path": relative_posix(path, paths.project_root),
            "exists": path.is_file(),
        }
        if path.is_file():
            entry["sha256"] = sha256_file(path)
            entry["size_bytes"] = path.stat().st_size
            payload = read_json(path)
            if filename == "pipeline.json":
                pipeline = payload
            elif filename == "stage_registry.json":
                stages = list(payload.get("stages", []))
        files.append(entry)
    return {
        "files": files,
        "pipeline": pipeline,
        "stages": stages,
        "statistics": {
            "file_count": len(files),
            "stage_count": len(stages)
            or len(pipeline.get("stages", [])),
        },
    }


def discover_validation(paths: BaselinePaths) -> dict[str, Any]:
    """Discover validation schemas, validators, and rules."""
    files: list[dict[str, Any]] = []
    validators: list[dict[str, Any]] = []
    rules: list[dict[str, Any]] = []
    stages: list[dict[str, Any]] = []
    severity_levels: list[dict[str, Any]] = []

    for filename in VALIDATION_DATA_FILES:
        path = paths.validation_dir / filename
        entry: dict[str, Any] = {
            "filename": filename,
            "path": relative_posix(path, paths.project_root),
            "exists": path.is_file(),
        }
        if path.is_file():
            entry["sha256"] = sha256_file(path)
            entry["size_bytes"] = path.stat().st_size
            payload = read_json(path)
            if filename == "validation_schema.json":
                stages = list(
                    payload.get("lifecycle", {}).get("stages", [])
                )
                severity_levels = list(payload.get("severity_levels", []))
            if "validator_id" in payload:
                validators.append(
                    {
                        "validator_id": payload.get("validator_id"),
                        "title": payload.get("title"),
                        "filename": filename,
                        "rule_count": len(payload.get("rules", [])),
                    }
                )
            for rule in payload.get("rules", []):
                if isinstance(rule, dict):
                    enriched = dict(rule)
                    enriched["source_file"] = filename
                    rules.append(enriched)
        files.append(entry)

    return {
        "files": files,
        "validators": validators,
        "rules": rules,
        "stages": stages,
        "severity_levels": severity_levels,
        "statistics": {
            "file_count": len(files),
            "validator_count": len(validators),
            "rule_count": len(rules),
            "stage_count": len(stages),
            "severity_level_count": len(severity_levels),
        },
    }


def discover_graph_specs(paths: BaselinePaths) -> dict[str, Any]:
    """Discover knowledge graph schema/spec files."""
    files: list[dict[str, Any]] = []
    if paths.graph_dir.is_dir():
        for path in sorted(paths.graph_dir.glob("*.json")):
            files.append(
                {
                    "filename": path.name,
                    "path": relative_posix(path, paths.project_root),
                    "sha256": sha256_file(path),
                    "size_bytes": path.stat().st_size,
                }
            )
    return {"files": files, "statistics": {"file_count": len(files)}}


def collect_ids(payload: Any, acc: list[str] | None = None) -> list[str]:
    """Recursively collect identifier-like string fields."""
    collected = acc if acc is not None else []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in _ID_FIELDS and isinstance(value, str) and value:
                collected.append(value)
            collect_ids(value, collected)
    elif isinstance(payload, list):
        for item in payload:
            collect_ids(item, collected)
    return collected


def is_kr_id(value: str) -> bool:
    """Return True when value matches KR-NNNNNN."""
    return bool(_KR_ID_RE.match(value))


def _count_records(payload: dict[str, Any]) -> int:
    records = payload.get("records")
    if isinstance(records, list):
        return len(records)
    items = payload.get("items")
    if isinstance(items, list):
        return len(items)
    return 0

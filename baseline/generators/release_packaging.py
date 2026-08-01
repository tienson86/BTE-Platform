"""Release packaging artifact generators."""

from __future__ import annotations

from typing import Any

from baseline.constants import SCHEMA_VERSION, SNAPSHOT_FILENAMES
from baseline.models import BuildContext


def generate_release_artifacts(
    context: BuildContext,
    artifact_paths: dict[str, str],
    checksums: dict[str, str],
) -> dict[str, Any]:
    """Generate release_artifacts.json."""
    artifacts = []
    for name in sorted(artifact_paths):
        artifacts.append(
            {
                "name": name,
                "path": artifact_paths[name],
                "sha256": checksums.get(name, checksums.get(artifact_paths[name], "")),
            }
        )
    return {
        "artifact": "release_artifacts",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "artifacts": artifacts,
    }


def generate_release_manifest(
    context: BuildContext,
    governance: dict[str, Any],
    statistics: dict[str, Any],
) -> dict[str, Any]:
    """Generate release_manifest.json."""
    return {
        "artifact": "release_manifest",
        "schema_version": SCHEMA_VERSION,
        "release_id": f"REL-PACK01-{context.version}",
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "channel": "freeze-candidate",
        "status": governance.get("overall_status"),
        "includes": list(SNAPSHOT_FILENAMES),
        "statistics": statistics,
        "readiness": {
            "freeze": governance.get("freeze_readiness", {}).get("ready"),
            "baseline": governance.get("baseline_readiness", {}).get("ready"),
            "compiler": governance.get("compiler_readiness", {}).get("ready"),
            "validation": governance.get("validation_readiness", {}).get("ready"),
            "release": governance.get("release_readiness", {}).get("ready"),
        },
    }


def generate_release_metadata(
    context: BuildContext,
    governance: dict[str, Any],
) -> dict[str, Any]:
    """Generate release_metadata.json."""
    return {
        "artifact": "release_metadata",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "encoding": "UTF-8",
        "deterministic": True,
        "reproducible": True,
        "immutable_sources": [
            "knowledge/bazi/01_fundamental_knowledge/records/",
            "knowledge/registry/",
            "knowledge/governance/",
        ],
        "generated_only": True,
        "governance_status": governance.get("overall_status"),
    }


def generate_release_inventory(
    context: BuildContext,
    inventories: dict[str, Any],
) -> dict[str, Any]:
    """Generate release_inventory.json."""
    return {
        "artifact": "release_inventory",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "knowledge_records": [
            {
                "record_id": item["record_id"],
                "path": item["path"],
                "sha256": item["sha256"],
            }
            for item in inventories["knowledge_records"]
        ],
        "registries": [
            {
                "registry_id": item["registry_id"],
                "path": item["path"],
                "record_count": item["record_count"],
            }
            for item in inventories["registries"]
        ],
        "ontology_files": inventories["ontology"]["files"],
        "compiler_files": inventories["compiler"]["files"],
        "validation_files": inventories["validation"]["files"],
        "graph_files": inventories["graph"]["files"],
    }


def generate_freeze_inventory(
    context: BuildContext,
    artifact_paths: dict[str, str],
    governance: dict[str, Any],
) -> dict[str, Any]:
    """Generate freeze_inventory.json."""
    return {
        "artifact": "freeze_inventory",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "freeze_ready": governance.get("freeze_readiness", {}).get("ready"),
        "frozen_artifacts": sorted(artifact_paths.keys()),
        "artifact_paths": artifact_paths,
        "policy": {
            "no_kr_modification": True,
            "no_registry_modification": True,
            "no_governance_markdown_modification": True,
            "generated_artifacts_only": True,
        },
    }

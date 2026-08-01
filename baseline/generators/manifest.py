"""Baseline manifest generator."""

from __future__ import annotations

from typing import Any

from baseline.constants import (
    PACK_CLASSIFICATION,
    PACK_ID,
    PACK_NAME,
    SCHEMA_VERSION,
)
from baseline.models import BuildContext
from baseline.paths import BaselinePaths


def generate_baseline_manifest(
    context: BuildContext,
    paths: BaselinePaths,
    inventories: dict[str, Any],
) -> dict[str, Any]:
    """Generate the top-level baseline manifest for Pack 01."""
    kr_inventory = inventories["knowledge_records"]
    registries = inventories["registries"]
    ontology = inventories["ontology"]
    compiler = inventories["compiler"]
    validation = inventories["validation"]
    graph = inventories["graph"]

    return {
        "artifact": "baseline_manifest",
        "schema_version": SCHEMA_VERSION,
        "pack": {
            "pack_id": PACK_ID,
            "name": PACK_NAME,
            "classification": PACK_CLASSIFICATION,
            "module": "01_fundamental_knowledge",
        },
        "version": context.version,
        "release": {
            "release_id": f"REL-PACK01-{context.version}",
            "channel": "freeze-candidate",
            "immutable_after_freeze": True,
        },
        "timestamp": context.timestamp,
        "project_root": paths.project_root.as_posix(),
        "kr_inventory": {
            "count": len(kr_inventory),
            "records": [
                {
                    "record_id": item["record_id"],
                    "canonical_name": item["canonical_name"],
                    "pattern": item["pattern"],
                    "layer": item["layer"],
                    "path": item["path"],
                    "exists": item["exists"],
                    "sha256": item["sha256"],
                }
                for item in kr_inventory
            ],
        },
        "registry_inventory": {
            "count": len(registries),
            "registries": [
                {
                    "registry_id": item["registry_id"],
                    "schema_version": item["schema_version"],
                    "record_count": item["record_count"],
                    "path": item["path"],
                    "exists": item["exists"],
                }
                for item in registries
            ],
        },
        "ontology_inventory": {
            "statistics": ontology["statistics"],
            "files": [
                {
                    "filename": item["filename"],
                    "path": item["path"],
                    "exists": item["exists"],
                    "sha256": item.get("sha256", ""),
                }
                for item in ontology["files"]
            ],
        },
        "compiler_inventory": {
            "statistics": compiler["statistics"],
            "files": [
                {
                    "filename": item["filename"],
                    "path": item["path"],
                    "exists": item["exists"],
                    "sha256": item.get("sha256", ""),
                }
                for item in compiler["files"]
            ],
        },
        "validation_inventory": {
            "statistics": validation["statistics"],
            "files": [
                {
                    "filename": item["filename"],
                    "path": item["path"],
                    "exists": item["exists"],
                    "sha256": item.get("sha256", ""),
                }
                for item in validation["files"]
            ],
        },
        "graph_inventory": {
            "statistics": graph["statistics"],
            "files": graph["files"],
        },
        "output": {
            "baseline_dir": paths.version_dir.as_posix(),
            "governance_generated": paths.governance_generated.as_posix(),
            "compiler_generated": paths.compiler_generated.as_posix(),
            "validation_generated": paths.validation_generated.as_posix(),
            "graph_generated": paths.graph_generated.as_posix(),
        },
    }

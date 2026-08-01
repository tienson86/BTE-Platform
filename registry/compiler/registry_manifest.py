"""Registry compiler manifest generator."""

from __future__ import annotations

from typing import Any

from registry.compiler.constants import COMPILER_VERSION, SCHEMA_VERSION
from registry.compiler.registry_loader import LoadedCatalog


def build_compiler_manifest(
    *,
    timestamp: str,
    domains: list[LoadedCatalog],
    auxiliary: list[LoadedCatalog],
    sidecars: list[LoadedCatalog],
    output_files: dict[str, str],
    statistics: dict[str, Any],
) -> dict[str, Any]:
    """Build the registry compiler manifest describing inputs and outputs."""
    return {
        "artifact": "registry_compiler_manifest",
        "schema_version": SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
        "timestamp": timestamp,
        "read_only_sources": True,
        "inputs": {
            "domain_catalogs": [
                {
                    "name": item.name,
                    "path": item.path,
                    "version": item.version,
                    "checksum": item.checksum,
                    "record_count": len(item.records),
                }
                for item in domains
            ],
            "auxiliary_catalogs": [
                {
                    "name": item.name,
                    "path": item.path,
                    "version": item.version,
                    "checksum": item.checksum,
                    "record_count": len(item.records),
                }
                for item in auxiliary
            ],
            "sidecar_indexes": [
                {
                    "name": item.name,
                    "path": item.path,
                    "checksum": item.checksum,
                    "entry_count": len(item.records),
                }
                for item in sidecars
            ],
        },
        "outputs": output_files,
        "statistics": statistics,
        "compiler_ready": True,
    }

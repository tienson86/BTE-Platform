"""Registry snapshot generator."""

from __future__ import annotations

from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.models import BuildContext


def generate_registry_snapshot(
    context: BuildContext,
    registries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate registry snapshot covering all Pack 01 registry domains."""
    entries = []
    for registry in registries:
        file_checksums = {
            item["filename"]: item["sha256"] for item in registry.get("files", [])
        }
        primary_checksum = ""
        primary_name = f"{registry['domain']}.json"
        if primary_name in file_checksums:
            primary_checksum = file_checksums[primary_name]
        elif registry.get("files"):
            primary_checksum = registry["files"][0]["sha256"]
        entries.append(
            {
                "registry_id": registry["registry_id"],
                "domain": registry["domain"],
                "schema_version": registry["schema_version"],
                "record_count": registry["record_count"],
                "checksum": primary_checksum,
                "file_checksums": file_checksums,
                "metadata": {
                    "path": registry["path"],
                    "primary_file": registry["primary_file"],
                    "exists": registry["exists"],
                    "file_count": registry["file_count"],
                },
            }
        )
    return {
        "artifact": "registry_snapshot",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "registry_count": len(entries),
        "registries": entries,
        "statistics": {
            "total_registries": len(entries),
            "total_records": sum(item["record_count"] for item in entries),
            "existing_registries": sum(
                1 for item in entries if item["metadata"]["exists"]
            ),
        },
    }

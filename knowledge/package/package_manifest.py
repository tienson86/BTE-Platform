"""Package manifest and inventory generators."""

from __future__ import annotations

from typing import Any

from knowledge.package.constants import BUILDER_VERSION, SCHEMA_VERSION


def build_package_manifest(
    *,
    pack_id: str,
    version: str,
    title: str,
    module_id: str,
    status: str,
    description: str,
    timestamp: str,
    record_ids: list[str],
    files: list[dict[str, Any]],
    formats: list[str],
    signature: dict[str, Any],
) -> dict[str, Any]:
    """Build package_manifest.json payload."""
    return {
        "artifact": "package_manifest",
        "schema_version": SCHEMA_VERSION,
        "builder_version": BUILDER_VERSION,
        "pack_id": pack_id,
        "version": version,
        "title": title,
        "module_id": module_id,
        "status": status,
        "description": description,
        "timestamp": timestamp,
        "record_ids": record_ids,
        "record_count": len(record_ids),
        "file_count": len(files),
        "formats": formats,
        "signature": signature,
        "compatible_future_packs": ["PACK_02"],
        "deterministic": True,
        "source_immutable": True,
    }


def build_package_inventory(
    *,
    pack_id: str,
    version: str,
    timestamp: str,
    files: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build package_inventory.json payload."""
    return {
        "artifact": "package_inventory",
        "schema_version": SCHEMA_VERSION,
        "pack_id": pack_id,
        "version": version,
        "timestamp": timestamp,
        "files": files,
        "count": len(files),
    }


def build_package_statistics(
    *,
    pack_id: str,
    version: str,
    timestamp: str,
    record_count: int,
    file_count: int,
    total_bytes: int,
    formats: list[str],
    optional_included: int,
    optional_missing: int,
) -> dict[str, Any]:
    """Build package_statistics.json payload."""
    return {
        "artifact": "package_statistics",
        "schema_version": SCHEMA_VERSION,
        "builder_version": BUILDER_VERSION,
        "pack_id": pack_id,
        "version": version,
        "timestamp": timestamp,
        "record_count": record_count,
        "file_count": file_count,
        "total_bytes": total_bytes,
        "formats": formats,
        "optional_artifacts_included": optional_included,
        "optional_artifacts_missing": optional_missing,
    }

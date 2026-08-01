"""Knowledge Pack package builder orchestrator."""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path
from typing import Any

from knowledge.package.constants import (
    BUILDER_VERSION,
    DEFAULT_TIMESTAMP,
    PACK_DEFINITIONS,
    SCHEMA_VERSION,
)
from knowledge.package.io_utils import (
    relative_posix,
    sha256_file,
    write_json,
)
from knowledge.package.package_exporter import PackageExporter
from knowledge.package.package_manifest import (
    build_package_inventory,
    build_package_manifest,
    build_package_statistics,
)
from knowledge.package.package_signer import PackageSigner
from knowledge.package.package_validator import PackageValidator

logger = logging.getLogger(__name__)


class PackageBuilder:
    """Build distributable Knowledge Pack packages without modifying sources."""

    def __init__(
        self,
        project_root: Path | None = None,
        *,
        timestamp: str | None = None,
    ) -> None:
        """Initialize builder."""
        self.project_root = (
            project_root.resolve()
            if project_root is not None
            else Path(__file__).resolve().parents[2]
        )
        self.timestamp = (
            timestamp
            or os.environ.get("SOURCE_DATE_EPOCH_ISO")
            or DEFAULT_TIMESTAMP
        )
        self.dist_root = self.project_root / "knowledge" / "package" / "dist"
        self.signer = PackageSigner()
        self.exporter = PackageExporter()
        self.validator = PackageValidator()

    def build(
        self,
        pack_id: str = "PACK_01",
        *,
        version: str | None = None,
    ) -> dict[str, Any]:
        """Build package directory and export .pack/.zip/.tar.gz."""
        definition = PACK_DEFINITIONS.get(pack_id)
        if definition is None:
            raise ValueError(f"Unknown pack_id: {pack_id}")

        pack_version = version or str(definition["version"])
        package_name = f"{pack_id}-{pack_version}"
        package_dir = self.dist_root / package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        content_dir = package_dir / "content"
        content_dir.mkdir(parents=True, exist_ok=True)

        files_meta: list[dict[str, Any]] = []
        checksums: dict[str, str] = {}
        optional_included = 0
        optional_missing = 0

        records_dir = self.project_root / str(definition["records_dir"])
        record_files = dict(definition.get("record_files") or {})
        for record_id in list(definition.get("record_ids") or []):
            filename = str(record_files.get(record_id) or "")
            source = records_dir / filename
            if not source.is_file():
                raise FileNotFoundError(f"Missing Knowledge Record file: {source}")
            rel = f"content/records/{filename}"
            dest = package_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Copy bytes only into package output; never modify source.
            dest.write_bytes(source.read_bytes())
            digest = sha256_file(dest)
            checksums[rel] = digest
            files_meta.append(
                {
                    "path": rel,
                    "source": relative_posix(source, self.project_root),
                    "sha256": digest,
                    "size_bytes": dest.stat().st_size,
                    "kind": "knowledge_record",
                    "record_id": record_id,
                }
            )

        for rel_source in list(definition.get("optional_artifacts") or []):
            source = self.project_root / str(rel_source)
            if not source.is_file():
                optional_missing += 1
                continue
            optional_included += 1
            rel = f"content/artifacts/{Path(rel_source).name}"
            dest = package_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(source.read_bytes())
            digest = sha256_file(dest)
            checksums[rel] = digest
            files_meta.append(
                {
                    "path": rel,
                    "source": relative_posix(source, self.project_root),
                    "sha256": digest,
                    "size_bytes": dest.stat().st_size,
                    "kind": "artifact",
                }
            )

        files_meta = sorted(files_meta, key=lambda item: item["path"])
        content_checksums = {
            item["path"]: item["sha256"]
            for item in files_meta
            if item["path"].startswith("content/")
        }
        signature = self.signer.sign_files(content_checksums)

        inventory = build_package_inventory(
            pack_id=pack_id,
            version=pack_version,
            timestamp=self.timestamp,
            files=files_meta,
        )
        statistics = build_package_statistics(
            pack_id=pack_id,
            version=pack_version,
            timestamp=self.timestamp,
            record_count=len(list(definition.get("record_ids") or [])),
            file_count=len(files_meta),
            total_bytes=sum(int(item["size_bytes"]) for item in files_meta),
            formats=["pack", "zip", "tar.gz"],
            optional_included=optional_included,
            optional_missing=optional_missing,
        )
        manifest = build_package_manifest(
            pack_id=pack_id,
            version=pack_version,
            title=str(definition["title"]),
            module_id=str(definition["module_id"]),
            status=str(definition["status"]),
            description=str(definition["description"]),
            timestamp=self.timestamp,
            record_ids=list(definition.get("record_ids") or []),
            files=files_meta,
            formats=["pack", "zip", "tar.gz"],
            signature=signature,
        )

        write_json(package_dir / "package_manifest.json", manifest)
        write_json(package_dir / "package_inventory.json", inventory)
        write_json(package_dir / "package_statistics.json", statistics)
        write_json(
            package_dir / "checksums.json",
            {
                "artifact": "checksums",
                "algorithm": "SHA256",
                "files": dict(sorted(checksums.items())),
                "count": len(checksums),
            },
        )
        write_json(package_dir / "signature.json", signature)

        # Also publish top-level generated metadata in dist/.
        write_json(self.dist_root / "package_manifest.json", manifest)
        write_json(self.dist_root / "package_inventory.json", inventory)
        write_json(self.dist_root / "package_statistics.json", statistics)

        archives = self.exporter.export_all(package_dir, self.dist_root / package_name)
        validation = self.validator.validate_directory(package_dir)
        archive_validations = {
            name: self.validator.validate_archive(path).to_dict()
            for name, path in archives.items()
        }

        summary = {
            "status": "PACKAGE_READY" if validation.ok else "PACKAGE_INVALID",
            "builder_version": BUILDER_VERSION,
            "schema_version": SCHEMA_VERSION,
            "pack_id": pack_id,
            "version": pack_version,
            "timestamp": self.timestamp,
            "package_dir": relative_posix(package_dir, self.project_root),
            "archives": {
                name: relative_posix(path, self.project_root)
                for name, path in archives.items()
            },
            "validation": validation.to_dict(),
            "archive_validations": archive_validations,
            "statistics": statistics,
        }
        write_json(self.dist_root / "package_build_summary.json", summary)
        logger.info(
            "Built package %s (%s) validation_ok=%s",
            pack_id,
            pack_version,
            validation.ok,
        )
        return summary

    def import_package(self, archive_path: Path, destination_dir: Path | None = None) -> dict[str, Any]:
        """Import a package archive and validate the extracted contents."""
        target = destination_dir or (
            self.dist_root / "imported" / archive_path.stem.replace(".tar", "")
        )
        extracted = self.exporter.import_archive(archive_path, target)
        validation = self.validator.validate_directory(extracted)
        return {
            "imported_to": relative_posix(extracted, self.project_root),
            "validation": validation.to_dict(),
        }


def build_pack(
    pack_id: str = "PACK_01",
    *,
    project_root: Path | None = None,
    version: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Convenience API to build a Knowledge Pack package."""
    return PackageBuilder(
        project_root=project_root,
        timestamp=timestamp,
    ).build(pack_id, version=version)

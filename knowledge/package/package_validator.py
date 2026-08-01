"""Package validator for built Knowledge Pack archives."""

from __future__ import annotations

import logging
import tarfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from knowledge.package.io_utils import read_json, sha256_file
from knowledge.package.package_signer import PackageSigner

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PackageValidationResult:
    """Validation outcome for a package artifact."""

    ok: bool
    package_path: str
    findings: list[dict[str, str]] = field(default_factory=list)
    statistics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation result."""
        return {
            "ok": self.ok,
            "package_path": self.package_path,
            "findings": self.findings,
            "statistics": self.statistics,
        }


class PackageValidator:
    """Validate package manifests, checksums, signatures, and archive integrity."""

    def __init__(self) -> None:
        """Initialize validator."""
        self.signer = PackageSigner()

    def validate_directory(self, package_dir: Path) -> PackageValidationResult:
        """Validate an extracted/built package directory."""
        findings: list[dict[str, str]] = []
        manifest_path = package_dir / "package_manifest.json"
        inventory_path = package_dir / "package_inventory.json"
        stats_path = package_dir / "package_statistics.json"
        checksums_path = package_dir / "checksums.json"
        signature_path = package_dir / "signature.json"

        for path in (
            manifest_path,
            inventory_path,
            stats_path,
            checksums_path,
            signature_path,
        ):
            if not path.is_file():
                findings.append(
                    {
                        "code": "MISSING_FILE",
                        "severity": "ERROR",
                        "message": f"Missing required file: {path.name}",
                    }
                )

        if findings:
            return PackageValidationResult(
                ok=False,
                package_path=str(package_dir),
                findings=findings,
            )

        manifest = read_json(manifest_path)
        inventory = read_json(inventory_path)
        checksums = read_json(checksums_path)
        signature = read_json(signature_path)

        for required in ("pack_id", "version", "record_ids", "timestamp"):
            if required not in manifest:
                findings.append(
                    {
                        "code": "MANIFEST_FIELD",
                        "severity": "ERROR",
                        "message": f"Manifest missing field: {required}",
                    }
                )

        files_map = checksums.get("files", {})
        if not isinstance(files_map, dict):
            findings.append(
                {
                    "code": "CHECKSUM_FORMAT",
                    "severity": "ERROR",
                    "message": "checksums.files must be an object",
                }
            )
            files_map = {}

        for rel, expected in sorted(files_map.items()):
            path = package_dir / rel
            if not path.is_file():
                findings.append(
                    {
                        "code": "MISSING_CONTENT",
                        "severity": "ERROR",
                        "message": f"Inventory file missing: {rel}",
                    }
                )
                continue
            actual = sha256_file(path)
            if actual != expected:
                findings.append(
                    {
                        "code": "CHECKSUM_MISMATCH",
                        "severity": "ERROR",
                        "message": f"Checksum mismatch for {rel}",
                    }
                )

        content_files = {
            rel: digest
            for rel, digest in files_map.items()
            if rel.startswith("content/")
        }
        if not self.signer.verify_payload(
            {"files": dict(sorted(content_files.items()))},
            signature,
        ):
            findings.append(
                {
                    "code": "SIGNATURE_INVALID",
                    "severity": "ERROR",
                    "message": "Package signature verification failed",
                }
            )

        inventory_count = int(inventory.get("count") or 0)
        if inventory_count != len(inventory.get("files") or []):
            findings.append(
                {
                    "code": "INVENTORY_COUNT",
                    "severity": "WARNING",
                    "message": "Inventory count does not match files list length",
                }
            )

        ok = not any(item["severity"] == "ERROR" for item in findings)
        return PackageValidationResult(
            ok=ok,
            package_path=str(package_dir),
            findings=findings,
            statistics={
                "file_count": len(files_map),
                "record_count": len(manifest.get("record_ids") or []),
                "finding_count": len(findings),
            },
        )

    def validate_archive(self, archive_path: Path) -> PackageValidationResult:
        """Validate a .zip/.pack/.tar.gz by inspecting members and required files."""
        findings: list[dict[str, str]] = []
        required = {
            "package_manifest.json",
            "package_inventory.json",
            "package_statistics.json",
            "checksums.json",
            "signature.json",
        }
        names: set[str] = set()
        try:
            if archive_path.suffix == ".gz" or archive_path.name.endswith(".tar.gz"):
                with tarfile.open(archive_path, "r:gz") as handle:
                    names = {member.name.replace("\\", "/") for member in handle.getmembers()}
            else:
                with zipfile.ZipFile(archive_path, "r") as handle:
                    names = {name.replace("\\", "/") for name in handle.namelist()}
        except (OSError, tarfile.TarError, zipfile.BadZipFile) as exc:
            findings.append(
                {
                    "code": "ARCHIVE_UNREADABLE",
                    "severity": "ERROR",
                    "message": str(exc),
                }
            )
            return PackageValidationResult(
                ok=False,
                package_path=str(archive_path),
                findings=findings,
            )

        for required_name in sorted(required):
            if required_name not in names and not any(
                name.endswith("/" + required_name) for name in names
            ):
                findings.append(
                    {
                        "code": "ARCHIVE_MISSING",
                        "severity": "ERROR",
                        "message": f"Archive missing {required_name}",
                    }
                )

        ok = not any(item["severity"] == "ERROR" for item in findings)
        return PackageValidationResult(
            ok=ok,
            package_path=str(archive_path),
            findings=findings,
            statistics={"member_count": len(names), "finding_count": len(findings)},
        )

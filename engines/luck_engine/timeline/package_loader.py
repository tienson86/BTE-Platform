"""Load the released Luck Foundation package. Read-only. No rule evaluation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from engines.luck_engine.exceptions import LuckPackageLoadError
from engines.luck_engine.timeline.constants import (
    PACKAGE_ID,
    PACKAGE_VERSION_CONSTRAINT,
    REQUIRED_SCHEMA_VERSION,
)
from engines.luck_engine.timeline.validation import validate_version_compatibility


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def parse_semver(value: str) -> tuple[int, int, int]:
    """Parse a dotted major.minor.patch version string."""
    parts = value.split(".")
    if len(parts) < 3:
        raise ValueError(f"invalid_semver:{value}")
    try:
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError as exc:
        raise ValueError(f"invalid_semver:{value}") from exc


def satisfies_version_constraint(version: str, constraint: str) -> bool:
    """Return True when version satisfies a simple SemVer constraint."""
    version_tuple = parse_semver(version)
    text = constraint.strip()
    if text.startswith("^"):
        base = parse_semver(text[1:])
        return version_tuple >= base and version_tuple[0] == base[0]
    if text.startswith(">="):
        return version_tuple >= parse_semver(text[2:].strip())
    if text.startswith("=="):
        return version_tuple == parse_semver(text[2:].strip())
    return version_tuple == parse_semver(text)


@dataclass(frozen=True, slots=True)
class LoadedLuckPackage:
    """Immutable snapshot of the Luck Foundation package identity."""

    package_id: str
    package_name: str
    package_type: str
    package_version: str
    schema_version: str
    status: str
    checksum: str | None
    root: Path
    published_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    manifest: Mapping[str, Any]
    identity: Mapping[str, Any]


class LuckPackageLoader:
    """Admit the released Luck Timeline Foundation package."""

    def __init__(self, package_root: Path | None = None) -> None:
        """Default root is knowledge/packages/luck/foundation."""
        self.package_root = package_root or (
            _repo_root() / "knowledge" / "packages" / "luck" / "foundation"
        )

    def load(
        self,
        *,
        expected_package_id: str = PACKAGE_ID,
        version_constraint: str = PACKAGE_VERSION_CONSTRAINT,
    ) -> LoadedLuckPackage:
        """Load and admit a released luck foundation package."""
        root = self.package_root
        identity_path = root / "PACKAGE.json"
        if not identity_path.is_file():
            raise LuckPackageLoadError(f"package_not_found:{root}")
        identity = json.loads(identity_path.read_text(encoding="utf-8"))
        manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        if identity.get("package_id") != expected_package_id:
            raise LuckPackageLoadError(f"unexpected_package_id:{identity.get('package_id')}")
        if identity.get("status") != "released":
            raise LuckPackageLoadError(f"package_not_released:{identity.get('status')}")
        schema_version = str(identity.get("schema_version") or "")
        package_version = str(identity.get("package_version") or "")
        try:
            validate_version_compatibility(
                timeline_version="1.0.0",
                schema_version=schema_version or REQUIRED_SCHEMA_VERSION,
            )
        except Exception as exc:
            raise LuckPackageLoadError(str(exc)) from exc
        if schema_version != REQUIRED_SCHEMA_VERSION:
            raise LuckPackageLoadError(f"incompatible_schema_version:{schema_version}")
        try:
            compatible = satisfies_version_constraint(package_version, version_constraint)
        except ValueError as exc:
            raise LuckPackageLoadError(str(exc)) from exc
        if not compatible:
            raise LuckPackageLoadError(f"incompatible_package_version:{package_version}")
        inputs_path = root / "assets" / "published_inputs.json"
        outputs_path = root / "assets" / "published_outputs.json"
        if not inputs_path.is_file() or not outputs_path.is_file():
            raise LuckPackageLoadError("missing_published_contracts")
        inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
        outputs = json.loads(outputs_path.read_text(encoding="utf-8"))
        checksum = identity.get("checksum", {}).get("value")
        return LoadedLuckPackage(
            package_id=str(identity["package_id"]),
            package_name=str(identity["package_name"]),
            package_type=str(identity["package_type"]),
            package_version=package_version,
            schema_version=schema_version,
            status=str(identity["status"]),
            checksum=str(checksum) if checksum else None,
            root=root,
            published_inputs=tuple(item["name"] for item in inputs["inputs"]),
            published_outputs=tuple(item["name"] for item in outputs["outputs"]),
            manifest=manifest,
            identity=identity,
        )

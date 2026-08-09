"""Load released Knowledge Packages for Analysis Engine orchestration."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from engines.analysis_engine.exceptions.pipeline_error import (
    IncompatiblePackageError,
    PackageLoadError,
)

logger = logging.getLogger(__name__)

REQUIRED_SCHEMA_VERSION = "2.0.0"
DEFAULT_PACKAGE_IDS: tuple[str, ...] = (
    "bz_01_strength_core",
    "bz_02_seasonal_core",
    "bz_03_temperature_core",
)
_PACKAGE_RELATIVE_ROOTS: dict[str, tuple[str, ...]] = {
    "bz_01_strength_core": ("knowledge", "packages", "strength", "core"),
    "bz_02_seasonal_core": ("knowledge", "packages", "seasonal", "core"),
    "bz_03_temperature_core": ("knowledge", "packages", "temperature", "core"),
    "bz_04_pattern_core": ("knowledge", "packages", "pattern", "core"),
    "bz_05_pattern_evaluation": ("knowledge", "packages", "pattern", "evaluation"),
    "bz_06_useful_god_foundation": (
        "knowledge",
        "packages",
        "useful_god",
        "foundation",
    ),
}


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


@dataclass(slots=True)
class LoadedPackage:
    """Immutable snapshot of a released knowledge package."""

    package_id: str
    package_name: str
    package_type: str
    package_version: str
    schema_version: str
    knowledge_version: str
    compatibility_version: str
    language: str
    status: str
    checksum: str | None
    description: str
    root: Path
    manifest: Mapping[str, Any] = field(repr=False)
    metadata: Mapping[str, Any] = field(repr=False)
    rule_ids: tuple[str, ...] = ()

    @property
    def rule_count(self) -> int:
        """Return the number of exported rule identifiers."""
        return len(self.rule_ids)


class PackageLoader:
    """Load and admit released Strength, Seasonal, and Temperature packages."""

    def __init__(
        self,
        *,
        knowledge_root: Path | None = None,
        package_roots: Mapping[str, Path] | None = None,
        required_schema_version: str = REQUIRED_SCHEMA_VERSION,
    ) -> None:
        """Initialize loader search paths."""
        self._knowledge_root = knowledge_root or (_repo_root() / "knowledge")
        self._package_roots = {
            package_id: Path(path) for package_id, path in (package_roots or {}).items()
        }
        self._required_schema_version = required_schema_version

    def default_root_for(self, package_id: str) -> Path:
        """Return the default on-disk root for a known package id."""
        if package_id in self._package_roots:
            return self._package_roots[package_id]
        relative = _PACKAGE_RELATIVE_ROOTS.get(package_id)
        if relative is None:
            raise PackageLoadError(f"unknown_package_id:{package_id}")
        if self._knowledge_root.name == "knowledge":
            return self._knowledge_root.joinpath(*relative[1:])
        return self._knowledge_root.joinpath(*relative)

    def load(
        self,
        package_id: str,
        *,
        version_constraint: str | None = None,
    ) -> LoadedPackage:
        """Load one released package and reject incompatible versions."""
        root = self.default_root_for(package_id)
        package_path = root / "PACKAGE.json"
        manifest_path = root / "MANIFEST.json"
        if not package_path.is_file() or not manifest_path.is_file():
            raise PackageLoadError(f"package_not_found:{package_id}:{root}")

        package_data = _read_json(package_path)
        manifest_data = _read_json(manifest_path)
        metadata_path = root / "metadata" / "package_metadata.json"
        metadata = _read_json(metadata_path) if metadata_path.is_file() else {}

        loaded = self._materialize(
            package_id=package_id,
            root=root,
            package_data=package_data,
            manifest_data=manifest_data,
            metadata=metadata,
        )
        self._assert_admissible(loaded, version_constraint=version_constraint)
        logger.debug(
            "package_loaded",
            extra={
                "package_id": loaded.package_id,
                "package_version": loaded.package_version,
            },
        )
        return loaded

    def load_core_packages(
        self,
        *,
        version_constraints: Mapping[str, str] | None = None,
    ) -> dict[str, LoadedPackage]:
        """Load Strength, Seasonal, and Temperature core packages."""
        constraints = dict(version_constraints or {})
        loaded: dict[str, LoadedPackage] = {}
        for package_id in DEFAULT_PACKAGE_IDS:
            loaded[package_id] = self.load(
                package_id,
                version_constraint=constraints.get(package_id),
            )
        self.assert_optional_dependencies(loaded)
        return loaded

    def _materialize(
        self,
        *,
        package_id: str,
        root: Path,
        package_data: Mapping[str, Any],
        manifest_data: Mapping[str, Any],
        metadata: Mapping[str, Any],
    ) -> LoadedPackage:
        declared_id = str(package_data.get("package_id", ""))
        if declared_id != package_id:
            raise PackageLoadError(
                f"package_id_mismatch:expected={package_id}:actual={declared_id}"
            )
        compatibility = package_data.get("compatibility") or {}
        checksum = package_data.get("checksum") or {}
        return LoadedPackage(
            package_id=declared_id,
            package_name=str(package_data.get("package_name", "")),
            package_type=str(package_data.get("package_type", "")),
            package_version=str(package_data.get("package_version", "")),
            schema_version=str(package_data.get("schema_version", "")),
            knowledge_version=str(package_data.get("knowledge_version", "")),
            compatibility_version=str(compatibility.get("compatibility_version", "")),
            language=str(package_data.get("language", "")),
            status=str(package_data.get("status", "")),
            checksum=checksum.get("value"),
            description=str(package_data.get("description", "")),
            root=root,
            manifest=dict(manifest_data),
            metadata=dict(metadata),
            rule_ids=_collect_rule_ids(root),
        )

    def _assert_admissible(
        self,
        package: LoadedPackage,
        *,
        version_constraint: str | None,
    ) -> None:
        if package.status != "released":
            raise IncompatiblePackageError(
                f"package_not_released:{package.package_id}:{package.status}"
            )
        if package.schema_version != self._required_schema_version:
            raise IncompatiblePackageError(
                f"schema_incompatible:{package.package_id}:{package.schema_version}"
            )
        if version_constraint and not satisfies_version_constraint(
            package.package_version,
            version_constraint,
        ):
            raise IncompatiblePackageError(
                f"version_incompatible:{package.package_id}:"
                f"{package.package_version}:{version_constraint}"
            )

    def assert_optional_dependencies(
        self,
        loaded: Mapping[str, LoadedPackage],
    ) -> None:
        by_id = {item.package_id: item for item in loaded.values()}
        for package in loaded.values():
            dep_path = package.root / "DEPENDENCIES.json"
            if not dep_path.is_file():
                continue
            dependencies = _read_json(dep_path)
            for entry in dependencies.get("optional") or []:
                dep_id = str(entry.get("package_id", ""))
                constraint = str(entry.get("version_constraint", ""))
                present = by_id.get(dep_id)
                if present is None or not constraint:
                    continue
                if not satisfies_version_constraint(present.package_version, constraint):
                    raise IncompatiblePackageError(
                        f"optional_dependency_incompatible:{dep_id}:"
                        f"{present.package_version}"
                    )


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageLoadError(f"invalid_json:{path}") from exc
    if not isinstance(payload, dict):
        raise PackageLoadError(f"invalid_json_object:{path}")
    return payload


def _collect_rule_ids(root: Path) -> tuple[str, ...]:
    ids: list[str] = []
    rules_dir = root / "rules"
    if not rules_dir.is_dir():
        return ()
    for path in sorted(rules_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        objects = payload.get("objects") if isinstance(payload, dict) else None
        if not isinstance(objects, list):
            continue
        for item in objects:
            if isinstance(item, dict) and item.get("id"):
                ids.append(str(item["id"]))
    return tuple(ids)

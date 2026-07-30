"""Registry JSON, schema, consistency, and duplicate validation."""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import Any

from services.registry_checksum import verify_checksum
from services.registry_constants import (
    ALLOWED_STATUSES,
    CONTAINER_SCHEMA_RELATIVE,
    NAMESPACE_REGISTRY_RELATIVE,
    OBJECT_TYPE_REGISTRY_RELATIVE,
    RECORD_SCHEMA_RELATIVE,
    REGISTRY_ID_PATTERN,
    SEMVER_PATTERN,
)
from services.registry_exceptions import RegistrySchemaError
from services.registry_loader import RegistryLoader
from services.registry_models import RegistryCatalog, ValidationIssue, ValidationResult

logger = logging.getLogger(__name__)


class RegistryValidator:
    """Validate registry catalogs for JSON, schema, consistency, and duplicates."""

    def __init__(self, loader: RegistryLoader) -> None:
        """Initialize validator with a registry loader."""
        self.loader = loader
        self._record_schema: dict[str, Any] | None = None
        self._container_schema: dict[str, Any] | None = None
        self._validator_cls: Any | None = None
        self._id_re = re.compile(REGISTRY_ID_PATTERN)
        self._semver_re = re.compile(SEMVER_PATTERN)

    def validate_all(
        self,
        *,
        include_samples: bool = False,
        check_schema: bool = True,
        check_duplicates: bool = True,
        check_consistency: bool = True,
    ) -> ValidationResult:
        """Run full validation across all domain catalogs."""
        result = ValidationResult(ok=True)
        catalogs = self.loader.load_all_catalogs()
        result.catalogs_checked = len(catalogs)

        for catalog in catalogs:
            self._validate_catalog_structure(catalog, result)
            if check_schema:
                self._validate_catalog_schema(catalog, result)
            for index, record in enumerate(catalog.records):
                result.records_checked += 1
                if check_schema:
                    self._validate_record_schema(
                        catalog,
                        record,
                        index,
                        result,
                    )
                self._validate_record_fields(catalog, record, index, result)

        if check_duplicates:
            self._detect_duplicates(catalogs, result)

        if check_consistency:
            self._check_consistency(catalogs, result)

        if include_samples:
            self._validate_sample_templates(result)

        result.ok = not result.errors
        return result

    def validate_json_files(self) -> ValidationResult:
        """Validate that catalog and index JSON files parse as objects."""
        result = ValidationResult(ok=True)
        paths = list(self.loader.list_catalog_paths())
        paths.extend(
            [
                self.loader.registry_root / NAMESPACE_REGISTRY_RELATIVE,
                self.loader.registry_root / OBJECT_TYPE_REGISTRY_RELATIVE,
                self.loader.registry_root
                / "global_registry"
                / "registry_statistics.json",
            ]
        )
        for path in paths:
            if not path.exists():
                result.issues.append(
                    ValidationIssue(
                        severity="error",
                        code="missing_file",
                        message=f"Missing JSON file: {path}",
                        path=str(path),
                    )
                )
                continue
            try:
                self.loader._read_json(path)  # noqa: SLF001 - shared parse
                result.catalogs_checked += 1
            except Exception as exc:  # noqa: BLE001 - collect all parse failures
                result.issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_json",
                        message=str(exc),
                        path=str(path),
                    )
                )
        result.ok = not result.errors
        return result

    def detect_duplicates(
        self,
        catalogs: list[RegistryCatalog] | None = None,
    ) -> list[ValidationIssue]:
        """Detect duplicate registry_id, object_id, and uri values."""
        result = ValidationResult(ok=True)
        self._detect_duplicates(
            catalogs or self.loader.load_all_catalogs(),
            result,
        )
        return result.issues

    def _load_jsonschema_validator(self) -> Any:
        if self._validator_cls is not None:
            return self._validator_cls
        try:
            from jsonschema import Draft202012Validator
        except ImportError as exc:
            raise RegistrySchemaError(
                "jsonschema is required for schema validation. "
                "Install with: pip install jsonschema"
            ) from exc
        self._validator_cls = Draft202012Validator
        return self._validator_cls

    def _get_record_schema(self) -> dict[str, Any]:
        if self._record_schema is None:
            path = self.loader.schema_path(RECORD_SCHEMA_RELATIVE)
            self._record_schema = self.loader._read_json(path)  # noqa: SLF001
        return self._record_schema

    def _get_container_schema(self) -> dict[str, Any]:
        if self._container_schema is None:
            path = self.loader.schema_path(CONTAINER_SCHEMA_RELATIVE)
            self._container_schema = self.loader._read_json(path)  # noqa: SLF001
        return self._container_schema

    def _validate_catalog_structure(
        self,
        catalog: RegistryCatalog,
        result: ValidationResult,
    ) -> None:
        if not catalog.version or not self._semver_re.match(catalog.version):
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="invalid_version",
                    message="Catalog version must be semver MAJOR.MINOR.PATCH",
                    path=catalog.path,
                )
            )
        if "records" not in catalog.raw:
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="missing_records",
                    message="Catalog missing required 'records' array",
                    path=catalog.path,
                )
            )

    def _validate_catalog_schema(
        self,
        catalog: RegistryCatalog,
        result: ValidationResult,
    ) -> None:
        validator_cls = self._load_jsonschema_validator()
        schema = self._get_container_schema()
        # Avoid resolving remote $ref for records during container check.
        local_schema = dict(schema)
        props = dict(local_schema.get("properties", {}))
        records_schema = dict(props.get("records", {"type": "array"}))
        records_schema["items"] = {"type": "object"}
        props["records"] = records_schema
        local_schema["properties"] = props

        validator = validator_cls(local_schema)
        for error in validator.iter_errors(catalog.raw):
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="container_schema",
                    message=error.message,
                    path=catalog.path,
                )
            )

    def _validate_record_schema(
        self,
        catalog: RegistryCatalog,
        record: dict[str, Any],
        index: int,
        result: ValidationResult,
    ) -> None:
        validator_cls = self._load_jsonschema_validator()
        schema = self._get_record_schema()
        validator = validator_cls(schema)
        registry_id = (
            str(record.get("identity", {}).get("registry_id", ""))
            if isinstance(record.get("identity"), dict)
            else ""
        )
        for error in validator.iter_errors(record):
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="record_schema",
                    message=f"records[{index}]: {error.message}",
                    path=catalog.path,
                    registry_id=registry_id,
                )
            )

    def _validate_record_fields(
        self,
        catalog: RegistryCatalog,
        record: dict[str, Any],
        index: int,
        result: ValidationResult,
    ) -> None:
        identity = record.get("identity")
        metadata = record.get("metadata")
        obj = record.get("object")
        if not isinstance(identity, dict):
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="missing_identity",
                    message=f"records[{index}] missing identity object",
                    path=catalog.path,
                )
            )
            return

        registry_id = str(identity.get("registry_id", ""))
        if registry_id and not self._id_re.match(registry_id):
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="invalid_registry_id",
                    message=f"Invalid registry_id: {registry_id}",
                    path=catalog.path,
                    registry_id=registry_id,
                )
            )

        if isinstance(metadata, dict):
            status = str(metadata.get("status", ""))
            if status and status not in ALLOWED_STATUSES:
                result.issues.append(
                    ValidationIssue(
                        severity="error",
                        code="invalid_status",
                        message=f"Invalid status: {status}",
                        path=catalog.path,
                        registry_id=registry_id,
                    )
                )

        if isinstance(obj, dict):
            declared = str(obj.get("checksum", ""))
            if declared:
                if not verify_checksum(declared, payload=record):
                    # Record checksum often excludes itself; warn only.
                    result.issues.append(
                        ValidationIssue(
                            severity="warning",
                            code="checksum_mismatch",
                            message=(
                                "Declared object.checksum does not match "
                                "full-record digest"
                            ),
                            path=catalog.path,
                            registry_id=registry_id,
                        )
                    )

    def _detect_duplicates(
        self,
        catalogs: list[RegistryCatalog],
        result: ValidationResult,
    ) -> None:
        """Optimized O(n) duplicate detection using hash sets/maps."""
        registry_ids: dict[str, str] = {}
        object_ids: dict[str, str] = {}
        uris: dict[str, str] = {}

        for catalog in catalogs:
            for record in catalog.records:
                identity = record.get("identity", {})
                obj = record.get("object", {})
                if not isinstance(identity, dict):
                    continue
                registry_id = str(identity.get("registry_id", "")).strip()
                object_id = str(identity.get("object_id", "")).strip()
                uri = (
                    str(obj.get("uri", "")).strip()
                    if isinstance(obj, dict)
                    else ""
                )

                if registry_id:
                    prior = registry_ids.get(registry_id)
                    if prior:
                        result.issues.append(
                            ValidationIssue(
                                severity="error",
                                code="duplicate_registry_id",
                                message=(
                                    f"Duplicate registry_id {registry_id} "
                                    f"in {catalog.path} (also {prior})"
                                ),
                                path=catalog.path,
                                registry_id=registry_id,
                            )
                        )
                    else:
                        registry_ids[registry_id] = catalog.path

                if object_id:
                    prior = object_ids.get(object_id)
                    if prior:
                        result.issues.append(
                            ValidationIssue(
                                severity="error",
                                code="duplicate_object_id",
                                message=(
                                    f"Duplicate object_id {object_id} "
                                    f"in {catalog.path} (also {prior})"
                                ),
                                path=catalog.path,
                                registry_id=registry_id,
                            )
                        )
                    else:
                        object_ids[object_id] = catalog.path

                if uri:
                    prior = uris.get(uri)
                    if prior:
                        result.issues.append(
                            ValidationIssue(
                                severity="error",
                                code="duplicate_uri",
                                message=(
                                    f"Duplicate URI {uri} in {catalog.path} "
                                    f"(also {prior})"
                                ),
                                path=catalog.path,
                                registry_id=registry_id,
                            )
                        )
                    else:
                        uris[uri] = catalog.path

    def _check_consistency(
        self,
        catalogs: list[RegistryCatalog],
        result: ValidationResult,
    ) -> None:
        known_ids = {
            str(record.get("identity", {}).get("registry_id", ""))
            for _, record in self.loader.iter_records()
            if isinstance(record.get("identity"), dict)
        }
        known_ids.discard("")

        namespaces = self._load_known_namespaces()
        object_types = self._load_known_object_types()
        index = self.loader.load_registry_index()
        indexed_names = {
            str(entry.get("registry_name", ""))
            for entry in index.get("entries", [])
            if isinstance(entry, dict)
        }

        for catalog in catalogs:
            if indexed_names and catalog.name not in indexed_names:
                result.issues.append(
                    ValidationIssue(
                        severity="warning",
                        code="missing_from_index",
                        message=(
                            f"Catalog {catalog.name} not listed in "
                            "registry_index.json"
                        ),
                        path=catalog.path,
                    )
                )

            for record in catalog.records:
                identity = record.get("identity", {})
                obj = record.get("object", {})
                if not isinstance(identity, dict):
                    continue
                registry_id = str(identity.get("registry_id", ""))
                namespace = str(identity.get("namespace", ""))
                if namespaces and namespace and namespace not in namespaces:
                    result.issues.append(
                        ValidationIssue(
                            severity="warning",
                            code="unknown_namespace",
                            message=f"Unknown namespace '{namespace}'",
                            path=catalog.path,
                            registry_id=registry_id,
                        )
                    )

                if isinstance(obj, dict):
                    object_type = str(obj.get("object_type", ""))
                    if (
                        object_types
                        and object_type
                        and object_type not in object_types
                    ):
                        result.issues.append(
                            ValidationIssue(
                                severity="warning",
                                code="unknown_object_type",
                                message=f"Unknown object_type '{object_type}'",
                                path=catalog.path,
                                registry_id=registry_id,
                            )
                        )

                deps = record.get("dependencies", [])
                if not isinstance(deps, list):
                    continue
                for dep in deps:
                    dep_id = str(dep)
                    if dep_id and dep_id not in known_ids:
                        result.issues.append(
                            ValidationIssue(
                                severity="error",
                                code="broken_dependency",
                                message=f"Dependency not found: {dep_id}",
                                path=catalog.path,
                                registry_id=registry_id,
                            )
                        )

                # Circular dependency (A->B->A) detection for direct pairs.
                # Full graph cycle detection is deferred (TODO).

        # Detect simple mutual dependencies.
        graph: dict[str, set[str]] = defaultdict(set)
        for catalog in catalogs:
            for record in catalog.records:
                identity = record.get("identity", {})
                if not isinstance(identity, dict):
                    continue
                src = str(identity.get("registry_id", ""))
                deps = record.get("dependencies", [])
                if not src or not isinstance(deps, list):
                    continue
                for dep in deps:
                    graph[src].add(str(dep))

        for src, deps in graph.items():
            for dep in deps:
                if src in graph.get(dep, set()):
                    result.issues.append(
                        ValidationIssue(
                            severity="error",
                            code="circular_dependency",
                            message=f"Circular dependency between {src} and {dep}",
                            registry_id=src,
                        )
                    )

    def _load_known_namespaces(self) -> set[str]:
        path = self.loader.registry_root / NAMESPACE_REGISTRY_RELATIVE
        if not path.exists():
            return set()
        data = self.loader._read_json(path)  # noqa: SLF001
        records = data.get("records", [])
        return {
            str(item.get("namespace", ""))
            for item in records
            if isinstance(item, dict) and item.get("namespace")
        }

    def _load_known_object_types(self) -> set[str]:
        path = self.loader.registry_root / OBJECT_TYPE_REGISTRY_RELATIVE
        if not path.exists():
            return set()
        data = self.loader._read_json(path)  # noqa: SLF001
        records = data.get("records", [])
        return {
            str(item.get("object_type", ""))
            for item in records
            if isinstance(item, dict) and item.get("object_type")
        }

    def _validate_sample_templates(self, result: ValidationResult) -> None:
        """Sample templates are structural only; do not fail publication checks."""
        sample = (
            self.loader.registry_root / "samples" / "empty_registry_record.json"
        )
        if not sample.exists():
            result.issues.append(
                ValidationIssue(
                    severity="warning",
                    code="missing_sample",
                    message="Empty sample record file is missing",
                    path=str(sample),
                )
            )
            return
        try:
            payload = self.loader._read_json(sample)  # noqa: SLF001
        except Exception as exc:  # noqa: BLE001
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="invalid_sample_json",
                    message=str(exc),
                    path=str(sample),
                )
            )
            return
        required = {
            "identity",
            "metadata",
            "object",
            "classification",
            "dependencies",
            "validation",
            "governance",
            "traceability",
            "revision_history",
        }
        missing = sorted(required - set(payload.keys()))
        if missing:
            result.issues.append(
                ValidationIssue(
                    severity="error",
                    code="sample_missing_keys",
                    message=f"Sample missing keys: {', '.join(missing)}",
                    path=str(sample),
                )
            )

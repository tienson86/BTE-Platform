"""Import registry catalogs from JSON files or bundles."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from services.registry_exceptions import RegistryIOError
from services.registry_loader import RegistryLoader
from services.registry_validator import RegistryValidator

logger = logging.getLogger(__name__)


class RegistryImporter:
    """Import registry catalogs with optional validation."""

    def __init__(
        self,
        loader: RegistryLoader,
        validator: RegistryValidator | None = None,
    ) -> None:
        """Initialize importer."""
        self.loader = loader
        self.validator = validator or RegistryValidator(loader)

    def import_catalog_file(
        self,
        source: str | Path,
        *,
        registry_name: str | None = None,
        dry_run: bool = False,
        validate: bool = True,
    ) -> Path:
        """Import one catalog JSON into the registry root."""
        source_path = Path(source)
        payload = self._read_json(source_path)
        name = registry_name or str(payload.get("registry_name") or source_path.stem)
        if "records" not in payload:
            raise RegistryIOError("Imported catalog must include 'records'")

        if validate:
            self._validate_payload(name, payload)

        destination = self._destination_for(name)
        if dry_run:
            logger.info("Dry-run import for %s -> %s", name, destination)
            return destination

        self._write_json(destination, payload)
        self.loader.clear_cache()
        logger.info("Imported catalog %s to %s", name, destination)
        return destination

    def import_bundle(
        self,
        source: str | Path,
        *,
        dry_run: bool = False,
        validate: bool = True,
    ) -> list[Path]:
        """Import a bundle produced by RegistryExporter.export_bundle."""
        payload = self._read_json(Path(source))
        catalogs = payload.get("catalogs")
        if not isinstance(catalogs, dict):
            raise RegistryIOError("Bundle missing 'catalogs' object")

        written: list[Path] = []
        for name, catalog_payload in catalogs.items():
            if not isinstance(catalog_payload, dict):
                raise RegistryIOError(f"Invalid catalog payload for {name}")
            if validate:
                self._validate_payload(str(name), catalog_payload)
            destination = self._destination_for(str(name))
            if not dry_run:
                self._write_json(destination, catalog_payload)
            written.append(destination)

        if not dry_run:
            self.loader.clear_cache()
        return written

    def _destination_for(self, registry_name: str) -> Path:
        folder = self.loader.registry_root / registry_name
        return folder / f"{registry_name}.json"

    def _validate_payload(self, name: str, payload: dict[str, Any]) -> None:
        from services.registry_models import RegistryCatalog, ValidationResult

        catalog = RegistryCatalog(
            name=name,
            path=f"<import:{name}>",
            version=str(payload.get("version", "")),
            prefix=str(payload.get("registry_prefix", "")),
            description=str(payload.get("description", "")),
            records=[
                item
                for item in payload.get("records", [])
                if isinstance(item, dict)
            ],
            raw=payload,
            checksum="",
        )
        result = ValidationResult(ok=True)
        self.validator._validate_catalog_structure(catalog, result)  # noqa: SLF001
        self.validator._validate_catalog_schema(catalog, result)  # noqa: SLF001
        for index, record in enumerate(catalog.records):
            self.validator._validate_record_schema(  # noqa: SLF001
                catalog,
                record,
                index,
                result,
            )
            self.validator._validate_record_fields(  # noqa: SLF001
                catalog,
                record,
                index,
                result,
            )
        if result.errors:
            messages = "; ".join(issue.message for issue in result.errors[:5])
            raise RegistryIOError(
                f"Import validation failed for {name}: {messages}"
            )

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise RegistryIOError(f"Import source not found: {path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RegistryIOError(f"Invalid JSON in {path}: {exc}") from exc
        except OSError as exc:
            raise RegistryIOError(f"Unable to read {path}: {exc}") from exc
        if not isinstance(payload, dict):
            raise RegistryIOError(f"Import JSON root must be object: {path}")
        return payload

    def _write_json(self, path: Path, payload: dict[str, Any]) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            raise RegistryIOError(f"Failed to write {path}: {exc}") from exc

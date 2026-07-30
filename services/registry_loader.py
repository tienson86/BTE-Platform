"""Lazy-loading Registry catalog loader with mtime cache."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from services.registry_checksum import checksum_file, checksum_payload
from services.registry_constants import (
    DEFAULT_REGISTRY_ROOT_RELATIVE,
    DOMAIN_REGISTRY_FILES,
    REGISTRY_INDEX_RELATIVE,
)
from services.registry_exceptions import RegistryLoadError
from services.registry_models import RegistryCatalog

logger = logging.getLogger(__name__)


class RegistryLoader:
    """Load Registry JSON catalogs with lazy loading and cache."""

    def __init__(
        self,
        registry_root: str | Path | None = None,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        """Initialize loader with optional explicit roots."""
        if registry_root is not None:
            self.registry_root = Path(registry_root).resolve()
            self.project_root = (
                Path(project_root).resolve()
                if project_root is not None
                else self.registry_root.parent.parent
            )
        else:
            self.project_root = (
                Path(project_root).resolve()
                if project_root is not None
                else Path.cwd().resolve()
            )
            self.registry_root = (
                self.project_root / DEFAULT_REGISTRY_ROOT_RELATIVE
            ).resolve()

        self._cache: dict[str, tuple[float, RegistryCatalog]] = {}
        self._index_cache: tuple[float, dict[str, Any]] | None = None

    def clear_cache(self) -> None:
        """Clear all cached catalogs and index data."""
        self._cache.clear()
        self._index_cache = None

    def list_catalog_paths(self) -> list[Path]:
        """Return catalog paths declared by registry_index or defaults."""
        index = self.load_registry_index()
        entries = index.get("entries", [])
        paths: list[Path] = []
        if isinstance(entries, list) and entries:
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                rel = str(entry.get("path", "")).replace("\\", "/")
                if not rel:
                    continue
                paths.append((self.registry_root / rel).resolve())
            return paths

        return [
            (self.registry_root / rel).resolve() for rel in DOMAIN_REGISTRY_FILES
        ]

    def load_registry_index(self) -> dict[str, Any]:
        """Load global registry_index.json with lazy cache."""
        path = self.registry_root / REGISTRY_INDEX_RELATIVE
        if not path.exists():
            return {"version": "1.0.0", "entries": []}

        mtime = path.stat().st_mtime
        if self._index_cache is not None and self._index_cache[0] == mtime:
            return self._index_cache[1]

        data = self._read_json(path)
        self._index_cache = (mtime, data)
        return data

    def load_catalog(self, path: str | Path) -> RegistryCatalog:
        """Load one catalog file, using cache when mtime is unchanged."""
        catalog_path = self._resolve_catalog_path(path)
        cache_key = str(catalog_path)
        mtime = catalog_path.stat().st_mtime
        cached = self._cache.get(cache_key)
        if cached is not None and cached[0] == mtime:
            return cached[1]

        raw = self._read_json(catalog_path)
        catalog = self._to_catalog(catalog_path, raw)
        self._cache[cache_key] = (mtime, catalog)
        logger.debug("Loaded registry catalog %s", catalog_path)
        return catalog

    def load_all_catalogs(self) -> list[RegistryCatalog]:
        """Lazy-load every known domain catalog."""
        catalogs: list[RegistryCatalog] = []
        for path in self.list_catalog_paths():
            if not path.exists():
                logger.warning("Missing registry catalog: %s", path)
                continue
            catalogs.append(self.load_catalog(path))
        return catalogs

    def iter_records(self) -> list[tuple[RegistryCatalog, dict[str, Any]]]:
        """Return all records paired with their owning catalog."""
        pairs: list[tuple[RegistryCatalog, dict[str, Any]]] = []
        for catalog in self.load_all_catalogs():
            for record in catalog.records:
                if isinstance(record, dict):
                    pairs.append((catalog, record))
        return pairs

    def schema_path(self, relative: str) -> Path:
        """Resolve a schema path under the registry root."""
        return (self.registry_root / relative).resolve()

    def _resolve_catalog_path(self, path: str | Path) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.registry_root / candidate
        candidate = candidate.resolve()
        if not candidate.exists():
            raise RegistryLoadError(f"Registry catalog not found: {candidate}")
        return candidate

    def _read_json(self, path: Path) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RegistryLoadError(
                f"Invalid JSON in {path}: {exc}"
            ) from exc
        except OSError as exc:
            raise RegistryLoadError(f"Unable to read {path}: {exc}") from exc

        if not isinstance(payload, dict):
            raise RegistryLoadError(f"Registry JSON root must be object: {path}")
        return payload

    def _to_catalog(self, path: Path, raw: dict[str, Any]) -> RegistryCatalog:
        records = raw.get("records", [])
        if not isinstance(records, list):
            raise RegistryLoadError(f"'records' must be a list: {path}")

        name = str(raw.get("registry_name") or path.stem)
        return RegistryCatalog(
            name=name,
            path=str(path),
            version=str(raw.get("version", "")),
            prefix=str(raw.get("registry_prefix", "")),
            description=str(raw.get("description", "")),
            records=[item for item in records if isinstance(item, dict)],
            raw=raw,
            checksum=checksum_file(path),
        )

    def catalog_checksum(self, catalog: RegistryCatalog) -> str:
        """Compute payload checksum for a catalog's raw content."""
        return checksum_payload(catalog.raw)

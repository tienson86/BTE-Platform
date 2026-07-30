"""Export registry catalogs and derived indexes."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from services.registry_checksum import checksum_payload
from services.registry_exceptions import RegistryIOError
from services.registry_indexer import RegistryIndexer
from services.registry_loader import RegistryLoader
from services.registry_models import RegistryIndex

logger = logging.getLogger(__name__)


class RegistryExporter:
    """Export registry data to JSON files or bundles."""

    def __init__(
        self,
        loader: RegistryLoader,
        indexer: RegistryIndexer | None = None,
    ) -> None:
        """Initialize exporter."""
        self.loader = loader
        self.indexer = indexer or RegistryIndexer(loader)

    def export_catalog(
        self,
        registry_name: str,
        destination: str | Path,
    ) -> Path:
        """Export a single catalog by registry name."""
        catalogs = {
            catalog.name: catalog for catalog in self.loader.load_all_catalogs()
        }
        catalog = catalogs.get(registry_name)
        if catalog is None:
            raise RegistryIOError(f"Unknown registry catalog: {registry_name}")
        return self._write_json(Path(destination), catalog.raw)

    def export_all(
        self,
        destination_dir: str | Path,
        *,
        include_indexes: bool = False,
    ) -> list[Path]:
        """Export all catalogs into a destination directory."""
        dest = Path(destination_dir)
        dest.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for catalog in self.loader.load_all_catalogs():
            out = dest / f"{catalog.name}.json"
            written.append(self._write_json(out, catalog.raw))

        if include_indexes:
            indexes = self.indexer.reindex()
            index_dir = dest / "indexes"
            index_dir.mkdir(parents=True, exist_ok=True)
            for name, index in indexes.items():
                written.append(
                    self._write_json(
                        index_dir / f"{name}.json",
                        self._index_to_dict(index),
                    )
                )

        manifest = {
            "version": "1.0.0",
            "catalog_count": len(written),
            "checksum": checksum_payload([path.name for path in written]),
        }
        written.append(self._write_json(dest / "manifest.json", manifest))
        logger.info("Exported %s registry artifacts to %s", len(written), dest)
        return written

    def export_bundle(
        self,
        destination: str | Path,
        *,
        include_indexes: bool = True,
    ) -> Path:
        """Export a single JSON bundle containing all catalogs."""
        catalogs = {
            catalog.name: catalog.raw
            for catalog in self.loader.load_all_catalogs()
        }
        payload: dict[str, Any] = {
            "version": "1.0.0",
            "catalogs": catalogs,
        }
        if include_indexes:
            indexes = self.indexer.reindex()
            payload["indexes"] = {
                name: self._index_to_dict(index)
                for name, index in indexes.items()
            }
        return self._write_json(Path(destination), payload)

    def _index_to_dict(self, index: RegistryIndex) -> dict[str, Any]:
        return {
            "version": "1.0.0",
            "index_name": index.name,
            "entries": [
                {
                    "key": entry.key,
                    "registry_ids": entry.registry_ids,
                    "metadata": entry.metadata,
                }
                for entry in index.entries
            ],
        }

    def _write_json(self, path: Path, payload: dict[str, Any]) -> Path:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            raise RegistryIOError(f"Failed to write {path}: {exc}") from exc
        return path

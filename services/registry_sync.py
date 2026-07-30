"""Synchronize derived registry indexes and statistics."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from services.registry_constants import STATISTICS_RELATIVE
from services.registry_exceptions import RegistrySyncError
from services.registry_exporter import RegistryExporter
from services.registry_indexer import RegistryIndexer
from services.registry_loader import RegistryLoader
from services.registry_statistics import RegistryStatistics

logger = logging.getLogger(__name__)


class RegistrySync:
    """Synchronize derived registry artifacts from authoritative catalogs."""

    def __init__(
        self,
        loader: RegistryLoader,
        indexer: RegistryIndexer | None = None,
        statistics: RegistryStatistics | None = None,
        exporter: RegistryExporter | None = None,
    ) -> None:
        """Initialize sync service."""
        self.loader = loader
        self.indexer = indexer or RegistryIndexer(loader)
        self.statistics = statistics or RegistryStatistics(loader)
        self.exporter = exporter or RegistryExporter(loader, self.indexer)

    def reindex(
        self,
        *,
        parallel: bool = True,
        write: bool = False,
        output_dir: str | Path | None = None,
    ) -> dict[str, Any]:
        """Rebuild indexes and optionally write them to disk."""
        indexes = self.indexer.reindex(parallel=parallel)
        payload = {
            name: {
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
            for name, index in indexes.items()
        }
        if write:
            dest = Path(output_dir) if output_dir else (
                self.loader.registry_root / ".derived" / "indexes"
            )
            try:
                dest.mkdir(parents=True, exist_ok=True)
                for name, body in payload.items():
                    path = dest / f"{name}.json"
                    path.write_text(
                        json.dumps(body, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                    )
            except OSError as exc:
                raise RegistrySyncError(f"Failed to write indexes: {exc}") from exc
            logger.info("Wrote derived indexes to %s", dest)
        return payload

    def refresh_statistics(self, *, write: bool = False) -> dict[str, Any]:
        """Recompute statistics and optionally update registry_statistics.json."""
        payload = self.statistics.to_dict()
        if write:
            path = self.loader.registry_root / STATISTICS_RELATIVE
            try:
                path.write_text(
                    json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
            except OSError as exc:
                raise RegistrySyncError(
                    f"Failed to write statistics: {exc}"
                ) from exc
            self.loader.clear_cache()
            logger.info("Updated statistics file %s", path)
        return payload

    def sync_all(
        self,
        *,
        parallel: bool = True,
        write: bool = False,
    ) -> dict[str, Any]:
        """Reindex and refresh statistics in one pass."""
        indexes = self.reindex(parallel=parallel, write=write)
        stats = self.refresh_statistics(write=write)
        return {"indexes": indexes, "statistics": stats}

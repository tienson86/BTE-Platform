"""Parallel registry indexing utilities."""

from __future__ import annotations

import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable

from services.registry_loader import RegistryLoader
from services.registry_models import IndexEntry, RegistryCatalog, RegistryIndex

logger = logging.getLogger(__name__)


class RegistryIndexer:
    """Build derived indexes from registry catalogs."""

    def __init__(
        self,
        loader: RegistryLoader,
        *,
        max_workers: int = 4,
    ) -> None:
        """Initialize indexer with optional worker pool size."""
        self.loader = loader
        self.max_workers = max(1, max_workers)
        self._cache: dict[str, RegistryIndex] = {}

    def clear_cache(self) -> None:
        """Clear derived index cache."""
        self._cache.clear()

    def reindex(
        self,
        *,
        parallel: bool = True,
        catalogs: list[RegistryCatalog] | None = None,
    ) -> dict[str, RegistryIndex]:
        """Rebuild all standard indexes."""
        catalogs = catalogs or self.loader.load_all_catalogs()
        builders: dict[str, Callable[[list[RegistryCatalog]], RegistryIndex]] = {
            "by_registry": self._index_by_registry,
            "by_status": self._index_by_status,
            "by_namespace": self._index_by_namespace,
            "by_domain": self._index_by_domain,
            "by_category": self._index_by_category,
            "by_object_id": self._index_by_object_id,
            "dependencies": self._index_dependencies,
        }

        if not parallel or len(builders) == 1:
            indexes = {
                name: builder(catalogs) for name, builder in builders.items()
            }
        else:
            indexes = self._build_parallel(builders, catalogs)

        self._cache = indexes
        logger.info("Rebuilt %s registry indexes", len(indexes))
        return indexes

    def get_index(self, name: str) -> RegistryIndex | None:
        """Return a cached index by name."""
        if not self._cache:
            self.reindex()
        return self._cache.get(name)

    def _build_parallel(
        self,
        builders: dict[str, Callable[[list[RegistryCatalog]], RegistryIndex]],
        catalogs: list[RegistryCatalog],
    ) -> dict[str, RegistryIndex]:
        indexes: dict[str, RegistryIndex] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(builder, catalogs): name
                for name, builder in builders.items()
            }
            for future in as_completed(futures):
                name = futures[future]
                indexes[name] = future.result()
        return indexes

    def _index_by_registry(
        self,
        catalogs: list[RegistryCatalog],
    ) -> RegistryIndex:
        entries: list[IndexEntry] = []
        for catalog in catalogs:
            ids = [
                str(record.get("identity", {}).get("registry_id", ""))
                for record in catalog.records
                if isinstance(record.get("identity"), dict)
            ]
            entries.append(
                IndexEntry(
                    key=catalog.name,
                    registry_ids=[item for item in ids if item],
                    metadata={"path": catalog.path, "count": len(ids)},
                )
            )
        return RegistryIndex(name="by_registry", entries=entries)

    def _index_by_status(self, catalogs: list[RegistryCatalog]) -> RegistryIndex:
        return self._group_records(
            "by_status",
            catalogs,
            lambda record: str(
                record.get("metadata", {}).get("status", "")
                if isinstance(record.get("metadata"), dict)
                else ""
            ),
        )

    def _index_by_namespace(
        self,
        catalogs: list[RegistryCatalog],
    ) -> RegistryIndex:
        return self._group_records(
            "by_namespace",
            catalogs,
            lambda record: str(
                record.get("identity", {}).get("namespace", "")
                if isinstance(record.get("identity"), dict)
                else ""
            ),
        )

    def _index_by_domain(self, catalogs: list[RegistryCatalog]) -> RegistryIndex:
        return self._group_records(
            "by_domain",
            catalogs,
            lambda record: str(
                record.get("classification", {}).get("domain", "")
                if isinstance(record.get("classification"), dict)
                else ""
            ),
        )

    def _index_by_category(
        self,
        catalogs: list[RegistryCatalog],
    ) -> RegistryIndex:
        return self._group_records(
            "by_category",
            catalogs,
            lambda record: str(
                record.get("classification", {}).get("category", "")
                if isinstance(record.get("classification"), dict)
                else ""
            ),
        )

    def _index_by_object_id(
        self,
        catalogs: list[RegistryCatalog],
    ) -> RegistryIndex:
        return self._group_records(
            "by_object_id",
            catalogs,
            lambda record: str(
                record.get("identity", {}).get("object_id", "")
                if isinstance(record.get("identity"), dict)
                else ""
            ),
        )

    def _index_dependencies(
        self,
        catalogs: list[RegistryCatalog],
    ) -> RegistryIndex:
        grouped: dict[str, list[str]] = defaultdict(list)
        for catalog in catalogs:
            for record in catalog.records:
                identity = record.get("identity", {})
                if not isinstance(identity, dict):
                    continue
                registry_id = str(identity.get("registry_id", ""))
                deps = record.get("dependencies", [])
                if not registry_id or not isinstance(deps, list):
                    continue
                for dep in deps:
                    grouped[str(dep)].append(registry_id)
        entries = [
            IndexEntry(key=key, registry_ids=sorted(set(values)))
            for key, values in sorted(grouped.items())
            if key
        ]
        return RegistryIndex(name="dependencies", entries=entries)

    def _group_records(
        self,
        name: str,
        catalogs: list[RegistryCatalog],
        key_fn: Callable[[dict[str, Any]], str],
    ) -> RegistryIndex:
        grouped: dict[str, list[str]] = defaultdict(list)
        for catalog in catalogs:
            for record in catalog.records:
                identity = record.get("identity", {})
                if not isinstance(identity, dict):
                    continue
                registry_id = str(identity.get("registry_id", ""))
                if not registry_id:
                    continue
                key = key_fn(record)
                if not key:
                    continue
                grouped[key].append(registry_id)
        entries = [
            IndexEntry(key=key, registry_ids=sorted(set(values)))
            for key, values in sorted(grouped.items())
        ]
        return RegistryIndex(name=name, entries=entries)

"""Registry cache runtime service."""

from __future__ import annotations

from engines.analysis_engine.registry.cache_contract import RegistryCacheContract
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class CacheService(RegistryCacheContract):
    """In-memory registry cache for derived lookup artifacts.

    Cache is not an authoritative knowledge source and does not mutate Pack 01.
    """

    def __init__(self) -> None:
        """Initialize empty entry and snapshot caches."""
        self._entries: dict[str, RegistryEntry] = {}
        self._snapshots: dict[str, RegistrySnapshot] = {}

    def get_entry(self, entry_id: str) -> RegistryEntry | None:
        """Return a cached registry entry by identifier."""
        return self._entries.get(entry_id)

    def put_entry(self, entry: RegistryEntry) -> None:
        """Store a registry entry in cache."""
        self._entries[entry.entry_id] = entry

    def get_snapshot(self, snapshot_id: str) -> RegistrySnapshot | None:
        """Return a cached registry snapshot by identifier."""
        return self._snapshots.get(snapshot_id)

    def put_snapshot(self, snapshot: RegistrySnapshot) -> None:
        """Store a registry snapshot in cache."""
        self._snapshots[snapshot.snapshot_id] = snapshot

    def invalidate(self, entry_id: str) -> None:
        """Invalidate a cached entry by identifier."""
        self._entries.pop(entry_id, None)

    def clear(self) -> None:
        """Clear all cached registry artifacts."""
        self._entries.clear()
        self._snapshots.clear()

    def size(self) -> tuple[int, int]:
        """Return ``(entry_count, snapshot_count)`` for diagnostics."""
        return (len(self._entries), len(self._snapshots))

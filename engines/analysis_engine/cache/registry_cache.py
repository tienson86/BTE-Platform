"""Registry cache for in-memory Pack-compatible registry artifacts."""

from __future__ import annotations

from engines.analysis_engine.cache.cache_policy import CachePolicy
from engines.analysis_engine.cache.memory_cache import CacheStats, MemoryCache
from engines.analysis_engine.registry.cache_contract import RegistryCacheContract
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryCache(RegistryCacheContract):
    """Memory-only registry cache compatible with Pack 01 cache boundaries.

    Caches derived lookup artifacts only.
    Does not mutate Pack 01 source knowledge and uses no external cache.
    """

    def __init__(self, policy: CachePolicy | None = None) -> None:
        """Initialize registry memory caches."""
        resolved = policy or CachePolicy(namespace="registry")
        if resolved.namespace == "default":
            resolved = CachePolicy(
                enabled=resolved.enabled,
                max_entries=resolved.max_entries,
                ttl_seconds=resolved.ttl_seconds,
                eviction=resolved.eviction,
                namespace="registry",
            )
        self._entries = MemoryCache(
            CachePolicy(
                enabled=resolved.enabled,
                max_entries=resolved.max_entries,
                ttl_seconds=resolved.ttl_seconds,
                eviction=resolved.eviction,
                namespace="registry_entry",
            )
        )
        self._snapshots = MemoryCache(
            CachePolicy(
                enabled=resolved.enabled,
                max_entries=resolved.max_entries,
                ttl_seconds=resolved.ttl_seconds,
                eviction=resolved.eviction,
                namespace="registry_snapshot",
            )
        )

    def get_entry(self, entry_id: str) -> RegistryEntry | None:
        """Return a cached registry entry by identifier."""
        value = self._entries.get(entry_id)
        return value if isinstance(value, RegistryEntry) else None

    def put_entry(self, entry: RegistryEntry) -> None:
        """Store a registry entry in cache."""
        self._entries.set(entry.entry_id, entry)

    def get_snapshot(self, snapshot_id: str) -> RegistrySnapshot | None:
        """Return a cached registry snapshot by identifier."""
        value = self._snapshots.get(snapshot_id)
        return value if isinstance(value, RegistrySnapshot) else None

    def put_snapshot(self, snapshot: RegistrySnapshot) -> None:
        """Store a registry snapshot in cache."""
        self._snapshots.set(snapshot.snapshot_id, snapshot)

    def invalidate(self, entry_id: str) -> None:
        """Invalidate a cached entry by identifier."""
        self._entries.delete(entry_id)

    def clear(self) -> None:
        """Clear all cached registry artifacts."""
        self._entries.clear()
        self._snapshots.clear()

    def size(self) -> tuple[int, int]:
        """Return ``(entry_count, snapshot_count)``."""
        return (self._entries.size(), self._snapshots.size())

    def stats(self) -> dict[str, CacheStats]:
        """Return stats for entry and snapshot stores."""
        return {
            "entries": self._entries.stats(),
            "snapshots": self._snapshots.stats(),
        }

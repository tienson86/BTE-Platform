"""Analysis Engine registry cache interface."""

from __future__ import annotations

from engines.analysis_engine.registry.cache_service import CacheService
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryCache:
    """Public interface for caching registry entries and snapshots."""

    def __init__(self, service: CacheService | None = None) -> None:
        """Initialize cache facade with an optional cache service."""
        self._service = service or CacheService()

    @property
    def service(self) -> CacheService:
        """Return the underlying cache service."""
        return self._service

    def get_entry(self, entry_id: str) -> RegistryEntry | None:
        """Return a cached registry entry."""
        return self._service.get_entry(entry_id)

    def put_entry(self, entry: RegistryEntry) -> None:
        """Store a registry entry in cache."""
        self._service.put_entry(entry)

    def get_snapshot(self, snapshot_id: str) -> RegistrySnapshot | None:
        """Return a cached registry snapshot."""
        return self._service.get_snapshot(snapshot_id)

    def put_snapshot(self, snapshot: RegistrySnapshot) -> None:
        """Store a registry snapshot in cache."""
        self._service.put_snapshot(snapshot)

    def invalidate(self, entry_id: str) -> None:
        """Invalidate a cached entry by identifier."""
        self._service.invalidate(entry_id)

    def clear(self) -> None:
        """Clear all cached registry data."""
        self._service.clear()

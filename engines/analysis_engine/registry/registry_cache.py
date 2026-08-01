"""Analysis Engine registry cache interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryCache:
    """Public interface for caching registry entries and snapshots."""

    def get_entry(self, entry_id: str) -> RegistryEntry | None:
        """Return a cached registry entry."""
        raise NotImplementedError

    def put_entry(self, entry: RegistryEntry) -> None:
        """Store a registry entry in cache."""
        raise NotImplementedError

    def get_snapshot(self, snapshot_id: str) -> RegistrySnapshot | None:
        """Return a cached registry snapshot."""
        raise NotImplementedError

    def put_snapshot(self, snapshot: RegistrySnapshot) -> None:
        """Store a registry snapshot in cache."""
        raise NotImplementedError

    def invalidate(self, entry_id: str) -> None:
        """Invalidate a cached entry by identifier."""
        raise NotImplementedError

    def clear(self) -> None:
        """Clear all cached registry data."""
        raise NotImplementedError

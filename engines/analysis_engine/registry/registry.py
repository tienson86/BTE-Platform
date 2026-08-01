"""Analysis Engine registry core interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class Registry:
    """Public interface for the Analysis Engine registry.

    Manages registration and lookup of analysis knowledge objects.
    """

    def register(self, entry: RegistryEntry) -> None:
        """Register a registry entry."""
        raise NotImplementedError

    def unregister(self, entry_id: str) -> None:
        """Remove a registry entry by identifier."""
        raise NotImplementedError

    def get(self, entry_id: str) -> RegistryEntry | None:
        """Return a registry entry by identifier."""
        raise NotImplementedError

    def list_entries(self) -> tuple[RegistryEntry, ...]:
        """Return all registered entries."""
        raise NotImplementedError

    def snapshot(self) -> RegistrySnapshot:
        """Return an immutable snapshot of the registry."""
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all registry entries."""
        raise NotImplementedError

"""Analysis Engine registry core interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot
from engines.analysis_engine.registry.registry_service import RegistryService


class Registry:
    """Public interface for the Analysis Engine registry.

    Thin facade over ``RegistryService`` for Pack 01-compatible register/lookup.
    """

    def __init__(self, service: RegistryService | None = None) -> None:
        """Initialize registry with an optional runtime service."""
        self._service = service or RegistryService()

    @property
    def service(self) -> RegistryService:
        """Return the underlying registry runtime service."""
        return self._service

    def register(self, entry: RegistryEntry) -> None:
        """Register a registry entry."""
        self._service.register(entry)

    def unregister(self, entry_id: str) -> None:
        """Remove a registry entry by identifier."""
        self._service.unregister(entry_id)

    def get(self, entry_id: str) -> RegistryEntry | None:
        """Return a registry entry by identifier."""
        return self._service.get(entry_id)

    def list_entries(self) -> tuple[RegistryEntry, ...]:
        """Return all registered entries."""
        return self._service.list_entries()

    def snapshot(self) -> RegistrySnapshot:
        """Return an immutable snapshot of the registry."""
        return self._service.snapshot()

    def clear(self) -> None:
        """Remove all registry entries."""
        self._service.clear()

"""Registry provider public interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryProviderInterface(ABC):
    """Public interface for accessing Analysis Engine registry data."""

    @abstractmethod
    def get_entry(self, entry_id: str) -> RegistryEntry:
        """Return a registry entry by identifier."""

    @abstractmethod
    def list_entries(self, object_type: str | None = None) -> tuple[RegistryEntry, ...]:
        """Return registry entries, optionally filtered by object type."""

    @abstractmethod
    def snapshot(self) -> RegistrySnapshot:
        """Return an immutable registry snapshot."""

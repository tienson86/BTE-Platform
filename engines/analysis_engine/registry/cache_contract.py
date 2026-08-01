"""Registry cache contract interface.

Compatible with Pack 01 Registry cache semantics.
No implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryCacheContract(ABC):
    """Public cache contract aligned with Pack 01 Registry cache boundaries.

    Cache stores derived lookup artifacts only.
    Cache must not mutate Pack 01 source knowledge.
    """

    @abstractmethod
    def get_entry(self, entry_id: str) -> RegistryEntry | None:
        """Return a cached registry entry by identifier."""

    @abstractmethod
    def put_entry(self, entry: RegistryEntry) -> None:
        """Store a registry entry in cache."""

    @abstractmethod
    def get_snapshot(self, snapshot_id: str) -> RegistrySnapshot | None:
        """Return a cached registry snapshot by identifier."""

    @abstractmethod
    def put_snapshot(self, snapshot: RegistrySnapshot) -> None:
        """Store a registry snapshot in cache."""

    @abstractmethod
    def invalidate(self, entry_id: str) -> None:
        """Invalidate a cached entry by identifier."""

    @abstractmethod
    def clear(self) -> None:
        """Clear all cached registry artifacts."""

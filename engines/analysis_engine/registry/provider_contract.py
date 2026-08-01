"""Registry provider contract interface.

Compatible with Pack 01 Registry serve/provider semantics.
No implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryProviderContract(ABC):
    """Public provider contract aligned with Pack 01 Registry serve responsibilities.

    Providers expose registered knowledge to Analysis Engine consumers.
    Providers must remain read-compatible with Pack 01 Registry object identity.
    """

    @abstractmethod
    def get_entry(self, entry_id: str) -> RegistryEntry:
        """Return a registry entry by Pack-compatible identifier."""

    @abstractmethod
    def list_entries(self, object_type: str | None = None) -> tuple[RegistryEntry, ...]:
        """Return registry entries, optionally filtered by Pack object type."""

    @abstractmethod
    def snapshot(self) -> RegistrySnapshot:
        """Return an immutable Pack-compatible registry snapshot."""

    @abstractmethod
    def resolve_reference(self, reference_id: str) -> RegistryEntry:
        """Resolve a Pack 01 reference identifier to a registry entry."""

    @abstractmethod
    def pack_id(self) -> str:
        """Return the pack identifier served by this provider."""

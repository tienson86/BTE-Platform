"""Registry query contract interface.

Compatible with Pack 01 Registry lookup/query responsibilities.
No implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistryQuerySpec


class RegistryQueryContract(ABC):
    """Public query contract aligned with Pack 01 Registry lookup semantics.

    Pack 01 Registry provides lookup and query over registered knowledge
    objects without mutating source knowledge.
    """

    @abstractmethod
    def query(self, spec: RegistryQuerySpec) -> tuple[RegistryEntry, ...]:
        """Query registry entries using a Pack-compatible query specification."""

    @abstractmethod
    def lookup(self, entry_id: str) -> RegistryEntry | None:
        """Lookup a single registry entry by stable identifier."""

    @abstractmethod
    def resolve(self, reference_id: str) -> RegistryEntry | None:
        """Resolve a Pack 01-compatible reference identifier to an entry."""

    @abstractmethod
    def exists(self, entry_id: str) -> bool:
        """Indicate whether an entry identifier is registered."""

    @abstractmethod
    def count(self, spec: RegistryQuerySpec) -> int:
        """Return the number of entries matching a query specification."""

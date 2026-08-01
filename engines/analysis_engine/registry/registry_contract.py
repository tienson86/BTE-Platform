"""Registry core contract interface.

Compatible with Pack 01 Registry register/index/manage/serve semantics.
No implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryContract(ABC):
    """Public registry contract aligned with Pack 01 Registry responsibilities.

    Pack 01 Registry responsibilities consumed here:
    - register
    - index
    - manage
    - lookup
    - resolve
    - serve

    Analysis Engine registry integration must not write Pack 01 source knowledge.
    """

    @abstractmethod
    def register(self, entry: RegistryEntry) -> None:
        """Register an analysis-layer registry entry using Pack-compatible identity."""

    @abstractmethod
    def unregister(self, entry_id: str) -> None:
        """Remove an analysis-layer registry entry by identifier."""

    @abstractmethod
    def get(self, entry_id: str) -> RegistryEntry | None:
        """Lookup a registry entry by Pack-compatible identifier."""

    @abstractmethod
    def list_entries(self) -> tuple[RegistryEntry, ...]:
        """Serve all currently registered entries."""

    @abstractmethod
    def snapshot(self) -> RegistrySnapshot:
        """Serve an immutable registry snapshot."""

    @abstractmethod
    def resolve(self, reference_id: str) -> RegistryEntry | None:
        """Resolve a Pack 01-compatible reference identifier."""

    @abstractmethod
    def clear(self) -> None:
        """Clear analysis-layer registry state without mutating Pack 01 source data."""

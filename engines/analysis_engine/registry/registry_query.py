"""Analysis Engine registry query interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistryQuerySpec


class RegistryQuery:
    """Public interface for querying registry entries."""

    def query(self, spec: RegistryQuerySpec) -> tuple[RegistryEntry, ...]:
        """Execute a registry query and return matching entries."""
        raise NotImplementedError

    def exists(self, entry_id: str) -> bool:
        """Indicate whether an entry identifier exists."""
        raise NotImplementedError

    def count(self, spec: RegistryQuerySpec) -> int:
        """Return the number of entries matching a query."""
        raise NotImplementedError

"""Analysis Engine registry query interface."""

from __future__ import annotations

from engines.analysis_engine.registry.query_engine import QueryEngine
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistryQuerySpec
from engines.analysis_engine.registry.registry_service import RegistryService


class RegistryQuery:
    """Public interface for querying registry entries."""

    def __init__(
        self,
        *,
        service: RegistryService | None = None,
        query_engine: QueryEngine | None = None,
    ) -> None:
        """Initialize query facade with registry service or query engine."""
        if query_engine is not None:
            self._engine = query_engine
        else:
            registry = service or RegistryService()
            self._engine = registry.query_engine

    def query(self, spec: RegistryQuerySpec) -> tuple[RegistryEntry, ...]:
        """Execute a registry query and return matching entries."""
        return self._engine.query(spec)

    def exists(self, entry_id: str) -> bool:
        """Indicate whether an entry identifier exists."""
        return self._engine.exists(entry_id)

    def count(self, spec: RegistryQuerySpec) -> int:
        """Return the number of entries matching a query."""
        return self._engine.count(spec)

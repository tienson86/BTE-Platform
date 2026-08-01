"""Analysis Engine registry builder interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot
from engines.analysis_engine.registry.registry_service import RegistryService


class RegistryBuilder:
    """Public interface for constructing registry instances and snapshots."""

    def create(self) -> Registry:
        """Create an empty registry instance."""
        return Registry(RegistryService())

    def add_entry(self, registry: Registry, entry: RegistryEntry) -> Registry:
        """Add an entry during registry construction."""
        registry.register(entry)
        return registry

    def build_snapshot(self, registry: Registry) -> RegistrySnapshot:
        """Build an immutable snapshot from a registry."""
        return registry.snapshot()

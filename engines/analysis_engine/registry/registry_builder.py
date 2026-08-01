"""Analysis Engine registry builder interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryBuilder:
    """Public interface for constructing registry instances and snapshots."""

    def create(self) -> Registry:
        """Create an empty registry instance."""
        raise NotImplementedError

    def add_entry(self, registry: Registry, entry: RegistryEntry) -> Registry:
        """Add an entry during registry construction."""
        raise NotImplementedError

    def build_snapshot(self, registry: Registry) -> RegistrySnapshot:
        """Build an immutable snapshot from a registry."""
        raise NotImplementedError

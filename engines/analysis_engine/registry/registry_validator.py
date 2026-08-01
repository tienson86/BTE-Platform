"""Analysis Engine registry validator interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistrySnapshot


class RegistryValidator:
    """Public interface for validating registry entries and snapshots."""

    def validate_entry(self, entry: RegistryEntry) -> bool:
        """Validate a single registry entry."""
        raise NotImplementedError

    def validate_registry(self, registry: Registry) -> bool:
        """Validate a complete registry instance."""
        raise NotImplementedError

    def validate_snapshot(self, snapshot: RegistrySnapshot) -> bool:
        """Validate a registry snapshot."""
        raise NotImplementedError

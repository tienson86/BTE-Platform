"""Analysis Engine registry export interface."""

from __future__ import annotations

from pathlib import Path

from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistrySnapshot


class RegistryExport:
    """Public interface for exporting registry data."""

    def export_registry(self, registry: Registry, path: Path) -> None:
        """Export a registry instance to a filesystem path."""
        raise NotImplementedError

    def export_snapshot(self, snapshot: RegistrySnapshot, path: Path) -> None:
        """Export a registry snapshot to a filesystem path."""
        raise NotImplementedError

    def export_entry_ids(self, registry: Registry) -> tuple[str, ...]:
        """Export the list of entry identifiers from a registry."""
        raise NotImplementedError

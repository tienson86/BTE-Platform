"""Analysis Engine registry loader interface."""

from __future__ import annotations

from pathlib import Path

from engines.analysis_engine.registry.module_loader import ModuleLoader
from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistrySnapshot


class RegistryLoader:
    """Public interface for loading registry data from external sources."""

    def __init__(self, module_loader: ModuleLoader | None = None) -> None:
        """Initialize loader facade with an optional module loader."""
        self._loader = module_loader or ModuleLoader()

    def load_from_path(self, path: Path) -> Registry:
        """Load a registry from a filesystem path."""
        snapshot = self._loader.load_snapshot(path)
        registry = Registry()
        registry.service.load_snapshot(snapshot)
        return registry

    def load_snapshot(self, path: Path) -> RegistrySnapshot:
        """Load a registry snapshot from a filesystem path."""
        return self._loader.load_snapshot(path)

    def load_entry_ids(self, path: Path) -> tuple[str, ...]:
        """Load entry identifiers available at a path."""
        return self._loader.list_entry_ids(path)

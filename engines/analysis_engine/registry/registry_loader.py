"""Analysis Engine registry loader interface."""

from __future__ import annotations

from pathlib import Path

from engines.analysis_engine.registry.registry import Registry
from engines.analysis_engine.registry.registry_models import RegistrySnapshot


class RegistryLoader:
    """Public interface for loading registry data from external sources."""

    def load_from_path(self, path: Path) -> Registry:
        """Load a registry from a filesystem path."""
        raise NotImplementedError

    def load_snapshot(self, path: Path) -> RegistrySnapshot:
        """Load a registry snapshot from a filesystem path."""
        raise NotImplementedError

    def load_entry_ids(self, path: Path) -> tuple[str, ...]:
        """Load entry identifiers available at a path."""
        raise NotImplementedError

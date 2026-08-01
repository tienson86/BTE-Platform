"""Analysis Engine registry index interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry_models import RegistryEntry


class RegistryIndex:
    """Public interface for indexing registry entries."""

    def index_entry(self, entry: RegistryEntry) -> None:
        """Add or update an entry in the index."""
        raise NotImplementedError

    def remove_entry(self, entry_id: str) -> None:
        """Remove an entry from the index."""
        raise NotImplementedError

    def find_by_type(self, object_type: str) -> tuple[str, ...]:
        """Return entry identifiers for an object type."""
        raise NotImplementedError

    def find_by_name(self, name: str) -> tuple[str, ...]:
        """Return entry identifiers matching a name."""
        raise NotImplementedError

    def rebuild(self, entries: tuple[RegistryEntry, ...]) -> None:
        """Rebuild the index from a full entry set."""
        raise NotImplementedError

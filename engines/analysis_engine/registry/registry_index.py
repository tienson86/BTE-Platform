"""Analysis Engine registry index interface."""

from __future__ import annotations

from engines.analysis_engine.registry.registry_models import RegistryEntry
from engines.analysis_engine.registry.registry_service import RegistryService


class RegistryIndex:
    """Public interface for indexing registry entries."""

    def __init__(self, service: RegistryService | None = None) -> None:
        """Initialize index facade backed by a registry service."""
        self._service = service or RegistryService()
        self._by_type: dict[str, set[str]] = {}
        self._by_name: dict[str, set[str]] = {}
        self._entries: dict[str, RegistryEntry] = {}

    def index_entry(self, entry: RegistryEntry) -> None:
        """Add or update an entry in the index."""
        self._entries[entry.entry_id] = entry
        self._by_type.setdefault(entry.object_type, set()).add(entry.entry_id)
        self._by_name.setdefault(entry.name, set()).add(entry.entry_id)
        self._service.register(entry)

    def remove_entry(self, entry_id: str) -> None:
        """Remove an entry from the index."""
        entry = self._entries.pop(entry_id, None)
        if entry is None:
            return
        typed = self._by_type.get(entry.object_type)
        if typed is not None:
            typed.discard(entry_id)
        named = self._by_name.get(entry.name)
        if named is not None:
            named.discard(entry_id)
        self._service.unregister(entry_id)

    def find_by_type(self, object_type: str) -> tuple[str, ...]:
        """Return entry identifiers for an object type."""
        return tuple(sorted(self._by_type.get(object_type, set())))

    def find_by_name(self, name: str) -> tuple[str, ...]:
        """Return entry identifiers matching a name."""
        return tuple(sorted(self._by_name.get(name, set())))

    def rebuild(self, entries: tuple[RegistryEntry, ...]) -> None:
        """Rebuild the index from a full entry set."""
        self._by_type.clear()
        self._by_name.clear()
        self._entries.clear()
        self._service.clear()
        for entry in entries:
            self.index_entry(entry)

"""Registry query engine runtime service."""

from __future__ import annotations

from collections.abc import Callable

from engines.analysis_engine.registry.query_contract import RegistryQueryContract
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistryQuerySpec


class QueryEngine(RegistryQueryContract):
    """Deterministic, read-only registry query engine.

    Compatible with Pack 01 lookup/query semantics.
    Does not mutate registry state or Pack 01 source knowledge.
    """

    def __init__(
        self,
        *,
        entry_provider: Callable[[], tuple[RegistryEntry, ...]],
        resolver: Callable[[str], RegistryEntry | None] | None = None,
    ) -> None:
        """Initialize query engine with entry and resolve providers."""
        self._entry_provider = entry_provider
        self._resolver = resolver

    def query(self, spec: RegistryQuerySpec) -> tuple[RegistryEntry, ...]:
        """Query registry entries using a Pack-compatible query specification."""
        matches = [
            entry
            for entry in self._entry_provider()
            if self._matches(entry, spec)
        ]
        matches.sort(key=lambda entry: entry.entry_id)
        return tuple(matches)

    def lookup(self, entry_id: str) -> RegistryEntry | None:
        """Lookup a single registry entry by stable identifier."""
        for entry in self._entry_provider():
            if entry.entry_id == entry_id:
                return entry
        return None

    def resolve(self, reference_id: str) -> RegistryEntry | None:
        """Resolve a Pack 01-compatible reference identifier to an entry."""
        if self._resolver is not None:
            return self._resolver(reference_id)
        direct = self.lookup(reference_id)
        if direct is not None:
            return direct
        for entry in self._entry_provider():
            object_id = entry.metadata.get("object_id")
            if object_id == reference_id:
                return entry
            if reference_id in entry.references:
                return entry
        return None

    def exists(self, entry_id: str) -> bool:
        """Indicate whether an entry identifier is registered."""
        return self.lookup(entry_id) is not None

    def count(self, spec: RegistryQuerySpec) -> int:
        """Return the number of entries matching a query specification."""
        return len(self.query(spec))

    def _matches(self, entry: RegistryEntry, spec: RegistryQuerySpec) -> bool:
        """Return True when an entry satisfies all populated query fields."""
        if spec.entry_id is not None and entry.entry_id != spec.entry_id:
            return False
        if spec.object_type is not None and entry.object_type != spec.object_type:
            return False
        if spec.name is not None and entry.name != spec.name:
            return False
        if spec.status is not None and entry.status != spec.status:
            return False
        if spec.tags:
            entry_tags = self._entry_tags(entry)
            if not set(spec.tags).issubset(entry_tags):
                return False
        return True

    def _entry_tags(self, entry: RegistryEntry) -> set[str]:
        """Extract tag identifiers from entry metadata."""
        raw = entry.metadata.get("tags") or ()
        if isinstance(raw, str):
            return {raw}
        if isinstance(raw, (list, tuple, set)):
            return {str(tag) for tag in raw}
        return set()

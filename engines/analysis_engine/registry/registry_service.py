"""Registry service runtime facade."""

from __future__ import annotations

from uuid import uuid4

from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.registry.cache_service import CacheService
from engines.analysis_engine.registry.dependency_graph import DependencyGraph
from engines.analysis_engine.registry.query_engine import QueryEngine
from engines.analysis_engine.registry.registry_contract import RegistryContract
from engines.analysis_engine.registry.registry_models import (
    RegistryEntry,
    RegistryQuerySpec,
    RegistrySnapshot,
)
from engines.analysis_engine.registry.version_resolver import VersionResolver


class RegistryService(RegistryContract):
    """Runtime registry service aligned with Pack 01 register/index/manage/serve.

    Manages analysis-layer registry state only.
    Does not write Pack 01 source knowledge and does not evaluate business rules.
    """

    def __init__(
        self,
        *,
        cache: CacheService | None = None,
        version_resolver: VersionResolver | None = None,
        schema_version: str = "1.0.0",
    ) -> None:
        """Initialize registry runtime collaborators."""
        self._entries: dict[str, RegistryEntry] = {}
        self._object_id_index: dict[str, str] = {}
        self._type_index: dict[str, set[str]] = {}
        self._cache = cache or CacheService()
        self._version_resolver = version_resolver or VersionResolver()
        self._dependency_graph = DependencyGraph()
        self._schema_version = schema_version
        self._query_engine = QueryEngine(
            entry_provider=self.list_entries,
            resolver=self.resolve,
        )

    @property
    def query_engine(self) -> QueryEngine:
        """Return the bound query engine."""
        return self._query_engine

    @property
    def cache(self) -> CacheService:
        """Return the bound cache service."""
        return self._cache

    @property
    def version_resolver(self) -> VersionResolver:
        """Return the bound version resolver."""
        return self._version_resolver

    @property
    def dependency_graph(self) -> DependencyGraph:
        """Return the current dependency graph snapshot builder."""
        return self._dependency_graph

    def register(self, entry: RegistryEntry) -> None:
        """Register an analysis-layer registry entry using Pack-compatible identity."""
        if not entry.entry_id:
            raise RegistryError("registry_entry_missing_id")
        self._entries[entry.entry_id] = entry
        object_id = entry.metadata.get("object_id")
        if isinstance(object_id, str) and object_id:
            self._object_id_index[object_id] = entry.entry_id
        self._type_index.setdefault(entry.object_type, set()).add(entry.entry_id)
        self._cache.put_entry(entry)
        self._rebuild_dependency_graph()

    def unregister(self, entry_id: str) -> None:
        """Remove an analysis-layer registry entry by identifier."""
        entry = self._entries.pop(entry_id, None)
        if entry is None:
            return
        object_id = entry.metadata.get("object_id")
        if isinstance(object_id, str):
            self._object_id_index.pop(object_id, None)
        typed = self._type_index.get(entry.object_type)
        if typed is not None:
            typed.discard(entry_id)
            if not typed:
                del self._type_index[entry.object_type]
        self._cache.invalidate(entry_id)
        self._rebuild_dependency_graph()

    def get(self, entry_id: str) -> RegistryEntry | None:
        """Lookup a registry entry by Pack-compatible identifier."""
        cached = self._cache.get_entry(entry_id)
        if cached is not None:
            return cached
        entry = self._entries.get(entry_id)
        if entry is not None:
            self._cache.put_entry(entry)
        return entry

    def list_entries(self) -> tuple[RegistryEntry, ...]:
        """Serve all currently registered entries in deterministic order."""
        return tuple(
            self._entries[entry_id] for entry_id in sorted(self._entries.keys())
        )

    def snapshot(self) -> RegistrySnapshot:
        """Serve an immutable registry snapshot."""
        snap = RegistrySnapshot(
            snapshot_id=str(uuid4()),
            schema_version=self._schema_version,
            entries=self.list_entries(),
        )
        self._cache.put_snapshot(snap)
        return snap

    def resolve(self, reference_id: str) -> RegistryEntry | None:
        """Resolve a Pack 01-compatible reference identifier."""
        direct = self.get(reference_id)
        if direct is not None:
            return direct
        mapped = self._object_id_index.get(reference_id)
        if mapped is not None:
            return self.get(mapped)
        for entry in self.list_entries():
            if reference_id in entry.references:
                return entry
        return None

    def clear(self) -> None:
        """Clear analysis-layer registry state without mutating Pack 01 source data."""
        self._entries.clear()
        self._object_id_index.clear()
        self._type_index.clear()
        self._dependency_graph.clear()
        self._cache.clear()

    def load_snapshot(self, snapshot: RegistrySnapshot) -> None:
        """Replace analysis-layer state from an immutable snapshot."""
        self.clear()
        self._schema_version = snapshot.schema_version
        for entry in snapshot.entries:
            self.register(entry)

    def query(self, spec: RegistryQuerySpec) -> tuple[RegistryEntry, ...]:
        """Delegate Pack-compatible queries to the query engine."""
        return self._query_engine.query(spec)

    def list_by_type(self, object_type: str) -> tuple[RegistryEntry, ...]:
        """Serve entries for a Pack object type in deterministic order."""
        entry_ids = sorted(self._type_index.get(object_type, set()))
        return tuple(self._entries[entry_id] for entry_id in entry_ids)

    def resolve_version(
        self,
        object_type: str,
        name: str,
        *,
        requested_version: str | None = None,
        allow_compatible: bool = True,
        allow_deprecated: bool = False,
    ) -> RegistryEntry:
        """Resolve a versioned entry family using Pack 01 version priority."""
        candidates = tuple(
            entry
            for entry in self.list_by_type(object_type)
            if entry.name == name
        )
        return self._version_resolver.resolve(
            candidates,
            requested_version=requested_version,
            allow_compatible=allow_compatible,
            allow_deprecated=allow_deprecated,
        )

    def dependency_order(self) -> tuple[str, ...]:
        """Return topological dependency order for registered entries."""
        self._rebuild_dependency_graph()
        return self._dependency_graph.topological_order()

    def _rebuild_dependency_graph(self) -> None:
        """Rebuild the structural dependency graph from current entries."""
        self._dependency_graph.build_from_entries(self.list_entries())

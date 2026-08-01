"""Interpreter registry public facade."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry.dependency_graph import DependencyGraph
from engines.interpretation_engine.registry.loader import Loader
from engines.interpretation_engine.registry.metadata import (
    InterpreterRegistryEntry,
    InterpreterRegistrySnapshot,
    Metadata,
)
from engines.interpretation_engine.registry.registry_interface import (
    InterpretationRegistryInterface,
)
from engines.interpretation_engine.registry.resolver import Resolver
from engines.interpretation_engine.registry.version_manager import VersionManager
from engines.interpretation_engine.utils.ids import new_id

_DEFAULT_SCHEMA_VERSION = "0.0.0-architecture"


class Registry(InterpretationRegistryInterface):
    """Public Interpreter Registry for Pack 03.

    Registers interpreter descriptors and resolves load order.
    Does not generate sentences or evaluate BaZi interpretation logic.
    Pack 01 remains read-only via ``Loader``.
    """

    def __init__(
        self,
        *,
        loader: Loader | None = None,
        version_manager: VersionManager | None = None,
        schema_version: str = _DEFAULT_SCHEMA_VERSION,
    ) -> None:
        """Initialize registry runtime collaborators."""
        self._entries: dict[str, InterpreterRegistryEntry] = {}
        self._loader = loader or Loader()
        self._version_manager = version_manager or VersionManager()
        self._dependency_graph = DependencyGraph()
        self._metadata = Metadata()
        self._schema_version = schema_version
        self._resolver = Resolver(
            entry_provider=self.list_entries,
            version_manager=self._version_manager,
            dependency_graph=self._dependency_graph,
        )

    @property
    def loader(self) -> Loader:
        """Return the bound read-only loader."""
        return self._loader

    @property
    def resolver(self) -> Resolver:
        """Return the bound resolver."""
        return self._resolver

    @property
    def version_manager(self) -> VersionManager:
        """Return the bound version manager."""
        return self._version_manager

    @property
    def dependency_graph(self) -> DependencyGraph:
        """Return the bound dependency graph."""
        return self._dependency_graph

    @property
    def metadata(self) -> Metadata:
        """Return the metadata helper."""
        return self._metadata

    def register(self, entry: InterpreterRegistryEntry) -> None:
        """Register an interpreter registry entry."""
        if not entry.validate():
            raise InterpretationRegistryError("registry_entry_invalid")
        self._entries[entry.entry_id] = entry
        self._rebuild_dependency_graph()

    def unregister(self, entry_id: str) -> None:
        """Remove an interpreter registry entry by identifier."""
        if entry_id in self._entries:
            del self._entries[entry_id]
            self._rebuild_dependency_graph()

    def get(self, key: str) -> Any:
        """Resolve a registry entry by key (entry_id)."""
        return self._entries.get(key)

    def get_entry(self, entry_id: str) -> InterpreterRegistryEntry | None:
        """Return a typed registry entry by identifier."""
        return self._entries.get(entry_id)

    def list_keys(self) -> tuple[str, ...]:
        """List available registry entry identifiers."""
        return tuple(sorted(self._entries.keys()))

    def list_entries(self) -> tuple[InterpreterRegistryEntry, ...]:
        """Return all registered entries in deterministic order."""
        return tuple(
            self._entries[entry_id] for entry_id in sorted(self._entries.keys())
        )

    def snapshot(self) -> InterpreterRegistrySnapshot:
        """Return an immutable snapshot of the registry."""
        return InterpreterRegistrySnapshot(
            snapshot_id=new_id("regsnap"),
            schema_version=self._schema_version,
            entries=self.list_entries(),
        )

    def load_snapshot(self, snapshot: InterpreterRegistrySnapshot) -> None:
        """Replace registry contents from an immutable snapshot."""
        self.clear()
        for entry in snapshot.entries:
            self.register(entry)
        self._schema_version = snapshot.schema_version

    def clear(self) -> None:
        """Remove all registry entries."""
        self._entries.clear()
        self._dependency_graph.clear()

    def validate(self) -> bool:
        """Validate registry readiness and dependency integrity."""
        entries = self.list_entries()
        if not all(entry.validate() for entry in entries):
            return False
        self._rebuild_dependency_graph()
        if self._dependency_graph.has_cycle():
            return False
        return True

    def resolve_load_order(self) -> tuple[str, ...]:
        """Resolve deterministic interpreter load order."""
        return self._resolver.resolve_load_order()

    def _rebuild_dependency_graph(self) -> None:
        """Rebuild dependency graph from current entries."""
        self._dependency_graph.build_from_entries(self.list_entries())

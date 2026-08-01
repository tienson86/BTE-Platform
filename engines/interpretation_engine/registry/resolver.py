"""Interpreter registry resolver."""

from __future__ import annotations

from collections.abc import Callable

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry.dependency_graph import DependencyGraph
from engines.interpretation_engine.registry.metadata import InterpreterRegistryEntry
from engines.interpretation_engine.registry.version_manager import VersionManager


class Resolver:
    """Resolve interpreter registry entries by id, domain, and version.

    Resolution is structural only. No sentence generation.
    """

    def __init__(
        self,
        *,
        entry_provider: Callable[[], tuple[InterpreterRegistryEntry, ...]],
        version_manager: VersionManager | None = None,
        dependency_graph: DependencyGraph | None = None,
    ) -> None:
        """Initialize resolver with entry provider and version manager."""
        self._entry_provider = entry_provider
        self._version_manager = version_manager or VersionManager()
        self._dependency_graph = dependency_graph or DependencyGraph()

    @property
    def version_manager(self) -> VersionManager:
        """Return the bound version manager."""
        return self._version_manager

    @property
    def dependency_graph(self) -> DependencyGraph:
        """Return the bound dependency graph."""
        return self._dependency_graph

    def resolve_by_id(self, entry_id: str) -> InterpreterRegistryEntry:
        """Resolve a single registry entry by entry identifier."""
        for entry in self._entry_provider():
            if entry.entry_id == entry_id:
                return entry
        raise InterpretationRegistryError(f"entry_not_found:{entry_id}")

    def resolve_by_interpreter_id(
        self,
        interpreter_id: str,
        *,
        requested_version: str | None = None,
        allow_compatible: bool = True,
        allow_deprecated: bool = False,
    ) -> InterpreterRegistryEntry:
        """Resolve an interpreter by stable interpreter_id and optional version."""
        candidates = tuple(
            entry
            for entry in self._entry_provider()
            if entry.interpreter_id == interpreter_id
        )
        if not candidates:
            raise InterpretationRegistryError(f"interpreter_not_found:{interpreter_id}")
        return self._version_manager.resolve(
            candidates,
            requested_version=requested_version,
            allow_compatible=allow_compatible,
            allow_deprecated=allow_deprecated,
        )

    def resolve_by_domain(self, domain: str) -> tuple[InterpreterRegistryEntry, ...]:
        """Resolve all registered interpreters for a domain."""
        if not domain:
            raise InterpretationRegistryError("domain_required")
        return tuple(
            entry
            for entry in self._entry_provider()
            if entry.domain == domain
        )

    def resolve_load_order(self) -> tuple[str, ...]:
        """Resolve deterministic interpreter load order via dependency graph."""
        entries = self._entry_provider()
        self._dependency_graph.build_from_entries(entries)
        return self._dependency_graph.topological_order()

    def resolve_dependencies(self, entry_id: str) -> tuple[InterpreterRegistryEntry, ...]:
        """Resolve direct dependency entries for an interpreter entry."""
        entry = self.resolve_by_id(entry_id)
        resolved: list[InterpreterRegistryEntry] = []
        for dependency_id in entry.dependencies:
            resolved.append(self.resolve_by_id(dependency_id))
        return tuple(resolved)

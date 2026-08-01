"""Architecture tests for interpretation interpreter registry runtime."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry import (
    DependencyGraph,
    InterpreterRegistryEntry,
    Loader,
    Registry,
    Resolver,
    VersionManager,
)


def _entry(
    entry_id: str,
    *,
    interpreter_id: str | None = None,
    version: str = "1.0.0",
    status: str = "active",
    domain: str = "personality",
    dependencies: tuple[str, ...] = (),
) -> InterpreterRegistryEntry:
    """Build a minimal interpreter registry entry."""
    return InterpreterRegistryEntry(
        entry_id=entry_id,
        interpreter_id=interpreter_id or entry_id,
        name=entry_id,
        version=version,
        status=status,
        domain=domain,
        dependencies=dependencies,
    )


def test_register_and_list() -> None:
    """Registry stores interpreter descriptors without sentence content."""
    registry = Registry()
    registry.register(_entry("interp_personality"))
    registry.register(_entry("interp_career", domain="career"))
    assert registry.list_keys() == ("interp_career", "interp_personality")
    assert registry.validate() is True
    assert registry.get("interp_personality").interpreter_id == "interp_personality"


def test_dependency_load_order() -> None:
    """Resolver returns topological load order from dependencies."""
    registry = Registry()
    registry.register(_entry("summary", domain="summary", dependencies=("personality",)))
    registry.register(_entry("personality", domain="personality"))
    assert registry.resolve_load_order() == ("personality", "summary")


def test_circular_dependency_invalidates() -> None:
    """Circular interpreter dependencies fail validation."""
    registry = Registry()
    registry.register(_entry("a", dependencies=("b",)))
    registry.register(_entry("b", dependencies=("a",)))
    assert registry.validate() is False
    with pytest.raises(InterpretationRegistryError, match="circular_dependency"):
        registry.resolve_load_order()


def test_version_manager_resolves_compatible() -> None:
    """Version manager prefers compatible newer patch versions."""
    manager = VersionManager()
    entries = (
        _entry("p", interpreter_id="personality", version="1.0.0"),
        _entry("p2", interpreter_id="personality", version="1.0.2", status="active"),
    )
    resolved = manager.resolve(entries, requested_version="1.0.1", allow_compatible=True)
    assert resolved.version == "1.0.2"


def test_resolver_by_interpreter_id() -> None:
    """Resolver selects interpreter by stable interpreter_id."""
    entries = (
        _entry("p_v1", interpreter_id="personality", version="1.0.0"),
        _entry("p_v2", interpreter_id="personality", version="1.1.0", status="active"),
    )
    resolver = Resolver(entry_provider=lambda: entries, version_manager=VersionManager())
    resolved = resolver.resolve_by_interpreter_id("personality")
    assert resolved.entry_id == "p_v2"


def test_loader_from_mapping_and_file(tmp_path: Path) -> None:
    """Loader loads interpreter descriptors from mapping and JSON file."""
    payload = {
        "schema_version": "0.0.0-architecture",
        "entries": [
            {
                "entry_id": "interp_health",
                "interpreter_id": "health",
                "name": "Health",
                "version": "1.0.0",
                "status": "active",
                "domain": "health",
                "dependencies": [],
            }
        ],
    }
    loader = Loader()
    entries = loader.load_entries_from_mapping(payload)
    assert len(entries) == 1
    assert entries[0].interpreter_id == "health"

    path = tmp_path / "interpreter_registry.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    snapshot = loader.load_snapshot(path)
    assert snapshot.entries[0].domain == "health"
    assert loader.is_read_only("PACK_01") is True


def test_dependency_graph_missing() -> None:
    """Dependency graph reports missing external dependencies."""
    graph = DependencyGraph()
    entries = (_entry("summary", dependencies=("missing_interp",)),)
    graph.build_from_entries(entries)
    assert graph.missing_dependencies(entries) == ("missing_interp",)

"""Registry infrastructure tests (mock interpreter descriptors only)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.registry import (
    DependencyGraph,
    InterpreterRegistryEntry,
    Loader,
    Metadata,
    Registry,
    Resolver,
    VersionManager,
)
from engines.interpretation_engine.registry.metadata import InterpreterRegistrySnapshot


def _entry(
    entry_id: str,
    *,
    interpreter_id: str | None = None,
    version: str = "1.0.0",
    status: str = "active",
    domain: str = "personality",
    dependencies: tuple[str, ...] = (),
) -> InterpreterRegistryEntry:
    """Build a mock registry entry."""
    return InterpreterRegistryEntry(
        entry_id=entry_id,
        interpreter_id=interpreter_id or entry_id,
        name=entry_id,
        version=version,
        status=status,
        domain=domain,
        dependencies=dependencies,
        metadata={"owner": "test"},
    )


class TestRegistryInfrastructure:
    """Mock-only interpreter registry coverage."""

    def test_register_resolve_load_order_snapshot(self) -> None:
        """Registry register/resolve/snapshot/load_order."""
        registry = Registry()
        registry.register(_entry("personality"))
        registry.register(_entry("summary", domain="summary", dependencies=("personality",)))
        assert registry.list_keys() == ("personality", "summary")
        assert registry.get_entry("personality") is not None
        assert registry.validate() is True
        assert registry.resolve_load_order() == ("personality", "summary")
        snap = registry.snapshot()
        registry.clear()
        assert registry.list_keys() == ()
        registry.load_snapshot(snap)
        assert registry.list_keys() == ("personality", "summary")
        registry.unregister("summary")
        assert "summary" not in registry.list_keys()

    def test_version_manager_edges(self) -> None:
        """Version manager parse/compare/resolve edges."""
        manager = VersionManager()
        assert manager.parse_version("1.2.3") == (1, 2, 3)
        assert manager.compare("1.0.0", "1.0.1") == -1
        assert manager.compare("2.0.0", "1.9.9") == 1
        assert manager.compare("1.0.0", "1.0.0") == 0
        assert manager.is_compatible("1.0.2", "1.0.1") is True
        assert manager.is_compatible("2.0.0", "1.0.0") is False
        entries = (
            _entry("a", interpreter_id="p", version="1.0.0", status="active"),
            _entry("b", interpreter_id="p", version="1.0.2", status="active"),
            _entry("c", interpreter_id="p", version="0.9.0", status="archived"),
            _entry("d", interpreter_id="p", version="1.0.0", status="deprecated"),
        )
        assert manager.resolve(entries).version == "1.0.2"
        assert manager.resolve(entries, requested_version="1.0.0").version == "1.0.0"
        assert (
            manager.resolve(
                (_entry("d", interpreter_id="p", version="1.0.0", status="deprecated"),),
                requested_version="1.0.0",
                allow_deprecated=True,
            ).version
            == "1.0.0"
        )
        assert (
            manager.resolve(entries, requested_version="1.0.1", allow_compatible=True).version
            == "1.0.2"
        )
        with pytest.raises(InterpretationRegistryError, match="version_not_found"):
            manager.resolve(entries, requested_version="9.0.0", allow_compatible=False)
        with pytest.raises(InterpretationRegistryError, match="invalid_version"):
            manager.parse_version("x.y")
        with pytest.raises(InterpretationRegistryError, match="version_resolution_empty"):
            manager.resolve(())

    def test_resolver_domain_and_dependencies(self) -> None:
        """Resolver resolves by interpreter id, domain, and dependencies."""
        entries = (
            _entry("personality"),
            _entry("summary", domain="summary", dependencies=("personality",)),
        )
        resolver = Resolver(entry_provider=lambda: entries)
        assert resolver.resolve_by_id("personality").domain == "personality"
        assert resolver.resolve_by_interpreter_id("summary").entry_id == "summary"
        assert resolver.resolve_by_domain("summary")[0].entry_id == "summary"
        deps = resolver.resolve_dependencies("summary")
        assert deps[0].entry_id == "personality"
        assert resolver.resolve_load_order()[0] == "personality"
        with pytest.raises(InterpretationRegistryError, match="entry_not_found"):
            resolver.resolve_by_id("missing")
        with pytest.raises(InterpretationRegistryError, match="domain_required"):
            resolver.resolve_by_domain("")

    def test_loader_mapping_file_and_pack_read(self, tmp_path: Path) -> None:
        """Loader loads descriptors and supports read-only pack checks."""
        payload = {
            "schema_version": "0.0.0-architecture",
            "interpreters": [
                {
                    "entry_id": "health",
                    "interpreter_id": "health",
                    "name": "Health",
                    "version": "1.0.0",
                    "status": "active",
                    "domain": "health",
                    "dependencies": [{"entry_id": "summary"}],
                    "tags": ["core"],
                }
            ],
        }
        loader = Loader()
        entries = loader.load_entries_from_mapping(payload)
        assert entries[0].interpreter_id == "health"
        assert entries[0].dependencies == ("summary",)
        path = tmp_path / "reg.json"
        path.write_text(json.dumps({"entries": payload["interpreters"]}), encoding="utf-8")
        snap = loader.load_snapshot(path)
        assert loader.list_entry_ids(path) == ("health",)
        loader.bind_pack("PACK_03", path)
        assert loader.is_read_only("PACK_01") is True
        assert loader.read("PACK_03", "registry")["entries"][0]["entry_id"] == "health"
        assert loader.load_pack_registry("PACK_03").entries
        with pytest.raises(InterpretationRegistryError, match="registry_payload_unsupported"):
            loader.load_entries_from_mapping({"foo": 1})
        with pytest.raises(InterpretationRegistryError, match="pack_resource_not_found"):
            loader.read("PACK_03", "missing_key")

    def test_metadata_and_dependency_graph_helpers(self) -> None:
        """Metadata helper and dependency graph node helpers."""
        entry = _entry("a", dependencies=("missing",))
        meta = Metadata().from_entry(entry)
        assert meta["interpreter_id"] == "a"
        assert Metadata().from_snapshot(
            InterpreterRegistrySnapshot(
                snapshot_id="s",
                schema_version="1",
                entries=(entry,),
            )
        )["a"]["entry_id"] == "a"
        assert Metadata().from_mapping({"entry_id": "x", "name": "X"})["entry_id"] == "x"
        nested = Metadata().from_mapping(
            {"metadata": {"owner": "t"}, "entry_id": "e1", "domain": "d"}
        )
        assert nested["owner"] == "t"
        with pytest.raises(InterpretationRegistryError):
            Metadata().from_mapping({"foo": 1})

        graph = DependencyGraph()
        graph.add_node("a")
        graph.add_edge("a", "b")
        assert graph.nodes() == ("a",)
        assert graph.dependencies_of("a") == ("b",)
        assert graph.dependents_of("b") == ("a",)
        assert graph.missing_dependencies() == ("b",)
        graph.build_from_entries((_entry("a", dependencies=("b",)),))
        assert graph.missing_dependencies((_entry("a", dependencies=("b",)),)) == ("b",)

    def test_registry_invalid_entry_and_cycle(self) -> None:
        """Invalid entries and cycles fail validation."""
        registry = Registry()
        with pytest.raises(InterpretationRegistryError, match="registry_entry_invalid"):
            registry.register(
                InterpreterRegistryEntry(
                    entry_id="",
                    interpreter_id="",
                    name="",
                )
            )
        registry.register(_entry("a", dependencies=("b",)))
        registry.register(_entry("b", dependencies=("a",)))
        assert registry.validate() is False

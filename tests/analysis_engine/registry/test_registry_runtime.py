"""Registry runtime integration tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.registry.dependency_graph import DependencyGraph
from engines.analysis_engine.registry.metadata_loader import MetadataLoader
from engines.analysis_engine.registry.module_loader import ModuleLoader
from engines.analysis_engine.registry.registry_builder import RegistryBuilder
from engines.analysis_engine.registry.registry_models import RegistryEntry, RegistryQuerySpec
from engines.analysis_engine.registry.registry_service import RegistryService
from engines.analysis_engine.registry.version_resolver import VersionResolver


class TestRegistryRuntimeIntegration:
    """Integration coverage for Pack 01-compatible registry runtime services."""

    def test_register_query_resolve_and_version(self) -> None:
        """Service should support register/query/resolve/version flows."""
        service = RegistryService()
        v1 = RegistryEntry(
            entry_id="registry_rule_000001",
            object_type="rule",
            name="mock_rule",
            version="1.0.0",
            status="active",
            metadata={"object_id": "rule_mock_001", "tags": ["mock"]},
            references=(),
        )
        v2 = RegistryEntry(
            entry_id="registry_rule_000002",
            object_type="rule",
            name="mock_rule",
            version="1.1.0",
            status="active",
            metadata={"object_id": "rule_mock_001"},
            references=("registry_rule_000001",),
        )
        service.register(v1)
        service.register(v2)

        matches = service.query(RegistryQuerySpec(object_type="rule", tags=("mock",)))
        assert [entry.entry_id for entry in matches] == ["registry_rule_000001"]
        assert service.resolve("registry_rule_000001") is not None
        assert service.resolve_version("rule", "mock_rule").version == "1.1.0"
        assert service.resolve_version(
            "rule",
            "mock_rule",
            requested_version="1.0.0",
        ).version == "1.0.0"

    def test_dependency_graph_order_and_cycle(self) -> None:
        """Dependency graph should order deps and detect cycles."""
        a = RegistryEntry(
            entry_id="a",
            object_type="t",
            name="a",
            references=(),
        )
        b = RegistryEntry(
            entry_id="b",
            object_type="t",
            name="b",
            references=("a",),
        )
        graph = DependencyGraph()
        graph.build_from_entries((a, b))
        order = graph.topological_order()
        assert order.index("a") < order.index("b")

        c1 = RegistryEntry(entry_id="c1", object_type="t", name="c1", references=("c2",))
        c2 = RegistryEntry(entry_id="c2", object_type="t", name="c2", references=("c1",))
        cyclic = DependencyGraph()
        cyclic.build_from_entries((c1, c2))
        assert cyclic.has_cycle() is True

    def test_module_loader_pack_registry(self) -> None:
        """Module loader should read PACK_01 descriptors read-only."""
        knowledge_root = Path("knowledge")
        loader = ModuleLoader(knowledge_root=knowledge_root)
        assert loader.supports_pack("PACK_01") is True
        snapshot = loader.load_pack_registry("PACK_01")
        assert any(entry.entry_id == "PACK_01" for entry in snapshot.entries)

    def test_builder_and_metadata(self) -> None:
        """Builder and metadata loader should operate without business rules."""
        registry = RegistryBuilder().create()
        entry = RegistryEntry(
            entry_id="e1",
            object_type="sentence",
            name="s1",
            metadata={"owner": "test"},
        )
        registry.register(entry)
        snap = RegistryBuilder().build_snapshot(registry)
        assert snap.entries[0].entry_id == "e1"
        meta = MetadataLoader().load_from_entry(entry)
        assert meta["owner"] == "test"

    def test_version_resolver_missing(self) -> None:
        """Version resolver should raise when no candidates exist."""
        with pytest.raises(RegistryError):
            VersionResolver().resolve(())

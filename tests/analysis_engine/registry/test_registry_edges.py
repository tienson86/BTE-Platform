"""Additional registry infrastructure edge-case tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.registry.cache_service import CacheService
from engines.analysis_engine.registry.dependency_graph import DependencyGraph
from engines.analysis_engine.registry.metadata_loader import MetadataLoader
from engines.analysis_engine.registry.module_loader import ModuleLoader
from engines.analysis_engine.registry.query_engine import QueryEngine
from engines.analysis_engine.registry.registry_index import RegistryIndex
from engines.analysis_engine.registry.registry_loader import RegistryLoader
from engines.analysis_engine.registry.registry_models import (
    RegistryEntry,
    RegistryQuerySpec,
    RegistrySnapshot,
)
from engines.analysis_engine.registry.registry_query import RegistryQuery
from engines.analysis_engine.registry.registry_service import RegistryService
from engines.analysis_engine.registry.version_resolver import VersionResolver


class TestRegistryInfrastructureEdges:
    """Extra coverage for registry runtime services."""

    def test_unregister_clear_cache_and_query_engine(self) -> None:
        """Service lifecycle helpers and query engine should work."""
        service = RegistryService()
        entry = RegistryEntry(
            entry_id="e1",
            object_type="rule",
            name="n1",
            metadata={"object_id": "obj1", "tags": "solo"},
        )
        service.register(entry)
        assert service.query_engine.exists("e1") is True
        assert service.query_engine.lookup("e1") is not None
        assert service.query_engine.count(RegistryQuerySpec(object_type="rule")) == 1
        assert service.resolve("obj1") is not None
        service.unregister("e1")
        assert service.get("e1") is None
        service.register(entry)
        service.clear()
        assert service.list_entries() == ()

        cache = CacheService()
        cache.put_entry(entry)
        cache.put_snapshot(
            RegistrySnapshot(snapshot_id="s1", schema_version="1.0.0", entries=(entry,))
        )
        assert cache.get_entry("e1") is not None
        assert cache.get_snapshot("s1") is not None
        cache.invalidate("e1")
        assert cache.get_entry("e1") is None
        cache.clear()
        assert cache.size() == (0, 0)

    def test_module_loader_snapshot_and_records(self, tmp_path: Path) -> None:
        """Module loader should parse entries and records payloads."""
        snapshot_path = tmp_path / "snap.json"
        snapshot_path.write_text(
            json.dumps(
                {
                    "snapshot_id": "snap1",
                    "schema_version": "1.0.0",
                    "entries": [
                        {
                            "entry_id": "entry_a",
                            "object_type": "rule",
                            "name": "A",
                            "version": "1.0.0",
                            "status": "active",
                            "references": ["entry_b"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        loader = ModuleLoader()
        snap = loader.load_snapshot(snapshot_path)
        assert snap.entries[0].entry_id == "entry_a"
        assert loader.list_entry_ids(snapshot_path) == ("entry_a",)

        record_path = tmp_path / "records.json"
        record_path.write_text(
            json.dumps(
                {
                    "version": "1.0.0",
                    "records": [
                        {
                            "identity": {
                                "registry_id": "RREG-000001",
                                "object_id": "obj",
                                "namespace": "rules",
                            },
                            "metadata": {
                                "version": "1.0.0",
                                "status": "draft",
                                "owner": "t",
                                "created_date": "",
                                "updated_date": "",
                            },
                            "object": {
                                "canonical_name": "Rule A",
                                "object_type": "rule",
                            },
                            "classification": {"tags": ["mock"], "domain": "d"},
                            "dependencies": [{"registry_id": "RREG-000002"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        records = loader.load_snapshot(record_path)
        assert records.entries[0].entry_id == "RREG-000001"
        meta = MetadataLoader().load_from_entry(records.entries[0])
        assert meta["entry_id"] == "RREG-000001"
        single_record = tmp_path / "one_record.json"
        single_record.write_text(
            json.dumps(
                {
                    "identity": {"registry_id": "RREG-000009", "object_id": "o", "namespace": "n"},
                    "metadata": {
                        "version": "1.0.0",
                        "status": "draft",
                        "owner": "t",
                        "created_date": "",
                        "updated_date": "",
                    },
                }
            ),
            encoding="utf-8",
        )
        loaded_meta = MetadataLoader().load_from_path(single_record)
        assert loaded_meta["registry_id"] == "RREG-000009"

        facade = RegistryLoader(module_loader=loader)
        registry = facade.load_from_path(snapshot_path)
        assert registry.get("entry_a") is not None

    def test_version_resolver_compatible_and_compare(self) -> None:
        """Version resolver should compare and resolve compatible versions."""
        resolver = VersionResolver()
        assert resolver.compare("1.0.0", "1.0.1") == -1
        assert resolver.is_compatible("1.1.0", "1.0.0") is True
        entries = (
            RegistryEntry(
                entry_id="a",
                object_type="rule",
                name="n",
                version="1.0.0",
                status="deprecated",
            ),
            RegistryEntry(
                entry_id="b",
                object_type="rule",
                name="n",
                version="1.2.0",
                status="active",
            ),
        )
        resolved = resolver.resolve(
            entries,
            requested_version="1.0.5",
            allow_compatible=True,
            allow_deprecated=False,
        )
        assert resolved.entry_id == "b"
        with pytest.raises(RegistryError):
            resolver.resolve(entries, requested_version="9.0.0", allow_compatible=False)
        deprecated = resolver.resolve(
            (entries[0],),
            requested_version="1.0.0",
            allow_compatible=False,
            allow_deprecated=True,
        )
        assert deprecated.entry_id == "a"

    def test_dependency_missing_and_index_query(self) -> None:
        """Missing dependencies and index/query facades should work."""
        entry = RegistryEntry(
            entry_id="x",
            object_type="t",
            name="x",
            references=("missing",),
        )
        graph = DependencyGraph()
        graph.build_from_entries((entry,))
        assert graph.missing_dependencies() == ("missing",)
        assert graph.dependencies_of("x") == ("missing",)

        index = RegistryIndex()
        index.index_entry(
            RegistryEntry(entry_id="i1", object_type="rule", name="alpha")
        )
        assert index.find_by_type("rule") == ("i1",)
        assert index.find_by_name("alpha") == ("i1",)
        index.remove_entry("i1")
        assert index.find_by_type("rule") == ()

        service = RegistryService()
        service.register(
            RegistryEntry(entry_id="q1", object_type="rule", name="q", status="active")
        )
        query = RegistryQuery(service=service)
        assert query.exists("q1") is True
        assert query.count(RegistryQuerySpec(status="active")) == 1

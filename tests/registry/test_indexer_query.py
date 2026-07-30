"""Unit tests for RegistryIndexer and RegistryQuery."""

from __future__ import annotations

import pytest

from services.registry_exceptions import RegistryQueryError
from services.registry_indexer import RegistryIndexer
from services.registry_loader import RegistryLoader
from services.registry_query import RegistryQuery


def test_reindex_parallel(loader: RegistryLoader) -> None:
    indexer = RegistryIndexer(loader, max_workers=2)
    indexes = indexer.reindex(parallel=True)
    assert "by_registry" in indexes
    assert "by_status" in indexes
    assert "by_namespace" in indexes
    by_registry = indexes["by_registry"]
    knowledge = next(entry for entry in by_registry.entries if entry.key == "knowledge_registry")
    assert len(knowledge.registry_ids) == 2


def test_reindex_sequential(loader: RegistryLoader) -> None:
    indexes = RegistryIndexer(loader).reindex(parallel=False)
    assert indexes["by_object_id"].entries


def test_list_and_get(loader: RegistryLoader) -> None:
    query = RegistryQuery(loader)
    hits = query.list_records(registry_name="knowledge_registry", status="published")
    assert len(hits) == 1
    assert hits[0].registry_id == "KREG-000001"
    record = query.get_by_registry_id("KREG-000001")
    assert record is not None
    assert query.get_by_object_id("RUL-000001") is not None
    assert query.get_by_registry_id("missing") is None


def test_search(loader: RegistryLoader) -> None:
    query = RegistryQuery(loader)
    hits = query.search("KREG-000001")
    assert hits
    assert hits[0].score >= 1.0
    with pytest.raises(RegistryQueryError):
        query.search("   ")

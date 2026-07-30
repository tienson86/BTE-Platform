"""Unit tests for Knowledge loaders and cache."""

from __future__ import annotations

from pathlib import Path

import pytest

from services.knowledge.cache import MtimeCache
from services.knowledge.exceptions import KnowledgeLoadError
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.record_loader import RecordLoader
from services.knowledge.schema_loader import SchemaLoader


def test_mtime_cache(tmp_path: Path) -> None:
    import os
    import time

    cache: MtimeCache[str] = MtimeCache()
    path = tmp_path / "a.txt"
    path.write_text("one", encoding="utf-8")
    cache.set(path, "v1")
    assert cache.get(path) == "v1"
    assert len(cache) == 1
    time.sleep(0.02)
    path.write_text("two", encoding="utf-8")
    os.utime(path, None)
    assert cache.get(path) is None
    cache.clear()
    assert len(cache) == 0


def test_schema_loader_loads_foundation(schema_root: Path) -> None:
    loader = SchemaLoader(schema_root)
    docs = loader.load_all()
    assert len(docs) >= 20
    base = loader.load_schema("knowledge_record.schema.json")
    assert "identity" in base.raw["properties"]
    five = loader.schema_for_domain("01_five_elements")
    assert five.name == "five_element.schema.json"
    assert loader.build_registry() is not None


def test_record_loader_skips_schema_files(loader: KnowledgeLoader) -> None:
    records = loader.load_records()
    assert len(records) == 2
    assert {item.knowledge_id for item in records} == {"KNO-000001", "KNO-000002"}
    assert loader.get_record("KNO-000001") is not None
    assert loader.get_record("missing") is None


def test_record_loader_cache(loader: KnowledgeLoader) -> None:
    first = loader.record_loader.load_domain("01_five_elements")
    second = loader.record_loader.load_domain("01_five_elements")
    assert first[0] is second[0]
    loader.clear_cache()
    third = loader.record_loader.load_domain("01_five_elements")
    assert first[0] is not third[0]


def test_dependencies(loader: KnowledgeLoader) -> None:
    edges = loader.load_dependencies()
    assert "KNO-000001" in edges["KNO-000002"]
    assert "KNO-000001" not in edges or "KNO-000002" not in edges.get("KNO-000001", [])


def test_stats_and_export(loader: KnowledgeLoader, tmp_path: Path) -> None:
    stats = loader.stats()
    assert stats.total_records == 2
    assert stats.schema_count >= 20
    bundle = loader.export_bundle()
    assert len(bundle["records"]) == 2


def test_missing_record_raises(canon_root: Path) -> None:
    with pytest.raises(KnowledgeLoadError):
        RecordLoader(canon_root).load_record(canon_root / "missing.json")

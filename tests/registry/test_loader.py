"""Unit tests for RegistryLoader."""

from __future__ import annotations

from pathlib import Path

import pytest

from services.registry_exceptions import RegistryLoadError
from services.registry_loader import RegistryLoader


def test_load_all_catalogs(loader: RegistryLoader) -> None:
    catalogs = loader.load_all_catalogs()
    names = {catalog.name for catalog in catalogs}
    assert "knowledge_registry" in names
    assert "rule_registry" in names


def test_lazy_cache_hit(loader: RegistryLoader) -> None:
    first = loader.load_catalog("knowledge_registry/knowledge_registry.json")
    second = loader.load_catalog("knowledge_registry/knowledge_registry.json")
    assert first is second


def test_clear_cache(loader: RegistryLoader) -> None:
    first = loader.load_catalog("knowledge_registry/knowledge_registry.json")
    loader.clear_cache()
    second = loader.load_catalog("knowledge_registry/knowledge_registry.json")
    assert first is not second
    assert first.checksum == second.checksum


def test_missing_catalog_raises(loader: RegistryLoader) -> None:
    with pytest.raises(RegistryLoadError):
        loader.load_catalog("missing/missing.json")


def test_invalid_json_raises(registry_root: Path) -> None:
    bad = registry_root / "knowledge_registry" / "knowledge_registry.json"
    bad.write_text("{not-json", encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    with pytest.raises(RegistryLoadError):
        loader.load_catalog(bad)


def test_iter_records(loader: RegistryLoader) -> None:
    pairs = loader.iter_records()
    assert len(pairs) == 3

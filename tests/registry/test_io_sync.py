"""Unit tests for export/import/statistics/sync."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.registry_exceptions import RegistryIOError
from services.registry_exporter import RegistryExporter
from services.registry_importer import RegistryImporter
from services.registry_loader import RegistryLoader
from services.registry_statistics import RegistryStatistics
from services.registry_sync import RegistrySync


def test_export_all_and_bundle(loader: RegistryLoader, tmp_path: Path) -> None:
    exporter = RegistryExporter(loader)
    written = exporter.export_all(tmp_path / "out", include_indexes=True)
    assert any(path.name == "manifest.json" for path in written)
    bundle = exporter.export_bundle(tmp_path / "bundle.json", include_indexes=True)
    payload = json.loads(bundle.read_text(encoding="utf-8"))
    assert "knowledge_registry" in payload["catalogs"]
    assert "indexes" in payload


def test_export_single_catalog(loader: RegistryLoader, tmp_path: Path) -> None:
    path = RegistryExporter(loader).export_catalog(
        "knowledge_registry",
        tmp_path / "knowledge_registry.json",
    )
    assert path.exists()


def test_export_unknown_catalog(loader: RegistryLoader, tmp_path: Path) -> None:
    with pytest.raises(RegistryIOError):
        RegistryExporter(loader).export_catalog("nope", tmp_path / "x.json")


def test_import_catalog_dry_run(loader: RegistryLoader, tmp_path: Path) -> None:
    source = tmp_path / "incoming.json"
    source.write_text(
        json.dumps(
            {
                "version": "1.0.0",
                "registry_name": "dataset_registry",
                "registry_prefix": "DREG",
                "records": [],
            }
        ),
        encoding="utf-8",
    )
    dest = RegistryImporter(loader).import_catalog_file(source, dry_run=True)
    assert "dataset_registry" in str(dest)
    assert not dest.exists()


def test_import_bundle(loader: RegistryLoader, tmp_path: Path) -> None:
    bundle = RegistryExporter(loader).export_bundle(tmp_path / "bundle.json")
    # Import into a fresh empty target folder name already present.
    imported = RegistryImporter(loader).import_bundle(bundle, dry_run=True)
    assert imported


def test_statistics_and_sync(loader: RegistryLoader, tmp_path: Path) -> None:
    stats = RegistryStatistics(loader).compute()
    assert stats.total_records == 3
    assert stats.by_registry["knowledge_registry"] == 2

    sync = RegistrySync(loader)
    payload = sync.sync_all(write=True, parallel=True)
    assert payload["statistics"]["statistics"]["total_records"] == 3
    derived = loader.registry_root / ".derived" / "indexes" / "by_status.json"
    # write indexes go to .derived when write=True via reindex
    assert (loader.registry_root / "global_registry" / "registry_statistics.json").exists()
    indexes = sync.reindex(write=True, output_dir=tmp_path / "indexes")
    assert "by_registry" in indexes

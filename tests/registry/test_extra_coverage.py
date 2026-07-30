"""Extra coverage tests for registry edge paths."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.registry_checksum import verify_checksum
from services.registry_exceptions import RegistryIOError, RegistryLoadError
from services.registry_importer import RegistryImporter
from services.registry_loader import RegistryLoader
from services.registry_validator import RegistryValidator


def test_verify_checksum_payload_and_errors() -> None:
    digest = "a" * 64
    assert verify_checksum(digest, payload={"x": 1}) is False
    assert verify_checksum("", payload={"x": 1}) is False
    with pytest.raises(ValueError):
        verify_checksum(digest)


def test_loader_default_project_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    loader = RegistryLoader()
    assert loader.project_root == tmp_path.resolve()


def test_loader_non_object_json(registry_root: Path) -> None:
    path = registry_root / "knowledge_registry" / "knowledge_registry.json"
    path.write_text("[1,2,3]", encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    with pytest.raises(RegistryLoadError):
        loader.load_catalog(path)


def test_loader_records_must_be_list(registry_root: Path) -> None:
    path = registry_root / "knowledge_registry" / "knowledge_registry.json"
    path.write_text(
        '{"version":"1.0.0","records":{}}',
        encoding="utf-8",
    )
    loader = RegistryLoader(registry_root=registry_root)
    with pytest.raises(RegistryLoadError):
        loader.load_catalog(path)


def test_validator_missing_json_file(registry_root: Path) -> None:
    (
        registry_root / "global_registry" / "namespace_registry.json"
    ).unlink()
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_json_files()
    assert not result.ok
    assert any(issue.code == "missing_file" for issue in result.errors)


def test_validator_invalid_registry_id(registry_root: Path) -> None:
    path = registry_root / "knowledge_registry" / "knowledge_registry.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"][0]["identity"]["registry_id"] = "BAD-1"
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_all()
    assert any(issue.code == "invalid_registry_id" for issue in result.errors)


def test_validator_duplicate_uri_and_object_id(registry_root: Path) -> None:
    path = registry_root / "knowledge_registry" / "knowledge_registry.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    clone = json.loads(json.dumps(payload["records"][0]))
    clone["identity"]["registry_id"] = "KREG-000099"
    # same object_id and uri -> duplicates
    payload["records"].append(clone)
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    issues = RegistryValidator(loader).detect_duplicates()
    codes = {issue.code for issue in issues}
    assert "duplicate_object_id" in codes
    assert "duplicate_uri" in codes


def test_validator_unknown_namespace_and_type(registry_root: Path) -> None:
    path = registry_root / "knowledge_registry" / "knowledge_registry.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"][0]["identity"]["namespace"] = "mystery"
    payload["records"][0]["object"]["object_type"] = "mystery_type"
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_all()
    codes = {issue.code for issue in result.warnings}
    assert "unknown_namespace" in codes
    assert "unknown_object_type" in codes


def test_validator_missing_sample(registry_root: Path) -> None:
    (registry_root / "samples" / "empty_registry_record.json").unlink()
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_all(include_samples=True)
    assert any(issue.code == "missing_sample" for issue in result.warnings)


def test_import_real_write_and_failures(
    loader: RegistryLoader,
    tmp_path: Path,
) -> None:
    importer = RegistryImporter(loader)
    source = tmp_path / "dataset_registry.json"
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
    dest = importer.import_catalog_file(source, validate=True, dry_run=False)
    assert dest.exists()

    with pytest.raises(RegistryIOError):
        importer.import_catalog_file(tmp_path / "missing.json")

    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(RegistryIOError):
        importer.import_catalog_file(bad)

    no_records = tmp_path / "norec.json"
    no_records.write_text('{"version":"1.0.0"}', encoding="utf-8")
    with pytest.raises(RegistryIOError):
        importer.import_catalog_file(no_records)

    bundle = tmp_path / "bundle.json"
    bundle.write_text('{"version":"1.0.0"}', encoding="utf-8")
    with pytest.raises(RegistryIOError):
        importer.import_bundle(bundle)


def test_cli_export_bundle_and_import(
    registry_root: Path,
    tmp_path: Path,
) -> None:
    import registry_cli

    bundle = tmp_path / "bundle.json"
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "export",
                "--bundle",
                "--output",
                str(bundle),
                "--include-indexes",
            ]
        )
        == 0
    )
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "import",
                "--source",
                str(bundle),
                "--bundle",
                "--dry-run",
            ]
        )
        == 0
    )
    single = tmp_path / "kr.json"
    assert (
        registry_cli.main(
            [
                "--registry-root",
                str(registry_root),
                "export",
                "--registry",
                "knowledge_registry",
                "--output",
                str(single),
            ]
        )
        == 0
    )


def test_indexer_get_index_and_clear(loader: RegistryLoader) -> None:
    from services.registry_indexer import RegistryIndexer

    indexer = RegistryIndexer(loader)
    assert indexer.get_index("by_status") is not None
    indexer.clear_cache()
    assert indexer.get_index("by_domain") is not None


def test_query_filters(loader: RegistryLoader) -> None:
    from services.registry_query import RegistryQuery

    query = RegistryQuery(loader)
    hits = query.list_records(namespace="rule", limit=1)
    assert len(hits) == 1
    assert hits[0].registry_id == "RREG-000001"

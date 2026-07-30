"""Unit tests for RegistryValidator."""

from __future__ import annotations

import json
from pathlib import Path

from services.registry_loader import RegistryLoader
from services.registry_validator import RegistryValidator


def test_validate_all_ok(loader: RegistryLoader) -> None:
    validator = RegistryValidator(loader)
    result = validator.validate_all(include_samples=True)
    assert result.ok
    assert result.records_checked == 3
    assert result.catalogs_checked == 2


def test_validate_json_files(loader: RegistryLoader) -> None:
    result = RegistryValidator(loader).validate_json_files()
    assert result.ok


def test_duplicate_registry_id_detected(
    registry_root: Path,
) -> None:
    catalog = registry_root / "knowledge_registry" / "knowledge_registry.json"
    payload = json.loads(catalog.read_text(encoding="utf-8"))
    payload["records"].append(payload["records"][0])
    catalog.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    issues = RegistryValidator(loader).detect_duplicates()
    assert any(issue.code == "duplicate_registry_id" for issue in issues)


def test_broken_dependency_detected(registry_root: Path) -> None:
    catalog = registry_root / "rule_registry" / "rule_registry.json"
    payload = json.loads(catalog.read_text(encoding="utf-8"))
    payload["records"][0]["dependencies"] = ["KREG-999999"]
    catalog.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_all()
    assert any(issue.code == "broken_dependency" for issue in result.errors)


def test_circular_dependency_detected(registry_root: Path) -> None:
    catalog = registry_root / "knowledge_registry" / "knowledge_registry.json"
    payload = json.loads(catalog.read_text(encoding="utf-8"))
    payload["records"][0]["dependencies"] = ["KREG-000002"]
    payload["records"][1]["dependencies"] = ["KREG-000001"]
    catalog.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_all()
    assert any(issue.code == "circular_dependency" for issue in result.errors)


def test_invalid_status_detected(registry_root: Path) -> None:
    catalog = registry_root / "knowledge_registry" / "knowledge_registry.json"
    payload = json.loads(catalog.read_text(encoding="utf-8"))
    payload["records"][0]["metadata"]["status"] = "not-a-status"
    catalog.write_text(json.dumps(payload), encoding="utf-8")
    loader = RegistryLoader(registry_root=registry_root)
    result = RegistryValidator(loader).validate_all()
    assert any(issue.code == "invalid_status" for issue in result.errors)

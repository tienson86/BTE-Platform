"""Package-level tests for bz_01_strength_core. No engine imports."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        objects.extend(payload["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_01_strength_core"
    assert package["package_type"] == "analytical"
    assert package["schema_version"] == "2.0.0"
    assert package["package_version"] == "1.2.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["checksum"]["algorithm"] == "sha256"
    assert package["checksum"]["value"]
    assert len(package["checksum"]["value"]) == 64


def test_manifest_valid() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["package_id"] == "bz_01_strength_core"
    assert manifest["validation_profile"] == "PVP-RELEASE"
    assert manifest["required_packages"] == []
    assert manifest["components"]["documentation"]["present"] is True
    assert manifest["components"]["rules"]["present"] is True
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported)
    assert len(exported) == len(set(exported))


@pytest.mark.skipif(
    not SPEC.exists(),
    reason="package_spec schemas not available",
)
def test_identity_and_manifest_against_kd3_schema() -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        pytest.skip("jsonschema not installed")

    schemas = {}
    registry = Registry()
    for name in (
        "package.schema.json",
        "package_manifest.schema.json",
        "package_dependency.schema.json",
        "package_release.schema.json",
        "package_validation.schema.json",
    ):
        data = json.loads((SPEC / name).read_text(encoding="utf-8"))
        schemas[name] = data
        resource = Resource.from_contents(data)
        registry = registry.with_resource(name, resource)
        if "$id" in data:
            registry = registry.with_resource(data["$id"], resource)

    Draft202012Validator(schemas["package.schema.json"], registry=registry).validate(_load("PACKAGE.json"))
    Draft202012Validator(schemas["package_manifest.schema.json"], registry=registry).validate(
        _load("MANIFEST.json")
    )
    Draft202012Validator(schemas["package_dependency.schema.json"], registry=registry).validate(
        _load("DEPENDENCIES.json")
    )
    Draft202012Validator(schemas["package_release.schema.json"], registry=registry).validate(
        _load("RELEASE.json")
    )
    Draft202012Validator(schemas["package_validation.schema.json"], registry=registry).validate(
        _load("validation/VALIDATION.json")
    )


def test_rule_ids_unique_and_complete() -> None:
    rules = _rules()
    assert 80 <= len(rules) <= 120
    ids = [item["id"] for item in rules]
    assert len(ids) == len(set(ids))
    required = ("id", "category", "priority", "conditions", "result", "explanation", "references", "tags", "enabled")
    for item in rules:
        for key in required:
            assert item.get(key) not in (None, "", []), f"{item['id']} missing {key}"
        assert item["enabled"] is True
        assert item["type"] == "rule"
        assert item["id"].startswith("SKC-")


def test_metadata_valid() -> None:
    metadata = _load("metadata/package_metadata.json")
    assert metadata["package_id"] == "bz_01_strength_core"
    assert metadata["domain_id"] == "DOM-STRENGTH"
    assert metadata["config"]["strong_threshold"] == 0.65
    assert metadata["config"]["weak_threshold"] == 0.35


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    assert {item["tendency"] for item in examples} >= {"strong", "weak", "balanced"}
    for example in examples:
        assert example["activates_rules"], example["example_id"]
        missing = [rid for rid in example["activates_rules"] if rid not in rule_ids]
        assert not missing, f"{example['example_id']} missing {missing}"


def test_reference_integrity() -> None:
    refs = _load("references/references.json")["references"]
    ref_ids = [item["id"] for item in refs]
    assert len(ref_ids) == len(set(ref_ids))
    known = set(ref_ids)
    for item in _rules():
        for ref in item["references"]:
            target = ref["target"] if isinstance(ref, dict) else ref
            assert target in known, f"{item['id']} -> {target}"


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules
    imported = [name for name in ("json", "pathlib", "pytest") if name in sys.modules]
    assert imported

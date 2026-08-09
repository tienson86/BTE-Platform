"""Package-level tests for bz_03_temperature_core KX-2B. No engine imports."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_03_temperature_core"
    assert package["package_type"] == "analytical"
    assert package["package_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert len(package["checksum"]["value"]) == 64
    assert (ROOT / "RELEASE.json").is_file()
    assert (ROOT / "assets" / "climate_axes.json").is_file()


def test_manifest_valid() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["validation_profile"] == "PVP-RELEASE"
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported)
    assert len(exported) == len(set(exported))


def test_metadata_valid() -> None:
    meta = _load("metadata/package_metadata.json")
    assert meta["domain_id"] == "DOM-TEMPERATURE"
    assert meta["config"]["score_target"] == "day_master.temperature_score"


@pytest.mark.skipif(not SPEC.exists(), reason="no spec")
def test_identity_and_manifest_against_kd3_schema() -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        pytest.skip("jsonschema not installed")
    schemas = {}
    registry = Registry()
    for name in ("package.schema.json", "package_manifest.schema.json", "package_dependency.schema.json", "package_release.schema.json", "package_validation.schema.json"):
        data = json.loads((SPEC / name).read_text(encoding="utf-8"))
        schemas[name] = data
        resource = Resource.from_contents(data)
        registry = registry.with_resource(name, resource)
        if "$id" in data:
            registry = registry.with_resource(data["$id"], resource)
    Draft202012Validator(schemas["package.schema.json"], registry=registry).validate(_load("PACKAGE.json"))
    Draft202012Validator(schemas["package_manifest.schema.json"], registry=registry).validate(_load("MANIFEST.json"))
    Draft202012Validator(schemas["package_dependency.schema.json"], registry=registry).validate(_load("DEPENDENCIES.json"))
    Draft202012Validator(schemas["package_release.schema.json"], registry=registry).validate(_load("RELEASE.json"))
    Draft202012Validator(schemas["package_validation.schema.json"], registry=registry).validate(_load("validation/VALIDATION.json"))


def test_rule_ids_unique_and_complete() -> None:
    rules = _rules()
    assert 80 <= len(rules) <= 120
    ids = [item["id"] for item in rules]
    assert len(ids) == len(set(ids))
    required = ("id", "category", "priority", "conditions", "result", "explanation", "references", "tags", "enabled")
    for item in rules:
        for key in required:
            assert item.get(key) not in (None, "", []), item["id"]
        assert item["id"].startswith("TEC-")
        assert item["result"]["score_target"] == "day_master.temperature_score"
        assert item["result"]["score_target"] not in {"day_master.strength_score", "day_master.season_score"}


def test_coverage_categories() -> None:
    cats = {item["category"] for item in _rules()}
    for req in ("cold_climate", "hot_climate", "dry_climate", "damp_climate", "balanced_climate", "seasonal_temp_adjustment", "dm_temperature_support", "temperature_imbalance", "climate_correction", "temperature_scoring"):
        assert req in cats


def test_evidence_links() -> None:
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["positive_examples"] and data["negative_examples"]


def test_reasoning_links() -> None:
    rule_ids = {item["id"] for item in _rules()}
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 3
    for name in ("cold", "hot", "balanced"):
        chain = _load(f"reasoning/chains/{name}.json")
        assert chain["dependency_chain"] == ["calendar", "four_pillars", "seasonal", "strength", "temperature"]
        assert chain["upstream_seasonal_rules"] and chain["upstream_strength_rules"]
        for rid in chain["rule_ids"]:
            assert rid in rule_ids
            assert (ROOT / f"evidence/bundles/{rid}.json").is_file()


def test_upstream_ids_exist_in_released_packages() -> None:
    seasonal_ids = set()
    for path in (KNOWLEDGE / "packages" / "seasonal" / "core" / "rules").glob("*.json"):
        seasonal_ids.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
    strength_ids = set()
    for path in (KNOWLEDGE / "packages" / "strength" / "core" / "rules").glob("*.json"):
        strength_ids.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
    for name in ("cold", "hot", "balanced"):
        chain = _load(f"reasoning/chains/{name}.json")
        for rid in chain["upstream_seasonal_rules"]:
            assert rid in seasonal_ids, rid
        for rid in chain["upstream_strength_rules"]:
            assert rid in strength_ids, rid


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    climates = {item["climate"] for item in examples}
    assert climates >= {"cold", "hot", "balanced", "dry", "damp"}
    for example in examples:
        assert example["activates_rules"] and example["activated_evidence"] and example["reasoning_path"]
        assert not [r for r in example["activates_rules"] if r not in rule_ids]


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


def test_no_v1_tmp_collision() -> None:
    for item in _rules():
        assert not item["id"].startswith("TMP-")


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

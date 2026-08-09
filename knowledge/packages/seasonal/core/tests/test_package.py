"""Package-level tests for bz_02_seasonal_core KX-2A. No engine imports."""
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
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_02_seasonal_core"
    assert package["package_type"] == "analytical"
    assert package["package_version"] == "1.0.0"
    assert package["schema_version"] == "2.0.0"
    assert package["knowledge_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert package["checksum"]["algorithm"] == "sha256"
    assert len(package["checksum"]["value"]) == 64
    assert (ROOT / "assets" / "season_phase_matrix.json").is_file()
    assert (ROOT / "RELEASE.json").is_file()
    assert (ROOT / "RELEASE_NOTES.md").is_file()


def test_manifest_valid() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["package_id"] == "bz_02_seasonal_core"
    assert manifest["validation_profile"] == "PVP-RELEASE"
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported)
    assert len(exported) == len(set(exported))


def test_metadata_valid() -> None:
    meta = _load("metadata/package_metadata.json")
    assert meta["package_id"] == "bz_02_seasonal_core"
    assert meta["domain_id"] == "DOM-SEASONAL"
    assert meta["config"]["score_target"] == "day_master.season_score"


@pytest.mark.skipif(not SPEC.exists(), reason="package_spec schemas not available")
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
    Draft202012Validator(schemas["package_manifest.schema.json"], registry=registry).validate(_load("MANIFEST.json"))
    Draft202012Validator(schemas["package_dependency.schema.json"], registry=registry).validate(_load("DEPENDENCIES.json"))
    Draft202012Validator(schemas["package_release.schema.json"], registry=registry).validate(_load("RELEASE.json"))
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
        assert item["id"].startswith("SEC-")
        assert item["result"]["score_target"] == "day_master.season_score"


def test_coverage_categories() -> None:
    cats = {item["category"] for item in _rules()}
    for required in (
        "month_branch",
        "current_season",
        "seasonal_qi_phase",
        "seasonal_element_support",
        "seasonal_element_restriction",
        "month_branch_weight",
        "seasonal_scoring",
    ):
        assert required in cats


def test_evidence_links() -> None:
    for item in _rules():
        bundle = ROOT / "evidence" / "bundles" / f"{item['id']}.json"
        assert bundle.is_file(), item["id"]
        data = json.loads(bundle.read_text(encoding="utf-8"))
        assert data["positive_examples"] and data["negative_examples"]
        assert data["explanation"] and data["rationale"]


def test_reasoning_links() -> None:
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 3
    rule_ids = {item["id"] for item in _rules()}
    for name in ("strong", "weak", "balanced"):
        chain = _load(f"reasoning/chains/{name}.json")
        assert chain["stages"][0]["stage"] == "observation"
        assert chain["stages"][-1]["stage"] == "final_conclusion"
        for rid in chain["rule_ids"]:
            assert rid in rule_ids
            assert (ROOT / f"evidence/bundles/{rid}.json").is_file()


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    seasons = {item["season"] for item in examples}
    assert seasons >= {"spring", "summer", "autumn", "winter", "transition"}
    for example in examples:
        assert example["activates_rules"]
        assert example["activated_evidence"]
        assert example["reasoning_path"]
        missing = [rid for rid in example["activates_rules"] if rid not in rule_ids]
        assert not missing, example["example_id"]


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


def test_no_v1_sea_collision() -> None:
    for item in _rules():
        assert not item["id"].startswith("SEA-")


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

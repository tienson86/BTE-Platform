"""Package-level tests for bz_06_useful_god_foundation KX-4A."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
INPUTS = {
    "season_score", "strength_score", "temperature_score", "pattern_score",
    "pattern_quality", "pattern_confidence", "pattern_integrity", "pattern_stability",
}
INTERNAL_PREFIXES = ("decision_", "candidate_", "published_")


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_06_useful_god_foundation"
    assert package["package_type"] == "decision"
    assert package["package_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert len(package["checksum"]["value"]) == 64
    assert (ROOT / "assets" / "published_inputs.json").is_file()
    assert (ROOT / "assets" / "published_outputs.json").is_file()


def test_manifest_valid() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["validation_profile"] == "PVP-RELEASE"
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported) and len(exported) == len(set(exported))


def test_metadata_valid() -> None:
    meta = _load("metadata/package_metadata.json")
    assert meta["domain_id"] == "DOM-USEFUL_GOD"
    assert meta["category_id"] == "foundation"
    assert meta["config"]["score_target"] == "day_master.decision_score"
    assert meta["config"]["package_kind"] == "decision"


@pytest.mark.skipif(not SPEC.exists(), reason="no spec")
def test_identity_and_manifest_against_kd3_schema() -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        pytest.skip("jsonschema not installed")
    schemas, registry = {}, Registry()
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
    forbidden = {"day_master.strength_score", "day_master.season_score", "day_master.temperature_score", "day_master.pattern_score"}
    for item in rules:
        for key in required:
            assert item.get(key) not in (None, "", []), item["id"]
        assert item["id"].startswith("UGD-")
        assert item["result"]["score_target"] == "day_master.decision_score"
        assert item["result"]["score_target"] not in forbidden


def test_input_contract_compliance() -> None:
    for item in _rules():
        for cond in item["conditions"]:
            field = cond["field"]
            if field in INPUTS:
                continue
            assert field.startswith(INTERNAL_PREFIXES) or field == "decision_score_raw", (item["id"], field)


def test_coverage_and_contracts() -> None:
    cats = {item["category"] for item in _rules()}
    for req in ("decision_prerequisites", "decision_eligibility", "candidate_useful_gods", "candidate_favorable_gods", "candidate_unfavorable_gods", "decision_confirmation", "decision_suppression", "decision_confidence", "decision_scoring", "decision_publication"):
        assert req in cats
    inputs = {i["name"] for i in _load("assets/published_inputs.json")["inputs"]}
    assert inputs == INPUTS
    outputs = {o["name"] for o in _load("assets/published_outputs.json")["outputs"]}
    assert outputs == {"useful_god", "favorable_gods", "unfavorable_gods", "decision_confidence", "decision_score", "decision_reasoning", "decision_diagnostics"}


def test_evidence_links() -> None:
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["positive_examples"] and data["negative_examples"]


def test_reasoning_links() -> None:
    rule_ids = {item["id"] for item in _rules()}
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 3
    expected = ["calendar", "four_pillars", "seasonal", "strength", "temperature", "pattern", "pattern_evaluation", "useful_god"]
    for name in ("strong", "weak", "conflict"):
        chain = _load(f"reasoning/chains/{name}.json")
        assert chain["dependency_chain"] == expected
        assert set(chain["consumed_published_inputs"]) == INPUTS
        for rid in chain["rule_ids"]:
            assert rid in rule_ids


def test_dependency_declarations() -> None:
    deps = _load("DEPENDENCIES.json")
    optional = {item["package_id"]: item for item in deps["optional"]}
    assert set(optional) >= {"bz_01_strength_core", "bz_02_seasonal_core", "bz_03_temperature_core", "bz_05_pattern_evaluation"}
    assert deps["required"] == []
    assert "strength_score" in optional["bz_01_strength_core"]["signals"]
    assert "pattern_quality" in optional["bz_05_pattern_evaluation"]["signals"]


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    tendencies = {item["tendency"] for item in examples}
    assert tendencies >= {"clear_useful_god", "multiple_candidates", "weak_decision", "conflicting_decision", "low_confidence_decision"}
    for example in examples:
        assert set(example["consumed_outputs"]) == INPUTS
        assert example["activates_rules"] and example["reasoning_path"]
        assert "final_decision" in example
        assert not [r for r in example["activates_rules"] if r not in rule_ids]


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

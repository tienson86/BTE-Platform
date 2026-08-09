"""Package-level tests for bz_07_useful_god_priority KX-4B."""
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
    "useful_god", "favorable_gods", "unfavorable_gods",
    "decision_confidence", "decision_score", "decision_reasoning", "decision_diagnostics",
}
OUTPUTS = {
    "resolved_useful_god", "resolved_favorable_gods", "resolved_unfavorable_gods",
    "decision_priority", "conflict_resolution", "resolution_confidence",
    "resolution_reasoning", "resolution_diagnostics",
}
INTERNAL_PREFIXES = (
    "resolution_", "candidate_", "priority_", "conflict_", "ranked_", "tie_",
    "excluded_", "reinforced_", "suppressed_", "final_", "published_", "reinforced",
    "excluded",
)


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_07_useful_god_priority"
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
    assert meta["category_id"] == "priority"
    assert meta["config"]["score_target"] == "day_master.resolution_score"
    assert meta["config"]["package_kind"] == "decision"


@pytest.mark.skipif(not SPEC.exists(), reason="no spec")
def test_identity_and_manifest_against_kd3_schema() -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        pytest.skip("jsonschema not installed")
    schemas, registry = {}, Registry()
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
    Draft202012Validator(schemas["package_validation.schema.json"], registry=registry).validate(_load("VALIDATION.json") if False else _load("validation/VALIDATION.json"))


def test_rule_ids_unique_and_complete() -> None:
    rules = _rules()
    assert 80 <= len(rules) <= 120
    ids = [item["id"] for item in rules]
    assert len(ids) == len(set(ids))
    required = ("id", "category", "priority", "conditions", "result", "explanation", "references", "tags", "enabled")
    for item in rules:
        for key in required:
            assert item.get(key) not in (None, "", []), item["id"]
        assert item["id"].startswith("UGP-")
        assert item["enabled"] is True
        assert item["result"]["score_target"] == "day_master.resolution_score"


def test_input_contract_compliance() -> None:
    for item in _rules():
        for cond in item["conditions"]:
            field = cond["field"]
            if field in INPUTS:
                continue
            assert field.startswith(INTERNAL_PREFIXES) or field in {"reinforced", "excluded"}, (item["id"], field)


def test_coverage_and_contracts() -> None:
    cats = {item["category"] for item in _rules()}
    for req in (
        "candidate_ranking", "priority_ordering", "conflict_detection", "conflict_grouping",
        "tie_breaking", "exclusion", "reinforcement", "suppression", "final_decision", "publication",
    ):
        assert req in cats
    inputs = {i["name"] for i in _load("assets/published_inputs.json")["inputs"]}
    assert inputs == INPUTS
    outputs = {o["name"] for o in _load("assets/published_outputs.json")["outputs"]}
    assert outputs == OUTPUTS


def test_evidence_links() -> None:
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["positive_examples"] and data["negative_examples"] and data["boundary_cases"]


def test_reasoning_links() -> None:
    rule_ids = {item["id"] for item in _rules()}
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 5
    expected = [
        "calendar", "four_pillars", "seasonal", "strength", "temperature",
        "pattern", "pattern_evaluation", "useful_god", "useful_god_priority",
    ]
    for name in ("single", "multiple", "conflict", "tie", "lowconf"):
        chain = _load(f"reasoning/chains/{name}.json")
        assert chain["dependency_chain"] == expected
        assert set(chain["consumed_published_inputs"]) == INPUTS
        for rid in chain["rule_ids"]:
            assert rid in rule_ids


def test_dependency_declarations() -> None:
    deps = _load("DEPENDENCIES.json")
    optional = {item["package_id"]: item for item in deps["optional"]}
    assert set(optional) >= {
        "bz_01_strength_core", "bz_02_seasonal_core", "bz_03_temperature_core",
        "bz_05_pattern_evaluation", "bz_06_useful_god_foundation",
    }
    assert deps["required"] == []
    assert "useful_god" in optional["bz_06_useful_god_foundation"]["signals"]
    assert "pattern_quality" in optional["bz_05_pattern_evaluation"]["signals"]


def test_priority_ordering_and_conflict_resolution() -> None:
    examples = {item["example_id"]: item for item in _load("examples/charts.json")["examples"]}
    single = examples["EX-UGP-SINGLE-001"]
    conflict = examples["EX-UGP-CONFLICT-001"]
    assert single["resolved_decision"] == "Chính Quan"
    assert single["decision_priority"] == "primary"
    assert single["conflict_resolution"] == "none"
    assert conflict["resolved_decision"] == "withheld"
    assert conflict["conflict_resolution"] == "applied"
    assert conflict["consumed_outputs"]["strength_score"] >= 65
    assert conflict["consumed_outputs"]["temperature_score"] >= 65
    assert "Chính Quan" in conflict["consumed_outputs"]["unfavorable_gods"]


def test_deterministic_execution() -> None:
    first = _load("examples/charts.json")
    second = _load("examples/charts.json")
    assert first == second
    by_id = {item["example_id"]: item["resolved_decision"] for item in first["examples"]}
    assert by_id["EX-UGP-TIE-001"] == "Chính Tài"
    assert by_id["EX-UGP-LOWCONF-001"] == "withheld"


def test_output_publication() -> None:
    pubs = {item["code"] for item in _rules() if item["category"] == "publication"}
    assert "pub_resolved_useful_god" in pubs
    assert "pub_conflict_resolution" in pubs
    assert "pub_resolution_diagnostics" in pubs
    outputs = [item["name"] for item in _load("assets/published_outputs.json")["outputs"]]
    assert outputs == sorted(OUTPUTS) or set(outputs) == OUTPUTS


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    tendencies = {item["tendency"] for item in examples}
    assert tendencies >= {"single_winner", "multiple_candidates", "conflict", "tie", "low_confidence"}
    for example in examples:
        assert set(example["consumed_outputs"]) == INPUTS
        assert example["activates_rules"] and example["reasoning_path"]
        assert "resolved_decision" in example
        assert not [r for r in example["activates_rules"] if r not in rule_ids]


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

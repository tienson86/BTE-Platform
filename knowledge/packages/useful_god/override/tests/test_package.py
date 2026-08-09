"""Package-level tests for bz_08_useful_god_override KX-4C."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
INPUTS = {
    "season_score", "strength_score", "temperature_score", "pattern_score",
    "pattern_quality", "pattern_confidence", "resolved_useful_god",
    "decision_priority", "resolution_confidence", "resolution_reasoning",
    "resolution_diagnostics",
}
OUTPUTS = {
    "final_useful_god", "final_favorable_gods", "final_unfavorable_gods",
    "override_applied", "override_reason", "override_confidence",
    "decision_trace", "decision_audit",
}
INTERNAL_PREFIXES = (
    "override_", "exceptional_", "follow_", "transform_", "dominant_",
    "contradiction_", "prohibited_", "eligible_", "published_", "audit_",
    "trace_", "final_sets", "no_recompute",
)
FORBIDDEN_FIELDS = {
    "strength_level", "temperature_level", "principal_pattern", "useful_god",
    "decision_score", "day_master", "month_branch",
}


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_08_useful_god_override"
    assert package["package_type"] == "decision"
    assert package["decision_role"] == "override"
    assert package["package_version"] == "1.0.0"
    assert package["status"] == "released"
    assert len(package["checksum"]["value"]) == 64


def test_manifest_and_metadata() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["validation_profile"] == "PVP-RELEASE"
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported) and len(exported) == len(set(exported))
    meta = _load("metadata/package_metadata.json")
    assert meta["category_id"] == "override"
    assert meta["config"]["decision_role"] == "override"
    assert meta["config"]["score_target"] == "day_master.override_score"


@pytest.mark.skipif(not SPEC.exists(), reason="no spec")
def test_identity_and_manifest_against_kd3_schema() -> None:
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        pytest.skip("jsonschema not installed")
    schemas, registry = {}, Registry()
    for name in (
        "package.schema.json", "package_manifest.schema.json",
        "package_dependency.schema.json", "package_release.schema.json",
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
        assert item["id"].startswith("UGO-")
        assert item["enabled"] is True
        assert item["result"]["score_target"] == "day_master.override_score"
        assert item["result"]["decision_role"] == "override"


def test_input_contract_and_override_legality() -> None:
    for item in _rules():
        for cond in item["conditions"]:
            field = cond["field"]
            assert field not in FORBIDDEN_FIELDS, (item["id"], field)
            if field in INPUTS:
                continue
            assert field.startswith(INTERNAL_PREFIXES) or field in {"final", "cap"}, (item["id"], field)


def test_coverage_and_contracts() -> None:
    cats = {item["category"] for item in _rules()}
    for req in (
        "override_eligibility", "override_prerequisites", "override_prohibition",
        "exceptional_conditions", "follow_pattern_override", "transformation_override",
        "dominant_element_override", "contradiction_override", "confidence_override",
        "final_override_publication",
    ):
        assert req in cats
    assert {i["name"] for i in _load("assets/published_inputs.json")["inputs"]} == INPUTS
    assert {o["name"] for o in _load("assets/published_outputs.json")["outputs"]} == OUTPUTS


def test_evidence_and_reasoning() -> None:
    rule_ids = {item["id"] for item in _rules()}
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["positive_examples"] and data["negative_examples"] and data["boundary_cases"]
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 5
    expected = [
        "calendar", "four_pillars", "seasonal", "strength", "temperature",
        "pattern", "pattern_evaluation", "useful_god", "useful_god_priority",
        "useful_god_override",
    ]
    for name in ("nooverride", "follow", "transform", "contradiction", "lowconf"):
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
        "bz_05_pattern_evaluation", "bz_07_useful_god_priority",
    }
    assert deps["required"] == []
    assert "resolved_useful_god" in optional["bz_07_useful_god_priority"]["signals"]


def test_override_conditions_and_rejection() -> None:
    examples = {item["example_id"]: item for item in _load("examples/charts.json")["examples"]}
    normal = examples["EX-UGO-NORMAL-001"]
    follow = examples["EX-UGO-FOLLOW-001"]
    rejected = examples["EX-UGO-REJECT-001"]
    assert normal["override_applied"] is False
    assert normal["final_decision"] == normal["consumed_outputs"]["resolved_useful_god"]
    assert follow["override_applied"] is True
    assert follow["override_reason"] == "follow_pattern"
    assert "follow_pattern" in follow["consumed_outputs"]["resolution_diagnostics"]
    assert rejected["override_applied"] is False
    assert "override_forbidden" in rejected["consumed_outputs"]["resolution_diagnostics"]
    assert examples["EX-UGO-TRANSFORM-001"]["override_applied"] is True
    assert examples["EX-UGO-CONTRA-001"]["final_decision"] == "withheld"


def test_deterministic_override() -> None:
    first = _load("examples/charts.json")
    second = _load("examples/charts.json")
    assert first == second
    by_id = {item["example_id"]: (item["final_decision"], item["override_applied"]) for item in first["examples"]}
    assert by_id["EX-UGO-NORMAL-001"] == ("Chính Quan", False)
    assert by_id["EX-UGO-FOLLOW-001"][1] is True
    assert by_id["EX-UGO-REJECT-001"] == ("Chính Tài", False)


def test_published_outputs_trace_and_audit() -> None:
    outputs = {o["name"] for o in _load("assets/published_outputs.json")["outputs"]}
    assert outputs == OUTPUTS
    trace_contract = _load("assets/decision_trace.contract.json")
    audit_contract = _load("assets/decision_audit.contract.json")
    for example in _load("examples/charts.json")["examples"]:
        trace = example["decision_trace"]
        audit = example["decision_audit"]
        for key in trace_contract["required"]:
            assert key in trace
        for key in audit_contract["required"]:
            assert key in audit
        assert audit["upstream_untouched"] is True
        assert audit["new_outputs_only"] is True
        assert audit["prohibition_checked"] is True
        assert audit["override_applied"] == example["override_applied"]


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    tendencies = {item["tendency"] for item in examples}
    assert tendencies >= {"normal_case", "follow_pattern", "transformation", "contradiction", "override_rejected"}
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

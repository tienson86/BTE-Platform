"""Package-level tests for bz_05_pattern_evaluation KX-3B. No engine imports."""
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
    assert package["package_id"] == "bz_05_pattern_evaluation"
    assert package["package_type"] == "analytical"
    assert package["package_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert len(package["checksum"]["value"]) == 64
    assert (ROOT / "assets" / "published_outputs.json").is_file()


def test_manifest_valid() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["validation_profile"] == "PVP-RELEASE"
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported)
    assert len(exported) == len(set(exported))


def test_metadata_valid() -> None:
    meta = _load("metadata/package_metadata.json")
    assert meta["domain_id"] == "DOM-PATTERN"
    assert meta["category_id"] == "evaluation"
    assert meta["config"]["score_target"] == "day_master.pattern_evaluation_score"
    assert meta["config"]["does_not_identify_pattern"] is True


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
    forbidden = {"day_master.strength_score", "day_master.season_score", "day_master.temperature_score", "day_master.pattern_score"}
    for item in rules:
        for key in required:
            assert item.get(key) not in (None, "", []), item["id"]
        assert item["id"].startswith("PEV-")
        assert item["result"]["score_target"] == "day_master.pattern_evaluation_score"
        assert item["result"]["score_target"] not in forbidden
        assert not str(item["result"]["effect"]).startswith("principal=")


def test_coverage_categories() -> None:
    cats = {item["category"] for item in _rules()}
    for req in ("pattern_completeness", "pattern_integrity", "pattern_stability", "pattern_reinforcement", "pattern_weakening", "pattern_rescue", "pattern_destruction", "pattern_confidence", "pattern_quality_levels", "evaluation_scoring"):
        assert req in cats
    assert "principal_pattern" not in cats


def test_evidence_links() -> None:
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["positive_examples"] and data["negative_examples"]


def test_reasoning_links() -> None:
    rule_ids = {item["id"] for item in _rules()}
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 3
    expected = ["calendar", "four_pillars", "seasonal", "strength", "temperature", "pattern", "pattern_evaluation"]
    for name in ("high", "weak", "broken"):
        chain = _load(f"reasoning/chains/{name}.json")
        assert chain["dependency_chain"] == expected
        assert chain["upstream_pattern_rules"] and chain["upstream_seasonal_rules"] and chain["upstream_strength_rules"] and chain["upstream_temperature_rules"]
        for rid in chain["rule_ids"]:
            assert rid in rule_ids


def test_upstream_ids_exist() -> None:
    pat = set()
    for path in (KNOWLEDGE / "packages" / "pattern" / "core" / "rules").glob("*.json"):
        pat.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
    sec = set()
    for path in (KNOWLEDGE / "packages" / "seasonal" / "core" / "rules").glob("*.json"):
        sec.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
    skc = set()
    for path in (KNOWLEDGE / "packages" / "strength" / "core" / "rules").glob("*.json"):
        skc.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
    tec = set()
    for path in (KNOWLEDGE / "packages" / "temperature" / "core" / "rules").glob("*.json"):
        tec.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
    for name in ("high", "weak", "broken"):
        chain = _load(f"reasoning/chains/{name}.json")
        for rid in chain["upstream_pattern_rules"]:
            assert rid in pat, rid
        for rid in chain["upstream_seasonal_rules"]:
            assert rid in sec, rid
        for rid in chain["upstream_strength_rules"]:
            assert rid in skc, rid
        for rid in chain["upstream_temperature_rules"]:
            assert rid in tec, rid


def test_dependency_declarations() -> None:
    deps = _load("DEPENDENCIES.json")
    optional = {item["package_id"]: item for item in deps["optional"]}
    assert "bz_04_pattern_core" in optional
    assert "principal_pattern" in optional["bz_04_pattern_core"]["signals"]
    assert deps["required"] == []


def test_published_outputs_contract() -> None:
    outputs = {item["name"] for item in _load("assets/published_outputs.json")["outputs"]}
    assert outputs == {"pattern_quality", "pattern_confidence", "pattern_integrity", "pattern_stability", "pattern_score", "evaluation_diagnostics"}


def test_example_references_valid() -> None:
    rule_ids = {item["id"] for item in _rules()}
    examples = _load("examples/charts.json")["examples"]
    qualities = {item["quality"] for item in examples}
    assert qualities >= {"excellent", "good", "average", "weak", "broken"}
    for example in examples:
        assert example["consumed_package_outputs"]["bz_04_pattern_core"]
        assert example["activates_rules"] and example["reasoning_path"]
        assert not [r for r in example["activates_rules"] if r not in rule_ids]


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


def test_no_pat_id_collision() -> None:
    for item in _rules():
        assert item["id"].startswith("PEV-")
        assert not item["id"].startswith("PAT-")


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

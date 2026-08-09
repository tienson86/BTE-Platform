"""Package-level tests for bz_10_follow_pattern_core KX-5A. No engine imports."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
ALLOWED = {
    "season_score",
    "strength_score",
    "temperature_score",
    "pattern_score",
    "pattern_quality",
    "pattern_confidence",
    "pattern_integrity",
    "pattern_stability",
    "resolved_useful_god",
    "decision_priority",
    "resolution_confidence",
}
OUTPUTS = {
    "follow_pattern",
    "follow_pattern_type",
    "follow_pattern_confidence",
    "follow_pattern_score",
    "follow_pattern_reasoning",
    "follow_pattern_diagnostics",
}
FORBIDDEN = {
    "month_branch",
    "day_stem",
    "year_stem",
    "hour_branch",
    "principal_pattern",
    "strength_level",
    "temperature_level",
    "season",
    "season_phase",
    "climate_type",
    "useful_god",
    "decision_score",
    "pattern_confirmed",
}


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _rules() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "rules").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_10_follow_pattern_core"
    assert package["package_type"] == "analytical"
    assert package["package_version"] == "1.0.0"
    assert package["schema_version"] == "2.0.0"
    assert package["knowledge_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert len(package["checksum"]["value"]) == 64


def test_contracts() -> None:
    inputs = {item["name"] for item in _load("assets/published_inputs.json")["inputs"]}
    outputs = {item["name"] for item in _load("assets/published_outputs.json")["outputs"]}
    assert inputs == ALLOWED
    assert outputs == OUTPUTS
    assert "raw chart fields" in " ".join(_load("assets/published_inputs.json")["forbidden"])


def test_duplicate_ids() -> None:
    rules = _rules()
    ids = [item["id"] for item in rules]
    assert 240 <= len(ids) <= 260
    assert len(ids) == len(set(ids))
    assert sorted(ids)[0] == "FPC-000001"
    assert sorted(ids)[-1] == "FPC-000250"


def test_evidence_completeness() -> None:
    for item in _rules():
        data = json.loads((ROOT / "evidence" / "bundles" / f"{item['id']}.json").read_text(encoding="utf-8"))
        assert data["explanation"] and data["rationale"]
        assert data["positive_examples"] and data["negative_examples"] and data["boundary_cases"]
        assert data["references"]


def test_reasoning_completeness() -> None:
    rule_ids = {item["id"] for item in _rules()}
    index = _load("reasoning/index.json")
    assert len(index["chains"]) == 6
    for slug in ("true", "false", "border", "contra", "lowconf", "mixed"):
        chain = _load(f"reasoning/chains/{slug}.json")
        assert chain["upstream_pattern_rules"]
        assert chain["upstream_pattern_evaluation_rules"]
        assert chain["upstream_seasonal_rules"]
        assert chain["upstream_strength_rules"]
        assert chain["upstream_temperature_rules"]
        assert any(rid.startswith("FPC-") for rid in chain["rule_ids"])
        for rid in chain["rule_ids"]:
            assert rid in rule_ids


def test_published_outputs_only() -> None:
    for item in _rules():
        for c in item["conditions"]:
            assert c["field"] in ALLOWED, (item["id"], c["field"])
            assert c["field"] not in FORBIDDEN
        pub = item["result"]["publishes"]
        assert pub in OUTPUTS


def test_validation_profile() -> None:
    assert _load("validation/profile.json")["validation_profile"] == "PVP-RELEASE"
    report = _load("validation/VALIDATION.json")
    assert report["profile"] == "PVP-RELEASE"
    assert report["counts"]["errors"] == 0
    assert all(c["status"] == "pass" for c in report["checks"])


def test_serialization_round_trip() -> None:
    raw = (ROOT / "PACKAGE.json").read_text(encoding="utf-8")
    encoded = json.dumps(json.loads(raw), sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded)["package_id"] == "bz_10_follow_pattern_core"


def test_deterministic_loading() -> None:
    first = json.dumps(_load("PACKAGE.json"), sort_keys=True)
    second = json.dumps(_load("PACKAGE.json"), sort_keys=True)
    assert first == second
    rules_a = json.dumps(_rules(), sort_keys=True, ensure_ascii=False)
    rules_b = json.dumps(_rules(), sort_keys=True, ensure_ascii=False)
    assert rules_a == rules_b


def test_upstream_ids_exist() -> None:
    def collect(rel: str) -> set[str]:
        found: set[str] = set()
        for path in (KNOWLEDGE / "packages" / rel / "rules").glob("*.json"):
            found.update(o["id"] for o in json.loads(path.read_text(encoding="utf-8"))["objects"])
        return found

    pat = collect("pattern/core")
    pev = collect("pattern/evaluation")
    sec = collect("seasonal/core")
    skc = collect("strength/core")
    tec = collect("temperature/core")
    for slug in ("true", "false", "border", "contra", "lowconf", "mixed"):
        chain = _load(f"reasoning/chains/{slug}.json")
        for rid in chain["upstream_pattern_rules"]:
            assert rid in pat, rid
        for rid in chain["upstream_pattern_evaluation_rules"]:
            assert rid in pev, rid
        for rid in chain["upstream_seasonal_rules"]:
            assert rid in sec, rid
        for rid in chain["upstream_strength_rules"]:
            assert rid in skc, rid
        for rid in chain["upstream_temperature_rules"]:
            assert rid in tec, rid


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _rules():
        for ref in item["references"]:
            assert ref["target"] in known


@pytest.mark.skipif(not SPEC.exists(), reason="no spec")
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
    Draft202012Validator(schemas["package_validation.schema.json"], registry=registry).validate(_load("validation/VALIDATION.json"))


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

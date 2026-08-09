"""Package-level tests for bz_09_luck_foundation LE-1."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
INPUTS = {
    "year_pillar",
    "month_pillar",
    "day_pillar",
    "hour_pillar",
    "gender",
    "birth_year",
    "birth_month",
    "birth_day",
    "birth_hour",
}
OUTPUTS = {
    "natal_chart",
    "major_cycles",
    "annual_cycles",
    "monthly_cycles",
    "timeline_metadata",
    "timeline_version",
}
FORBIDDEN = {
    "score",
    "quality",
    "favorable",
    "unfavorable",
    "useful_god",
    "judgment",
    "interpretation",
    "fortune",
}


def _load(rel: str) -> object:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _definitions() -> list[dict]:
    objects: list[dict] = []
    for path in sorted((ROOT / "definitions").glob("*.json")):
        objects.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return objects


def test_package_loads() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_09_luck_foundation"
    assert package["package_type"] == "reference"
    assert package["package_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["domain_id"] == "DOM-LUCK_CYCLE"
    assert package["language"] == "vi"
    assert len(package["checksum"]["value"]) == 64
    assert (ROOT / "assets" / "published_inputs.json").is_file()
    assert (ROOT / "assets" / "published_outputs.json").is_file()
    assert (ROOT / "assets" / "timeline.contract.json").is_file()


def test_manifest_valid() -> None:
    manifest = _load("MANIFEST.json")
    assert manifest["validation_profile"] == "PVP-RELEASE"
    exported = [item["id"] for item in manifest["exported_objects"]]
    assert exported == sorted(exported) and len(exported) == len(set(exported))
    assert len(exported) == 12


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
    Draft202012Validator(schemas["package.schema.json"], registry=registry).validate(
        _load("PACKAGE.json")
    )
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


def test_metadata_valid() -> None:
    meta = _load("metadata/package_metadata.json")
    assert meta["domain_id"] == "DOM-LUCK_CYCLE"
    assert meta["category_id"] == "foundation"
    assert meta["config"]["timeline_version"] == "1.0.0"
    assert meta["config"]["score_target"] is None
    assert meta["config"]["package_kind"] == "reference"


def test_definition_ids_unique() -> None:
    items = _definitions()
    assert 12 <= len(items) <= 20
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids))
    required = ("id", "category", "priority", "conditions", "result", "explanation", "references", "tags", "enabled")
    for item in items:
        for key in required:
            assert item.get(key) not in (None, "", []), item["id"]
        assert item["id"].startswith("LTF-")
        assert "score" not in item["result"]


def test_contracts_and_no_scores() -> None:
    inputs = {item["name"] for item in _load("assets/published_inputs.json")["inputs"]}
    assert inputs == INPUTS
    outputs = {item["name"] for item in _load("assets/published_outputs.json")["outputs"]}
    assert outputs == OUTPUTS
    contract = _load("assets/timeline.contract.json")
    assert contract["scores"] is False
    assert contract["judgments"] is False
    dumped = json.dumps(_load("assets/published_outputs.json"))
    for token in FORBIDDEN:
        assert token not in dumped


def test_dependency_declarations() -> None:
    deps = _load("DEPENDENCIES.json")
    assert deps["required"] == []
    assert deps["optional"] == []


def test_reference_integrity() -> None:
    known = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _definitions():
        for ref in item["references"]:
            assert ref["target"] in known


def test_example_timeline_has_no_scores() -> None:
    examples = _load("examples/timelines.json")["examples"]
    assert examples
    dumped = json.dumps(examples)
    for token in ("luck_score", "favorable", "unfavorable", "useful_god"):
        assert token not in dumped


def test_no_engine_import() -> None:
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.decision_engine" not in sys.modules
    assert "engines.rule_engine" not in sys.modules

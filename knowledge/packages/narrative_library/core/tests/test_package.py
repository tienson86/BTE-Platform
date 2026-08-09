"""Package-level tests for bz_18_narrative_library_core IK-3. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
EXP_ROOT = KNOWLEDGE / "packages" / "explanation_library" / "core"
EXP_RE = re.compile(r"^EXP-\d{6}$")
ALLOWED = re.compile(r"^(analysis|decision|luck|interpretation)\.[a-z0-9_]+$")
SECTIONS = ["opening", "body", "closing", "summary"]
PROSE_KEYS = {"text", "title", "body", "sentence", "prose", "narrative"}


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _templates() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "templates").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["template_id"])


def _explanations() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for path in (EXP_ROOT / "explanations").glob("*.json"):
        if path.name == "index.json":
            continue
        for item in json.loads(path.read_text(encoding="utf-8"))["objects"]:
            found[item["explanation_id"]] = item
    return found


def _flatten_flow(flow: dict) -> list[str]:
    ordered: list[str] = [flow["opening"]]
    ordered.extend(flow["body"])
    ordered.append(flow["closing"])
    ordered.append(flow["summary"])
    return ordered


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_18_narrative_library_core"
    assert package["package_type"] == "interpretation"
    assert package["category_id"] == "narrative_library"
    assert package["package_version"] == "1.0.0"
    assert package["schema_version"] == "2.0.0"
    assert package["knowledge_version"] == "1.0.0"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["domain_id"] == "DOM-INTERPRETATION"
    assert len(package["checksum"]["value"]) == 64


def test_serialization_round_trip() -> None:
    encoded = json.dumps(_load("PACKAGE.json"), sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded)["package_id"] == "bz_18_narrative_library_core"


def test_package_loading() -> None:
    items = _templates()
    assert len(items) == 1200
    assert items[0]["template_id"] == "NAR-000001"
    assert items[-1]["template_id"] == "NAR-001200"
    index = _load("templates/index.json")
    assert index["count"] == 1200
    assert len(index["template_ids"]) == 1200


def test_duplicate_ids() -> None:
    items = _templates()
    ids = [item["template_id"] for item in items]
    assert len(ids) == len(set(ids))
    sequences = [tuple(item["explanation_ids"]) for item in items]
    assert len(sequences) == len(set(sequences))


def test_deterministic_ordering() -> None:
    items = _templates()
    assert [item["template_id"] for item in items] == sorted(item["template_id"] for item in items)


def test_flow_integrity() -> None:
    for item in _templates():
        assert item["section_order"] == SECTIONS
        assert list(item["flow"].keys()) == SECTIONS
        assert isinstance(item["flow"]["opening"], str) and EXP_RE.match(item["flow"]["opening"])
        assert isinstance(item["flow"]["closing"], str) and EXP_RE.match(item["flow"]["closing"])
        assert isinstance(item["flow"]["summary"], str) and EXP_RE.match(item["flow"]["summary"])
        assert isinstance(item["flow"]["body"], list) and item["flow"]["body"]
        assert all(EXP_RE.match(eid) for eid in item["flow"]["body"])
        flat = _flatten_flow(item["flow"])
        assert item["explanation_ids"] == flat
        assert len(flat) == len(set(flat))
        trans = item["transition_ids"]
        assert trans["opening"] == item["flow"]["opening"]
        assert trans["body"] == item["flow"]["body"][0]
        assert trans["closing"] == item["flow"]["closing"]
        assert trans["summary"] == item["flow"]["summary"]


def test_explanation_references() -> None:
    explanations = _explanations()
    assert len(explanations) == 3000
    for item in _templates():
        assert 4 <= len(item["explanation_ids"]) <= 6
        for eid in item["explanation_ids"]:
            assert eid in explanations
            assert explanations[eid]["title"] not in json.dumps(item, ensure_ascii=False)
            assert explanations[eid]["body"] not in json.dumps(item, ensure_ascii=False)
        assert not PROSE_KEYS.intersection(item.keys())


def test_placeholder_validation() -> None:
    explanations = _explanations()
    for item in _templates():
        assert item["placeholders"]
        for token in item["placeholders"]:
            assert ALLOWED.match(token), token
        expected: list[str] = []
        for eid in item["explanation_ids"]:
            for token in explanations[eid]["placeholders"]:
                if token not in expected:
                    expected.append(token)
        assert item["placeholders"] == expected


def test_reasoning_links() -> None:
    catalog = {item["id"] for item in _load("reasoning/index.json")["chains"]}
    explanations = _explanations()
    for item in _templates():
        assert item["reasoning_ids"]
        for rid in item["reasoning_ids"]:
            assert rid in catalog
        expected: list[str] = []
        for eid in item["explanation_ids"]:
            for rid in explanations[eid]["reasoning_ids"]:
                if rid not in expected:
                    expected.append(rid)
        assert item["reasoning_ids"] == expected


def test_evidence_catalog() -> None:
    known = set(_load("reasoning/evidence_catalog.json")["evidence_ids"])
    explanations = _explanations()
    cited: set[str] = set()
    for item in _templates():
        for eid in item["explanation_ids"]:
            cited.update(explanations[eid]["evidence_ids"])
    assert cited <= known
    assert known == cited


def test_reference_links() -> None:
    refs = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _templates():
        assert item["references"]
        for ref in item["references"]:
            assert ref in refs


def test_validation_profile() -> None:
    assert _load("validation/profile.json")["validation_profile"] == "PVP-RELEASE"
    report = _load("validation/VALIDATION.json")
    assert report["counts"]["errors"] == 0
    assert all(check["status"] == "pass" for check in report["checks"])


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
    Draft202012Validator(schemas["package_validation.schema.json"], registry=registry).validate(_load("validation/VALIDATION.json"))


def test_no_engine_import() -> None:
    assert "engines.interpretation_engine" not in sys.modules
    assert "engines.analysis_engine" not in sys.modules
    assert "engines.report_engine" not in sys.modules

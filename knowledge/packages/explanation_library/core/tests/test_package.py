"""Package-level tests for bz_17_explanation_library_core IK-2. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
SEN_ROOT = KNOWLEDGE / "packages" / "sentence_library" / "core"
PH_IN_TEXT = re.compile(r"\{\{([a-z0-9_.]+)\}\}")
ALLOWED = re.compile(r"^(analysis|decision|luck|interpretation)\.[a-z0-9_]+$")
FORBIDDEN_MARKUP = re.compile(r"[<>]|[*#`]|markdown|html", re.I)


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _explanations() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "explanations").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["explanation_id"])


def _sentences() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for path in (SEN_ROOT / "sentences").glob("*.json"):
        if path.name == "index.json":
            continue
        for item in json.loads(path.read_text(encoding="utf-8"))["objects"]:
            found[item["sentence_id"]] = item
    return found


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_17_explanation_library_core"
    assert package["package_type"] == "interpretation"
    assert package["category_id"] == "explanation_library"
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
    assert json.loads(encoded)["package_id"] == "bz_17_explanation_library_core"


def test_package_loading() -> None:
    items = _explanations()
    assert len(items) == 3000
    assert items[0]["explanation_id"] == "EXP-000001"
    assert items[-1]["explanation_id"] == "EXP-003000"
    index = _load("explanations/index.json")
    assert index["count"] == 3000
    assert len(index["explanation_ids"]) == 3000


def test_duplicate_ids() -> None:
    items = _explanations()
    ids = [item["explanation_id"] for item in items]
    assert len(ids) == len(set(ids))
    titles = [item["title"] for item in items]
    assert len(titles) == len(set(titles))
    sequences = [tuple(item["sentence_ids"]) for item in items]
    assert len(sequences) == len(set(sequences))


def test_deterministic_ordering() -> None:
    items = _explanations()
    ids = [item["explanation_id"] for item in items]
    assert ids == sorted(ids)
    for item in items:
        assert len(item["sentence_ids"]) == len(set(item["sentence_ids"]))


def test_sentence_references() -> None:
    sentences = _sentences()
    assert len(sentences) == 5000
    for item in _explanations():
        assert 2 <= len(item["sentence_ids"]) <= 4
        assert len(item["sentence_ids"]) == len(set(item["sentence_ids"]))
        for sid in item["sentence_ids"]:
            assert sid in sentences
            assert sentences[sid]["text"] not in item["body"]
            assert sentences[sid]["text"] not in item["title"]


def test_placeholder_validation() -> None:
    sentences = _sentences()
    for item in _explanations():
        found = PH_IN_TEXT.findall(item["body"])
        assert set(found) == set(item["placeholders"])
        for token in item["placeholders"]:
            assert ALLOWED.match(token), token
        expected: list[str] = []
        for sid in item["sentence_ids"]:
            for token in sentences[sid]["placeholders"]:
                if token not in expected:
                    expected.append(token)
        assert item["placeholders"] == expected
        assert not FORBIDDEN_MARKUP.search(item["body"].replace("{{", "").replace("}}", ""))
        assert not FORBIDDEN_MARKUP.search(item["title"])


def test_reasoning_links() -> None:
    catalog = {item["id"] for item in _load("reasoning/index.json")["chains"]}
    sentences = _sentences()
    for item in _explanations():
        assert item["reasoning_ids"]
        for rid in item["reasoning_ids"]:
            assert rid in catalog
        expected: list[str] = []
        for sid in item["sentence_ids"]:
            for rid in sentences[sid]["reasoning_ids"]:
                if rid not in expected:
                    expected.append(rid)
        assert item["reasoning_ids"] == expected


def test_evidence_links() -> None:
    known = set(_load("reasoning/evidence_catalog.json")["evidence_ids"])
    sentences = _sentences()
    for item in _explanations():
        assert item["evidence_ids"]
        for eid in item["evidence_ids"]:
            assert eid in known
        expected: list[str] = []
        for sid in item["sentence_ids"]:
            for eid in sentences[sid]["evidence_ids"]:
                if eid not in expected:
                    expected.append(eid)
        assert item["evidence_ids"] == expected


def test_reference_links() -> None:
    refs = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _explanations():
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

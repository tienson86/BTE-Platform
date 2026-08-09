"""Package-level tests for bz_16_sentence_library_core IK-1. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
PH_IN_TEXT = re.compile(r"\{\{([a-z0-9_.]+)\}\}")
ALLOWED = re.compile(r"^(analysis|decision|luck|interpretation)\.[a-z0-9_]+$")
FORBIDDEN_MARKUP = re.compile(r"[<>]|[*#`]|markdown|html", re.I)


def _load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _sentences() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "sentences").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["sentence_id"])


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_16_sentence_library_core"
    assert package["package_type"] == "sentence"
    assert package["category_id"] == "sentence_library"
    assert package["package_version"] == "1.0.0"
    assert package["schema_version"] == "2.0.0"
    assert package["knowledge_version"] == "1.0.0"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["domain_id"] == "DOM-INTERPRETATION"
    assert len(package["checksum"]["value"]) == 64


def test_serialization_round_trip() -> None:
    encoded = json.dumps(json.loads((ROOT / "PACKAGE.json").read_text(encoding="utf-8")), sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded)["package_id"] == "bz_16_sentence_library_core"


def test_package_loading() -> None:
    sentences = _sentences()
    assert len(sentences) == 5000
    assert sentences[0]["sentence_id"] == "SEN-000001"
    assert sentences[-1]["sentence_id"] == "SEN-005000"
    index = _load("sentences/index.json")
    assert index["count"] == 5000
    assert len(index["sentence_ids"]) == 5000


def test_duplicate_ids() -> None:
    sentences = _sentences()
    ids = [item["sentence_id"] for item in sentences]
    assert len(ids) == len(set(ids))
    texts = [item["text"] for item in sentences]
    assert len(texts) == len(set(texts))


def test_deterministic_ordering() -> None:
    sentences = _sentences()
    ids = [item["sentence_id"] for item in sentences]
    assert ids == sorted(ids)
    assert json.dumps(sentences, sort_keys=True, ensure_ascii=False) == json.dumps(sentences, sort_keys=True, ensure_ascii=False)


def test_placeholder_validation() -> None:
    for item in _sentences():
        found = PH_IN_TEXT.findall(item["text"])
        assert found
        assert set(found) == set(item["placeholders"])
        for token in item["placeholders"]:
            assert ALLOWED.match(token), token
        assert not FORBIDDEN_MARKUP.search(item["text"].replace("{{", "").replace("}}", ""))


def test_reasoning_links() -> None:
    catalog = {item["id"] for item in _load("reasoning/index.json")["chains"]}
    for item in _sentences():
        assert item["reasoning_ids"]
        for rid in item["reasoning_ids"]:
            assert rid in catalog


def test_evidence_links() -> None:
    known = set(_load("reasoning/evidence_catalog.json")["evidence_ids"])
    for item in _sentences():
        assert item["evidence_ids"]
        for eid in item["evidence_ids"]:
            assert eid in known


def test_template_and_reference_links() -> None:
    templates = {item["template_id"] for item in _load("assets/templates.json")["templates"]}
    refs = {item["id"] for item in _load("references/references.json")["references"]}
    for item in _sentences():
        assert item["template_id"] in templates
        assert item["references"]
        for ref in item["references"]:
            assert ref in refs or ref.startswith("REF-")


def test_upstream_evidence_exists() -> None:
    catalog = _load("reasoning/evidence_catalog.json")
    by_package = catalog["by_package"]
    for package_id, ids in by_package.items():
        rel = {
            "bz_01_strength_core": "strength/core",
            "bz_02_seasonal_core": "seasonal/core",
            "bz_03_temperature_core": "temperature/core",
            "bz_04_pattern_core": "pattern/core",
            "bz_05_pattern_evaluation": "pattern/evaluation",
            "bz_06_useful_god_foundation": "useful_god/foundation",
            "bz_07_useful_god_priority": "useful_god/priority",
            "bz_08_useful_god_override": "useful_god/override",
            "bz_10_follow_pattern_core": "follow_pattern/core",
            "bz_11_transformation_core": "transformation/core",
            "bz_12_combination_clash_core": "combination_clash/core",
            "bz_13_ten_gods_advanced": "ten_gods/advanced",
            "bz_14_twelve_growth_advanced": "twelve_growth/advanced",
            "bz_15_hidden_stems_advanced": "hidden_stems/advanced",
        }[package_id]
        folder = KNOWLEDGE / "packages" / rel / "evidence" / "bundles"
        for eid in ids:
            assert (folder / f"{eid}.json").is_file(), eid


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

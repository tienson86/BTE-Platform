"""Package-level tests for bz_19_composition_library_core IK-4. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
NAR_ROOT = KNOWLEDGE / "packages" / "narrative_library" / "core"
ALLOWED = re.compile(r"^(analysis|decision|luck|interpretation)\.[a-z0-9_]+$")
EXPR = re.compile(r"[+*/()=<>]|if\b|lambda|eval|\$\{")
PROSE_KEYS = {"text", "title", "body", "prose", "narrative", "sentence"}


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _compositions() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "composition").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["composition_id"])


def _placeholders() -> list[dict]:
    return _load("placeholders/placeholders.json")["objects"]


def _narratives() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for path in (NAR_ROOT / "templates").glob("*.json"):
        if path.name == "index.json":
            continue
        for item in json.loads(path.read_text(encoding="utf-8"))["objects"]:
            found[item["template_id"]] = item
    return found


def _acyclic(edges: dict[str, list[str]]) -> bool:
    indeg: dict[str, int] = {}
    for src, dests in edges.items():
        indeg.setdefault(src, 0)
        for dest in dests:
            indeg.setdefault(dest, 0)
            indeg[dest] += 1
    queue = deque([node for node, deg in indeg.items() if deg == 0])
    seen = 0
    graph = {node: list(edges.get(node, [])) for node in indeg}
    while queue:
        node = queue.popleft()
        seen += 1
        for dest in graph[node]:
            indeg[dest] -= 1
            if indeg[dest] == 0:
                queue.append(dest)
    return seen == len(indeg)


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_19_composition_library_core"
    assert package["package_type"] == "interpretation"
    assert package["category_id"] == "composition_library"
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
    assert json.loads(encoded)["package_id"] == "bz_19_composition_library_core"


def test_package_loading() -> None:
    rules = _compositions()
    placeholders = _placeholders()
    assert len(rules) == 800
    assert rules[0]["composition_id"] == "CMP-000001"
    assert rules[-1]["composition_id"] == "CMP-000800"
    assert len(placeholders) == 120
    assert placeholders[0]["placeholder_id"] == "PH-000001"
    assert placeholders[-1]["placeholder_id"] == "PH-000120"
    assert _load("composition/index.json")["count"] == 800
    assert _load("placeholders/index.json")["count"] == 120


def test_duplicate_ids() -> None:
    rules = _compositions()
    placeholders = _placeholders()
    assert len({item["composition_id"] for item in rules}) == 800
    assert len({tuple(item["narrative_template_ids"]) for item in rules}) == 800
    assert len({item["placeholder_id"] for item in placeholders}) == 120
    assert len({item["placeholder_path"] for item in placeholders}) == 120


def test_deterministic_ordering() -> None:
    rules = _compositions()
    assert [item["composition_id"] for item in rules] == sorted(item["composition_id"] for item in rules)
    placeholders = _placeholders()
    assert [item["placeholder_id"] for item in placeholders] == sorted(item["placeholder_id"] for item in placeholders)


def test_placeholder_validation() -> None:
    for item in _placeholders():
        assert ALLOWED.match(item["placeholder_path"]), item["placeholder_path"]
        assert item["scope"] == item["placeholder_path"].split(".", 1)[0]
        assert item["value_type"] in {"number", "enum", "string", "list", "object", "boolean"}
        fallback = item["fallback"]
        if fallback is not None:
            assert not EXPR.search(json.dumps(fallback, ensure_ascii=False))
        assert "expression" not in item
        assert "script" not in item


def test_composition_placeholder_coverage() -> None:
    path_by_id = {item["placeholder_id"]: item["placeholder_path"] for item in _placeholders()}
    narratives = _narratives()
    required_extra = {"interpretation.composition_id", "interpretation.module_id", "interpretation.section"}
    for item in _compositions():
        assert not PROSE_KEYS.intersection(item.keys())
        paths = {path_by_id[pid] for pid in item["placeholder_ids"]}
        expected = set()
        for nid in item["narrative_template_ids"]:
            assert nid in narratives
            expected.update(narratives[nid]["placeholders"])
        expected |= required_extra
        assert expected <= paths


def test_dependency_validation() -> None:
    rules = _compositions()
    ids = {item["composition_id"] for item in rules}
    edges: dict[str, list[str]] = {}
    for item in rules:
        deps = item["dependencies"]
        assert isinstance(deps, list)
        for dep in deps:
            assert dep in ids
            assert dep != item["composition_id"]
        edges[item["composition_id"]] = list(deps)
        assert item["ordering"]["dependency"] == deps
        assert item["ordering"]["section"] == ["opening", "body", "closing", "summary"]
    assert _acyclic(edges)


def test_reference_map() -> None:
    refmap = _load("assets/reference_map.json")
    assert refmap["narrative_templates"] >= 1
    assert refmap["explanation_blocks"] >= 1
    assert refmap["sentence_ids"] >= 1
    assert refmap["evidence_ids"] >= 1
    assert refmap["reasoning_ids"] >= 1
    rules = _compositions()
    narratives = _narratives()
    cited_nar = {nid for item in rules for nid in item["narrative_template_ids"]}
    assert cited_nar <= set(narratives)


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

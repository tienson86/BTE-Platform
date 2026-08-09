"""Package-level tests for bz_20_theme_library_core PK-1. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
CMP_ROOT = KNOWLEDGE / "packages" / "composition_library" / "core"
STYLE_FORBIDDEN = re.compile(r"[#<>]|rgb\(|hsl\(|px\b|rem\b|\dem\b|pt\b|color:|font-|css|html|pdf", re.I)
PROSE_KEYS = {"text", "title", "body", "prose", "html", "css"}


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _themes() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "themes").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["theme_id"])


def _component_ids() -> dict[str, set[str]]:
    catalog = _load("assets/component_catalog.json")
    return {kind: {item["id"] for item in entries} for kind, entries in catalog["components"].items()}


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_20_theme_library_core"
    assert package["package_type"] == "report"
    assert package["category_id"] == "theme_library"
    assert package["package_version"] == "1.0.0"
    assert package["schema_version"] == "2.0.0"
    assert package["knowledge_version"] == "1.0.0"
    assert package["compatibility"]["compatibility_version"] == "1.0.0"
    assert package["status"] == "released"
    assert package["language"] == "vi"
    assert package["domain_id"] == "DOM-REPORT"
    assert len(package["checksum"]["value"]) == 64


def test_serialization_round_trip() -> None:
    encoded = json.dumps(_load("PACKAGE.json"), sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded)["package_id"] == "bz_20_theme_library_core"


def test_package_loading() -> None:
    themes = _themes()
    assert len(themes) == 300
    assert themes[0]["theme_id"] == "THM-000001"
    assert themes[-1]["theme_id"] == "THM-000300"
    index = _load("themes/index.json")
    assert index["count"] == 300
    assert len(index["theme_ids"]) == 300


def test_duplicate_ids() -> None:
    themes = _themes()
    assert len({item["theme_id"] for item in themes}) == 300
    assert len({item["theme_name"] for item in themes}) == 300
    signatures = [
        (
            item["palette_id"],
            item["typography_id"],
            item["spacing_id"],
            item["icon_set_id"],
            item["cover_style"],
            item["header_style"],
            item["footer_style"],
            item["table_style"],
            item["chart_style"],
            item["note_style"],
            item["warning_style"],
            item["reference_style"],
            item["layout_id"],
        )
        for item in themes
    ]
    assert len(signatures) == len(set(signatures))


def test_deterministic_ordering() -> None:
    themes = _themes()
    assert [item["theme_id"] for item in themes] == sorted(item["theme_id"] for item in themes)


def test_component_integrity() -> None:
    catalog = _component_ids()
    for item in _themes():
        assert not PROSE_KEYS.intersection(item.keys())
        assert item["palette_id"] in catalog["palette"]
        assert item["typography_id"] in catalog["typography"]
        assert item["spacing_id"] in catalog["spacing"]
        assert item["icon_set_id"] in catalog["icon_set"]
        assert item["cover_style"] in catalog["cover"]
        assert item["header_style"] in catalog["header"]
        assert item["footer_style"] in catalog["footer"]
        assert item["table_style"] in catalog["table"]
        assert item["chart_style"] in catalog["chart"]
        assert item["note_style"] in catalog["note"]
        assert item["warning_style"] in catalog["warning"]
        assert item["reference_style"] in catalog["reference_style"]
        assert item["layout_id"] in catalog["layout"]
        assert item["report_contract_id"] in catalog["report_contract"]
        for sid in item["section_ids"]:
            assert sid in catalog["section"]
        blob = json.dumps(item, ensure_ascii=False)
        assert not STYLE_FORBIDDEN.search(blob)


def test_reference_integrity() -> None:
    cmp_ids = set(_load("composition/index.json", CMP_ROOT)["composition_ids"])
    for item in _themes():
        assert item["composition_ids"]
        for cid in item["composition_ids"]:
            assert cid in cmp_ids
        assert item["layout_id"].startswith("LAY-")
        assert item["report_contract_id"].startswith("RCT-")


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
    assert "engines.report_engine" not in sys.modules
    assert "engines.interpretation_engine" not in sys.modules
    assert "engines.analysis_engine" not in sys.modules

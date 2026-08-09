"""Package-level tests for bz_21_layout_library_core PK-2. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
THM_ROOT = KNOWLEDGE / "packages" / "theme_library" / "core"
STYLE_FORBIDDEN = re.compile(r"[#<>]|rgb\(|hsl\(|px\b|rem\b|\dem\b|pt\b|color:|font-|css|html|pdf|page\s*\d", re.I)
PROSE_KEYS = {"text", "title", "body", "prose", "html", "css"}
PAGE_NUM_KEYS = {"page_number", "page_numbers", "pagination"}


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _layouts() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "layouts").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["layout_id"])


def _component_ids() -> dict[str, set[str]]:
    catalog = _load("assets/component_catalog.json")
    return {kind: {item["id"] for item in entries} for kind, entries in catalog["components"].items()}


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_21_layout_library_core"
    assert package["package_type"] == "report"
    assert package["category_id"] == "layout_library"
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
    assert json.loads(encoded)["package_id"] == "bz_21_layout_library_core"


def test_package_loading() -> None:
    layouts = _layouts()
    assert len(layouts) == 500
    assert layouts[0]["layout_id"] == "LAY-000001"
    assert layouts[-1]["layout_id"] == "LAY-000500"
    index = _load("layouts/index.json")
    assert index["count"] == 500
    assert len(index["layout_ids"]) == 500


def test_duplicate_ids() -> None:
    layouts = _layouts()
    assert len({item["layout_id"] for item in layouts}) == 500
    assert len({item["layout_name"] for item in layouts}) == 500
    orders = [tuple(item["section_order"]) for item in layouts]
    assert len(set(orders)) >= 10
    signatures = [
        (
            item["theme_id"],
            item["page_structure"],
            tuple(item["section_order"]),
            tuple(item["block_order"]),
            item["column_model"],
            item["page_break_policy"],
            item["keep_together"],
            item["widow_orphan_policy"],
            item["toc_policy"],
            item["appendix_policy"],
        )
        for item in layouts
    ]
    assert len(signatures) == len(set(signatures))


def test_deterministic_ordering() -> None:
    layouts = _layouts()
    assert [item["layout_id"] for item in layouts] == sorted(item["layout_id"] for item in layouts)
    for item in layouts:
        assert item["section_order"]
        assert item["section_order"] == list(item["section_order"])
        assert len(item["section_order"]) == len(set(item["section_order"]))
        assert len(item["block_order"]) == len(set(item["block_order"]))


def test_component_integrity() -> None:
    catalog = _component_ids()
    for item in _layouts():
        assert not PROSE_KEYS.intersection(item.keys())
        assert not PAGE_NUM_KEYS.intersection(item.keys())
        assert item["page_structure"] in catalog["page_structure"]
        assert item["column_model"] in catalog["column_model"]
        assert item["page_break_policy"] in catalog["page_break_policy"]
        assert item["keep_together"] in catalog["keep_together"]
        assert item["widow_orphan_policy"] in catalog["widow_orphan_policy"]
        assert item["toc_policy"] in catalog["toc_policy"]
        assert item["appendix_policy"] in catalog["appendix_policy"]
        for sid in item["section_order"]:
            assert sid in catalog["section"]
        for bid in item["block_order"]:
            assert bid in catalog["block"]
        for tid in item["table_ids"]:
            assert tid in catalog["table"]
        for cid in item["chart_ids"]:
            assert cid in catalog["chart"]
        for wid in item["widget_ids"]:
            assert wid in catalog["widget"]
        blob = json.dumps(item, ensure_ascii=False)
        assert not STYLE_FORBIDDEN.search(blob)


def test_reference_integrity() -> None:
    theme_ids = set(_load("themes/index.json", THM_ROOT)["theme_ids"])
    rct_ids = {item["id"] for item in _load("assets/component_catalog.json", THM_ROOT)["components"]["report_contract"]}
    for item in _layouts():
        assert item["theme_id"] in theme_ids
        assert item["report_contract_id"] in rct_ids
        assert item["composition_ids"]
        assert all(cid.startswith("CMP-") for cid in item["composition_ids"])


def test_theme_layout_contract() -> None:
    layouts = {item["layout_id"] for item in _layouts()}
    for path in (THM_ROOT / "themes").glob("*.json"):
        if path.name == "index.json":
            continue
        for theme in json.loads(path.read_text(encoding="utf-8"))["objects"]:
            assert theme["layout_id"] in layouts


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

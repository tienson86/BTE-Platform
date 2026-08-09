"""Package-level tests for bz_22_widget_library_core PK-3. No engine imports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT.parents[2] / "package_spec"
KNOWLEDGE = ROOT.parents[2]
LAY_ROOT = KNOWLEDGE / "packages" / "layout_library" / "core"
THM_ROOT = KNOWLEDGE / "packages" / "theme_library" / "core"
STYLE_FORBIDDEN = re.compile(
    r"[#<>]|rgb\(|hsl\(|px\b|rem\b|\dem\b|pt\b|color:|font-|css\b|jsx\b|svg\b",
    re.I,
)
PROSE_KEYS = {"text", "title", "body", "prose", "html", "css", "jsx", "svg"}
RENDERERS = {"pdf", "docx", "html", "markdown", "json"}
CONTRACT_PREFIX = {
    "RCT": "report_contract",
    "ANL": "analysis_contract",
    "DCS": "decision_contract",
    "LCK": "luck_contract",
    "ITP": "interpretation_contract",
}


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _widgets() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "widgets").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["widget_id"])


def _component_ids() -> dict[str, set[str]]:
    catalog = _load("assets/component_catalog.json")
    return {kind: {item["id"] for item in entries} for kind, entries in catalog["components"].items()}


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_22_widget_library_core"
    assert package["package_type"] == "report"
    assert package["category_id"] == "widget_library"
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
    assert json.loads(encoded)["package_id"] == "bz_22_widget_library_core"


def test_package_loading() -> None:
    widgets = _widgets()
    assert len(widgets) == 400
    assert widgets[0]["widget_id"] == "WDG-000001"
    assert widgets[-1]["widget_id"] == "WDG-000400"
    index = _load("widgets/index.json")
    assert index["count"] == 400
    assert len(index["widget_ids"]) == 400


def test_duplicate_ids() -> None:
    widgets = _widgets()
    assert len({item["widget_id"] for item in widgets}) == 400
    assert len({item["widget_name"] for item in widgets}) == 400
    signatures = [
        (
            item["category"],
            item["layout_id"],
            tuple(item["theme_ids"]),
            tuple(item["required_contracts"]),
            tuple(item["optional_contracts"]),
            tuple(item["required_assets"]),
            tuple(item["supported_renderers"]),
            item["placement"],
        )
        for item in widgets
    ]
    assert len(signatures) == len(set(signatures))


def test_deterministic_ordering() -> None:
    widgets = _widgets()
    assert [item["widget_id"] for item in widgets] == sorted(item["widget_id"] for item in widgets)
    for item in widgets:
        assert item["theme_ids"] == list(item["theme_ids"])
        assert len(item["theme_ids"]) == len(set(item["theme_ids"]))
        assert item["required_contracts"]
        assert len(item["required_contracts"]) == len(set(item["required_contracts"]))
        assert len(item["optional_contracts"]) == len(set(item["optional_contracts"]))


def test_reference_integrity() -> None:
    catalog = _component_ids()
    for item in _widgets():
        assert not PROSE_KEYS.intersection(item.keys())
        assert item["layout_id"].startswith("LAY-")
        assert item["placement"] in catalog["placement"]
        for tid in item["theme_ids"]:
            assert tid.startswith("THM-")
        for cid in item["required_contracts"] + item["optional_contracts"]:
            prefix = cid.split("-", 1)[0]
            assert prefix in CONTRACT_PREFIX
            assert cid in catalog[CONTRACT_PREFIX[prefix]]
        for aid in item["required_assets"]:
            assert aid in catalog["asset_slot"]
        blob = json.dumps(item, ensure_ascii=False)
        assert not STYLE_FORBIDDEN.search(blob)


def test_layout_theme_compatibility() -> None:
    widgets = _widgets()
    if (LAY_ROOT / "layouts" / "index.json").exists():
        layout_ids = set(_load("layouts/index.json", LAY_ROOT)["layout_ids"])
        for item in widgets:
            assert item["layout_id"] in layout_ids
        catalog_wdg = {
            entry["id"]
            for entry in _load("assets/component_catalog.json", LAY_ROOT)["components"]["widget"]
        }
        present = {item["widget_id"] for item in widgets}
        assert catalog_wdg <= present
    if (THM_ROOT / "themes" / "index.json").exists():
        theme_ids = set(_load("themes/index.json", THM_ROOT)["theme_ids"])
        for item in widgets:
            for tid in item["theme_ids"]:
                assert tid in theme_ids


def test_renderer_compatibility() -> None:
    catalog = _load("assets/component_catalog.json")
    allowed = {entry["renderer_key"] for entry in catalog["components"]["renderer"]}
    assert allowed == RENDERERS
    for item in _widgets():
        assert item["supported_renderers"]
        assert set(item["supported_renderers"]) <= RENDERERS
        assert item["supported_renderers"] == [key for key in ("pdf", "docx", "html", "markdown", "json") if key in item["supported_renderers"]]


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

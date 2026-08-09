"""Package-level tests for bz_23_report_presets_core PK-4. No engine imports."""
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
LAY_ROOT = KNOWLEDGE / "packages" / "layout_library" / "core"
WDG_ROOT = KNOWLEDGE / "packages" / "widget_library" / "core"
NAR_ROOT = KNOWLEDGE / "packages" / "narrative_library" / "core"
STYLE_FORBIDDEN = re.compile(
    r"[#<>]|rgb\(|hsl\(|\bpx\b|\brem\b|\dem\b|\bpt\b|color:|font-|css\b|jsx\b|svg\b",
    re.I,
)
PROSE_KEYS = {"text", "title", "body", "prose", "html", "css", "jsx", "svg"}
RENDERERS = {"pdf", "docx", "html", "markdown", "json"}


def _load(rel: str, base: Path = ROOT):
    return json.loads((base / rel).read_text(encoding="utf-8"))


def _presets() -> list[dict]:
    items: list[dict] = []
    for path in sorted((ROOT / "presets").glob("*.json")):
        if path.name == "index.json":
            continue
        items.extend(json.loads(path.read_text(encoding="utf-8"))["objects"])
    return sorted(items, key=lambda item: item["preset_id"])


def _ids(folder: Path, index_name: str, key: str) -> set[str]:
    index = json.loads((folder / index_name).read_text(encoding="utf-8"))
    return set(index[key])


def test_package_identity() -> None:
    package = _load("PACKAGE.json")
    assert package["package_id"] == "bz_23_report_presets_core"
    assert package["package_type"] == "report"
    assert package["category_id"] == "report_presets"
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
    assert json.loads(encoded)["package_id"] == "bz_23_report_presets_core"


def test_package_loading() -> None:
    presets = _presets()
    assert len(presets) == 250
    assert presets[0]["preset_id"] == "RPT-000001"
    assert presets[-1]["preset_id"] == "RPT-000250"
    index = _load("presets/index.json")
    assert index["count"] == 250
    assert len(index["preset_ids"]) == 250


def test_duplicate_ids() -> None:
    presets = _presets()
    assert len({item["preset_id"] for item in presets}) == 250
    assert len({item["preset_name"] for item in presets}) == 250
    signatures = [
        (
            item["theme_id"],
            item["layout_id"],
            tuple(item["widget_ids"]),
            tuple(item["narrative_template_ids"]),
            tuple(item["section_sequence"]),
            tuple(item["renderer_preferences"]),
            tuple(item["supported_contracts"]),
        )
        for item in presets
    ]
    assert len(signatures) == len(set(signatures))


def test_deterministic_ordering() -> None:
    presets = _presets()
    assert [item["preset_id"] for item in presets] == sorted(item["preset_id"] for item in presets)
    for item in presets:
        assert item["widget_ids"]
        assert len(item["widget_ids"]) == len(set(item["widget_ids"]))
        assert item["narrative_template_ids"]
        assert len(item["narrative_template_ids"]) == len(set(item["narrative_template_ids"]))
        assert item["section_sequence"]
        assert len(item["section_sequence"]) == len(set(item["section_sequence"]))
        assert item["supported_contracts"]
        assert all(cid.startswith("RCT-") for cid in item["supported_contracts"])


def test_reference_integrity() -> None:
    catalog = _load("assets/component_catalog.json")
    rct_ids = {entry["id"] for entry in catalog["components"]["report_contract"]}
    for item in _presets():
        assert not PROSE_KEYS.intersection(item.keys())
        assert item["theme_id"].startswith("THM-")
        assert item["layout_id"].startswith("LAY-")
        assert all(wid.startswith("WDG-") for wid in item["widget_ids"])
        assert all(nid.startswith("NAR-") for nid in item["narrative_template_ids"])
        assert all(sid.startswith("SEC-") for sid in item["section_sequence"])
        for cid in item["supported_contracts"]:
            assert cid in rct_ids
        blob = json.dumps(item, ensure_ascii=False)
        assert not STYLE_FORBIDDEN.search(blob)
        assert set(item["renderer_preferences"]) <= RENDERERS
        assert item["renderer_preferences"] == [
            key for key in ("pdf", "docx", "html", "markdown", "json") if key in item["renderer_preferences"]
        ]


def test_preset_compatibility() -> None:
    presets = _presets()
    if (THM_ROOT / "themes" / "index.json").exists():
        theme_ids = _ids(THM_ROOT / "themes", "index.json", "theme_ids")
        for item in presets:
            assert item["theme_id"] in theme_ids
    if (LAY_ROOT / "layouts" / "index.json").exists():
        layout_ids = _ids(LAY_ROOT / "layouts", "index.json", "layout_ids")
        layouts = {}
        for path in (LAY_ROOT / "layouts").glob("*.json"):
            if path.name == "index.json":
                continue
            for layout in json.loads(path.read_text(encoding="utf-8"))["objects"]:
                layouts[layout["layout_id"]] = layout
        for item in presets:
            assert item["layout_id"] in layout_ids
            layout = layouts[item["layout_id"]]
            assert item["section_sequence"] == layout["section_order"]
            assert set(layout["widget_ids"]) <= set(item["widget_ids"])
    if (WDG_ROOT / "widgets" / "index.json").exists():
        widget_ids = _ids(WDG_ROOT / "widgets", "index.json", "widget_ids")
        for item in presets:
            for wid in item["widget_ids"]:
                assert wid in widget_ids
    if (NAR_ROOT / "templates" / "index.json").exists():
        narrative_ids = _ids(NAR_ROOT / "templates", "index.json", "template_ids")
        for item in presets:
            for nid in item["narrative_template_ids"]:
                assert nid in narrative_ids


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

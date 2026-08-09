"""QC-2 report snapshots reference sealed presentation identifiers."""
from __future__ import annotations

import json
from pathlib import Path

QC2 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
THM = REPO / "knowledge" / "packages" / "theme_library" / "core"
LAY = REPO / "knowledge" / "packages" / "layout_library" / "core"
WDG = REPO / "knowledge" / "packages" / "widget_library" / "core"
RPT = REPO / "knowledge" / "packages" / "report_presets" / "core"


def test_report_snapshots_use_presentation_prefixes() -> None:
    folder = QC2 / "snapshots" / "report"
    assert len(list(folder.glob("*.json"))) == 13
    for path in folder.glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        outputs = item["canonical_outputs"]
        assert outputs["preset_id"].startswith("RPT-")
        assert outputs["theme_id"].startswith("THM-")
        assert outputs["layout_id"].startswith("LAY-")
        assert outputs["report_contract_id"].startswith("RCT-")
        assert outputs["widget_ids"]
        assert all(wid.startswith("WDG-") for wid in outputs["widget_ids"])
        assert item["audit"]["pdf"] is False
        assert item["audit"]["html"] is False
        assert item["audit"]["docx"] is False


def test_report_ids_exist_in_sealed_packages() -> None:
    themes = set(json.loads((THM / "themes" / "index.json").read_text(encoding="utf-8"))["theme_ids"])
    layouts = set(json.loads((LAY / "layouts" / "index.json").read_text(encoding="utf-8"))["layout_ids"])
    widgets = set(json.loads((WDG / "widgets" / "index.json").read_text(encoding="utf-8"))["widget_ids"])
    presets = set(json.loads((RPT / "presets" / "index.json").read_text(encoding="utf-8"))["preset_ids"])
    for path in (QC2 / "snapshots" / "report").glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        outputs = item["canonical_outputs"]
        assert outputs["theme_id"] in themes
        assert outputs["layout_id"] in layouts
        assert outputs["preset_id"] in presets
        for wid in outputs["widget_ids"]:
            assert wid in widgets

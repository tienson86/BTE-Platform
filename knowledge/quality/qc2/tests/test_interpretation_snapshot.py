"""QC-2 interpretation snapshots reference sealed IK identifiers."""
from __future__ import annotations

import json
from pathlib import Path

QC2 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
NAR = REPO / "knowledge" / "packages" / "narrative_library" / "core"
SEN = REPO / "knowledge" / "packages" / "sentence_library" / "core"


def test_interpretation_snapshots_use_ik_prefixes() -> None:
    folder = QC2 / "snapshots" / "interpretation"
    assert len(list(folder.glob("*.json"))) == 13
    for path in folder.glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        outputs = item["canonical_outputs"]
        assert outputs["sentence_ids"]
        assert outputs["explanation_ids"]
        assert outputs["narrative_template_ids"]
        assert outputs["composition_ids"]
        assert all(sid.startswith("SEN-") for sid in outputs["sentence_ids"])
        assert all(eid.startswith("EXP-") for eid in outputs["explanation_ids"])
        assert all(nid.startswith("NAR-") for nid in outputs["narrative_template_ids"])
        assert all(cid.startswith("CMP-") for cid in outputs["composition_ids"])
        assert "bz_16_sentence_library_core" in item["trace"]["package_ids"]
        assert "bz_18_narrative_library_core" in item["trace"]["package_ids"]


def test_interpretation_ids_exist_in_sealed_packages() -> None:
    nar_ids = set(json.loads((NAR / "templates" / "index.json").read_text(encoding="utf-8"))["template_ids"])
    sen_ids = set(json.loads((SEN / "sentences" / "index.json").read_text(encoding="utf-8"))["sentence_ids"])
    for path in (QC2 / "snapshots" / "interpretation").glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        for nid in item["canonical_outputs"]["narrative_template_ids"]:
            assert nid in nar_ids
        for sid in item["canonical_outputs"]["sentence_ids"]:
            assert sid in sen_ids

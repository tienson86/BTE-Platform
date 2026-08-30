"""N-IMP-11 Presentation Export Layer tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.export import (
    PresentationExportLayer,
    presentation_from_mapping,
    serialize_presentation,
)
from engines.narrative_v2.export.export_errors import IncompatiblePresentationVersion
from engines.narrative_v2.presentation import PRESENTATION_VERSION, NarrativeV2Presentation
from engines.narrative_v2.runtime import NarrativeRuntime

REPO = Path(__file__).resolve().parents[2]
FROZEN = (
    REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
)
EXPORT_PY = REPO / "applications" / "api" / "routes" / "export.py"
EXPORT_DIR = REPO / "engines" / "narrative_v2" / "export"
PACK05_ENGINE = REPO / "engines" / "narrative_engine" / "engine.py"


@pytest.fixture(scope="module")
def case0001_presentation(case_0001_canonical: dict[str, Any]) -> NarrativeV2Presentation:
    result = NarrativeRuntime().run(case_0001_canonical)
    assert isinstance(result.presentation, NarrativeV2Presentation)
    return result.presentation


@pytest.fixture(scope="module")
def case0001_bundle(case0001_presentation: NarrativeV2Presentation, tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("nimp11")
    layer = PresentationExportLayer()
    return layer.export_all(
        case0001_presentation,
        pdf_path=root / "pdf_shadow.pdf",
        docx_path=root / "docx_shadow.docx",
    )


def test_json_equals_presentation(case0001_bundle) -> None:
    payload = serialize_presentation(presentation_from_mapping(dict(case0001_bundle.json.payload)))
    assert case0001_bundle.json.payload == payload
    assert case0001_bundle.json.payload == case0001_bundle.context.presentation
    assert case0001_bundle.json.version == PRESENTATION_VERSION


def test_portal_export_is_presentation_copy(case0001_bundle) -> None:
    portal = case0001_bundle.portal
    assert portal.shadow_mode is True
    assert portal.replaces_pack05 is False
    assert portal.presentation == case0001_bundle.json.payload
    assert portal.version == PRESENTATION_VERSION


def test_parity_portal_pdf_docx_json(case0001_bundle) -> None:
    expected = tuple(block.text for block in case0001_bundle.context.blocks)
    assert expected
    assert tuple(block.text for block in case0001_bundle.portal.blocks) == expected
    assert tuple(block.text for block in case0001_bundle.json.blocks) == expected
    from engines.narrative_v2.export.pdf_export import extract_html_texts

    assert extract_html_texts(case0001_bundle.pdf.html) == expected
    assert case0001_bundle.docx.paragraphs == expected
    assert case0001_bundle.pdf.pdf_bytes[:4] == b"%PDF"
    assert Path(case0001_bundle.docx.path or "").is_file()


def test_no_private_tokens_in_exports(case0001_bundle) -> None:
    blob = (
        case0001_bundle.json.text
        + case0001_bundle.pdf.html
        + "\n".join(case0001_bundle.docx.paragraphs)
    )
    for token in (
        "pipeline_trace",
        "NR-REL-",
        "knowledge.pattern.chinh_an",
        "source_unit_ids",
        "runtime_metrics",
        "evidence.strength.level",
    ):
        assert token not in blob


def test_consumers_do_not_compose() -> None:
    for name in ("pdf_export.py", "docx_export.py", "portal_export.py", "json_export.py"):
        source = (EXPORT_DIR / name).read_text(encoding="utf-8")
        assert "if consumer" not in source
        assert "create summary" not in source.lower()
        assert "overview.observation" not in source
    builder = (EXPORT_DIR / "export_builder.py").read_text(encoding="utf-8")
    assert "does not join" in builder.lower()
    pdf_source = (EXPORT_DIR / "pdf_export.py").read_text(encoding="utf-8")
    assert "block.text" in pdf_source
    docx_source = (EXPORT_DIR / "docx_export.py").read_text(encoding="utf-8")
    assert "block.text" in docx_source


def test_incompatible_version_rejected(case0001_presentation: NarrativeV2Presentation) -> None:
    from dataclasses import replace

    from engines.narrative_v2.presentation.presentation_metadata import PresentationMetadata

    bad = replace(
        case0001_presentation,
        metadata=replace(case0001_presentation.metadata, version="bte.presentation.v2"),
    )
    with pytest.raises(IncompatiblePresentationVersion):
        PresentationExportLayer().prepare(bad)


def test_shadow_mode_production_untouched() -> None:
    export = EXPORT_PY.read_text(encoding="utf-8")
    assert "narrative_v2" not in export
    assert PACK05_ENGINE.is_file()
    for path in EXPORT_DIR.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "engines.narrative_engine" not in text
        assert "engines.report_engine" not in text
        assert "HtmlReportV1Renderer" not in text


def test_frozen_case0001_json_roundtrip() -> None:
    import json

    payload = json.loads(FROZEN.read_text(encoding="utf-8"))
    presentation = presentation_from_mapping(payload)
    again = serialize_presentation(presentation)
    assert again["interpretation"]["consulting_flow"] == payload["interpretation"]["consulting_flow"]
    assert again["metadata"]["version"] == PRESENTATION_VERSION


def test_null_fields_not_invented(case0001_bundle) -> None:
    overview = case0001_bundle.json.payload["overview"]
    assert overview["identity"] is None
    assert overview["balance"] is None
    assert overview["conclusion"] is None
    fields = {block.field for block in case0001_bundle.context.blocks}
    assert "overview.identity" not in fields
    assert case0001_bundle.json.payload["commercial"] is None

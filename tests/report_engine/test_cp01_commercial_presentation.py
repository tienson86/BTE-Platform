"""CP-01 commercial presentation: adapter, HTML, PDF, and DOCX."""

from __future__ import annotations

import json
from pathlib import Path

from docx import Document

from engines.report_engine.adapters.commercial_presentation_adapter import (
    COMMERCIAL_PRESENTATION_EMPTY,
    CommercialPresentationAdapter,
)
from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.exporting.docx_exporter_v1 import DocxExporterV1
from engines.report_engine.exporting.pdf_exporter_v1 import PdfExporterV1
from engines.report_engine.rendering.html_report_v1 import render_html
from engines.report_engine.rendering.report_sections_v1 import build_presented_report

_ADAPTER_SRC = (
    Path(__file__).resolve().parents[2]
    / "engines"
    / "report_engine"
    / "adapters"
    / "commercial_presentation_adapter.py"
)


def _complete_payload() -> dict:
    """Two-domain composed consulting fixture. Presentation must copy, not invent."""
    return {
        "status": "complete",
        "sections": [
            {
                "domain": "career",
                "title": "Sự nghiệp",
                "summary": "Tóm tắt sự nghiệp.",
                "meaning": ["Ý nghĩa sự nghiệp."],
                "recommendations": ["Hành động sự nghiệp."],
                "source_unit_ids": ["ck-career-001"],
            },
            {
                "domain": "finance",
                "title": "Tài chính",
                "summary": "Tóm tắt tài chính.",
                "meaning": ["Ý nghĩa tài chính."],
                "recommendations": ["Hành động tài chính."],
                "source_unit_ids": ["ck-finance-001"],
            },
        ],
    }


def _insufficient_payload() -> dict:
    """Empty composed consulting. Presentation must not invent advice."""
    return {"status": "insufficient", "sections": []}


def _document_text(path: Path) -> str:
    """Join DOCX paragraph text for content comparison."""
    document = Document(str(path))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


class _CapturePdfBackend:
    """Record HTML passed to PDF. Do not invent a second template."""

    def __init__(self) -> None:
        self.html = ""

    def html_to_pdf(self, html: str, output_path: Path, *, title: str) -> int | None:
        """Write a minimal valid PDF signature so the exporter can finish."""
        self.html = html
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n" + b"0" * 2048)
        return 1


def test_adapter_does_not_match_or_compose() -> None:
    """Presentation adapter stays a formatter. Matcher and composer stay upstream."""
    source = _ADAPTER_SRC.read_text(encoding="utf-8")
    assert "match_published_knowledge" not in source
    assert "compose_commercial" not in source
    assert "match_consulting_knowledge" not in source


def test_p1_commercial_section_displays_customer_fields() -> None:
    """P1: composed consulting appears as title, summary, meaning, recommendations."""
    model = CommercialPresentationAdapter().adapt(_complete_payload())
    assert model.visible is True
    assert model.status == "complete"
    first = model.sections[0]
    assert first.title == "Sự nghiệp"
    assert first.summary == "Tóm tắt sự nghiệp."
    assert first.meaning == ("Ý nghĩa sự nghiệp.",)
    assert first.recommendations == ("Hành động sự nghiệp.",)
    assert first.source_unit_ids == ("ck-career-001",)
    assert "source_unit_ids" not in first.customer_dict()
    html = render_html(ReportInputV1(commercial_consulting=_complete_payload()))
    assert "Sự nghiệp" in html
    assert "Tóm tắt sự nghiệp." in html
    assert "Ý nghĩa sự nghiệp." in html
    assert "Hành động sự nghiệp." in html
    assert "ck-career-001" not in html
    assert "source_unit_ids" not in html


def test_p2_domains_keep_composer_order() -> None:
    """P2: multiple domains render in the composed order."""
    model = CommercialPresentationAdapter().adapt(_complete_payload())
    assert [section.domain for section in model.sections] == ["career", "finance"]
    presented = build_presented_report(
        ReportInputV1(commercial_consulting=_complete_payload())
    )
    titles = [section.title for section in presented.sections]
    career_at = titles.index("Sự nghiệp")
    finance_at = titles.index("Tài chính")
    recommendations_at = titles.index("16. Khuyến nghị")
    conclusion_at = titles.index("17. Tổng kết")
    assert career_at < finance_at < recommendations_at < conclusion_at


def test_p3_insufficient_hides_advice() -> None:
    """P3: insufficient consulting shows the canonical empty copy, not invented advice."""
    model = CommercialPresentationAdapter().adapt(_insufficient_payload())
    assert model.visible is False
    assert model.sections == ()
    assert model.customer_texts() == ()
    html = render_html(ReportInputV1(commercial_consulting=_insufficient_payload()))
    assert COMMERCIAL_PRESENTATION_EMPTY in html
    assert "Hành động sự nghiệp." not in html
    omitted = render_html(ReportInputV1())
    assert COMMERCIAL_PRESENTATION_EMPTY not in omitted
    assert "Tóm tắt sự nghiệp." not in omitted


def test_p4_html_pdf_docx_share_presentation_model(tmp_path: Path) -> None:
    """P4: HTML, PDF, and DOCX consume the same presentation model."""
    report_input = ReportInputV1(commercial_consulting=_complete_payload())
    model = CommercialPresentationAdapter().adapt(report_input.commercial_consulting)
    html = render_html(report_input)
    backend = _CapturePdfBackend()
    PdfExporterV1(backend=backend).export(report_input, tmp_path / "consulting.pdf")
    docx_path = tmp_path / "consulting.docx"
    DocxExporterV1().export(report_input, docx_path)
    docx_text = _document_text(docx_path)
    assert backend.html == html
    for text in model.customer_texts():
        assert text in html
        assert text in docx_text
    assert "ck-career-001" not in html
    assert "ck-finance-001" not in html
    assert "ck-career-001" not in docx_text
    assert "ck-finance-001" not in docx_text


def test_p5_case_0001_snapshot_presents_without_trace_ids() -> None:
    """P5: CASE-0001 snapshot consulting is rendered; source_unit_ids stay internal."""
    expected_path = (
        Path(__file__).resolve().parents[1]
        / "golden_dataset"
        / "report_v1"
        / "CASE-0001"
        / "expected_report_input.json"
    )
    snapshot = json.loads(expected_path.read_text(encoding="utf-8"))
    consulting = snapshot["commercial_consulting"]
    assert consulting["status"] == "complete"
    html = render_html(ReportInputV1(commercial_consulting=consulting))
    first = consulting["sections"][0]
    assert first["title"] in html
    assert first["summary"] in html
    for section in consulting["sections"]:
        for unit_id in section["source_unit_ids"]:
            assert unit_id not in html


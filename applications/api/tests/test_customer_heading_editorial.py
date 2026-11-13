"""Customer headings stay meaningful across the screen and both export formats."""
from pathlib import Path
from docx import Document
import pytest
from applications.api.services.customer_export import (
    _split_structured_paragraph, _split_domain_paragraph, _structured_chapter_html,
    _docx_structured_chapter, _infer_domain_title,
)

@pytest.mark.parametrize("chapter,title", [
    ("four_pillars", "Vai trò trong Tứ trụ"),
    ("day_master", "Khí chất và cách ứng xử"),
    ("strength_structure_useful_god", "Cân bằng toàn cục"),
    ("ten_gods", "Ý nghĩa và mối liên hệ"),
    ("shen_sha", "Ý nghĩa bổ trợ"),
    ("bone_weight", "Ý nghĩa cân lượng"),
    ("palace_feng_shui", "Ứng dụng phương vị"),
    ("luck_cycles", "Trọng tâm giai đoạn"),
])
def test_fallback_is_semantic_not_numbered(chapter, title):
    body = "Bạn nên cân nhắc điều phù hợp với hoàn cảnh của mình."
    assert _split_structured_paragraph(chapter, body, 7) == (title, body)
    html = _structured_chapter_html(chapter, [body])
    assert f"<h3>{title}</h3>" in html
    document = Document()
    _docx_structured_chapter(document, chapter, [body])
    assert document.paragraphs[-2].text == f"01. {title}"
    assert document.paragraphs[-1].text == body
    root = Path(__file__).resolve().parents[3]
    for relative in (
        "customer_portal/static/js/bazi_report_document_mount.js",
        "customer_portal/src/screens/commercial_dashboard/ReportDocumentSection.tsx",
    ):
        source = (root / "applications" / relative).read_text(encoding="utf-8")
        assert f'cardTitle: "{title}"' in source
        assert "${meta.cardTitle} ${" not in source

@pytest.mark.parametrize("placeholder", ["Luận trục 3", "Luận Cân xương 2", "Góc nhìn bổ sung 1"])
def test_legacy_placeholder_is_removed_without_losing_body(placeholder):
    body = "Bạn nên giữ một kế hoạch vừa sức."
    assert _split_structured_paragraph("bone_weight", placeholder + ": " + body, 1) == ("Ý nghĩa cân lượng", body)
    assert _split_domain_paragraph(placeholder + ": " + body, 1) == ("Ứng dụng trong đời sống", body)


def test_specific_headings_and_content_are_preserved():
    value = "Bính Tuất, 2022–2031: Chính Tài và trách nhiệm với nguồn thu."
    assert _split_structured_paragraph("luck_cycles", value, 4) == (
        "Bính Tuất, 2022–2031", "Chính Tài và trách nhiệm với nguồn thu.")
    assert _infer_domain_title("Một lời nhắc phù hợp.", 10) == "Ứng dụng trong đời sống"


@pytest.mark.parametrize("has_counts", [True, False])
def test_five_elements_keeps_every_canonical_paragraph_in_html_and_docx(tmp_path, monkeypatch, has_counts):
    from types import SimpleNamespace
    from applications.api.services import customer_export as exports
    paragraphs = ["Canonical lead <retained>.", "Second canonical paragraph.", "Final canonical paragraph."]
    chapter = {"id": "five_elements", "title": "Five elements", "paragraphs": paragraphs, "bullets": []}
    report = SimpleNamespace(
        modern_report={"chapters": [chapter]},
        five_elements=SimpleNamespace(**{key: (i if has_counts else None) for i, key in enumerate(("wood", "fire", "earth", "metal", "water"), 1)}),
        metadata=SimpleNamespace(case_id="five-elements-regression", generated_at=""),
    )
    html = exports._chapter_html(chapter, report)
    from html import escape
    for paragraph in paragraphs:
        assert html.count(escape(paragraph)) == 1
    if has_counts:
        assert html.index('class="element"') < html.index(escape(paragraphs[0]))
    monkeypatch.setattr(exports, "_docx_opening_chart", lambda document, report_input: None)
    output = tmp_path / "five-elements.docx"
    exports._render_modern_report_docx(report, output)
    document = Document(output)
    lines = [paragraph.text for paragraph in document.paragraphs]
    for paragraph in paragraphs:
        assert lines.count(paragraph) == 1
    assert len(document.tables) == (1 if has_counts else 0)
    if has_counts:
        children = list(document.element.body)
        assert children.index(document.tables[0]._tbl) < children.index(document.paragraphs[1]._p)


def test_domain_print_layout_can_fragment_without_orphaning_headings():
    from applications.api.services import customer_export as exports
    source = Path(exports.__file__).read_text(encoding="utf-8")
    assert "#life_domains { break-inside: auto; }" in source
    assert "#life_domains > h2, #life_domains .domain-group > h3 { break-after: avoid; page-break-after: avoid; }" in source
    assert "#life_domains .domains, #life_domains .domain-grid { display: block; }" in source
    assert "#life_domains .domain-group { break-inside: auto;" in source

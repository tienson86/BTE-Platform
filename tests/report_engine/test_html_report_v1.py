"""Tests for HTML Report V1 renderer."""

from __future__ import annotations

from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from engines.report_engine.rendering.html_report_v1 import HtmlReportV1Renderer, render_html
from tests.report_engine.case_0001_runtime import build_case_0001_source


def test_render_html_returns_utf8_document() -> None:
    """Renderer returns a UTF-8 HTML document string."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    html = render_html(report_input)
    assert html.startswith("<!DOCTYPE html>")
    assert 'charset="utf-8"' in html.lower()


def test_render_html_preserves_vietnamese() -> None:
    """Vietnamese diacritics are preserved in output."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    html = render_html(report_input)
    assert "Nguyễn Tiến Sơn" in html
    assert "Báo cáo" in html


def test_render_html_required_headings_present() -> None:
    """Required report section headings are present."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    html = HtmlReportV1Renderer().render(report_input)
    for heading in (
        "01. Thông tin lá số",
        "02. Tứ Trụ",
        "03. Ngũ hành",
        "04. Thân vượng nhược",
        "10. Luận giải tổng thể",
        "17. Tổng kết",
    ):
        assert heading in html


def test_case_0001_renders_without_exception() -> None:
    """CASE-0001 integration path renders end-to-end."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    html = render_html(report_input)
    assert len(html) > 500
    assert "Canh" in html

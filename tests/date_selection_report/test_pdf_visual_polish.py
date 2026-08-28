"""P6-03A visual polish: presentation only."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.date_selection_report.exporting.html_projection import project_render_tree_to_html
from engines.date_selection_report.exporting.pdf_exporter import DateSelectionPdfExporter
from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.tree import build_render_tree, create_render_context
from engines.report_engine.exporting.pdf_exporter_v1 import MIN_PDF_BYTES, validate_pdf_file


def test_commercial_layout_classes(presentation_model: DateSelectionReportModel) -> None:
    html = project_render_tree_to_html(
        build_render_tree(create_render_context(presentation_model))
    )
    assert 'class="ds-cover"' in html or "ds-cover" in html
    assert "ds-card" in html
    assert "ds-kv" in html
    assert "ds-summary" in html
    assert "ds-recommendation" in html
    assert "ds-date-day" in html
    assert "ds-day-info" in html
    assert "ds-ke-group" in html
    assert "ds-pill" in html
    assert "ds-exec" in html
    assert "Khách hàng" in html
    assert "letter-spacing" in html
    assert "page-break-inside: avoid" in html
    assert "Cấn" in html and "Thổ" in html
    assert "{{" not in html


def test_visual_polish_does_not_mutate_model(
    presentation_model: DateSelectionReportModel,
) -> None:
    before = presentation_model.to_dict()
    project_render_tree_to_html(build_render_tree(create_render_context(presentation_model)))
    assert presentation_model.to_dict() == before
    assert presentation_model.recommendations[0].cung == "Cấn"
    assert presentation_model.recommendations[0].cung_element == "Thổ"


def test_unicode_and_pagination_css(presentation_model: DateSelectionReportModel) -> None:
    html = project_render_tree_to_html(
        build_render_tree(create_render_context(presentation_model))
    )
    assert "Nguyễn Tiến Sơn" in html
    assert "BÁO CÁO CHỌN NGÀY TỐT" in html
    assert ".ds-recommendation" in html
    assert "break-inside: avoid" in html


def test_polished_pdf_generates(
    presentation_model: DateSelectionReportModel,
    tmp_path: Path,
) -> None:
    pytest.importorskip("playwright")
    tree = build_render_tree(create_render_context(presentation_model))
    result = DateSelectionPdfExporter().export(tree, tmp_path)
    output = Path(result.file_path)
    validate_pdf_file(output)
    assert result.page_count is not None and result.page_count > 0
    assert output.stat().st_size > MIN_PDF_BYTES
    assert "Nguyễn Tiến Sơn" in project_render_tree_to_html(tree)


def test_executive_summary_reuses_existing_fields(
    presentation_model: DateSelectionReportModel,
) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    html = project_render_tree_to_html(tree)
    assert "Khách hàng" in html
    assert tree.person.rows[0].value in html
    assert "Tây Tứ Trạch" in html
    assert "09/2026" in html
    assert tree.search_period.recommendation_count in html


def test_recommendation_content_unchanged(
    presentation_model: DateSelectionReportModel,
) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    html = project_render_tree_to_html(tree)
    rec = tree.recommendations[0]
    assert html.index(rec.date_header.solar_date) < html.index(rec.compatible_hours.rows[0].display)
    assert [hour.display for hour in rec.compatible_hours.rows] == [
        "Giờ Thìn (07:01–09:00) · Càn (Kim)",
        "Giờ Tỵ (09:01–11:00) · Khôn (Thổ)",
    ]
    labels = [group.label for group in rec.positive_times.groups]
    assert labels == ["Đại An", "Tốc Hỷ", "Tiểu Cát"]
    for hour in rec.compatible_hours.rows:
        assert hour.display in html
    for group in rec.positive_times.groups:
        assert group.label in html
        for item in group.items:
            assert item.time_range in html

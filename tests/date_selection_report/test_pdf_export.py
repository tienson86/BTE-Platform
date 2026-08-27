"""PDF export tests for PACK 06 P6-03. Fake backend plus Playwright integration."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.date_selection_report.exporting.filename import build_pdf_filename
from engines.date_selection_report.exporting.html_projection import (
    PDF_AUTHOR,
    PDF_DOCUMENT_TITLE,
    PDF_SUBJECT,
    project_render_tree_to_html,
)
from engines.date_selection_report.exporting.pdf_exporter import DateSelectionPdfExporter
from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.labels import FORBIDDEN_PUBLIC_TERMS
from engines.date_selection_report.rendering.tree import build_render_tree, create_render_context
from engines.report_engine.contracts.report_export_result_v1 import MEDIA_TYPE_PDF
from engines.report_engine.exporting.pdf_exporter_v1 import MIN_PDF_BYTES, validate_pdf_file


class _FakePdfBackend:
    """Fast PACK 05-compatible PDF backend for unit tests."""

    def html_to_pdf(self, html: str, output_path: Path, *, title: str) -> int | None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = b"%PDF-1.4\n" + html.encode("utf-8") + b"\n%%EOF\n"
        if len(payload) < MIN_PDF_BYTES:
            payload += b"0" * (MIN_PDF_BYTES - len(payload))
        output_path.write_bytes(payload)
        return 1


def _export(presentation_model: DateSelectionReportModel, tmp_path: Path):
    tree = build_render_tree(create_render_context(presentation_model))
    before = presentation_model.to_dict()
    html = project_render_tree_to_html(tree)
    result = DateSelectionPdfExporter(backend=_FakePdfBackend()).export(tree, tmp_path)
    return tree, html, result, before, presentation_model.to_dict()


def test_pdf_filename_pattern(presentation_model: DateSelectionReportModel) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    assert build_pdf_filename(tree) == "bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf"


def test_pdf_generated_and_page_count(
    presentation_model: DateSelectionReportModel,
    tmp_path: Path,
) -> None:
    tree, html, result, before, after = _export(presentation_model, tmp_path)
    output = Path(result.file_path)
    validate_pdf_file(output)
    assert result.media_type == MEDIA_TYPE_PDF
    assert result.page_count is not None and result.page_count > 0
    assert result.file_name == "bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf"
    assert before == after
    assert tree.recommendations[0].rank == 1
    assert "{{" not in html


def test_pdf_html_renders_required_sections(
    presentation_model: DateSelectionReportModel,
) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    html = project_render_tree_to_html(tree)
    assert "BÁO CÁO CHỌN NGÀY TỐT" in html
    assert "BTE Platform" in html
    assert "THÔNG TIN NGƯỜI XEM" in html
    assert "Nguyễn Tiến Sơn" in html
    assert "Họ và tên" in html
    assert "Giới tính" in html
    assert "Ngày sinh dương" in html
    assert "Ngày sinh âm" in html
    assert "Can Chi năm" in html
    assert "Nạp âm" in html
    assert "Cung Phi" in html
    assert "Nhóm Trạch" in html
    assert "THÔNG TIN TÌM NGÀY TỐT" in html
    assert "09/2026" in html
    assert "CÁC NGÀY ĐỀ XUẤT" in html
    assert "04/09/2026" in html
    assert "Đại An" in html
    assert "Cấn (Thổ)" in html
    assert "Giờ phù hợp Nhóm Trạch của bạn" in html
    assert "Giờ Thìn (07:01–09:00) · Càn (Kim)" in html
    assert "Giờ Tỵ (09:01–11:00) · Khôn (Thổ)" in html
    assert "Các thời điểm đẹp" in html
    assert "Tốc Hỷ" in html
    assert "Tiểu Cát" in html
    assert "HƯỚNG DẪN THAM KHẢO" in html
    assert "ds-footer" in html
    assert PDF_DOCUMENT_TITLE in html
    assert PDF_AUTHOR in html
    assert PDF_SUBJECT in html
    for term in FORBIDDEN_PUBLIC_TERMS:
        assert term not in html
    assert "Lưu Liên" not in html
    assert "Xích Khẩu" not in html
    assert "Không Vong" not in html
    assert html.index("04/09/2026") < html.index("Giờ Thìn")
    assert "page-break-inside: avoid" in html


def test_pdf_unicode_preserved_in_file(
    presentation_model: DateSelectionReportModel,
    tmp_path: Path,
) -> None:
    _, html, result, _, _ = _export(presentation_model, tmp_path)
    data = Path(result.file_path).read_bytes()
    assert "Nguyễn Tiến Sơn".encode("utf-8") in data
    assert "Cấn (Thổ)".encode("utf-8") in data
    assert "BÁO CÁO CHỌN NGÀY TỐT".encode("utf-8") in html.encode("utf-8")


def test_recommendation_order_preserved(
    presentation_model: DateSelectionReportModel,
) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    html = project_render_tree_to_html(tree)
    solar = [node.date_header.solar_date for node in tree.recommendations]
    last = 0
    for date in solar:
        index = html.index(date, last)
        last = index
    assert solar == ["04/09/2026"]


def test_playwright_pdf_integration(
    presentation_model: DateSelectionReportModel,
    tmp_path: Path,
) -> None:
    pytest.importorskip("playwright")
    tree = build_render_tree(create_render_context(presentation_model))
    result = DateSelectionPdfExporter().export(tree, tmp_path)
    output = Path(result.file_path)
    validate_pdf_file(output)
    assert output.read_bytes()[:4] == b"%PDF"
    assert result.page_count is None or result.page_count > 0
    assert output.stat().st_size > MIN_PDF_BYTES

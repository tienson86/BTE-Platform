"""New customer copy is gated by published chart facts."""

from applications.api.services.core_reading_editorial import (
    _catalog,
    day_master_paragraphs,
    pattern_useful_paragraphs,
    shen_sha_paragraphs,
)
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.customer_export import _split_structured_paragraph
from applications.api.services.customer_export import _render_modern_report_html, _render_modern_report_docx
from applications.api.services.customer_report_input import build_customer_report_input
from applications.api.services.result_identity import stamp_customer_result_identity
from docx import Document


def test_catalog_covers_five_elements_strength_levels_and_patterns() -> None:
    catalog = _catalog()
    assert len(catalog["day_master"]) == len(catalog["strength"]) == len(catalog["useful"]) == 5
    assert len(catalog["pattern"]) == 10


def test_case_0001_selects_fire_control_and_combines_day_de_stars() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=31,
        gender="male", timezone="Asia/Bangkok",
    )
    day = day_master_paragraphs(payload)
    pattern = pattern_useful_paragraphs(payload)
    stars = shen_sha_paragraphs(payload)
    assert "Canh thuộc Dương Kim" in day[0]
    assert "Thiên Can của trụ ngày" in day[0]
    assert any("Mệnh cục Chính Ấn" in item for item in pattern)
    assert any("Hỏa chế Kim" in item and "Đinh Hỏa" in item for item in pattern)
    assert any("Bính Hỏa" in item and "Hỷ thần" in item for item in pattern)
    assert any("Thiên Đức và Nguyệt Đức cùng hiện" in item for item in stars)
    assert len(stars) == 3
    assert not any("engine" in item.lower() for item in day + pattern + stars)


def test_missing_useful_god_does_not_invent_an_element_or_star() -> None:
    payload = {"bazi": {"day_master": "Ất", "day_master_element": "Mộc"},
               "strength": {"strength_level": "weak"},
               "pattern": {}, "useful_god": {}, "bazi_missing_stars": True}
    assert len(day_master_paragraphs(payload)) == 2
    assert pattern_useful_paragraphs(payload) == []
    assert shen_sha_paragraphs(payload) == []


def test_huynh_pattern_name_and_month_basis_survive_pdf_and_docx_cards() -> None:
    payload = OrchestratorService().analyze(
        year=1966, month=9, day=24, hour=4, minute=15,
        gender="male", timezone="Asia/Bangkok",
    )
    paragraphs = pattern_useful_paragraphs(payload)
    assert payload["pattern"]["cach_cuc"] == "Chính Tài"
    assert "nguyệt lệnh Dậu" in paragraphs[0]
    assert "khí chính Tân" in paragraphs[0]
    assert "Nhật Chủ Bính" in paragraphs[0]
    assert "không tự khẳng định bạn giàu có" in paragraphs[0]
    assert "Canh Thiên Tài hiện ở trụ giờ" in paragraphs[1]
    title, body = _split_structured_paragraph("strength_structure_useful_god", paragraphs[0], 0)
    assert title == "Mệnh cục Chính Tài"
    assert "nguyệt lệnh Dậu" in body


def test_huynh_pattern_name_is_visible_in_both_exports(tmp_path) -> None:
    birth = {
        "full_name": "Lương Ngọc Huỳnh", "birth_place": "Hà Nội",
        "year": 1966, "month": 9, "day": 24, "hour": 4, "minute": 15,
        "gender": "male", "timezone": "Asia/Bangkok",
    }
    payload = OrchestratorService().analyze(**{
        key: birth[key] for key in ("year", "month", "day", "hour", "minute", "gender", "timezone")
    })
    payload = stamp_customer_result_identity(payload, "huynh-pattern-1966")
    report = build_customer_report_input(
        analysis_id="huynh-pattern-1966", data=payload, birth_input=birth,
    )
    html = _render_modern_report_html(report)
    assert "<h3>Mệnh cục Chính Tài</h3>" in html
    assert "nguyệt lệnh Dậu" in html
    target = tmp_path / "huynh.docx"
    _render_modern_report_docx(report, target)
    word_text = "\n".join(paragraph.text for paragraph in Document(target).paragraphs)
    assert "Mệnh cục Chính Tài" in word_text
    assert "nguyệt lệnh Dậu" in word_text

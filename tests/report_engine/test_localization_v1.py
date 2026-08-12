"""Tests for Report V1 localization and customer-text filtering."""

from __future__ import annotations

from engines.report_engine.contracts.report_input_v1 import (
    ReportCalendarV1,
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
    ReportMetadataV1,
    ReportPatternV1,
    ReportProfileV1,
    ReportShenShaItemV1,
    ReportStrengthV1,
    ReportUsefulGodV1,
)
from engines.report_engine.localization.customer_text import (
    customer_text,
    is_rule_engine_sentence,
)
from engines.report_engine.localization.display import display_text, unwrap_display_object
from engines.report_engine.localization.shensha_audit import audit_shensha_duplicates
from engines.report_engine.rendering.html_report_v1 import render_html
from engines.report_engine.rendering.report_sections_v1 import build_presented_report


def test_display_gender_and_strength() -> None:
    """Internal codes map to Vietnamese customer labels."""
    assert display_text("male", "gender") == "Nam"
    assert display_text("female", "gender") == "Nữ"
    assert display_text("strong", "strength") == "Thân vượng"
    assert display_text("success", "pattern_status") == "Đắc cách"
    assert display_text("hot", "temperature") == "Nhiệt"


def test_unwrap_solar_term_dict_repr() -> None:
    """Python dict leakage is reduced to the display name."""
    leaked = "{'name': 'Đại Hàn', 'index': 23}"
    assert unwrap_display_object(leaked) == "Đại Hàn"
    assert display_text({"name": "Đại Hàn", "index": 23}) == "Đại Hàn"


def test_rule_engine_sentences_are_filtered() -> None:
    """Instructional Rule Engine text is not kept for customers."""
    assert is_rule_engine_sentence("Nếu tháng sinh thuộc mùa Đông thì điều chỉnh.")
    assert is_rule_engine_sentence("Kích hoạt khi xác định Chính Cách.")
    assert is_rule_engine_sentence("Áp dụng bảng trạng thái ngũ hành của mùa đã được xác định.")
    kept = customer_text(
        "Áp dụng bảng trạng thái ngũ hành của mùa đã được xác định.\n\n"
        "Tổng quan: Nhật Chủ Canh, cách cục Chinh An."
    )
    assert "Áp dụng" not in kept
    assert "Tổng quan: Nhật Chủ Canh" in kept


def test_presented_report_localizes_case_values() -> None:
    """Presentation layer localizes codes without changing ReportInputV1."""
    report_input = ReportInputV1(
        metadata=ReportMetadataV1(case_id="CASE-TEST"),
        profile=ReportProfileV1(full_name="Nguyễn Tiến Sơn", gender="male"),
        calendar=ReportCalendarV1(solar_term="{'name': 'Đại Hàn', 'index': 23}"),
        strength=ReportStrengthV1(level="strong", classification="strong", summary="Thân vượng"),
        pattern=ReportPatternV1(status="success", primary_pattern="Chính Ấn"),
        useful_god=ReportUsefulGodV1(temperature_adjustment="hot"),
        interpretation=ReportInterpretationV1(
            sections=[
                ReportInterpretationSectionV1(
                    id="summary",
                    title="Tổng quan",
                    content=(
                        "Kích hoạt khi tháng sinh thuộc mùa Đông.\n\n"
                        "Tổng quan: Nhật Chủ Canh, cách cục Chinh An."
                    ),
                )
            ]
        ),
    )
    presented = build_presented_report(report_input)
    profile = presented.sections[0]
    values = dict(profile.meta_rows)
    assert values["Giới tính"] == "Nam"
    assert values["Tiết khí"] == "Đại Hàn"
    strength = next(section for section in presented.sections if section.id == "strength")
    assert dict(strength.meta_rows)["Mức"] == "Thân vượng"
    pattern = next(section for section in presented.sections if section.id == "pattern")
    assert dict(pattern.meta_rows)["Trạng thái"] == "Đắc cách"
    useful = next(section for section in presented.sections if section.id == "useful-god")
    assert dict(useful.meta_rows)["Điều hậu nhiệt"] == "Nhiệt"
    summary = next(section for section in presented.sections if section.id == "executive-summary")
    assert summary.paragraphs
    assert "Kích hoạt" not in " ".join(summary.paragraphs)
    assert "Tổng quan: Nhật Chủ Canh" in summary.paragraphs[0]


def test_html_does_not_leak_internal_codes() -> None:
    """HTML output uses localized labels and unwrapped solar term."""
    report_input = ReportInputV1(
        profile=ReportProfileV1(full_name="Nguyễn Tiến Sơn", gender="male"),
        calendar=ReportCalendarV1(solar_term="{'name': 'Đại Hàn', 'index': 23}"),
        strength=ReportStrengthV1(level="strong"),
        pattern=ReportPatternV1(status="success"),
        useful_god=ReportUsefulGodV1(temperature_adjustment="hot"),
    )
    html = render_html(report_input)
    assert "Nam" in html
    assert ">male<" not in html
    assert "Đại Hàn" in html
    assert "{'name'" not in html
    assert "Thân vượng" in html
    assert ">strong<" not in html
    assert "Đắc cách" in html
    assert ">success<" not in html
    assert "Nhiệt" in html
    assert ">hot<" not in html


def test_shensha_duplicate_candidates_are_audited_not_merged() -> None:
    """Alias candidates are reported; both names remain."""
    items = [
        ReportShenShaItemV1(name="Thiên Ất Quý Nhân", present=True),
        ReportShenShaItemV1(name="Thiên Ất", present=True),
    ]
    candidates = audit_shensha_duplicates(items)
    assert len(candidates) == 1
    assert candidates[0].left == "Thiên Ất"
    assert candidates[0].right == "Thiên Ất Quý Nhân"

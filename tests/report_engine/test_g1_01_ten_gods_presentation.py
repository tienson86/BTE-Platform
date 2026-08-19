"""G1-01 Report presentation uses canonical Ten Gods entries, not stem-name lists."""

from __future__ import annotations

from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from engines.report_engine.rendering.report_sections_v1 import build_presented_report
from tests.report_engine.case_0001_runtime import build_case_0001_source


def test_case_0001_report_splits_visible_and_hidden() -> None:
    """HTML/PDF/DOCX shared presentation keeps hidden Ten Gods with provenance."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    assert len(report_input.ten_gods.visible) == 4
    assert len(report_input.ten_gods.hidden) == 11
    assert len(report_input.ten_gods.hidden_entries) == 11
    assert all(item.get("ten_god") for item in report_input.ten_gods.hidden_entries)
    assert all(item.get("pillar") for item in report_input.ten_gods.hidden_entries)
    hidden_gods = {item["ten_god"] for item in report_input.ten_gods.hidden_entries}
    assert "Thiên Tài" in hidden_gods
    assert "Chính Quan" in hidden_gods
    presented = build_presented_report(report_input)
    ten_gods_section = next(item for item in presented.sections if item.id == "ten-gods")
    labels = {row[0]: row[1] for row in ten_gods_section.meta_rows}
    assert "Lộ can" in labels
    assert "Tàng can" in labels
    assert "Thất Sát" in labels["Lộ can"]
    assert "Giáp · Mộc · Thiên Tài" in labels["Tàng can"]
    assert "Đinh · Hỏa · Chính Quan" in labels["Tàng can"]
    assert "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ." in labels["Ghi chú"]
    pillars = next(item for item in presented.sections if item.id == "four-pillars")
    year_lines = {row[0]: row[1] for row in pillars.pillars[0].lines}
    assert "Bính · Hỏa" in year_lines["Thiên can"]
    assert "Giáp · Mộc · Thiên Tài" in year_lines["Ẩn can"]

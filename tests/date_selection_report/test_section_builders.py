"""C–G, I, J, L. Section builder presentation contracts."""

from __future__ import annotations

from pathlib import Path

from engines.date_selection_report.constants import NEGATIVE_KE_RESULTS
from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.builders import (
    CompatibleHoursSectionBuilder,
    PositiveTimesSectionBuilder,
)
from engines.date_selection_report.rendering.tokens import DAY_PRESENTATION_ORDER
from engines.date_selection_report.rendering.tree import build_render_tree, create_render_context

BUILDERS = (
    Path(__file__).resolve().parents[2]
    / "engines"
    / "date_selection_report"
    / "rendering"
    / "builders.py"
)


def _tree(presentation_model: DateSelectionReportModel):
    return build_render_tree(create_render_context(presentation_model))


def test_person_section_fields(presentation_model: DateSelectionReportModel) -> None:
    tree = _tree(presentation_model)
    keys = [row.key for row in tree.person.rows]
    assert keys == [
        "full_name",
        "gender",
        "birth_solar",
        "birth_lunar",
        "year_ganzhi",
        "nayin",
        "cung_phi",
        "trach_group",
    ]
    values = {row.key: row.value for row in tree.person.rows}
    assert values["full_name"] == "Nguyễn Tiến Sơn"
    assert values["year_ganzhi"] == "Bính Dần"
    assert values["cung_phi"] == "Khôn (Thổ)"
    assert tree.person.cung_display == "Khôn (Thổ)"
    assert tree.person.title == "THÔNG TIN NGƯỜI XEM"


def test_search_period_section(presentation_model: DateSelectionReportModel) -> None:
    search = _tree(presentation_model).search_period
    assert search.title == "THÔNG TIN TÌM NGÀY TỐT"
    assert search.month_label == "Tháng tìm ngày tốt"
    assert search.month_display == "09/2026"
    assert search.recommendation_count == "1"
    assert "dữ liệu cá nhân" in search.explanation


def test_recommendation_section_order(presentation_model: DateSelectionReportModel) -> None:
    rec = _tree(presentation_model).recommendations[0]
    assert rec.presentation_field_keys() == DAY_PRESENTATION_ORDER
    assert rec.date_header.solar_date == "04/09/2026"
    assert rec.date_header.lunar_display == "23/07/2026 âm"
    assert rec.date_header.day_result == "Đại An"
    assert rec.pagination.keep_together is True
    assert rec.pagination.do_not_split == ("date_header", "day_information")


def test_cung_presentation_combines_element(
    presentation_model: DateSelectionReportModel,
) -> None:
    rec = _tree(presentation_model).recommendations[0]
    assert rec.day_information.cung_display == "Cấn (Thổ)"
    cung_row = next(row for row in rec.day_information.rows if row.key == "cung_phi")
    assert cung_row.value == "Cấn (Thổ)"
    assert cung_row.label == "Cung Phi"


def test_compatible_hour_presentation(presentation_model: DateSelectionReportModel) -> None:
    hours = _tree(presentation_model).recommendations[0].compatible_hours
    assert hours.title == "Giờ phù hợp Nhóm Trạch của bạn"
    assert hours.rows[0].display == "Giờ Thìn (07:01–09:00) · Càn (Kim)"
    assert hours.rows[1].display == "Giờ Tỵ (09:01–11:00) · Khôn (Thổ)"
    assert "hour_result" not in hours.rows[0].to_dict()


def test_positive_group_order_and_negative_absent(
    presentation_model: DateSelectionReportModel,
) -> None:
    groups = _tree(presentation_model).recommendations[0].positive_times.groups
    assert [group.label for group in groups] == ["Đại An", "Tốc Hỷ", "Tiểu Cát"]
    blob = str(_tree(presentation_model).recommendations[0].positive_times.to_dict())
    for name in NEGATIVE_KE_RESULTS:
        assert name not in blob
    assert groups[0].items[0].branch_display == "Giờ Thìn"
    assert groups[0].items[0].time_range == "07:01–07:20"


def test_guidance_section_order(presentation_model: DateSelectionReportModel) -> None:
    guidance = _tree(presentation_model).guidance
    assert guidance.title == "HƯỚNG DẪN THAM KHẢO"
    assert [item.label for item in guidance.items] == ["Đại An", "Tốc Hỷ", "Tiểu Cát"]
    text = " ".join(item.text for item in guidance.items)
    assert "bắt buộc" not in text.lower()
    assert "must" not in text.lower()


def test_builders_do_not_import_calculators() -> None:
    source = BUILDERS.read_text(encoding="utf-8")
    assert "from engines.date_selection.ranking" not in source
    assert "from engines.date_selection.liu_ren" not in source
    assert "from engines.date_selection.cung_phi" not in source
    assert CompatibleHoursSectionBuilder is not None
    assert PositiveTimesSectionBuilder is not None

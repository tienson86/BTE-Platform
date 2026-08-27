"""Validation tests for PACK 06 Date Selection report foundation."""

from __future__ import annotations

import copy

import pytest

from engines.date_selection.service import DateSelectionService
from engines.date_selection_report.exceptions import DateSelectionReportValidationError
from engines.date_selection_report.models import (
    CompatibleHourReportData,
    DateSelectionReportModel,
    GuidanceItem,
    GuidanceReportData,
    Metadata,
    PersonReportData,
    PositiveKeReportData,
    Provenance,
    RecommendedDateReportData,
    SearchPeriodReportData,
)
from engines.date_selection_report.validators import validate_report_model, validate_search_result


def _payload() -> dict:
    return DateSelectionService().search(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_year=1987,
        birth_month=1,
        birth_day=21,
        target_year=2026,
        target_month=9,
    ).to_dict()


def test_valid_search_result_passes() -> None:
    validate_search_result(_payload())


def test_missing_person_name_fails() -> None:
    payload = _payload()
    payload["person"]["full_name"] = ""
    with pytest.raises(DateSelectionReportValidationError, match="full_name"):
        validate_search_result(payload)


def test_invalid_month_fails() -> None:
    payload = _payload()
    payload["target_month"] = 13
    with pytest.raises(DateSelectionReportValidationError, match="month"):
        validate_search_result(payload)


def test_empty_recommendations_fail() -> None:
    payload = _payload()
    payload["dates"] = []
    with pytest.raises(DateSelectionReportValidationError, match="recommendations"):
        validate_search_result(payload)


def test_negative_ke_is_rejected() -> None:
    payload = copy.deepcopy(_payload())
    payload["dates"][0]["compatible_hours"][0]["positive_ke"].append(
        {"index": 9, "time_range": "00:00–00:20", "result": "Lưu Liên"}
    )
    with pytest.raises(DateSelectionReportValidationError, match="negative ke"):
        validate_search_result(payload)


def test_hour_result_is_rejected() -> None:
    payload = copy.deepcopy(_payload())
    payload["dates"][0]["compatible_hours"][0]["hour_result"] = "Đại An"
    with pytest.raises(DateSelectionReportValidationError, match="hour_result"):
        validate_search_result(payload)


def test_opposite_trach_hour_fails() -> None:
    payload = copy.deepcopy(_payload())
    payload["dates"][0]["compatible_hours"][0]["trach_group"] = "dong"
    payload["dates"][0]["compatible_hours"][0]["trach_group_label"] = "Đông Tứ Trạch"
    with pytest.raises(DateSelectionReportValidationError, match="trach"):
        validate_search_result(payload)


def test_report_model_rejects_empty_guidance() -> None:
    hour = CompatibleHourReportData(
        branch="Thìn",
        time_range="07:01–09:00",
        ganzhi="Bính Thìn",
        nayin="Thổ",
        cung="Càn",
        cung_element="Kim",
        trach_group="Tây Tứ Trạch",
        positive_ke=(PositiveKeReportData(1, "07:01–07:20", "Đại An"),),
    )
    model = DateSelectionReportModel(
        metadata=Metadata(
            report_id="r1",
            report_schema_version="1.0",
            report_type="date_selection",
            generated_at="2026-08-27T00:00:00+00:00",
            locale="vi-VN",
            title="BÁO CÁO CHỌN NGÀY TỐT",
            generator="pack_06.date_selection_report",
        ),
        person=PersonReportData(
            full_name="A",
            gender="Nam",
            birth_solar="21/01/1987",
            birth_lunar="22/12/1986",
            year_ganzhi="Bính Dần",
            nayin="Hỏa",
            cung_phi="Khôn",
            cung_element="Thổ",
            trach_group="Tây Tứ Trạch",
        ),
        search_period=SearchPeriodReportData(9, 2026, "09/2026"),
        recommendations=(
            RecommendedDateReportData(
                rank=1,
                solar_date="04/09/2026",
                lunar_date="23/07/2026",
                year_ganzhi="Bính Ngọ",
                month_ganzhi="Giáp Thân",
                day_ganzhi="Tân Tỵ",
                day_result="Đại An",
                nayin="Kim",
                cung="Cấn",
                cung_element="Thổ",
                trach_group="Tây Tứ Trạch",
                compatible_hours=(hour,),
            ),
        ),
        guidance=GuidanceReportData(title="Hướng dẫn tham khảo", items=()),
        provenance=Provenance("date_selection", None, "2026-08-27T00:00:00+00:00", "1.0.0"),
    )
    with pytest.raises(DateSelectionReportValidationError, match="guidance"):
        validate_report_model(model)

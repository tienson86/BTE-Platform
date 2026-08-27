"""Shared Date Selection report presentation fixtures."""

from __future__ import annotations

import pytest

from engines.date_selection_report.constants import GUIDANCE_ITEMS, GUIDANCE_TITLE
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


def build_presentation_model() -> DateSelectionReportModel:
    """Validated-shaped model with all three positive classes."""
    hour_thin = CompatibleHourReportData(
        branch="Thìn",
        time_range="07:01–09:00",
        ganzhi="Bính Thìn",
        nayin="Thổ",
        cung="Càn",
        cung_element="Kim",
        trach_group="Tây Tứ Trạch",
        positive_ke=(
            PositiveKeReportData(index=1, time_range="07:01–07:20", result="Đại An"),
            PositiveKeReportData(index=3, time_range="07:41–08:00", result="Tốc Hỷ"),
        ),
    )
    hour_ty = CompatibleHourReportData(
        branch="Tỵ",
        time_range="09:01–11:00",
        ganzhi="Đinh Tỵ",
        nayin="Hỏa",
        cung="Khôn",
        cung_element="Thổ",
        trach_group="Tây Tứ Trạch",
        positive_ke=(
            PositiveKeReportData(index=6, time_range="10:21–10:40", result="Tiểu Cát"),
        ),
    )
    return DateSelectionReportModel(
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
            full_name="Nguyễn Tiến Sơn",
            gender="Nam",
            birth_solar="21/01/1987",
            birth_lunar="22/12/1986",
            year_ganzhi="Bính Dần",
            nayin="Hỏa",
            cung_phi="Khôn",
            cung_element="Thổ",
            trach_group="Tây Tứ Trạch",
        ),
        search_period=SearchPeriodReportData(month=9, year=2026, display="09/2026"),
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
                compatible_hours=(hour_thin, hour_ty),
            ),
        ),
        guidance=GuidanceReportData(
            title=GUIDANCE_TITLE,
            items=tuple(GuidanceItem(label, text) for label, text in GUIDANCE_ITEMS),
        ),
        provenance=Provenance(
            source="date_selection",
            search_result_id=None,
            generated_at="2026-08-27T00:00:00+00:00",
            engine_version="1.0.0",
        ),
    )


@pytest.fixture
def presentation_model() -> DateSelectionReportModel:
    """Pytest fixture wrapping the canonical presentation model."""
    return build_presentation_model()

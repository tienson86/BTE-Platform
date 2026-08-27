"""Model tests for PACK 06 Date Selection report foundation."""

from __future__ import annotations

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


def _person() -> PersonReportData:
    return PersonReportData(
        full_name="Nguyễn Tiến Sơn",
        gender="Nam",
        birth_solar="21/01/1987",
        birth_lunar="22/12/1986",
        year_ganzhi="Bính Dần",
        nayin="Hỏa",
        cung_phi="Khôn",
        cung_element="Thổ",
        trach_group="Tây Tứ Trạch",
    )


def _hour() -> CompatibleHourReportData:
    return CompatibleHourReportData(
        branch="Thìn",
        time_range="07:01–09:00",
        ganzhi="Bính Thìn",
        nayin="Thổ",
        cung="Càn",
        cung_element="Kim",
        trach_group="Tây Tứ Trạch",
        positive_ke=(
            PositiveKeReportData(index=1, time_range="07:01–07:20", result="Đại An"),
        ),
    )


def _model() -> DateSelectionReportModel:
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
        person=_person(),
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
                compatible_hours=(_hour(),),
            ),
        ),
        guidance=GuidanceReportData(
            title="Hướng dẫn tham khảo",
            items=(GuidanceItem("Đại An", "Thiên về sự ổn định, bền vững và yên định."),),
        ),
        provenance=Provenance(
            source="date_selection",
            search_result_id=None,
            generated_at="2026-08-27T00:00:00+00:00",
            engine_version="1.0.0",
        ),
    )


def test_root_model_contains_canonical_sections() -> None:
    payload = _model().to_dict()
    assert set(payload) == {
        "metadata",
        "person",
        "search_period",
        "recommendations",
        "guidance",
        "provenance",
    }
    person = payload["person"]
    assert person["cung_phi"] == "Khôn"
    assert person["cung_element"] == "Thổ"
    assert person["trach_group"] == "Tây Tứ Trạch"


def test_hour_model_has_no_hour_result() -> None:
    hour = _hour().to_dict()
    assert "hour_result" not in hour
    assert hour["positive_ke"][0]["result"] == "Đại An"
    assert hour["cung"] == "Càn"
    assert hour["cung_element"] == "Kim"


def test_recommendation_preserves_separate_cung_fields() -> None:
    rec = _model().recommendations[0]
    assert rec.cung == "Cấn"
    assert rec.cung_element == "Thổ"
    assert rec.day_result == "Đại An"
    assert rec.rank == 1


def test_metadata_does_not_carry_analytical_fields() -> None:
    meta = _model().metadata.to_dict()
    assert "nayin" not in meta
    assert "day_result" not in meta
    assert meta["report_type"] == "date_selection"
    assert meta["locale"] == "vi-VN"

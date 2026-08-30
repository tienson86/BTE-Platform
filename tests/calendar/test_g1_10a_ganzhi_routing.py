"""G1-10A: Year/Month Ganzhi Cung follow Tam Nguyên; Day/Hour stay Hạ Nguyên."""

from __future__ import annotations

import pytest

from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.cung_phi import cung_for_ganzhi, ganzhi_label_for_year
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.ganzhi_routing import (
    routing_table,
    stamp_bazi_source_nguyen,
)
from engines.calendar_engine.tam_nguyen import (
    HA_NGUYEN,
    THUONG_NGUYEN,
    TRUNG_NGUYEN,
    TAM_NGUYEN_EPOCH_YEAR,
    CYCLE_YEARS,
    tam_nguyen_for_year,
)
from engines.date_selection.service import DateSelectionService
from engines.identity import build_canonical_identity
from engines.report_engine.adapters.report_input_v1_adapter import (
    ReportInputV1Adapter,
    ReportInputV1Source,
)

_CASE_YEAR = 1966
_CASE_MONTH = 9
_CASE_DAY = 24
_CASE_HOUR = 4
_CASE_MINUTE = 15


def _label(pillar: object) -> str:
    return f"{pillar.stem} {pillar.branch}".strip()


def _dataset_year_cung(ganzhi: str, year: int) -> str:
    return cung_for_ganzhi(
        ganzhi,
        tam_nguyen=tam_nguyen_for_year(year),
        reference_year=year,
        gender="male",
    )


def _dataset_ha_cung(ganzhi: str, year: int) -> str:
    return cung_for_ganzhi(
        ganzhi,
        tam_nguyen=HA_NGUYEN,
        reference_year=year,
        gender="male",
    )


def test_case_1966_calendar_and_routing() -> None:
    calendar = CalendarEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    assert calendar.tam_nguyen == TRUNG_NGUYEN
    assert calendar.cuu_van == 6
    assert calendar.cung_phi == "Đoài"
    assert calendar.house_group == "Tây Tứ Trạch"
    routing = calendar.ganzhi_routing or {}
    assert routing["year"]["source_nguyen"] == TRUNG_NGUYEN
    assert routing["month"]["source_nguyen"] == TRUNG_NGUYEN
    assert routing["day"]["source_nguyen"] == HA_NGUYEN
    assert routing["hour"]["source_nguyen"] == HA_NGUYEN
    expected_year = ganzhi_label_for_year(_CASE_YEAR)
    assert routing["year"]["ganzhi"] == expected_year
    assert routing["year"]["cung_phi"] == _dataset_year_cung(expected_year, _CASE_YEAR)
    assert routing["month"]["cung_phi"] == _dataset_year_cung(
        routing["month"]["ganzhi"],
        _CASE_YEAR,
    )
    assert routing["day"]["cung_phi"] == _dataset_ha_cung(
        routing["day"]["ganzhi"],
        _CASE_YEAR,
    )
    assert routing["hour"]["cung_phi"] == _dataset_ha_cung(
        routing["hour"]["ganzhi"],
        _CASE_YEAR,
    )


def test_case_1966_identity_year_month_use_trung_nguyen_dataset() -> None:
    calendar = CalendarEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    chart = BaziEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    identity = build_canonical_identity(bazi=chart, calendar=calendar)
    four = identity.four_pillars
    assert four is not None
    assert four.year.can_chi == _label(chart.year_pillar)
    assert four.month.can_chi == _label(chart.month_pillar)
    assert four.year.cung_phi == _dataset_year_cung(four.year.can_chi, _CASE_YEAR)
    assert four.month.cung_phi == _dataset_year_cung(four.month.can_chi, _CASE_YEAR)
    assert four.day.cung_phi == _dataset_ha_cung(four.day.can_chi, _CASE_YEAR)
    assert four.hour.cung_phi == _dataset_ha_cung(four.hour.can_chi, _CASE_YEAR)
    assert four.year.cung_phi != _dataset_ha_cung(four.year.can_chi, _CASE_YEAR)


def test_case_1966_header_matches_bazi() -> None:
    calendar = CalendarEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    chart = BaziEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    four = build_canonical_identity(bazi=chart, calendar=calendar).four_pillars
    assert four is not None
    assert four.year.can_chi == _label(chart.year_pillar)
    assert four.month.can_chi == _label(chart.month_pillar)
    assert four.day.can_chi == _label(chart.day_pillar)
    assert four.hour.can_chi == _label(chart.hour_pillar)


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (1923, THUONG_NGUYEN),
        (1924, TRUNG_NGUYEN),
        (1983, TRUNG_NGUYEN),
        (1984, HA_NGUYEN),
        (2043, HA_NGUYEN),
        (2044, THUONG_NGUYEN),
    ],
)
def test_boundary_year_month_source_follows_tam_nguyen(year: int, expected: str) -> None:
    routes = routing_table(year, 6, 15, 12)
    assert tam_nguyen_for_year(year) == expected
    assert routes["year"].source_nguyen == expected
    assert routes["month"].source_nguyen == expected
    assert routes["day"].source_nguyen == HA_NGUYEN
    assert routes["hour"].source_nguyen == HA_NGUYEN


def test_180_year_cycle_source_nguyen_property() -> None:
    start = TAM_NGUYEN_EPOCH_YEAR
    for year in range(start, start + CYCLE_YEARS):
        yuan = tam_nguyen_for_year(year)
        routes = routing_table(year, 6, 15, 12)
        assert routes["year"].source_nguyen == yuan
        assert routes["month"].source_nguyen == yuan
        assert routes["day"].source_nguyen == HA_NGUYEN
        assert routes["hour"].source_nguyen == HA_NGUYEN


def test_homepage_result_and_report_share_canonical_ganzhi() -> None:
    calendar = CalendarEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    chart = BaziEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    day = DateSelectionService().inspect_day(_CASE_YEAR, _CASE_MONTH, _CASE_DAY)
    payload = day.to_dict()
    hour_branch = DateSelectionService().current_hour_branch(_CASE_HOUR, _CASE_MINUTE)
    hour_row = next(item for item in payload["hours"] if item["window"]["branch"] == hour_branch)
    year_ganzhi = _label(chart.year_pillar)
    month_ganzhi = _label(chart.month_pillar)
    day_ganzhi = _label(chart.day_pillar)
    hour_ganzhi = _label(chart.hour_pillar)
    assert payload["year"]["can_chi"] == year_ganzhi
    assert payload["month"]["can_chi"] == month_ganzhi
    assert payload["day"]["can_chi"] == day_ganzhi
    assert hour_row["can_chi"] == hour_ganzhi
    assert calendar.month_can_chi == month_ganzhi
    assert (calendar.ganzhi_routing or {})["day"]["ganzhi"] == day_ganzhi
    assert payload["year"]["source_nguyen"] == TRUNG_NGUYEN
    assert payload["month"]["source_nguyen"] == TRUNG_NGUYEN
    assert payload["day"]["source_nguyen"] == HA_NGUYEN
    assert payload["year"]["cung_phi"] == _dataset_year_cung(year_ganzhi, _CASE_YEAR)
    assert payload["month"]["cung_phi"] == _dataset_year_cung(month_ganzhi, _CASE_YEAR)
    view = build_bazi_view(chart)
    stamped = stamp_bazi_source_nguyen(view.to_dict(), calendar.ganzhi_routing)
    assert stamped["year_pillar"]["source_nguyen"] == TRUNG_NGUYEN
    assert stamped["month_pillar"]["source_nguyen"] == TRUNG_NGUYEN
    assert stamped["day_pillar"]["source_nguyen"] == HA_NGUYEN
    assert stamped["hour_pillar"]["source_nguyen"] == HA_NGUYEN
    analysis = AnalysisResult(bazi=view, meta=AnalysisMeta(contract_version="1.0"))
    report = ReportInputV1Adapter().build(
        ReportInputV1Source(analysis=analysis, calendar=calendar.to_dict())
    )
    assert f"{report.pillars.year.stem} {report.pillars.year.branch}" == year_ganzhi
    assert f"{report.pillars.month.stem} {report.pillars.month.branch}" == month_ganzhi
    assert f"{report.pillars.day.stem} {report.pillars.day.branch}" == day_ganzhi
    assert f"{report.pillars.hour.stem} {report.pillars.hour.branch}" == hour_ganzhi

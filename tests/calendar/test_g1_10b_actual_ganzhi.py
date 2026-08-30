"""G1-10B: Year/Month actual Can Chi come from the Tam Nguyên dataset."""

from __future__ import annotations

import inspect

import pytest

from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.tam_nguyen import (
    HA_NGUYEN,
    THUONG_NGUYEN,
    TRUNG_NGUYEN,
    tam_nguyen_for_year,
)
from engines.calendar_engine.tam_nguyen_dataset import (
    CALENDAR_RULE_VERSION,
    jiazi_row_at,
    jiazi_row_for_year,
    resolve_month_pillar,
    resolve_year_pillar,
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


def test_1966_year_month_stems_match_trung_nguyen_dataset() -> None:
    year_row = jiazi_row_for_year(_CASE_YEAR)
    assert year_row.tam_nguyen == TRUNG_NGUYEN
    year_pillar = resolve_year_pillar(_CASE_YEAR)
    month_pillar = resolve_month_pillar(_CASE_YEAR, _CASE_MONTH, _CASE_DAY)
    assert year_pillar.heavenly_stem == year_row.heavenly_stem
    assert year_pillar.earthly_branch == year_row.earthly_branch
    assert year_pillar.ganzhi == year_row.ganzhi
    assert year_pillar.nap_am == year_row.nap_am
    assert year_pillar.source_nguyen == TRUNG_NGUYEN
    assert month_pillar.source_nguyen == TRUNG_NGUYEN
    assert month_pillar.heavenly_stem
    assert month_pillar.earthly_branch
    chart = BaziEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    assert chart.year_pillar.stem == year_row.heavenly_stem
    assert chart.year_pillar.branch == year_row.earthly_branch
    assert chart.month_pillar.stem == month_pillar.heavenly_stem
    assert chart.month_pillar.branch == month_pillar.earthly_branch
    view = build_bazi_view(chart)
    assert view.year_pillar.nap_am == year_pillar.nap_am
    assert view.month_pillar.nap_am == month_pillar.nap_am


def test_year_pillar_does_not_use_legacy_ganzhi_algorithm(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_year(_year: int) -> dict[str, str]:
        return {"can": "Giáp", "chi": "Tý"}

    monkeypatch.setattr(GanzhiAlgorithm, "year", staticmethod(fake_year))
    row = jiazi_row_for_year(_CASE_YEAR)
    chart = BaziEngine().build(
        _CASE_YEAR,
        _CASE_MONTH,
        _CASE_DAY,
        _CASE_HOUR,
        _CASE_MINUTE,
        gender="male",
    )
    assert chart.year_pillar.stem == row.heavenly_stem
    assert chart.year_pillar.branch == row.earthly_branch
    assert _label(chart.year_pillar) != "Giáp Tý"
    source = inspect.getsource(BaziEngine.build)
    assert "GanzhiAlgorithm.year" not in source
    assert "resolve_year_pillar" in source
    assert "resolve_month_pillar" in source


def test_same_cycle_index_uses_selected_nguyen_row() -> None:
    index = 42
    thuong = jiazi_row_at(THUONG_NGUYEN, index)
    trung = jiazi_row_at(TRUNG_NGUYEN, index)
    ha = jiazi_row_at(HA_NGUYEN, index)
    assert thuong.sample_year != trung.sample_year != ha.sample_year
    assert resolve_year_pillar(trung.sample_year).ganzhi == trung.ganzhi
    assert resolve_year_pillar(thuong.sample_year).source_nguyen == THUONG_NGUYEN
    assert resolve_year_pillar(ha.sample_year).source_nguyen == HA_NGUYEN
    assert resolve_year_pillar(trung.sample_year).heavenly_stem == trung.heavenly_stem
    assert resolve_year_pillar(trung.sample_year).earthly_branch == trung.earthly_branch


@pytest.mark.parametrize(
    "year",
    [1864, 1924, 1966, 1984, 2026],
)
def test_three_nguyen_year_month_match_dataset(year: int) -> None:
    yuan = tam_nguyen_for_year(year)
    row = jiazi_row_for_year(year)
    year_pillar = resolve_year_pillar(year)
    month_pillar = resolve_month_pillar(year, 9, 24)
    assert row.tam_nguyen == yuan
    assert year_pillar.heavenly_stem == row.heavenly_stem
    assert year_pillar.earthly_branch == row.earthly_branch
    assert year_pillar.nap_am == row.nap_am
    assert month_pillar.heavenly_stem
    assert month_pillar.nap_am
    assert month_pillar.source_nguyen == yuan


@pytest.mark.parametrize(
    ("year", "expected_yuan"),
    [
        (1923, THUONG_NGUYEN),
        (1924, TRUNG_NGUYEN),
        (1983, TRUNG_NGUYEN),
        (1984, HA_NGUYEN),
        (2043, HA_NGUYEN),
        (2044, THUONG_NGUYEN),
    ],
)
def test_boundary_switches_actual_dataset_row(year: int, expected_yuan: str) -> None:
    row = jiazi_row_for_year(year)
    pillar = resolve_year_pillar(year)
    assert row.tam_nguyen == expected_yuan
    assert pillar.heavenly_stem == row.heavenly_stem
    assert pillar.earthly_branch == row.earthly_branch
    assert pillar.ganzhi == row.ganzhi


def test_1923_1924_actual_can_chi_change() -> None:
    previous = resolve_year_pillar(1923)
    nxt = resolve_year_pillar(1924)
    assert previous.ganzhi != nxt.ganzhi
    assert previous.source_nguyen == THUONG_NGUYEN
    assert nxt.source_nguyen == TRUNG_NGUYEN


def test_pages_share_actual_stems_for_1966() -> None:
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
    row = jiazi_row_for_year(_CASE_YEAR)
    month = resolve_month_pillar(_CASE_YEAR, _CASE_MONTH, _CASE_DAY)
    assert calendar.calendar_rule_version == CALENDAR_RULE_VERSION
    assert calendar.year_stem == row.heavenly_stem
    assert calendar.year_branch == row.earthly_branch
    assert chart.year_pillar.stem == row.heavenly_stem
    assert chart.month_pillar.stem == month.heavenly_stem
    payload = DateSelectionService().inspect_day(_CASE_YEAR, _CASE_MONTH, _CASE_DAY).to_dict()
    assert payload["year"]["can_chi"] == row.ganzhi
    assert payload["month"]["can_chi"] == month.ganzhi
    four = build_canonical_identity(bazi=chart, calendar=calendar).four_pillars
    assert four is not None
    assert four.year.stem == row.heavenly_stem
    assert four.year.branch == row.earthly_branch
    assert four.month.stem == month.heavenly_stem
    assert four.month.branch == month.earthly_branch
    view = build_bazi_view(chart)
    report = ReportInputV1Adapter().build(
        ReportInputV1Source(
            analysis=AnalysisResult(bazi=view, meta=AnalysisMeta(contract_version="1.0")),
            calendar=calendar.to_dict(),
        )
    )
    assert report.pillars.year.stem == row.heavenly_stem
    assert report.pillars.year.branch == row.earthly_branch
    assert report.pillars.month.stem == month.heavenly_stem
    assert report.pillars.month.branch == month.earthly_branch


def test_1966_live_diagnostic_payload() -> None:
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
    routing = calendar.ganzhi_routing or {}
    year_row = jiazi_row_for_year(_CASE_YEAR)
    month = resolve_month_pillar(_CASE_YEAR, _CASE_MONTH, _CASE_DAY)
    assert calendar.tam_nguyen == TRUNG_NGUYEN
    assert routing["year"]["heavenly_stem"] == year_row.heavenly_stem
    assert routing["year"]["earthly_branch"] == year_row.earthly_branch
    assert routing["year"]["ganzhi"] == year_row.ganzhi
    assert routing["year"]["source_nguyen"] == TRUNG_NGUYEN
    assert routing["month"]["heavenly_stem"] == month.heavenly_stem
    assert routing["month"]["earthly_branch"] == month.earthly_branch
    assert routing["month"]["ganzhi"] == month.ganzhi
    assert routing["month"]["source_nguyen"] == TRUNG_NGUYEN
    assert routing["day"]["source_nguyen"] == HA_NGUYEN
    assert routing["hour"]["source_nguyen"] == HA_NGUYEN
    assert _label(chart.year_pillar) == year_row.ganzhi
    assert _label(chart.month_pillar) == month.ganzhi
    assert _label(chart.day_pillar) == routing["day"]["ganzhi"]
    assert _label(chart.hour_pillar) == routing["hour"]["ganzhi"]

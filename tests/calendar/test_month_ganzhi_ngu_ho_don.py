"""CAL-BZ-01: canonical month Ganzhi = 12 Tiết + Ngũ Hổ Độn."""

from __future__ import annotations

import pytest

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.month_ganzhi import (
    MONTH_PILLAR_STANDARD,
    month_ganzhi_label,
    month_pillar,
    month_stem_for,
    solar_term_month,
    yin_start_stem_index,
)
from engines.calendar_engine.solar_terms.engine import SolarTermEngine
from engines.date_selection.calendar_adapter import snapshot_for_solar
from engines.date_selection.identity import pillar_contract

BINH_YEAR_SEQUENCE = (
    ("Dần", "Canh Dần", 2026, 2, 10),
    ("Mão", "Tân Mão", 2026, 3, 20),
    ("Thìn", "Nhâm Thìn", 2026, 4, 20),
    ("Tỵ", "Quý Tỵ", 2026, 5, 20),
    ("Ngọ", "Giáp Ngọ", 2026, 6, 20),
    ("Mùi", "Ất Mùi", 2026, 7, 20),
    ("Thân", "Bính Thân", 2026, 8, 28),
    ("Dậu", "Đinh Dậu", 2026, 9, 20),
    ("Tuất", "Mậu Tuất", 2026, 10, 20),
    ("Hợi", "Kỷ Hợi", 2026, 11, 20),
    ("Tý", "Canh Tý", 2026, 12, 20),
    ("Sửu", "Tân Sửu", 2027, 1, 20),
)

DAN_START_YEARS = (
    (2024, "Giáp", "Bính"),
    (2025, "Ất", "Mậu"),
    (2026, "Bính", "Canh"),
    (2027, "Đinh", "Nhâm"),
    (2008, "Mậu", "Giáp"),
    (2009, "Kỷ", "Bính"),
    (2010, "Canh", "Mậu"),
    (2011, "Tân", "Canh"),
    (2012, "Nhâm", "Nhâm"),
    (2013, "Quý", "Giáp"),
)

NGU_HO_DON_PROGRESSION = {
    "Giáp": ("Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh"),
    "Kỷ": ("Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh"),
    "Ất": ("Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"),
    "Canh": ("Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"),
    "Bính": ("Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"),
    "Tân": ("Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"),
    "Đinh": ("Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"),
    "Nhâm": ("Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"),
    "Mậu": ("Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất"),
    "Quý": ("Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất"),
}


def test_month_pillar_standard_is_solar_term() -> None:
    assert MONTH_PILLAR_STANDARD == "BTE-MONTH-PILLAR-SOLAR-TERM-V1.0"


def test_ngu_ho_don_csv_covers_ten_stems() -> None:
    mapping = yin_start_stem_index()
    assert mapping["Giáp"] == 2
    assert mapping["Kỷ"] == 2
    assert mapping["Ất"] == 4
    assert mapping["Canh"] == 4
    assert mapping["Bính"] == 6
    assert mapping["Tân"] == 6
    assert mapping["Đinh"] == 8
    assert mapping["Nhâm"] == 8
    assert mapping["Mậu"] == 0
    assert mapping["Quý"] == 0


@pytest.mark.parametrize("year_stem,expected", list(NGU_HO_DON_PROGRESSION.items()))
def test_stem_progression_all_twelve_months(year_stem: str, expected: tuple[str, ...]) -> None:
    stems = tuple(month_stem_for(year_stem, index) for index in range(1, 13))
    assert stems == expected


@pytest.mark.parametrize("year,year_stem,dan_stem", DAN_START_YEARS)
def test_dan_start_stem_for_all_year_groups(year: int, year_stem: str, dan_stem: str) -> None:
    stem, branch = month_pillar(year, 2, 10)
    year_gz = GanzhiAlgorithm.year(year)
    assert year_gz["can"] == year_stem
    assert branch == "Dần"
    assert stem == dan_stem
    assert month_stem_for(year_stem, 1) == dan_stem


@pytest.mark.parametrize("branch,ganzhi,year,month,day", BINH_YEAR_SEQUENCE)
def test_binh_year_twelve_month_sequence(
    branch: str,
    ganzhi: str,
    year: int,
    month: int,
    day: int,
) -> None:
    stem, month_branch = month_pillar(year, month, day)
    assert month_branch == branch
    assert f"{stem} {month_branch}" == ganzhi
    assert month_ganzhi_label(year, month, day) == ganzhi


def test_2026_08_28_is_binh_than_not_giap_than() -> None:
    calendar = CalendarEngine().build(2026, 8, 28)
    chart = BaziEngine().build(2026, 8, 28, 12, 0)
    snapshot = snapshot_for_solar(2026, 8, 28)
    info = solar_term_month(2026, 8, 28)
    assert calendar.lunar.year_can_chi == "Bính Ngọ"
    assert info.branch == "Thân"
    assert info.start_term == "Lập Thu"
    assert calendar.month_can_chi == "Bính Thân"
    assert calendar.month_branch == "Thân"
    assert f"{chart.year_pillar.stem} {chart.year_pillar.branch}" == "Bính Ngọ"
    assert f"{chart.month_pillar.stem} {chart.month_pillar.branch}" == "Bính Thân"
    assert snapshot.year_ganzhi == "Bính Ngọ"
    assert snapshot.month_ganzhi == "Bính Thân"
    assert "Giáp Thân" not in (
        calendar.month_can_chi,
        snapshot.month_ganzhi,
        f"{chart.month_pillar.stem} {chart.month_pillar.branch}",
    )
    identity = pillar_contract("Bính Thân")
    assert identity["nayin_element"] == "Hỏa"
    assert identity["cung_phi"] == "Khôn"


def test_lap_thu_boundary_changes_together() -> None:
    before = month_pillar(2026, 8, 6)
    on = month_pillar(2026, 8, 7)
    assert before == ("Ất", "Mùi")
    assert on == ("Bính", "Thân")
    assert SolarTermEngine().get_bazi_month(2026, 8, 6).start_term == "Tiểu Thử"
    assert SolarTermEngine().get_bazi_month(2026, 8, 7).start_term == "Lập Thu"


def test_bach_lo_boundary_changes_together() -> None:
    before = month_pillar(2026, 9, 6)
    on = month_pillar(2026, 9, 7)
    assert before == ("Bính", "Thân")
    assert on == ("Đinh", "Dậu")
    assert SolarTermEngine().get_bazi_month(2026, 9, 6).start_term == "Lập Thu"
    assert SolarTermEngine().get_bazi_month(2026, 9, 7).start_term == "Bạch Lộ"


def test_ganzhi_algorithm_month_matches_ngu_ho_don() -> None:
    binh_index = GanzhiAlgorithm.STEM.index("Bính")
    than = GanzhiAlgorithm.month(binh_index, 6)
    assert f"{than['can']} {than['chi']}" == "Bính Thân"
    dan = GanzhiAlgorithm.month(binh_index, 0)
    assert f"{dan['can']} {dan['chi']}" == "Canh Dần"


def test_son_1987_01_21_month_remains_tan_suu() -> None:
    stem, branch = month_pillar(1987, 1, 21)
    chart = BaziEngine().build(1987, 1, 21, 4, 30)
    assert (stem, branch) == ("Tân", "Sửu")
    assert (chart.month_pillar.stem, chart.month_pillar.branch) == ("Tân", "Sửu")

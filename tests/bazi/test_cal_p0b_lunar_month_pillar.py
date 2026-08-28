"""CAL-P0B lunar display vs Four Pillars month (CAL-BZ-01).

Lunar month number remains a display field.
Four Pillars month Ganzhi follows 12 Tiết + Ngũ Hổ Độn
(BTE-MONTH-PILLAR-SOLAR-TERM-V1.0), which supersedes
BTE-MONTH-PILLAR-LUNAR-V1.0.
"""

from __future__ import annotations

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.month_ganzhi import MONTH_PILLAR_STANDARD
from engines.calendar_engine.month_pillar import lunar_month_to_branch
from engines.calendar_engine.solar_terms.engine import SolarTermEngine


def _pillars(chart) -> tuple[tuple[str, str], tuple[str, str], tuple[str, str], tuple[str, str]]:
    return (
        (chart.year_pillar.stem, chart.year_pillar.branch),
        (chart.month_pillar.stem, chart.month_pillar.branch),
        (chart.day_pillar.stem, chart.day_pillar.branch),
        (chart.hour_pillar.stem, chart.hour_pillar.branch),
    )


def test_month_pillar_standard_id() -> None:
    assert MONTH_PILLAR_STANDARD == "BTE-MONTH-PILLAR-SOLAR-TERM-V1.0"
    assert lunar_month_to_branch(8) == "Dậu"
    assert lunar_month_to_branch(12) == "Sửu"


def test_hung_solar_term_month_binh_than() -> None:
    calendar = CalendarEngine().build(1981, 8, 29, 4, 30, timezone_name="Asia/Ho_Chi_Minh")
    chart = BaziEngine().build(calendar, gender="male")
    assert calendar.lunar_date == "01/08/1981"
    assert calendar.lunar_month == 8
    assert _pillars(chart) == (
        ("Tân", "Dậu"),
        ("Bính", "Thân"),
        ("Kỷ", "Mão"),
        ("Bính", "Dần"),
    )


def test_son_month_remains_tan_suu() -> None:
    chart = BaziEngine().build(1987, 1, 21, 4, 30, gender="male")
    assert (chart.month_pillar.stem, chart.month_pillar.branch) == ("Tân", "Sửu")


def test_huynh_month_remains_dinh_dau() -> None:
    chart = BaziEngine().build(1966, 9, 24, 4, 15, gender="male")
    assert (chart.month_pillar.stem, chart.month_pillar.branch) == ("Đinh", "Dậu")


def test_dung_month_remains_at_ty() -> None:
    chart = BaziEngine().build(1982, 5, 22, 9, 30, gender="female")
    assert (chart.month_pillar.stem, chart.month_pillar.branch) == ("Ất", "Tỵ")


def test_four_pillars_month_follows_solar_term_branch() -> None:
    """29/08/1981 is Thân under 12 Tiết; Four Pillars must use Bính Thân, not lunar Dậu."""
    jieqi = SolarTermEngine().get_bazi_month(1981, 8, 29)
    assert jieqi.branch == "Thân"
    chart = BaziEngine().build(1981, 8, 29, 4, 30, gender="male")
    assert chart.month_pillar.branch == "Thân"
    assert chart.month_pillar.stem == "Bính"

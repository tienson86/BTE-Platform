"""Calendar serialized day Ganzhi must use integer JDN like Bazi."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.calendar_engine.julian.julian import JulianDay


def test_to_dict_day_ganzhi_2026_08_27_quy_dau() -> None:
    calendar = CalendarEngine().build(2026, 8, 27)
    chart = BaziEngine().build(2026, 8, 27, 12, 0)
    assert calendar.julian_day == JulianDay.from_gregorian(2026, 8, 27)
    assert calendar.julian_day == 2461279.5
    assert calendar.to_dict()["lunar_can_chi"]["day"] == "Quý Dậu"
    assert f"{chart.day_pillar.stem} {chart.day_pillar.branch}" == "Quý Dậu"


def test_to_dict_day_ganzhi_1987_01_21_canh_ngo() -> None:
    calendar = CalendarEngine().build(1987, 1, 21, 3, 30)
    chart = BaziEngine().build(1987, 1, 21, 3, 30)
    assert calendar.to_dict()["lunar_can_chi"]["day"] == "Canh Ngọ"
    assert f"{chart.day_pillar.stem} {chart.day_pillar.branch}" == "Canh Ngọ"

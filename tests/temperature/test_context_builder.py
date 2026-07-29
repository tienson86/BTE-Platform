from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context


def test_context_builder_from_bazi() -> None:
    cal = CalendarEngine().build(1990, 7, 15, 12, 0)
    bazi = BaziEngine().build(cal, gender="male")
    ctx = build_temperature_context(bazi, calendar=cal)
    assert ctx.day_master
    assert ctx.climate_type in {"warm", "hot", "cool", "cold"}
    assert ctx.season in {"spring", "summer", "autumn", "winter"}


def test_context_builder_produces_scorable_result() -> None:
    cal = CalendarEngine().build(1985, 1, 8, 6, 0)
    bazi = BaziEngine().build(cal, gender="female")
    ctx = build_temperature_context(bazi, calendar=cal)
    result = TemperatureEngine(database_path="database/11_temperature").calculate(ctx)
    assert result.success
    assert result.matched_rules

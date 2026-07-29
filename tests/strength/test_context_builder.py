from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context


def test_context_builder_from_bazi() -> None:
    cal = CalendarEngine().build(1990, 5, 15, 10, 0)
    bazi = BaziEngine().build(cal, gender="male")
    ctx = build_strength_context(bazi, calendar=cal)
    assert ctx.day_master
    assert ctx.month_branch
    assert ctx.month_status in {"Đắc lệnh", "Tướng", "Hưu", "Tù", "Tử"}
    assert ctx.root_level


def test_context_builder_produces_scorable_result() -> None:
    cal = CalendarEngine().build(1985, 3, 8, 6, 0)
    bazi = BaziEngine().build(cal, gender="female")
    ctx = build_strength_context(bazi, calendar=cal)
    result = StrengthEngine(database_path="database/12_strength").calculate(ctx)
    assert result.success
    assert result.matched_rules

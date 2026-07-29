from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.context_engine.engine import ContextEngine
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def test_engine_build_and_publish_rule_context() -> None:
    cal = CalendarEngine().build(1990, 5, 15, 10, 0)
    bazi = BaziEngine().build(cal, gender="male")

    sctx = build_strength_context(bazi, calendar=cal)
    sres = StrengthEngine(database_path="database/12_strength").calculate(sctx)
    tctx = build_temperature_context(bazi, calendar=cal, strength_level=sres.strength_level, strength_score=sres.strength_score)
    tres = TemperatureEngine(database_path="database/11_temperature").calculate(tctx)

    pctx = build_pattern_context(bazi, calendar=cal)
    pctx.strength_level = sres.strength_level
    pctx.strength_score = sres.strength_score
    pctx.temperature_type = tres.to_pattern_temperature_type()
    pres = PatternEngine().calculate(pctx)
    uctx = build_useful_god_context(pctx, pres)
    ures = UsefulGodEngine(database_path="database/13_useful_god").calculate(uctx)

    engine = ContextEngine()
    unified, rule_context = engine.build_and_publish(
        calendar=cal,
        bazi=bazi,
        strength=sres,
        temperature=tres,
        pattern=pres,
        useful_god=ures,
    )

    assert unified.strength.level == sres.strength_level
    assert unified.temperature.type == tres.to_pattern_temperature_type()
    assert unified.useful_god.primary == (ures.useful_god or "")
    assert rule_context["strength"]["level"] == sres.strength_level
    assert rule_context["useful_god"]["name"] == (ures.useful_god or None)
    assert "unified_context" in rule_context
    assert rule_context.get("temperature_type") == tres.to_pattern_temperature_type()

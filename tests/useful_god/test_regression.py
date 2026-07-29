from collections import Counter

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.pattern_engine.engine import PatternEngine
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def test_regression_not_single_useful_god() -> None:
    pattern_engine = PatternEngine()
    useful_engine = UsefulGodEngine(database_path="database/13_useful_god")

    dist = Counter()
    for year in range(1970, 1990):
        cal = CalendarEngine().build(year, 6, 15, 12, 0)
        bazi = BaziEngine().build(cal, gender="male")
        pctx = build_pattern_context(bazi, calendar=cal)
        pres = pattern_engine.calculate(pctx)
        uctx = build_useful_god_context(pctx, pres)
        ures = useful_engine.calculate(uctx)
        dist[ures.useful_god or "NONE"] += 1

    total = sum(dist.values())
    top = max(dist.values()) if dist else 0
    assert total > 0
    assert (top / total) < 0.95

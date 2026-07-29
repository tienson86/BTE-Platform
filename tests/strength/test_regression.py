from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.loader import StrengthLoader
from engines.strength_engine.utils.context_builder import build_strength_context


def generate_100_cases() -> list[tuple[int, int, int, int, int, str]]:
    cases = []
    years = list(range(1940, 2021))
    months = list(range(1, 13))
    i = 0
    while len(cases) < 100:
        y = years[i % len(years)]
        m = months[i % len(months)]
        d = 5 + (i % 20)
        h = (i * 2) % 24
        gender = "male" if i % 2 == 0 else "female"
        cases.append((y, m, d, h, 0, gender))
        i += 1
    return cases


def test_regression_100_charts_distribution() -> None:
    engine = StrengthEngine(database_path="database/12_strength")
    loader = StrengthLoader("database/12_strength")
    grouped = loader.load_rule_groups()
    all_rule_ids = {
        str(r.get("rule_id"))
        for rows in grouped.values()
        for r in rows
        if r.get("rule_id")
    }

    level_counts: dict[str, int] = {}
    rule_hits: dict[str, int] = {}

    for y, m, d, h, minute, gender in generate_100_cases():
        cal = CalendarEngine().build(y, m, d, h, minute)
        bazi = BaziEngine().build(cal, gender=gender)
        ctx = build_strength_context(bazi, calendar=cal)
        result = engine.calculate(ctx)
        assert result.success
        level_counts[result.strength_level] = level_counts.get(result.strength_level, 0) + 1
        for rid in result.matched_rules:
            rule_hits[rid] = rule_hits.get(rid, 0) + 1

    assert sum(level_counts.values()) == 100
    assert len(level_counts) >= 2
    dead = [rid for rid in all_rule_ids if rid and rule_hits.get(rid, 0) == 0]
    assert len(dead) < len(all_rule_ids)

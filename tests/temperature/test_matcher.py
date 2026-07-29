from engines.temperature_engine.context import TemperatureContext
from engines.temperature_engine.matcher import TemperatureMatcher


def test_matcher_climate() -> None:
    ctx = TemperatureContext(climate_type="hot")
    matcher = TemperatureMatcher()
    rule = {
        "conditions": '[{"field": "climate_type", "operator": "==", "value": "hot"}]',
    }
    assert matcher.match(ctx, rule)


def test_matcher_season_in() -> None:
    ctx = TemperatureContext(season="summer")
    matcher = TemperatureMatcher()
    rule = {
        "conditions": '[{"field": "season", "operator": "==", "value": "summer"}]',
    }
    assert matcher.match(ctx, rule)


def test_matcher_fire_count() -> None:
    ctx = TemperatureContext(fire_count=3)
    matcher = TemperatureMatcher()
    rule = {
        "conditions": '[{"field": "fire_count", "operator": ">=", "value": 3}]',
    }
    assert matcher.match(ctx, rule)

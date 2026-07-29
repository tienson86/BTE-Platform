from engines.temperature_engine.context import TemperatureContext
from engines.temperature_engine.matcher import TemperatureMatcher
from engines.temperature_engine.priority import TemperaturePriorityResolver


def test_priority_resolves_hot_level() -> None:
    ctx = TemperatureContext()
    ctx.temperature_score = 0.70
    rules = [
        {
            "rule_id": "pri_level_hot",
            "priority": 100,
            "score_target": "level",
            "temperature_level": "hot",
            "conditions": '[{"field": "temperature_score", "operator": ">=", "value": 0.65}]',
            "status": "active",
            "enabled": "true",
        },
    ]
    resolver = TemperaturePriorityResolver([])
    winner = resolver.resolve_level(ctx, rules, TemperatureMatcher())
    assert winner is not None
    assert winner["temperature_level"] == "hot"

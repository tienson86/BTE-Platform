from engines.strength_engine.context import StrengthContext
from engines.strength_engine.priority import StrengthPriorityResolver


def test_priority_resolves_level() -> None:
    ctx = StrengthContext()
    ctx.strength_score = 0.70
    rules = [
        {
            "rule_id": "pri_level_strong",
            "priority": 100,
            "score_target": "level",
            "strength_level": "strong",
            "conditions": '[{"field": "strength_score", "operator": ">=", "value": 0.65}]',
            "status": "active",
            "enabled": "true",
        },
    ]
    resolver = StrengthPriorityResolver([])
    from engines.strength_engine.matcher import StrengthMatcher

    winner = resolver.resolve_level(ctx, rules, StrengthMatcher())
    assert winner is not None
    assert winner["strength_level"] == "strong"

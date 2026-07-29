from engines.useful_god_engine.priority import PriorityResolver


def test_priority_prefers_special_group() -> None:
    rules = [
        {"conditions": '[{"field":"rule_group","operator":"==","value":"special"}]', "priority": 100},
        {"conditions": '[{"field":"rule_group","operator":"==","value":"strength"}]', "priority": 80},
    ]
    resolver = PriorityResolver(rules)
    winner = resolver.resolve([
        {"rule_group": "strength", "score": 0.9, "priority": 10},
        {"rule_group": "special", "score": 0.8, "priority": 10},
    ])
    assert winner["rule_group"] == "special"

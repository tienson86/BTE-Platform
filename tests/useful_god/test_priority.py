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


def test_flow_remains_evidence_below_structural_strength_fallback() -> None:
    resolver = PriorityResolver([])
    winner = resolver.resolve([
        {
            "rule_id": "str_004",
            "rule_group": "strength",
            "conditions": '[{"field":"strength_level","operator":"==","value":"strong"}]',
            "score": 0.77,
            "priority": 76,
        },
        {
            "rule_id": "flo_002",
            "rule_group": "flow",
            "conditions": '[{"field":"element_distribution","operator":"contains","value":"Hỏa"}]',
            "score": 0.76,
            "priority": 74,
        },
    ])
    assert winner["rule_id"] == "str_004"


def test_specific_strength_rule_beats_flow_candidate() -> None:
    resolver = PriorityResolver([])
    winner = resolver.resolve([
        {
            "rule_id": "str_specific",
            "rule_group": "strength",
            "conditions": (
                '[{"field":"strength_level","operator":"==","value":"strong"},'
                '{"field":"day_master_element","operator":"==","value":"Hỏa"},'
                '{"field":"month_branch","operator":"==","value":"Dần"}]'
            ),
            "score": 0.9,
            "priority": 90,
        },
        {
            "rule_id": "flo_002",
            "rule_group": "flow",
            "conditions": '[{"field":"element_distribution","operator":"contains","value":"Hỏa"}]',
            "score": 0.76,
            "priority": 74,
        },
    ])
    assert winner["rule_id"] == "str_specific"

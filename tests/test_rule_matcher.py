"""
Tests for RuleMatcher
"""

from interpretation_engine.context import InterpretationContext
from interpretation_engine.rule_loader import RuleLoader
from interpretation_engine.rule_matcher import RuleMatcher


def test_create_matcher():

    matcher = RuleMatcher()

    assert matcher is not None


def test_match_returns_list():

    loader = RuleLoader()

    rules = loader.load(
        "tests/data/test_rules.csv"
    )

    context = InterpretationContext()

    context.bazi = {
        "day_master": "Canh"
    }

    matcher = RuleMatcher()

    result = matcher.match(
        context,
        rules,
    )

    assert isinstance(result, list)


def test_match_empty_rules():

    matcher = RuleMatcher()

    context = InterpretationContext()

    result = matcher.match(
        context,
        [],
    )

    assert result == []


def test_match_rule_has_rule_id():

    loader = RuleLoader()

    rules = loader.load(
        "tests/data/test_rules.csv"
    )

    context = InterpretationContext()

    matcher = RuleMatcher()

    matched = matcher.match(
        context,
        rules,
    )

    for rule in matched:

        assert "rule_id" in rule


def test_match_result_is_subset():

    loader = RuleLoader()

    rules = loader.load(
        "tests/data/test_rules.csv"
    )

    matcher = RuleMatcher()

    context = InterpretationContext()

    matched = matcher.match(
        context,
        rules,
    )

    assert len(matched) <= len(rules)

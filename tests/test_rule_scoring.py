"""
Tests for RuleScoring
"""

from interpretation_engine.rule_loader import RuleLoader
from interpretation_engine.rule_scoring import RuleScoring


def test_create_scoring():

    scoring = RuleScoring()

    assert scoring is not None


def test_score_empty():

    scoring = RuleScoring()

    score = scoring.score([])

    assert score == 0


def test_score_rules():

    loader = RuleLoader()

    rules = loader.load(
        "tests/data/test_rules.csv"
    )

    scoring = RuleScoring()

    result = scoring.score(
        rules
    )

    assert isinstance(result, (int, float))


def test_score_non_negative_type():

    scoring = RuleScoring()

    result = scoring.score(
        [
            {
                "score": 10
            },
            {
                "score": -5
            }
        ]
    )

    assert isinstance(result, (int, float))


def test_score_loaded_rules():

    loader = RuleLoader()

    rules = loader.load(
        "tests/data/test_rules.csv"
    )

    scoring = RuleScoring()

    result = scoring.score(
        rules
    )

    assert result is not None

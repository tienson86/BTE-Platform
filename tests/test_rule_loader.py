"""
Tests for RuleLoader
"""

from pathlib import Path

import pytest

from interpretation_engine.rule_loader import RuleLoader


TEST_RULE_FILE = Path("tests/data/test_rules.csv")
EMPTY_RULE_FILE = Path("tests/data/empty_rules.csv")


def test_create_loader():

    loader = RuleLoader()

    assert loader is not None


def test_load_rule_file():

    loader = RuleLoader()

    rules = loader.load(TEST_RULE_FILE)

    assert isinstance(rules, list)


def test_rule_count():

    loader = RuleLoader()

    rules = loader.load(TEST_RULE_FILE)

    assert len(rules) > 0


def test_rule_has_required_fields():

    loader = RuleLoader()

    rules = loader.load(TEST_RULE_FILE)

    rule = rules[0]

    required_fields = [

        "rule_id",
        "category",
        "condition",
        "score",

    ]

    for field in required_fields:

        assert field in rule


def test_load_empty_rule_file():

    loader = RuleLoader()

    rules = loader.load(EMPTY_RULE_FILE)

    assert rules == []


def test_missing_file():

    loader = RuleLoader()

    with pytest.raises(FileNotFoundError):

        loader.load("tests/data/not_found.csv")

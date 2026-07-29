"""
test_rule_loader.py
===================

Kiểm thử RuleLoader.
"""

from pathlib import Path

from engines.interpretation_engine.rule_engine import RuleLoader


def test_load_empty_directory(tmp_path: Path):

    loader = RuleLoader()

    rules = loader.load(tmp_path)

    assert isinstance(rules, list)

    assert len(rules) == 0


def test_loader_returns_rule_list(sample_rules):

    assert isinstance(sample_rules, list)

    assert len(sample_rules) == 1

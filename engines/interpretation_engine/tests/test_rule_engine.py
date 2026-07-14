"""
test_rule_engine.py
===================
"""

from engines.interpretation_engine.rule_engine import RuleEngine


def test_rule_engine_run(sample_context, sample_rules):

    engine = RuleEngine()

    results = engine.run_matched(

        context=sample_context,

        rules=sample_rules,

    )

    assert isinstance(results, list)


def test_rule_engine_result_count(sample_context, sample_rules):

    engine = RuleEngine()

    results = engine.run_matched(

        context=sample_context,

        rules=sample_rules,

    )

    assert len(results) <= len(sample_rules)

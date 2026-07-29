"""
test_models.py
==============

Kiểm thử Models.
"""

from engines.interpretation_engine.models import (
    InterpretationContext,
    InterpretationReport,
    Rule,
    RuleResult,
)


def test_context_set_get():

    context = InterpretationContext()

    context.set("name", "BTE")

    assert context.get("name") == "BTE"


def test_context_nested():

    context = InterpretationContext()

    context.update({

        "bazi": {

            "day_master": "Canh"

        }

    })

    assert context.resolve(
        "bazi.day_master"
    ) == "Canh"


def test_rule():

    rule = Rule(

        id="R001",

        name="Test Rule",

    )

    assert rule.id == "R001"


def test_rule_result():

    rule = Rule(

        id="R001",

        name="Rule",

    )

    result = RuleResult(

        rule=rule,

        matched=True,

    )

    assert result.matched is True


def test_report():

    report = InterpretationReport()

    assert report.section_count == 0

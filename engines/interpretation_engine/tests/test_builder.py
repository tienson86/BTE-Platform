"""
test_builder.py
===============
"""

from engines.interpretation_engine.builders import (
    InterpretationBuilder,
)
from engines.interpretation_engine.models import (
    RuleResult,
)


def test_builder(sample_context, sample_rule):

    builder = InterpretationBuilder()

    result = RuleResult(

        rule=sample_rule,

        matched=True,

        score=100,

    )

    report = builder.build(

        context=sample_context,

        results=[result],

    )

    assert report is not None


def test_report_section_count(sample_context, sample_rule):

    builder = InterpretationBuilder()

    result = RuleResult(

        rule=sample_rule,

        matched=True,

    )

    report = builder.build(

        context=sample_context,

        results=[result],

    )

    assert report.section_count >= 0

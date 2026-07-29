"""
test_v1.py
==========

Integration Test

Pipeline:

Context
    ↓
Rule Engine
    ↓
Builder
    ↓
Report
"""

from engines.interpretation_engine import (
    InterpretationEngine,
)


def test_v1_pipeline(

    sample_context,

    sample_rules,

):

    engine = InterpretationEngine()

    report = engine.interpret(

        context=sample_context,

        rules=sample_rules,

    )

    assert report is not None

    assert report.section_count >= 0


def test_v1_markdown(

    sample_context,

    sample_rules,

):

    engine = InterpretationEngine()

    report = engine.interpret(

        context=sample_context,

        rules=sample_rules,

    )

    markdown = engine.to_markdown(report)

    assert isinstance(markdown, str)


def test_v1_json(

    sample_context,

    sample_rules,

):

    engine = InterpretationEngine()

    report = engine.interpret(

        context=sample_context,

        rules=sample_rules,

    )

    json_text = engine.to_json(report)

    assert isinstance(json_text, str)

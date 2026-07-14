"""
test_engine.py
==============
"""

from engines.interpretation_engine import (
    InterpretationEngine,
)


def test_engine_create():

    engine = InterpretationEngine()

    assert engine is not None


def test_engine_interpret(sample_context, sample_rules):

    engine = InterpretationEngine()

    report = engine.interpret(

        context=sample_context,

        rules=sample_rules,

    )

    assert report is not None

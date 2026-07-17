"""
Integration Tests for InterpretationEngine
"""

from interpretation_engine.engine import InterpretationEngine


def test_create_engine():

    engine = InterpretationEngine()

    assert engine is not None


def test_run_empty_context():

    engine = InterpretationEngine()

    result = engine.run({})

    assert result is not None


def test_run_basic_chart():

    engine = InterpretationEngine()

    chart = {

        "day_master": "Canh",

        "month_branch": "Sửu",

    }

    result = engine.run(chart)

    assert result is not None


def test_pipeline_returns_result():

    engine = InterpretationEngine()

    chart = {

        "day_master": "Canh",

    }

    result = engine.run(chart)

    assert result is not None


def test_pipeline_has_summary():

    engine = InterpretationEngine()

    chart = {

        "day_master": "Canh",

    }

    result = engine.run(chart)

    if isinstance(result, dict):

        assert "summary" in result

    else:

        assert hasattr(result, "summary")


def test_pipeline_has_score():

    engine = InterpretationEngine()

    chart = {

        "day_master": "Canh",

    }

    result = engine.run(chart)

    if isinstance(result, dict):

        assert "score" in result

    else:

        assert hasattr(result, "score")

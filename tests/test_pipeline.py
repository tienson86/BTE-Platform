"""
Test Interpretation Pipeline

Kiểm tra toàn bộ luồng Engine
"""


from interpretation_engine.engine import InterpretationEngine



def test_engine_create():

    engine = InterpretationEngine()

    assert engine is not None



def test_full_pipeline():

    engine = InterpretationEngine()


    input_data = {

        "nhat_chu":
        "Canh Kim",

        "ngu_hanh":
        "Kim"

    }


    result = engine.run(
        input_data
    )


    assert result is not None



def test_pipeline_has_score():

    engine = InterpretationEngine()


    input_data = {

        "nhat_chu":
        "Canh Kim"

    }


    result = engine.run(
        input_data
    )


    assert hasattr(
        result,
        "score"
    )



def test_pipeline_has_text():

    engine = InterpretationEngine()


    input_data = {

        "nhat_chu":
        "Canh Kim"

    }


    result = engine.run(
        input_data
    )


    assert hasattr(
        result,
        "text"
    )



def test_pipeline_empty_input():

    engine = InterpretationEngine()


    result = engine.run(
        {}
    )


    assert result is not None

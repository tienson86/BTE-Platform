"""
Tests for SentenceGenerator
"""

from interpretation_engine.interpretation_builder import InterpretationBuilder
from interpretation_engine.sentence_generator import SentenceGenerator


def test_create_generator():

    generator = SentenceGenerator()

    assert generator is not None


def test_generate_result():

    builder = InterpretationBuilder()

    interpretation = builder.build(
        [
            {
                "description": "Nhật chủ Canh Kim có lực."
            }
        ]
    )

    generator = SentenceGenerator()

    result = generator.generate(
        interpretation
    )

    assert result is not None


def test_generate_returns_string():

    builder = InterpretationBuilder()

    interpretation = builder.build(
        [
            {
                "description": "Kim vượng."
            }
        ]
    )

    generator = SentenceGenerator()

    result = generator.generate(
        interpretation
    )

    assert isinstance(result, str)


def test_generate_not_empty():

    builder = InterpretationBuilder()

    interpretation = builder.build(
        [
            {
                "description": "Quan tinh xuất hiện."
            }
        ]
    )

    generator = SentenceGenerator()

    result = generator.generate(
        interpretation
    )

    assert len(result) > 0

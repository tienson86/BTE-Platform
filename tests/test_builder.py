"""
Tests for InterpretationBuilder
"""

from interpretation_engine.interpretation_builder import (
    InterpretationBuilder,
)


def test_create_builder():

    builder = InterpretationBuilder()

    assert builder is not None


def test_build_empty():

    builder = InterpretationBuilder()

    result = builder.build([])

    assert result is not None


def test_build_single_rule():

    builder = InterpretationBuilder()

    matched_rules = [

        {

            "rule_id": "R001",

            "description": "Nhật chủ Canh Kim vượng.",

            "score": 10,

        }

    ]

    result = builder.build(matched_rules)

    assert result is not None


def test_build_multiple_rules():

    builder = InterpretationBuilder()

    matched_rules = [

        {

            "rule_id": "R001",

            "description": "Nhật chủ mạnh.",

            "score": 10,

        },

        {

            "rule_id": "R002",

            "description": "Quan tinh rõ.",

            "score": 6,

        },

    ]

    result = builder.build(matched_rules)

    assert result is not None


def test_result_has_sections():

    builder = InterpretationBuilder()

    result = builder.build([])

    assert hasattr(result, "sections")


def test_result_has_summary():

    builder = InterpretationBuilder()

    result = builder.build([])

    assert hasattr(result, "summary")

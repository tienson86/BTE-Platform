"""
Temperature Score Calculator

Đánh giá điều hòa hàn nhiệt từ RuleContext temperature facts.

Rules: ``database/15_score_engine/10_temperature/``.
"""

from __future__ import annotations

from ..base.generic_score_calculator import GenericScoreCalculator


class TemperatureScoreCalculator(GenericScoreCalculator):
    """Calculator chấm điểm khí hậu (hàn / nhiệt)."""

    MODULE_NAME = "temperature"

    RULE_FOLDER = "10_temperature"

    DIMENSION_NAME = "Khí hậu"

    DESCRIPTION = "Đánh giá mức độ điều hòa hàn nhiệt của lá số."

    def post_process(self, result, context):
        return result

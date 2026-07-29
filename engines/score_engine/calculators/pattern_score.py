"""
Cách Cục Score Calculator
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class PatternScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "pattern"

    RULE_FOLDER = "05_pattern"

    DIMENSION_NAME = "Cách cục"

    DESCRIPTION = (
        "Đánh giá Cách cục."
    )

    def post_process(self, result, context):

        return result

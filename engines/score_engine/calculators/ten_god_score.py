"""
Thập Thần Score Calculator
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class TenGodScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "ten_gods"

    RULE_FOLDER = "04_ten_gods"

    DIMENSION_NAME = "Thập thần"

    DESCRIPTION = (
        "Đánh giá cấu trúc Thập thần."
    )

    def post_process(self, result, context):

        return result

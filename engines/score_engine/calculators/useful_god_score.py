"""
Dụng Thần Score Calculator
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class UsefulGodScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "useful_god"

    RULE_FOLDER = "06_useful_god"

    DIMENSION_NAME = "Dụng thần"

    DESCRIPTION = (
        "Đánh giá Dụng thần - Hỷ thần - Kỵ thần."
    )

    def post_process(self, result, context):

        return result

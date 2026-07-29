"""
Thần Sát Score Calculator
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class ShenshaScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "shensha"

    RULE_FOLDER = "07_shensha"

    DIMENSION_NAME = "Thần sát"

    DESCRIPTION = (
        "Đánh giá ảnh hưởng của Thần sát."
    )

    def post_process(self, result, context):

        return result

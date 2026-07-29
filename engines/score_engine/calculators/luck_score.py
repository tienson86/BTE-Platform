"""
Đại Vận Score Calculator
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class LuckScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "luck"

    RULE_FOLDER = "08_luck"

    DIMENSION_NAME = "Đại vận"

    DESCRIPTION = (
        "Đánh giá Đại vận và Lưu niên."
    )

    def post_process(self, result, context):

        return result

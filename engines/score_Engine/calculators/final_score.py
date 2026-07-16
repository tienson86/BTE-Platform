"""
Final Score Calculator

Tổng hợp toàn bộ điểm của Score Engine.
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class FinalScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "final_score"

    RULE_FOLDER = "09_final_score"

    DIMENSION_NAME = "Điểm tổng"

    DESCRIPTION = (
        "Tổng hợp và xếp hạng toàn bộ Score Engine."
    )

    def post_process(self, result, context):
        """
        Hook dành cho xử lý đặc biệt.

        V2:
            - Xếp hạng A/B/C/S
            - Confidence
            - Recommendation
            - Risk Level
        """

        return result

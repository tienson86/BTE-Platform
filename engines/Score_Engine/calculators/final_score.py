"""
Final Score Calculator
"""

from ..base import BaseCalculator


class FinalScoreCalculator(BaseCalculator):

    module_name = "final_score"

    def calculate(self, context):

        result = self.create_result()

        # TODO:
        # Nhận điểm từ:
        # - wuxing
        # - strength
        # - ten_gods
        # - pattern
        # - useful_god
        # - shensha
        # - luck
        #
        # Áp dụng trọng số trong:
        # 09_final_score/04_dimension_weight.csv
        #
        # Sinh:
        # total_score
        # grade
        # confidence
        # recommendation

        return result

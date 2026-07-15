"""
Thân Vượng Nhược Score Calculator

Đánh giá:

- Đắc lệnh
- Đắc địa
- Đắc thế
- Có gốc
- Có trợ
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class StrengthScoreCalculator(GenericScoreCalculator):

    MODULE_NAME = "strength"

    RULE_FOLDER = "03_strength"

    DIMENSION_NAME = "Thân vượng nhược"

    DESCRIPTION = (
        "Đánh giá độ mạnh yếu của Nhật chủ."
    )

    def post_process(self, result, context):

        return result

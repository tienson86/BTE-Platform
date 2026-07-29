"""
Ngũ Hành Score Calculator

Đánh giá:

- Cân bằng Ngũ hành
- Đắc lệnh
- Sinh khắc
- Lưu thông
- Điều hậu
"""

from ..base.generic_score_calculator import GenericScoreCalculator


class WuxingScoreCalculator(GenericScoreCalculator):
    """
    Calculator chấm điểm Ngũ hành.
    """

    MODULE_NAME = "wuxing"

    RULE_FOLDER = "02_wuxing"

    DIMENSION_NAME = "Ngũ hành"

    DESCRIPTION = "Đánh giá mức độ cân bằng và chất lượng Ngũ hành."

    def post_process(self, result, context):
        """
        Hook dành cho xử lý riêng của Ngũ hành.

        V1.0:
            Chưa có xử lý đặc biệt.

        V2.0:
            - Điều hậu
            - Khí hậu
            - Độ lưu thông
            - Điểm cân bằng nâng cao
        """
        return result

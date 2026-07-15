"""
Ngũ Hành Score Calculator

Chức năng
---------
Đánh giá điểm Ngũ hành của lá số dựa trên:

- Phân bố Ngũ hành
- Cân bằng Ngũ hành
- Mùa sinh
- Sinh khắc
- Hợp hóa

Không xác định Dụng thần.
Không xác định Cách cục.

Chỉ chấm điểm.
"""

from pathlib import Path

from ..base import BaseCalculator


class WuxingScoreCalculator(BaseCalculator):

    module_name = "wuxing"

    RULE_FILES = [
        "02_wuxing/01_balance_score.csv",
        "02_wuxing/02_season_score.csv",
        "02_wuxing/03_generation_score.csv",
        "02_wuxing/04_control_score.csv",
        "02_wuxing/05_combination_score.csv",
        "02_wuxing/06_special_case.csv",
    ]

    def calculate(self, context):

        result = self.create_result()

        total_score = 0.0

        applied_rules = []

        for file_name in self.RULE_FILES:

            df = self.load_rules(file_name)

            #
            # TODO:
            #
            # Rule Matcher sẽ xử lý:
            #
            #   1. Đọc từng rule
            #   2. Kiểm tra điều kiện
            #   3. Nếu match:
            #           cộng điểm
            #
            #

            for _, rule in df.iterrows():

                # Hiện tại chỉ load dữ liệu.
                # Logic match sẽ làm ở matcher.py.

                applied_rules.append(rule["id"])

        result.score = total_score

        result.details = {
            "loaded_rule_files": self.RULE_FILES,
            "loaded_rule_count": len(applied_rules),
        }

        result.score = self.normalize(result.score)

        return result

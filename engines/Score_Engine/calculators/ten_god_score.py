"""
Ten God Score Calculator
"""

from ..base import BaseCalculator


class TenGodScoreCalculator(BaseCalculator):

    module_name = "ten_gods"

    RULE_FILES = [
        "04_ten_gods/01_positive_score.csv",
        "04_ten_gods/02_negative_score.csv",
        "04_ten_gods/03_combination_score.csv",
        "04_ten_gods/04_structure_score.csv",
        "04_ten_gods/05_special_case.csv",
        "04_ten_gods/06_priority.csv",
    ]

    def calculate(self, context):

        result = self.create_result()

        total_score = 0.0
        loaded_rules = 0

        for file_name in self.RULE_FILES:
            df = self.load_rules(file_name)
            loaded_rules += len(df)

        result.score = self.normalize(total_score)

        result.details = {
            "rule_files": self.RULE_FILES,
            "loaded_rules": loaded_rules,
        }

        return result

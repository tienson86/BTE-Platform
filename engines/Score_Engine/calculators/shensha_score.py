"""
Shen Sha Score Calculator
"""

from ..base import BaseCalculator


class ShenshaScoreCalculator(BaseCalculator):

    module_name = "shensha"

    RULE_FILES = [
        "07_shensha/01_positive_star.csv",
        "07_shensha/02_negative_star.csv",
        "07_shensha/03_marriage_star.csv",
        "07_shensha/04_career_star.csv",
        "07_shensha/05_health_star.csv",
        "07_shensha/06_wealth_star.csv",
        "07_shensha/07_priority.csv",
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

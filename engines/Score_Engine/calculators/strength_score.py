"""
Strength Score Calculator
"""

from ..base import BaseCalculator


class StrengthScoreCalculator(BaseCalculator):

    module_name = "strength"

    RULE_FILES = [
        "03_strength/01_month_power.csv",
        "03_strength/02_root_power.csv",
        "03_strength/03_support_power.csv",
        "03_strength/04_control_power.csv",
        "03_strength/05_follow_pattern.csv",
        "03_strength/06_special_case.csv",
        "03_strength/07_strength_level.csv",
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

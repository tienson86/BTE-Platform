"""
Pattern Score Calculator
"""

from ..base import BaseCalculator


class PatternScoreCalculator(BaseCalculator):

    module_name = "pattern"

    RULE_FILES = [
        "05_pattern/01_pattern_success.csv",
        "05_pattern/02_pattern_failure.csv",
        "05_pattern/03_pattern_priority.csv",
        "05_pattern/04_special_pattern.csv",
        "05_pattern/05_follow_pattern.csv",
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

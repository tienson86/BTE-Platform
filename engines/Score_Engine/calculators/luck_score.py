"""
Luck Score Calculator
"""

from ..base import BaseCalculator


class LuckScoreCalculator(BaseCalculator):

    module_name = "luck"

    RULE_FILES = [
        "08_luck/01_luck_support.csv",
        "08_luck/02_luck_attack.csv",
        "08_luck/03_luck_combination.csv",
        "08_luck/04_luck_clash.csv",
        "08_luck/05_luck_priority.csv",
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

"""
Useful God Score Calculator
"""

from ..base import BaseCalculator


class UsefulGodScoreCalculator(BaseCalculator):

    module_name = "useful_god"

    RULE_FILES = [
        "06_useful_god/01_useful_present.csv",
        "06_useful_god/02_useful_support.csv",
        "06_useful_god/03_useful_destroy.csv",
        "06_useful_god/04_joy_god.csv",
        "06_useful_god/05_enemy_god.csv",
        "06_useful_god/06_priority.csv",
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

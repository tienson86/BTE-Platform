"""
Pattern Calculator.

Điều phối toàn bộ quá trình nhận diện Cách Cục.
"""

from typing import Dict, Any

from .loader import PatternLoader
from .matcher import PatternMatcher
from .validator import PatternValidator


class PatternCalculator:

    def __init__(self, loader: PatternLoader):

        self.loader = loader
        self.matcher = PatternMatcher()

    def calculate(self, context):

        result = {
            "success": True,
            "pattern": None,
            "matched_rules": [],
            "score": 0,
            "priority": 0,
        }

        if not self.loader.exists("rules.csv"):
            result["success"] = False
            result["error"] = "rules.csv not found"
            return result

        df = self.loader.load_csv("rules.csv")

        PatternValidator.validate_dataframe(df)

        rules = df.to_dict("records")

        for rule in rules:

            if self.matcher.match(context, rule):

                result["matched_rules"].append(
                    rule["rule_id"]
                )

                if rule["priority"] >= result["priority"]:

                    result["priority"] = rule["priority"]
                    result["pattern"] = rule["pattern"]
                    result["score"] = rule.get(
                        "score",
                        0
                    )

        return result

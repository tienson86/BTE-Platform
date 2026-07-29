"""
Rule Loader.
"""

from pathlib import Path
import pandas as pd

from ..models.pattern_rule import PatternRule


class RuleLoader:

    def __init__(self, folder):

        self.folder = Path(folder)

    def load(self, filename):

        file = self.folder / filename

        df = pd.read_csv(file)

        rules = []

        for row in df.to_dict("records"):

            rules.append(

                PatternRule(

                    rule_id=row["rule_id"],

                    pattern=row["pattern"],

                    priority=int(row["priority"]),

                    score=float(row.get("score", 0)),

                    conditions=row.get("conditions", ""),

                    description=row.get("description", ""),

                    enabled=bool(row.get("enabled", True))

                )

            )

        return rules

"""
Pattern Validator.
"""

import pandas as pd


REQUIRED_COLUMNS = [

    "rule_id",

    "pattern",

    "priority",

    "conditions",

]


class PatternValidator:

    @staticmethod
    def validate_dataframe(df: pd.DataFrame):

        if df is None:
            raise ValueError("DataFrame is None")

        if df.empty:
            raise ValueError("DataFrame is empty")

        missing = [

            col

            for col in REQUIRED_COLUMNS

            if col not in df.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

        return True

    @staticmethod
    def validate_rule(rule: dict):

        for key in REQUIRED_COLUMNS:

            if key not in rule:

                raise ValueError(

                    f"Missing key: {key}"

                )

        return True

"""
Score Validator
"""

from typing import List


class ScoreValidator:

    REQUIRED_FIELDS = [
        "id",
        "score",
    ]

    @classmethod
    def validate_dataframe(cls, dataframe):

        missing = []

        for field in cls.REQUIRED_FIELDS:

            if field not in dataframe.columns:

                missing.append(field)

        if missing:

            raise ValueError(
                f"CSV thiếu cột: {', '.join(missing)}"
            )

    @classmethod
    def validate_score(cls, score):

        if score is None:

            raise ValueError(
                "Score không được None."
            )

    @classmethod
    def validate_weight(cls, weight):

        if weight <= 0:

            raise ValueError(
                "Weight phải lớn hơn 0."
            )

    @classmethod
    def validate_rules(
        cls,
        rules: List
    ):

        if rules is None:

            raise ValueError(
                "Rule rỗng."
            )

"""
Score Validator

Kiểm tra dữ liệu đầu vào trước khi tính điểm.
"""

from typing import Iterable


class ScoreValidator:

    REQUIRED_RULE_COLUMNS = [
        "id",
        "rule_code",
        "condition",
        "score",
    ]

    @classmethod
    def validate_dataframe(cls, dataframe):

        missing = [
            column
            for column in cls.REQUIRED_RULE_COLUMNS
            if column not in dataframe.columns
        ]

        if missing:
            raise ValueError(
                "Thiếu cột bắt buộc: "
                + ", ".join(missing)
            )

    @classmethod
    def validate_score(cls, score):

        if not isinstance(score, (int, float)):
            raise TypeError(
                "Score phải là số."
            )

    @classmethod
    def validate_weight(cls, weight):

        if not isinstance(weight, (int, float)):
            raise TypeError(
                "Weight phải là số."
            )

        if weight <= 0:
            raise ValueError(
                "Weight phải lớn hơn 0."
            )

    @classmethod
    def validate_context(cls, context):

        if context is None:
            raise ValueError(
                "Context không được để trống."
            )

    @classmethod
    def validate_rules(cls, rules):

        if rules is None:
            raise ValueError(
                "Rules không được None."
            )

        if isinstance(rules, Iterable):

            if len(rules) == 0:
                raise ValueError(
                    "Rules rỗng."
                )

    @classmethod
    def validate_result(cls, result):

        if result is None:
            raise ValueError(
                "CalculatorResult không hợp lệ."
            )

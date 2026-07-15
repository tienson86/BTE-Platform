"""
Rule Matcher

Chức năng

- Đọc điều kiện (condition) trong Rule CSV.
- Đánh giá Rule có thỏa mãn hay không.
- Trả về danh sách Rule đã match.

Không cộng điểm.
Không diễn giải.

Chỉ Match.
"""

from typing import Dict, List, Any


class RuleMatcher:

    def __init__(self):
        pass

    # =====================================================
    # Match nhiều Rule
    # =====================================================

    def match(
        self,
        rules,
        context
    ) -> List[Dict[str, Any]]:

        matched = []

        for _, rule in rules.iterrows():

            if self.evaluate(rule, context):

                matched.append(rule.to_dict())

        return matched

    # =====================================================
    # Match một Rule
    # =====================================================

    def evaluate(
        self,
        rule,
        context
    ) -> bool:

        condition = str(
            rule.get("condition", "")
        ).strip()

        if condition == "":
            return True

        return self.evaluate_expression(
            condition,
            context
        )

    # =====================================================
    # Parser
    # =====================================================

    def evaluate_expression(
        self,
        expression: str,
        context
    ) -> bool:

        """
        Parser đơn giản.

        Giai đoạn V1:

            a == b

            a != b

            a > b

            a >= b

            a < b

            a <= b

        V2 sẽ bổ sung

            and

            or

            ()

            in

            contains
        """

        expression = expression.strip()

        operators = [
            "==",
            "!=",
            ">=",
            "<=",
            ">",
            "<",
        ]

        for operator in operators:

            if operator in expression:

                left, right = expression.split(
                    operator,
                    1
                )

                left = left.strip()

                right = right.strip()

                return self.compare(
                    left,
                    operator,
                    right,
                    context,
                )

        return False

    # =====================================================
    # Compare
    # =====================================================

    def compare(
        self,
        left,
        operator,
        right,
        context
    ):

        left_value = self.resolve(
            left,
            context
        )

        right_value = self.resolve(
            right,
            context
        )

        if operator == "==":
            return left_value == right_value

        if operator == "!=":
            return left_value != right_value

        if operator == ">":
            return left_value > right_value

        if operator == "<":
            return left_value < right_value

        if operator == ">=":
            return left_value >= right_value

        if operator == "<=":
            return left_value <= right_value

        return False

    # =====================================================
    # Resolve
    # =====================================================

    def resolve(
        self,
        value,
        context
    ):

        """
        Resolve biến.

        Ví dụ

            day_master

            season

            pattern

            strength

        """

        if hasattr(context, value):

            return getattr(
                context,
                value
            )

        #
        # số
        #

        try:

            return int(value)

        except Exception:

            pass

        try:

            return float(value)

        except Exception:

            pass

        #
        # string
        #

        return value

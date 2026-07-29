"""
condition_evaluator.py
======================

Đánh giá AST của Rule trên InterpretationContext.

Flow

Condition String
        │
        ▼
ConditionParser
        │
        ▼
ASTNode
        │
        ▼
ConditionEvaluator
        │
        ▼
True / False
"""

from __future__ import annotations

from typing import Any
from typing import List

from .condition_parser import (
    ASTNode,
    ConditionNode,
    Logic,
    LogicNode,
    Operator,
)


class ConditionEvaluator:
    """
    Đánh giá AST Condition.
    """

    # ======================================================
    # Public
    # ======================================================

    def evaluate(
        self,
        context: Any,
        nodes: List[ASTNode],
    ) -> bool:
        """
        Đánh giá toàn bộ AST.

        Mặc định hỗ trợ:

            A
            A AND B
            A OR B

        NOT sẽ bổ sung ở phiên bản tiếp theo.
        """

        if not self.validate(nodes):
            raise ValueError("Invalid condition AST")

        if not nodes:
            return True

        result = None

        logic = Logic.AND

        for node in nodes:

            if isinstance(node, LogicNode):

                logic = node.logic
                continue

            current = self.evaluate_node(
                context,
                node,
            )

            if result is None:

                result = current
                continue

            if logic == Logic.AND:

                result = result and current

            elif logic == Logic.OR:

                result = result or current

        return bool(result)

    # ======================================================
    # Node
    # ======================================================

    def evaluate_node(
        self,
        context: Any,
        node: ConditionNode,
    ) -> bool:

        actual = self.get_value(
            context,
            node.field,
        )

        return self.compare(
            actual,
            node.operator,
            node.value,
        )

    # ======================================================
    # Context
    # ======================================================

    def get_value(
        self,
        context: Any,
        field: str,
    ) -> Any:
        """
        Đọc dữ liệu từ InterpretationContext.

        Hỗ trợ:

            bazi.day_master

            score.strength

            pattern.name

            ten_gods.chinh_quan
        """

        current = context

        for part in field.split("."):

            if current is None:
                return None

            if isinstance(current, dict):

                current = current.get(part)
                continue

            if hasattr(current, part):

                current = getattr(current, part)
                continue

            return None

        return current

    # ======================================================
    # Compare
    # ======================================================

    def compare(
        self,
        actual: Any,
        operator: Operator,
        expected: Any,
    ) -> bool:
        """
        Part 2 sẽ hoàn thiện.
        """

        raise NotImplementedError
          # ======================================================
    # Compare
    # ======================================================

    def compare(
        self,
        actual: Any,
        operator: Operator,
        expected: Any,
    ) -> bool:
        """
        So sánh giá trị.

        Hỗ trợ:

            ==
            !=
            >
            <
            >=
            <=
            contains
            not_contains
            exists
            not_exists
        """

        # ----------------------------
        # EXISTS
        # ----------------------------

        if operator == Operator.EXISTS:

            return actual is not None

        if operator == Operator.NOT_EXISTS:

            return actual is None

        # ----------------------------
        # None
        # ----------------------------

        if actual is None:

            return False

        # ----------------------------
        # Number
        # ----------------------------

        actual_number = self.to_number(actual)
        expected_number = self.to_number(expected)

        if (
            actual_number is not None
            and expected_number is not None
        ):

            if operator == Operator.EQ:
                return actual_number == expected_number

            if operator == Operator.NE:
                return actual_number != expected_number

            if operator == Operator.GT:
                return actual_number > expected_number

            if operator == Operator.GTE:
                return actual_number >= expected_number

            if operator == Operator.LT:
                return actual_number < expected_number

            if operator == Operator.LTE:
                return actual_number <= expected_number

        # ----------------------------
        # String
        # ----------------------------

        actual_text = str(actual).strip()

        expected_text = ""

        if expected is not None:

            expected_text = str(expected).strip()

        if operator == Operator.EQ:

            return actual_text == expected_text

        if operator == Operator.NE:

            return actual_text != expected_text

        if operator == Operator.CONTAINS:

            return expected_text in actual_text

        if operator == Operator.NOT_CONTAINS:

            return expected_text not in actual_text

        return False

    # ======================================================
    # Helper
    # ======================================================

    @staticmethod
    def to_number(
        value: Any,
    ) -> float | None:
        """
        Chuyển về số.

        Không chuyển được sẽ trả None.
        """

        if value is None:

            return None

        try:

            return float(value)

        except Exception:

            return None
              # ======================================================
    # Logic Helper
    # ======================================================

    def evaluate_not(
        self,
        value: bool,
    ) -> bool:
        """
        Phủ định kết quả.
        """
        return not value

    def evaluate_and(
        self,
        left: bool,
        right: bool,
    ) -> bool:
        """
        Phép AND.
        """
        return left and right

    def evaluate_or(
        self,
        left: bool,
        right: bool,
    ) -> bool:
        """
        Phép OR.
        """
        return left or right

    # ======================================================
    # AST Validation
    # ======================================================

    def validate(
        self,
        nodes: List[ASTNode],
    ) -> bool:
        """
        Kiểm tra AST hợp lệ.

        Ví dụ:

            Condition
            Condition AND Condition
            NOT Condition
        """

        if not nodes:
            return True

        expect_condition = True

        for node in nodes:

            if expect_condition:

                if isinstance(node, LogicNode):

                    if node.logic != Logic.NOT:
                        return False

                elif isinstance(node, ConditionNode):

                    expect_condition = False

            else:

                if not isinstance(node, LogicNode):
                    return False

                expect_condition = True

        return True

    # ======================================================
    # Callable
    # ======================================================

    def __call__(
        self,
        context: Any,
        nodes: List[ASTNode],
    ) -> bool:
        """
        Cho phép gọi:

            evaluator(context, nodes)
        """

        return self.evaluate(
            context=context,
            nodes=nodes,
        )

    # ======================================================
    # Debug
    # ======================================================

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}()"
        )

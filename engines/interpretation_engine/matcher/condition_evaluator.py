"""
BTE Platform
=============================

Interpretation Engine

Condition Evaluator

Đánh giá điều kiện của Rule.

Author : BTE Project
Version : 1.0.0
"""

from __future__ import annotations

from typing import Any
from collections.abc import Mapping

from .context import MatchContext
from .operators import get_operator


class ConditionEvaluator:
    """
    Bộ đánh giá điều kiện.

    Trách nhiệm

    - Đánh giá Rule
    - Đánh giá Group
    - Đánh giá Condition
    - Hỗ trợ AND / OR / NOT
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        explain: bool = False,
        debug: bool = False,
    ) -> None:

        self.explain = explain

        self.debug = debug

        self._statistics = {

            "rules": 0,

            "groups": 0,

            "conditions": 0,

            "success": 0,

            "failed": 0,

        }

    # =====================================================
    # Public API
    # =====================================================

    def evaluate(
        self,
        condition: Mapping[str, Any],
        context: MatchContext,
    ) -> bool:
        """
        Entry Point.

        Parameters
        ----------
        condition

        context

        Returns
        -------
        bool
        """

        if not condition:

            return True

        return self.evaluate_group(
            condition,
            context,
        )

    def evaluate_rule(
        self,
        rule: Mapping[str, Any],
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá Rule.
        """

        self._statistics["rules"] += 1

        condition = rule.get(
            "condition"
        )

        if not condition:

            return True

        return self.evaluate(
            condition,
            context,
        )

    def evaluate_group(
        self,
        group: Mapping[str, Any],
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá một nhóm điều kiện.

        Hoàn thiện ở Part 2.
        """

        raise NotImplementedError(
            "evaluate_group() sẽ được hoàn thiện ở Part 2."
        )

    def evaluate_condition(
        self,
        condition: Mapping[str, Any],
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá Condition.

        Hoàn thiện ở Part 2.
        """

        raise NotImplementedError(
            "evaluate_condition() sẽ được hoàn thiện ở Part 2."
        )

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def statistics(self):

        return self._statistics.copy()

    def reset_statistics(self):

        self._statistics = {

            "rules": 0,

            "groups": 0,

            "conditions": 0,

            "success": 0,

            "failed": 0,

        }

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        return {

            "version": self.VERSION,

            "statistics": self.statistics,

        }

    def __repr__(self):

        return (

            f"<ConditionEvaluator "

            f"rules={self._statistics['rules']} "

            f"conditions={self._statistics['conditions']}>"

        )
          # =====================================================
    # Group Evaluation
    # =====================================================

    def evaluate_group(
        self,
        group: Mapping[str, Any],
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá một nhóm điều kiện.

        Hỗ trợ:

        {
            "operator": "AND",
            "conditions": [...]
        }

        {
            "operator": "OR",
            "conditions": [...]
        }

        {
            "operator": "NOT",
            "conditions": [...]
        }
        """

        self._statistics["groups"] += 1

        operator = str(
            group.get(
                "operator",
                "AND",
            )
        ).upper()

        conditions = group.get(
            "conditions",
            [],
        )

        if not isinstance(
            conditions,
            list,
        ):
            raise TypeError(
                "'conditions' phải là list."
            )

        if operator == "AND":

            return self._evaluate_and(
                conditions,
                context,
            )

        if operator == "OR":

            return self._evaluate_or(
                conditions,
                context,
            )

        if operator == "NOT":

            return self._evaluate_not(
                conditions,
                context,
            )

        raise ValueError(
            f"Operator group '{operator}' không hợp lệ."
        )

    # =====================================================
    # Logical Operators
    # =====================================================

    def _evaluate_and(
        self,
        conditions: list,
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá AND.

        Short Circuit.
        """

        for item in conditions:

            if self._is_group(item):

                result = self.evaluate_group(
                    item,
                    context,
                )

            else:

                result = self.evaluate_condition(
                    item,
                    context,
                )

            if not result:

                self._statistics["failed"] += 1

                return False

        self._statistics["success"] += 1

        return True

    def _evaluate_or(
        self,
        conditions: list,
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá OR.

        Short Circuit.
        """

        for item in conditions:

            if self._is_group(item):

                result = self.evaluate_group(
                    item,
                    context,
                )

            else:

                result = self.evaluate_condition(
                    item,
                    context,
                )

            if result:

                self._statistics["success"] += 1

                return True

        self._statistics["failed"] += 1

        return False

    def _evaluate_not(
        self,
        conditions: list,
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá NOT.
        """

        if len(conditions) != 1:

            raise ValueError(
                "NOT chỉ nhận đúng một điều kiện."
            )

        item = conditions[0]

        if self._is_group(item):

            return not self.evaluate_group(
                item,
                context,
            )

        return not self.evaluate_condition(
            item,
            context,
        )

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _is_group(
        item: Mapping[str, Any],
    ) -> bool:
        """
        Kiểm tra có phải Condition Group.
        """

        return (
            isinstance(item, Mapping)
            and "conditions" in item
        )

    @staticmethod
    def _is_condition(
        item: Mapping[str, Any],
    ) -> bool:
        """
        Kiểm tra có phải Condition đơn.
        """

        return (
            isinstance(item, Mapping)
            and "field" in item
            and "operator" in item
        )
          # =====================================================
    # Condition Evaluation
    # =====================================================

    def evaluate_condition(
        self,
        condition: Mapping[str, Any],
        context: MatchContext,
    ) -> bool:
        """
        Đánh giá một điều kiện đơn.

        Ví dụ

        {
            "field": "day_master",
            "operator": "eq",
            "value": "Canh"
        }
        """

        self._statistics["conditions"] += 1

        if not self._is_condition(condition):

            raise ValueError(
                "Condition không hợp lệ."
            )

        field = condition["field"]

        operator_name = condition["operator"]

        expected = condition.get("value")

        actual = self.resolve_field(
            field,
            context,
        )

        expected = self.resolve_value(
            expected,
            context,
        )

        operator = get_operator(
            operator_name
        )

        try:

            result = operator(
                actual,
                expected,
            )

        except Exception as ex:

            if self.debug:

                raise

            raise RuntimeError(
                f"Lỗi khi đánh giá operator "
                f"'{operator_name}': {ex}"
            ) from ex

        if result:

            self._statistics["success"] += 1

        else:

            self._statistics["failed"] += 1

        return result

    # =====================================================
    # Value Resolver
    # =====================================================

    def resolve_field(
        self,
        field: str,
        context: MatchContext,
    ) -> Any:
        """
        Lấy giá trị từ MatchContext.

        Hỗ trợ đường dẫn:

            year.stem
            month.branch
            day.ten_god
        """

        if "." not in field:

            return context.get(field)

        value = context.chart

        for key in field.split("."):

            if value is None:

                return None

            if isinstance(
                value,
                Mapping,
            ):

                value = value.get(key)

            else:

                value = getattr(
                    value,
                    key,
                    None,
                )

        return value

    def resolve_value(
        self,
        value: Any,
        context: MatchContext,
    ) -> Any:
        """
        Resolve giá trị.

        Nếu value là biến:

            ${variable}

        thì lấy từ context.variables.
        """

        if not isinstance(
            value,
            str,
        ):

            return value

        if not value.startswith("${"):

            return value

        if not value.endswith("}"):

            return value

        variable = value[2:-1]

        return context.variables.get(
            variable
        )

    # =====================================================
    # Variable Resolver
    # =====================================================

    def resolve_variable(
        self,
        name: str,
        context: MatchContext,
        default=None,
    ):
        """
        Resolve một biến.
        """

        return context.variables.get(
            name,
            default,
        )

    # =====================================================
    # Utilities
    # =====================================================

    @staticmethod
    def normalize_operator(
        operator: str,
    ) -> str:
        """
        Chuẩn hóa tên operator.
        """

        return operator.strip().lower()

    @staticmethod
    def normalize_field(
        field: str,
    ) -> str:
        """
        Chuẩn hóa tên field.
        """

        return field.strip()

    @staticmethod
    def normalize_value(
        value: Any,
    ) -> Any:
        """
        Hook chuẩn hóa value.

        Có thể override.
        """

        return value
          # =====================================================
    # Validation
    # =====================================================

    def validate_condition(
        self,
        condition: Mapping[str, Any],
    ) -> bool:
        """
        Kiểm tra cấu trúc Condition.
        """

        if not isinstance(
            condition,
            Mapping,
        ):
            return False

        required = (
            "field",
            "operator",
        )

        for field in required:

            if field not in condition:

                return False

        return True

    def validate_group(
        self,
        group: Mapping[str, Any],
    ) -> bool:
        """
        Kiểm tra Group Condition.
        """

        if not isinstance(
            group,
            Mapping,
        ):
            return False

        if "conditions" not in group:

            return False

        if not isinstance(
            group["conditions"],
            list,
        ):
            return False

        return True

    # =====================================================
    # Explain
    # =====================================================

    def explain(
        self,
        condition: Mapping[str, Any],
        context: MatchContext,
    ) -> dict[str, Any]:
        """
        Giải thích kết quả đánh giá.

        Chỉ phục vụ Debug.
        """

        result = self.evaluate(
            condition,
            context,
        )

        return {

            "result": result,

            "condition": condition,

            "statistics": self.statistics,

        }

    # =====================================================
    # Debug
    # =====================================================

    def dump_statistics(self):

        return self.statistics

    def reset(self):

        self.reset_statistics()

    # =====================================================
    # Hooks
    # =====================================================

    def before_group(
        self,
        group: Mapping[str, Any],
        context: MatchContext,
    ) -> None:
        """
        Hook trước khi đánh giá Group.
        """

        return None

    def after_group(
        self,
        group: Mapping[str, Any],
        result: bool,
    ) -> None:
        """
        Hook sau khi đánh giá Group.
        """

        return None

    def before_condition(
        self,
        condition: Mapping[str, Any],
        context: MatchContext,
    ) -> None:
        """
        Hook trước khi đánh giá Condition.
        """

        return None

    def after_condition(
        self,
        condition: Mapping[str, Any],
        result: bool,
    ) -> None:
        """
        Hook sau khi đánh giá Condition.
        """

        return None

    # =====================================================
    # Lifecycle
    # =====================================================

    def initialize(self) -> None:
        """
        Khởi tạo Evaluator.
        """

        self.reset_statistics()

    def shutdown(self) -> None:
        """
        Giải phóng tài nguyên.
        """

        return None

    # =====================================================
    # Information
    # =====================================================

    @property
    def version(self) -> str:

        return self.VERSION

    @property
    def rule_count(self) -> int:

        return self._statistics["rules"]

    @property
    def group_count(self) -> int:

        return self._statistics["groups"]

    @property
    def condition_count(self) -> int:

        return self._statistics["conditions"]

    @property
    def success_count(self) -> int:

        return self._statistics["success"]

    @property
    def failed_count(self) -> int:

        return self._statistics["failed"]

    # =====================================================
    # Health
    # =====================================================

    def health(self) -> dict[str, Any]:
        """
        Trạng thái của Evaluator.
        """

        return {

            "version": self.VERSION,

            "statistics": self.statistics,

            "ready": True,

        }

    # =====================================================
    # Magic Methods
    # =====================================================

    def __len__(self):

        return self.condition_count

    def __repr__(self):

        return (

            f"<ConditionEvaluator "

            f"rules={self.rule_count} "

            f"groups={self.group_count} "

            f"conditions={self.condition_count}>"

        )

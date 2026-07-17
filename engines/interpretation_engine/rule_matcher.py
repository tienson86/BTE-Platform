"""
rule_matcher.py
===============

Rule Matcher cho BTE Platform V1.0

Nhiệm vụ:

- Nhận danh sách Rule từ RuleLoader
- Kiểm tra điều kiện Rule
- Trả về danh sách Rule phù hợp

RuleMatcher KHÔNG thực hiện luận giải.
Nó chỉ xác định Rule nào được kích hoạt.
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class RuleMatcher:
    """
    Rule Matcher.

    Chịu trách nhiệm:

    - lọc Rule
    - kiểm tra điều kiện
    - trả về Rule hợp lệ
    """

    def __init__(self, strict: bool = False):

        # strict=True:
        # thiếu dữ liệu -> False
        #
        # strict=False:
        # thiếu dữ liệu -> bỏ qua

        self.strict = strict

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def match(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Match toàn bộ Rule.

        Parameters
        ----------
        context
            InterpretationContext

        rules
            Danh sách Rule từ RuleLoader

        Returns
        -------
        List[dict]
            Danh sách Rule đã match.
        """

        matched: List[Dict[str, Any]] = []

        if not rules:
            return matched

        for rule in rules:

            if not isinstance(rule, dict):
                continue

            condition = rule.get("condition")

            if self.check_condition(
                context=context,
                condition=condition,
            ):
                matched.append(rule)

        matched = self.sort_by_priority(matched)

        return matched

    # ---------------------------------------------------------
    # Condition
    # ---------------------------------------------------------

    def check_condition(
        self,
        context: Any,
        condition: Any,
    ) -> bool:
        """
        Part 2 sẽ triển khai.
        """
        raise NotImplementedError

    def normalize_condition(
        self,
        condition: Any,
    ) -> Dict[str, Any]:
        """
        Part 2 sẽ triển khai.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Context
    # ---------------------------------------------------------

    def get_context_value(
        self,
        context: Any,
        path: str,
    ) -> Any:
        """
        Part 3 sẽ triển khai.
        """
        raise NotImplementedError

    def compare_value(
        self,
        actual: Any,
        expected: Any,
    ) -> bool:
        """
        Part 3 sẽ triển khai.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Filter
    # ---------------------------------------------------------

    def filter_by_category(
        self,
        rules: List[Dict[str, Any]],
        category: Optional[str],
    ) -> List[Dict[str, Any]]:

        if not category:
            return rules

        return [
            rule
            for rule in rules
            if rule.get("category") == category
        ]

    def filter_by_layer(
        self,
        rules: List[Dict[str, Any]],
        layer: Optional[str],
    ) -> List[Dict[str, Any]]:

        if not layer:
            return rules

        return [
            rule
            for rule in rules
            if rule.get("layer") == layer
        ]

    # ---------------------------------------------------------
    # Sort
    # ---------------------------------------------------------

    def sort_by_priority(
        self,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Sắp xếp Rule theo priority giảm dần.
        """

        return sorted(
            rules,
            key=lambda x: x.get("priority", 0),
            reverse=True,
        )
            # ---------------------------------------------------------
    # Condition
    # ---------------------------------------------------------

    def normalize_condition(
        self,
        condition: Any,
    ) -> Dict[str, Any]:
        """
        Chuẩn hóa condition về dict.

        Hỗ trợ:

        - dict
        - JSON string
        - key=value
        - key=value;key2=value2
        """

        if condition is None:
            return {}

        if isinstance(condition, dict):
            return condition

        if not isinstance(condition, str):
            return {}

        condition = condition.strip()

        if condition == "":
            return {}

        # ----------------------------
        # JSON
        # ----------------------------

        if condition.startswith("{"):

            import json

            try:
                data = json.loads(condition)

                if isinstance(data, dict):
                    return data

            except Exception:
                return {}

        # ----------------------------
        # key=value
        # ----------------------------

        result = {}

        parts = [
            p.strip()
            for p in condition.split(";")
            if p.strip()
        ]

        for item in parts:

            if "=" not in item:
                continue

            key, value = item.split("=", 1)

            result[key.strip()] = value.strip()

        return result

    def check_condition(
        self,
        context: Any,
        condition: Any,
    ) -> bool:
        """
        Kiểm tra Rule condition.
        """

        condition = self.normalize_condition(condition)

        if not condition:
            return True

        for key, expected in condition.items():

            actual = self.get_context_value(
                context=context,
                path=key,
            )

            if actual is None:

                if self.strict:
                    return False

                continue

            if not self.compare_value(
                actual,
                expected,
            ):
                return False

        return True
            # ---------------------------------------------------------
    # Context
    # ---------------------------------------------------------

    def get_context_value(
        self,
        context: Any,
        path: str,
    ) -> Any:
        """
        Lấy giá trị trong InterpretationContext.

        Ví dụ:

            bazi.day_master
            score.strength
            pattern.name
            elements.fire
        """

        if context is None:
            return None

        if not path:
            return None

        current = context

        for part in path.split("."):

            if current is None:
                return None

            # dict
            if isinstance(current, dict):
                current = current.get(part)
                continue

            # object
            if hasattr(current, part):
                current = getattr(current, part)
                continue

            return None

        return current

    def compare_value(
        self,
        actual: Any,
        expected: Any,
    ) -> bool:
        """
        So sánh actual và expected.

        Hỗ trợ:

        value
        !=value
        >value
        <value
        >=value
        <=value
        in:a,b,c
        not in:a,b,c
        """

        if expected is None:
            return actual is None

        expected = str(expected).strip()

        # ------------------------
        # not in
        # ------------------------

        if expected.startswith("not in:"):

            values = [
                x.strip()
                for x in expected[7:].split(",")
                if x.strip()
            ]

            return str(actual) not in values

        # ------------------------
        # in
        # ------------------------

        if expected.startswith("in:"):

            values = [
                x.strip()
                for x in expected[3:].split(",")
                if x.strip()
            ]

            return str(actual) in values

        # ------------------------
        # !=
        # ------------------------

        if expected.startswith("!="):

            return str(actual) != expected[2:].strip()

        # ------------------------
        # >=
        # ------------------------

        if expected.startswith(">="):

            try:
                return float(actual) >= float(expected[2:].strip())
            except Exception:
                return False

        # ------------------------
        # <=
        # ------------------------

        if expected.startswith("<="):

            try:
                return float(actual) <= float(expected[2:].strip())
            except Exception:
                return False

        # ------------------------
        # >
        # ------------------------

        if expected.startswith(">"):

            try:
                return float(actual) > float(expected[1:].strip())
            except Exception:
                return False

        # ------------------------
        # <
        # ------------------------

        if expected.startswith("<"):

            try:
                return float(actual) < float(expected[1:].strip())
            except Exception:
                return False

        # ------------------------
        # bool
        # ------------------------

        if expected.lower() == "true":
            return bool(actual) is True

        if expected.lower() == "false":
            return bool(actual) is False

        # ------------------------
        # number
        # ------------------------

        try:

            actual_number = float(actual)
            expected_number = float(expected)

            return actual_number == expected_number

        except Exception:
            pass

        # ------------------------
        # string
        # ------------------------

        return str(actual).strip() == expected
            # ---------------------------------------------------------
    # Filter
    # ---------------------------------------------------------

    def filter_by_category(
        self,
        rules: List[Dict[str, Any]],
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Lọc Rule theo category.
        """

        if not category:
            return list(rules)

        return [
            rule
            for rule in rules
            if rule.get("category") == category
        ]

    def filter_by_layer(
        self,
        rules: List[Dict[str, Any]],
        layer: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Lọc Rule theo layer.
        """

        if not layer:
            return list(rules)

        return [
            rule
            for rule in rules
            if rule.get("layer") == layer
        ]

    # ---------------------------------------------------------
    # Sort
    # ---------------------------------------------------------

    def sort_by_priority(
        self,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Sắp xếp Rule theo priority giảm dần.
        Nếu priority không tồn tại sẽ mặc định bằng 0.
        """

        return sorted(
            rules,
            key=lambda rule: int(rule.get("priority", 0)),
            reverse=True,
        )

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    def validate_rule(
        self,
        rule: Dict[str, Any],
    ) -> bool:
        """
        Kiểm tra Rule có hợp lệ hay không.
        """

        if not isinstance(rule, dict):
            return False

        if "condition" not in rule:
            return False

        return True

    def match_one(
        self,
        context: Any,
        rule: Dict[str, Any],
    ) -> bool:
        """
        Match một Rule.
        """

        if not self.validate_rule(rule):
            return False

        return self.check_condition(
            context=context,
            condition=rule.get("condition"),
        )

    def match_all(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Alias của match() để tương thích các module khác.
        """

        return self.match(
            context=context,
            rules=rules,
        )

    # ---------------------------------------------------------
    # Magic
    # ---------------------------------------------------------

    def __call__(
        self,
        context: Any,
        rules: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Cho phép gọi trực tiếp:
            matcher(context, rules)
        """

        return self.match(
            context=context,
            rules=rules,
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(strict={self.strict})"
        )

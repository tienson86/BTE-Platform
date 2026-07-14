"""
registry.py
===========

Operator Registry.

Quản lý toàn bộ Operator của Rule Engine.

RuleMatcher không tạo Operator trực tiếp,
mà luôn lấy từ Registry.
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from .operators.base import BaseOperator


class OperatorRegistry:
    """
    Registry quản lý Operator.
    """

    def __init__(self) -> None:

        self._operators: Dict[str, BaseOperator] = {}

    # =====================================================
    # Register
    # =====================================================

    def register(self, operator: BaseOperator) -> None:
        """
        Đăng ký một Operator.
        """

        name = operator.operator

        if name in self._operators:
            raise ValueError(
                f"Operator '{name}' đã tồn tại."
            )

        self._operators[name] = operator

    def unregister(self, name: str) -> None:

        self._operators.pop(name, None)

    # =====================================================
    # Query
    # =====================================================

    def get(self, name: str) -> Optional[BaseOperator]:

        return self._operators.get(name)

    def has(self, name: str) -> bool:

        return name in self._operators

    def all(self) -> Iterable[BaseOperator]:

        return self._operators.values()

    def names(self) -> list[str]:

        return sorted(self._operators.keys())

    def clear(self) -> None:

        self._operators.clear()

    # =====================================================
    # Metadata
    # =====================================================

    @property
    def count(self) -> int:

        return len(self._operators)

    def __len__(self) -> int:

        return len(self._operators)

    def __contains__(self, name: str) -> bool:

        return self.has(name)

    def __repr__(self) -> str:

        return (
            f"OperatorRegistry("
            f"{self.count} operators)"
        )

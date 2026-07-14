"""
base.py
=======

Lớp cơ sở cho toàn bộ Operator của Rule Engine.

Mỗi Operator chỉ chịu trách nhiệm đánh giá
một loại toán tử hoặc một loại điều kiện.

Ví dụ:

==
!=
>
<
contains
exists
HAS_SHENSHA
HAS_PATTERN
HAS_COMBINATION
...

RuleMatcher sẽ không biết chi tiết từng toán tử,
mà chỉ gọi OperatorRegistry để lấy Operator phù hợp.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ...models.context import InterpretationContext
from ...models.rule import Rule
from ..condition_parser import ConditionNode


class BaseOperator(ABC):
    """
    Lớp cha của tất cả Operator.

    Mỗi Operator phải khai báo:

    - name: tên toán tử
    - evaluate(): đánh giá điều kiện
    """

    #: Tên toán tử mà Operator xử lý
    name: str = ""

    #: Độ ưu tiên (dùng khi có nhiều Operator cùng hỗ trợ)
    priority: int = 100

    # =====================================================
    # API bắt buộc
    # =====================================================

    @abstractmethod
    def evaluate(
        self,
        context: InterpretationContext,
        node: ConditionNode,
        rule: Rule | None = None,
    ) -> bool:
        """
        Đánh giá điều kiện.

        Parameters
        ----------
        context:
            Context của lá số.

        node:
            Điều kiện đã được parser.

        rule:
            Rule đang xử lý (không bắt buộc).

        Returns
        -------
        bool
        """
        raise NotImplementedError

    # =====================================================
    # Helper
    # =====================================================

    def resolve(
        self,
        context: InterpretationContext,
        field: str,
    ) -> Any:
        """
        Lấy giá trị từ Context.

        Ví dụ:

        strength

        day.stem

        current_luck.branch

        useful_god
        """

        return context.resolve(field)

    def normalize(self, value: Any) -> Any:
        """
        Chuẩn hóa dữ liệu trước khi so sánh.

        Có thể override nếu cần.
        """

        if isinstance(value, str):
            return value.strip()

        return value

    def compare(
        self,
        left: Any,
        right: Any,
    ) -> bool:
        """
        So sánh mặc định.

        Operator có thể override.
        """

        return self.normalize(left) == self.normalize(right)

    # =====================================================
    # Metadata
    # =====================================================

    @property
    def operator(self) -> str:
        """
        Alias của name.
        """

        return self.name

    def supports(self, operator: str) -> bool:
        """
        Operator có xử lý toán tử này hay không.
        """

        return operator == self.name

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(operator='{self.name}')"
        )

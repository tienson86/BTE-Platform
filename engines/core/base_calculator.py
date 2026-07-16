"""
Base Calculator.

Tất cả Calculator trong BTE Platform đều kế thừa lớp này.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .base_context import BaseContext
from .base_result import BaseResult


class BaseCalculator(ABC):

    def __call__(
        self,
        context: BaseContext
    ) -> BaseResult:

        return self.calculate(context)

    @abstractmethod
    def calculate(
        self,
        context: BaseContext
    ) -> BaseResult:
        """
        Calculator con phải triển khai.
        """
        raise NotImplementedError

    def safe_execute(
        self,
        context: BaseContext
    ) -> BaseResult:

        try:

            return self.calculate(
                context
            )

        except Exception as exc:

            result = BaseResult()

            result.success = False

            result.error = str(exc)

            return result

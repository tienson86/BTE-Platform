"""
Base Engine.

Engine cơ sở của toàn bộ BTE Platform.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod

from .base_context import BaseContext
from .base_result import BaseResult


class BaseEngine(ABC):

    def execute(self, context: BaseContext) -> BaseResult:
        """
        Hàm chuẩn để thực thi Engine.
        """

        start = time.perf_counter()

        result = self.calculate(context)

        result.execution_time = (
            time.perf_counter() - start
        )

        return result

    @abstractmethod
    def calculate(
        self,
        context: BaseContext,
    ) -> BaseResult:
        """
        Engine con phải triển khai.
        """
        raise NotImplementedError

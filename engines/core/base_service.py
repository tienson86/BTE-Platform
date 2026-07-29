"""
Base Service.

Lớp trung gian giữa Engine và Calculator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .base_context import BaseContext
from .base_result import BaseResult


class BaseService(ABC):

    @abstractmethod
    def process(
        self,
        context: BaseContext,
    ) -> BaseResult:
        """
        Xử lý nghiệp vụ.

        Service không nên chứa thuật toán phức tạp,
        mà chỉ điều phối các Calculator.
        """
        raise NotImplementedError

"""
Pipeline Stage.

Định nghĩa lớp cơ sở cho từng giai đoạn trong Pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .context import IntegrationContext
from .result import IntegrationResult


class PipelineStage(ABC):
    """
    Lớp cơ sở của mọi Stage.
    """

    def __init__(self, name: str, engine: Any):
        self.name = name
        self.engine = engine

    @abstractmethod
    def build_context(
        self,
        context: IntegrationContext,
    ) -> Any:
        """
        Chuyển IntegrationContext thành Context
        phù hợp với Engine.
        """
        raise NotImplementedError

    @abstractmethod
    def save_result(
        self,
        context: IntegrationContext,
        result: IntegrationResult,
        engine_result: Any,
    ) -> None:
        """
        Lưu kết quả của Engine vào
        IntegrationContext và IntegrationResult.
        """
        raise NotImplementedError

    def execute(
        self,
        context: IntegrationContext,
        result: IntegrationResult,
    ) -> bool:
        """
        Chạy Stage.
        """

        engine_context = self.build_context(context)

        engine_result = self.engine.execute(
            engine_context
        )

        self.save_result(
            context,
            result,
            engine_result,
        )

        return getattr(engine_result, "success", False)

"""
Base Engine

Lớp cơ sở cho toàn bộ Engine trong BTE Platform.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from time import perf_counter

from .context import EngineContext
from .result import EngineResult


class BaseEngine(ABC):
    """
    Base class của mọi Engine.
    """

    name: str = "BaseEngine"

    version: str = "1.0.0"

    description: str = ""

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self) -> None:

        self.enabled = True

    # =====================================================
    # Public API
    # =====================================================

    def execute(
        self,
        context: EngineContext,
    ) -> EngineResult:
        """
        API chuẩn để Pipeline gọi.

        Không Engine nào được override hàm này.
        Chỉ override run().
        """

        start = perf_counter()

        self.before_run(context)

        result = self.run(context)

        self.after_run(context, result)

        elapsed = (perf_counter() - start) * 1000

        result.metrics.execution_time_ms = round(elapsed, 3)

        result.metrics.finished_at = datetime.utcnow()

        return result

    # =====================================================
    # Before
    # =====================================================

    def before_run(
        self,
        context: EngineContext,
    ) -> None:

        context.add_log(

            "INFO",

            f"{self.name} started",

        )

    # =====================================================
    # Main Logic
    # =====================================================

    @abstractmethod
    def run(
        self,
        context: EngineContext,
    ) -> EngineResult:
        """
        Logic chính của Engine.
        """

    # =====================================================
    # After
    # =====================================================

    def after_run(
        self,
        context: EngineContext,
        result: EngineResult,
    ) -> None:

        context.add_log(

            "INFO",

            f"{self.name} finished ({result.status.value})",

        )

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        context: EngineContext,
    ) -> bool:
        """
        Validate dữ liệu đầu vào.

        Có thể override.
        """

        return True

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:
        """
        Reset trạng thái Engine.
        """

        pass

    # =====================================================
    # Enable
    # =====================================================

    def enable(self) -> None:

        self.enabled = True

    def disable(self) -> None:

        self.enabled = False

    @property
    def is_enabled(self) -> bool:

        return self.enabled

    # =====================================================
    # Information
    # =====================================================

    def info(self) -> dict:

        return {

            "name": self.name,

            "version": self.version,

            "description": self.description,

            "enabled": self.enabled,

        }

    # =====================================================
    # String
    # =====================================================

    def __str__(self) -> str:

        return f"{self.name} ({self.version})"

    def __repr__(self) -> str:

        return self.__str__()

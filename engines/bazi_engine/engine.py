"""
BTE Platform
Bazi Engine

Engine trung tâm của Bazi Engine.
"""

from __future__ import annotations

from typing import Optional

from engines.core.base_engine import BaseEngine

from .calculator import BaziCalculator
from .config import BaziConfig
from .loader import BaziLoader
from .models import (
    BaziContext,
    BaziResult,
)
from .validator import BaziValidator


class BaziEngine(BaseEngine):
    """
    Engine chính của Bazi Engine.
    """

    def __init__(
        self,
        config: Optional[BaziConfig] = None,
    ) -> None:

        super().__init__()

        self.config = config or BaziConfig()

        self.loader = BaziLoader()

        self.validator = BaziValidator()

        self.calculator = BaziCalculator()

        self._initialized = False

    # ======================================================
    # Lifecycle
    # ======================================================

    def initialize(self) -> None:
        """
        Khởi tạo Engine.
        """

        if self._initialized:
            return

        self.loader.load_all()

        self._initialized = True

    def shutdown(self) -> None:
        """
        Giải phóng tài nguyên.
        """

        self.loader.clear_cache()

        self._initialized = False

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: BaziContext,
    ) -> BaziResult:
        """
        Thực thi Bazi Engine.
        """

        if not self._initialized:
            self.initialize()

        self.validator.validate_context(context)

        result = self.calculator.calculate(
            context=context,
            loader=self.loader,
            config=self.config,
        )

        return result

    # ======================================================
    # Status
    # ======================================================

    @property
    def initialized(self) -> bool:
        """
        Trạng thái khởi tạo.
        """

        return self._initialized

    @property
    def version(self) -> str:
        """
        Phiên bản Engine.
        """

        return self.config.engine_version

    @property
    def name(self) -> str:
        """
        Tên Engine.
        """

        return self.config.engine_name

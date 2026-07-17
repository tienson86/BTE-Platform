"""
BTE Platform
Interpretation Service

Lớp Service cung cấp API công khai cho
Interpretation Engine.
"""

from __future__ import annotations

from .calculator import InterpretationCalculator
from .config import DEFAULT_CONFIG, InterpretationConfig
from .loader import InterpretationLoader
from .models import (
    InterpretationContext,
    InterpretationResult,
)
from .validator import InterpretationValidator


class InterpretationService:
    """
    Public Service của Interpretation Engine.
    """

    def __init__(
        self,
        config: InterpretationConfig | None = None,
    ) -> None:

        self.config = config or DEFAULT_CONFIG

        self.loader = InterpretationLoader(
            self.config
        )

        self.validator = (
            InterpretationValidator()
        )

        self.calculator = (
            InterpretationCalculator(
                loader=self.loader,
                validator=self.validator,
            )
        )

    # ======================================================
    # Main
    # ======================================================

    def interpret(
        self,
        context: InterpretationContext,
    ) -> InterpretationResult:
        """
        Thực hiện diễn giải Bát Tự.
        """

        return self.calculator.calculate(
            context
        )

    # ======================================================
    # Reload
    # ======================================================

    def reload(self) -> None:
        """
        Xóa cache và nạp lại dữ liệu.
        """

        self.loader.clear_cache()

        self.loader.load_all()

    # ======================================================
    # Cache
    # ======================================================

    def clear_cache(self) -> None:

        self.loader.clear_cache()

    @property
    def cache(self):

        return self.loader.cache

    # ======================================================
    # Information
    # ======================================================

    @property
    def version(self):

        return self.config.engine_version

    @property
    def name(self):

        return self.config.engine_name

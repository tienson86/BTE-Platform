"""
BTE Platform
Interpretation Service
"""

from __future__ import annotations

from .calculator import InterpretationCalculator
from .config import DEFAULT_CONFIG
from .loader import InterpretationLoader
from .models import (
    InterpretationContext,
    InterpretationResult,
)
from .validator import InterpretationValidator


class InterpretationService:
    """
    API công khai của Interpretation Engine.
    """

    def __init__(self) -> None:

        self.loader = InterpretationLoader(DEFAULT_CONFIG)

        self.validator = InterpretationValidator()

        self.calculator = InterpretationCalculator(
            loader=self.loader,
            validator=self.validator,
        )

    def interpret(
        self,
        context: InterpretationContext,
    ) -> InterpretationResult:

        return self.calculator.calculate(context)

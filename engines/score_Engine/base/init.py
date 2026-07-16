"""
Base classes cho Score Engine.

Các Calculator trong Score Engine đều kế thừa từ BaseCalculator.
"""

from .base_calculator import BaseCalculator
from .calculator_result import CalculatorResult

__all__ = [
    "BaseCalculator",
    "CalculatorResult",
]

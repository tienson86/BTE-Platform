"""Exceptions for the Number Energy Engine (Bát Cực Linh Số / Năng lượng số)."""

from __future__ import annotations


class NumberEnergyEngineError(Exception):
    """Base error for Number Energy Engine."""


class NumberEnergyValidationError(NumberEnergyEngineError):
    """Invalid input for number-energy analysis."""

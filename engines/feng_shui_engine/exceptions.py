"""Feng Shui Engine exceptions."""

from __future__ import annotations


class FengShuiEngineError(Exception):
    """Base error for Feng Shui Engine."""


class FengShuiValidationError(FengShuiEngineError):
    """Invalid input for Cung Phi calculation."""

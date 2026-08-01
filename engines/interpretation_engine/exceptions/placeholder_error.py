"""Placeholder Engine exception."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class PlaceholderEngineError(InterpretationArchitectureError):
    """Raised for placeholder engine infrastructure failures.

    Pack 03 placeholder engine performs no BaZi interpretation.
    """

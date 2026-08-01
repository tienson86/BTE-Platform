"""Context contract-related Interpretation Engine exceptions."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class InterpretationContextError(InterpretationArchitectureError):
    """Raised for interpretation context contract failures."""

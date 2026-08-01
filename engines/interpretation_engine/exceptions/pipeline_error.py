"""Pipeline contract or orchestration-related Interpretation Engine exceptions."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class InterpretationPipelineError(InterpretationArchitectureError):
    """Raised for interpretation pipeline contract or orchestration failures."""

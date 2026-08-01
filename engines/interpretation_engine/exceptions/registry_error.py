"""Registry lookup/resolve-related Interpretation Engine exceptions."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class InterpretationRegistryError(InterpretationArchitectureError):
    """Raised for interpretation registry lookup/resolve failures."""

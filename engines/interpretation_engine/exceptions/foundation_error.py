"""IE-1 Interpretation Foundation exceptions."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class InterpretationFoundationError(InterpretationArchitectureError):
    """Base error for Interpretation Foundation failures."""


class InterpretationContractError(InterpretationFoundationError):
    """Raised when an interpretation foundation contract is invalid."""


class InterpretationDuplicateIdError(InterpretationFoundationError):
    """Raised when a foundation identifier is published twice."""


class InterpretationVersionError(InterpretationFoundationError):
    """Raised when upstream or foundation versions are incompatible."""


class InterpretationContextIntegrityError(InterpretationFoundationError):
    """Raised when Interpretation Context integrity checks fail."""


class InterpretationPackageNotReleasedError(InterpretationFoundationError):
    """Raised when a future Interpretation Package is requested before release."""

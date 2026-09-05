"""Pack 07 foundation exceptions."""

from __future__ import annotations

from engines.core.exceptions import BTEError, EngineError, ValidationError


class DetailedInterpretationError(EngineError):
    """Pack 07 foundation / contract error."""


class DetailedInterpretationContractError(DetailedInterpretationError, ValidationError):
    """Serialized payload does not match the frozen runtime contract."""


class DetailedInterpretationVersionError(DetailedInterpretationContractError):
    """Unknown or incompatible Pack 07 schema / contract version."""


class Pack07Error(DetailedInterpretationError, BTEError):
    """Compatibility alias for Pack 07 errors."""


class DetailedInterpretationValidationError(DetailedInterpretationContractError):
    """Fail-closed Pack 07 contract validation failure."""

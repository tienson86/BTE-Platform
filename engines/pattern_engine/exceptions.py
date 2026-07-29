"""Pattern Engine exceptions."""


class PatternEngineError(Exception):
    """Base error for Pattern Engine failures."""


class PatternCalculationError(PatternEngineError):
    """Raised when pattern recognition fails unexpectedly."""


"""Luck Engine exceptions."""


class LuckEngineError(Exception):
    """Base error for Luck Engine failures."""


class LuckContextError(LuckEngineError):
    """Raised when Luck Engine inputs are unusable."""


class TimelineError(LuckEngineError):
    """Base error for LE-1 timeline foundation failures."""


class TimelineValidationError(TimelineError):
    """Raised when a timeline fails schema, continuity, or contract checks."""


class TimelineRegistryError(TimelineError):
    """Raised when the timeline registry catalog is invalid."""


class TimelineContractError(TimelineError):
    """Raised when the published timeline contract is violated."""


class LuckPackageLoadError(TimelineError):
    """Raised when the Luck Foundation package cannot be admitted."""

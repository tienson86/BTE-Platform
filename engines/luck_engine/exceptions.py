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


class LuckAnalysisError(LuckEngineError):
    """Base error for LE-2 Luck Analysis failures."""


class LuckAnalysisValidationError(LuckAnalysisError):
    """Raised when Luck Analysis validation fails before publication."""


class DuplicateImpactError(LuckAnalysisError):
    """Raised when a stage republishes an existing impact output."""


class ImpactDependencyError(LuckAnalysisError):
    """Raised when impact stage order or inputs are violated."""


class ImpactRegistryError(LuckAnalysisError):
    """Raised when the impact registry catalog is invalid."""

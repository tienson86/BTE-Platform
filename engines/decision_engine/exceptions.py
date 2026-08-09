"""Decision Engine exception hierarchy. Never raised through the public run API."""

from __future__ import annotations


class DecisionEngineError(Exception):
    """Base exception for Decision Engine orchestration."""


class DecisionPipelineError(DecisionEngineError):
    """Raised for Decision Pipeline orchestration failures."""


class PackageLoadError(DecisionPipelineError):
    """Raised when a released decision package cannot be loaded."""


class IncompatiblePackageError(DecisionPipelineError):
    """Raised when a package version or schema is incompatible."""


class DependencyViolationError(DecisionPipelineError):
    """Raised when canonical decision order or inputs are violated."""


class DuplicatePublicationError(DecisionPipelineError):
    """Raised when a stage overwrites a published stage or field."""


class ContractViolationError(DecisionPipelineError):
    """Raised when a package or stage contract is violated before execution."""

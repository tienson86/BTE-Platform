"""Pipeline-related Analysis Engine exceptions."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError


class PipelineError(AnalysisError):
    """Raised for pipeline orchestration or stage execution failures."""


class PackageLoadError(PipelineError):
    """Raised when a released knowledge package cannot be loaded."""


class IncompatiblePackageError(PipelineError):
    """Raised when a package version or schema is incompatible."""


class DependencyViolationError(PipelineError):
    """Raised when canonical dependency order or inputs are violated."""


class DuplicateExecutionError(PipelineError):
    """Raised when a stage attempts to overwrite a published result."""


class ContractViolationError(PipelineError):
    """Raised when a package or stage contract is violated before execution."""

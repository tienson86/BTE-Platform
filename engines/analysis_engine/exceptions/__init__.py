"""Analysis Engine exception hierarchy."""

from __future__ import annotations

from engines.analysis_engine.exceptions.analysis_error import AnalysisError
from engines.analysis_engine.exceptions.cache_error import CacheError
from engines.analysis_engine.exceptions.conflict_error import ConflictError
from engines.analysis_engine.exceptions.context_error import ContextError
from engines.analysis_engine.exceptions.decision_error import DecisionError
from engines.analysis_engine.exceptions.pipeline_error import (
    ContractViolationError,
    DependencyViolationError,
    DuplicateExecutionError,
    IncompatiblePackageError,
    PackageLoadError,
    PipelineError,
)
from engines.analysis_engine.exceptions.registry_error import RegistryError
from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.exceptions.rule_error import RuleError
from engines.analysis_engine.exceptions.runtime_error import AnalysisRuntimeError
from engines.analysis_engine.exceptions.score_error import ScoreError
from engines.analysis_engine.exceptions.validation_error import ValidationError

__all__ = [
    "AnalysisError",
    "AnalysisRuntimeError",
    "CacheError",
    "ConflictError",
    "ContextError",
    "ContractViolationError",
    "DecisionError",
    "DependencyViolationError",
    "DuplicateExecutionError",
    "IncompatiblePackageError",
    "PackageLoadError",
    "PipelineError",
    "RegistryError",
    "ResultError",
    "RuleError",
    "ScoreError",
    "ValidationError",
]

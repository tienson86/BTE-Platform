"""Analysis Runtime framework.

Implements orchestration for Analysis Engine stages without business rules,
interpretation, or report rendering.
"""

from __future__ import annotations

from engines.analysis_engine.runtime.analysis_runtime import AnalysisRuntime
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.cache_manager import CacheManager
from engines.analysis_engine.runtime.dependency_resolver import DependencyResolver
from engines.analysis_engine.runtime.error_handler import ErrorHandler
from engines.analysis_engine.runtime.exceptions import (
    AbortedError,
    AdmissionError,
    AnalysisRuntimeError,
    CacheError,
    CompatibilityError,
    IntegrityError,
    KnowledgeError,
    PrerequisiteError,
    RegistrationError,
    StageExecutionError,
    StateError,
    ValidationError,
)
from engines.analysis_engine.runtime.execution_manager import ExecutionManager
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    ConfidenceEvaluation,
    DiagnosticInfo,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
    RuleEvidence,
    StageMetrics,
    StageResult,
    TraceSpan,
)
from engines.analysis_engine.runtime.module_executor import ModuleExecutor
from engines.analysis_engine.runtime.pipeline import RuntimePipeline
from engines.analysis_engine.runtime.protocols import AnalysisModule, ModuleDescriptor
from engines.analysis_engine.runtime.validation_manager import (
    ValidationManager,
    ValidationReport,
)

__all__ = [
    "AbortedError",
    "AdmissionError",
    "AnalysisContext",
    "AnalysisModule",
    "AnalysisResult",
    "AnalysisRuntime",
    "AnalysisRuntimeError",
    "BaseAnalysisModule",
    "CacheError",
    "CacheManager",
    "CompatibilityError",
    "ConfidenceEvaluation",
    "DependencyResolver",
    "DiagnosticInfo",
    "ErrorHandler",
    "ExecutionManager",
    "ExecutionMetadata",
    "ExecutionTrace",
    "IntegrityError",
    "KnowledgeError",
    "ModuleDescriptor",
    "ModuleExecutor",
    "PerformanceMetrics",
    "PrerequisiteError",
    "RegistrationError",
    "RuleEvidence",
    "RuntimePipeline",
    "StageExecutionError",
    "StageMetrics",
    "StageResult",
    "StateError",
    "TraceSpan",
    "ValidationError",
    "ValidationManager",
    "ValidationReport",
]

__version__ = "1.0.0"

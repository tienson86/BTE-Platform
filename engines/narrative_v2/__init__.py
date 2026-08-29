"""Narrative V2 — shadow-mode runtime skeleton (N-IMP-01).

This package is independent of Pack05 (`engines.narrative_engine`).
It does not generate customer narrative and does not connect Portal.
"""

from __future__ import annotations

from engines.narrative_v2.runtime import (
    SHADOW_MODE,
    CANONICAL_STAGES,
    BuilderError,
    NarrativeRuntime,
    NarrativeRuntimeContext,
    NarrativeRuntimeResult,
    PipelineError,
    PipelineTrace,
    RuntimeMetrics,
    RuntimeRegistry,
    RuntimeState,
    RuntimeValidator,
    ValidationError,
)
from engines.narrative_v2.runtime.runtime_errors import RuntimeError

__all__ = [
    "SHADOW_MODE",
    "CANONICAL_STAGES",
    "BuilderError",
    "NarrativeRuntime",
    "NarrativeRuntimeContext",
    "NarrativeRuntimeResult",
    "PipelineError",
    "PipelineTrace",
    "RuntimeError",
    "RuntimeMetrics",
    "RuntimeRegistry",
    "RuntimeState",
    "RuntimeValidator",
    "ValidationError",
]

__version__ = "0.1.0-skeleton"

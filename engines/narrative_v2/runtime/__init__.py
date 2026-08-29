"""Narrative V2 runtime skeleton public surface."""

from __future__ import annotations

from engines.narrative_v2.runtime.narrative_runtime import (
    NARRATIVE_VERSION,
    RUNTIME_VERSION,
    SHADOW_MODE,
    NarrativeRuntime,
)
from engines.narrative_v2.runtime.runtime_context import (
    NarrativeRuntimeContext,
    PipelineTrace,
    PipelineTraceEntry,
)
from engines.narrative_v2.runtime.runtime_errors import (
    BuilderError,
    PipelineError,
    ValidationError,
)
from engines.narrative_v2.runtime.runtime_errors import RuntimeError
from engines.narrative_v2.runtime.runtime_events import (
    ActionFinished,
    ActionStarted,
    CommercialFinished,
    CommercialStarted,
    EvidenceFinished,
    EvidenceStarted,
    InterpretationFinished,
    InterpretationStarted,
    KnowledgeFinished,
    KnowledgeStarted,
    NarrativeStarted,
    PublishFinished,
    PublishStarted,
    ReasoningFinished,
    ReasoningStarted,
    RewriteFinished,
    RewriteStarted,
    RuntimeEvent,
    RuntimeFailed,
    SummaryFinished,
    SummaryStarted,
    ValidationFinished,
    ValidationStarted,
)
from engines.narrative_v2.runtime.runtime_metrics import RuntimeMetrics
from engines.narrative_v2.runtime.runtime_pipeline import (
    BUILDER_STAGES,
    CANONICAL_STAGES,
    PRE_VALIDATE_STAGES,
    RuntimePipeline,
    StageResult,
)
from engines.narrative_v2.runtime.runtime_registry import BuilderRegistration, RuntimeRegistry
from engines.narrative_v2.runtime.runtime_result import NarrativeRuntimeResult
from engines.narrative_v2.runtime.runtime_state import (
    ALLOWED_TRANSITIONS,
    RuntimeState,
    can_transition,
    transition,
)
from engines.narrative_v2.runtime.runtime_validator import RuntimeValidator, ValidationOutcome

__all__ = [
    "ALLOWED_TRANSITIONS",
    "BUILDER_STAGES",
    "CANONICAL_STAGES",
    "NARRATIVE_VERSION",
    "PRE_VALIDATE_STAGES",
    "RUNTIME_VERSION",
    "SHADOW_MODE",
    "ActionFinished",
    "ActionStarted",
    "BuilderError",
    "BuilderRegistration",
    "CommercialFinished",
    "CommercialStarted",
    "EvidenceFinished",
    "EvidenceStarted",
    "InterpretationFinished",
    "InterpretationStarted",
    "KnowledgeFinished",
    "KnowledgeStarted",
    "NarrativeRuntime",
    "NarrativeRuntimeContext",
    "NarrativeRuntimeResult",
    "NarrativeStarted",
    "PipelineError",
    "PipelineTrace",
    "PipelineTraceEntry",
    "PublishFinished",
    "PublishStarted",
    "ReasoningFinished",
    "ReasoningStarted",
    "RewriteFinished",
    "RewriteStarted",
    "RuntimeError",
    "RuntimeEvent",
    "RuntimeFailed",
    "RuntimeMetrics",
    "RuntimePipeline",
    "RuntimeRegistry",
    "RuntimeState",
    "RuntimeValidator",
    "StageResult",
    "SummaryFinished",
    "SummaryStarted",
    "ValidationError",
    "ValidationFinished",
    "ValidationOutcome",
    "ValidationStarted",
    "can_transition",
    "transition",
]

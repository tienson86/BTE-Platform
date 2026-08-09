"""Interpretation pipeline architecture and runtime package.

Re-exports legacy ``InterpretationPipeline`` for backward compatibility.
"""

from __future__ import annotations

from engines.interpretation_engine.legacy_runtime.pipeline import InterpretationPipeline
from engines.interpretation_engine.pipeline.execution_context import (
    ExecutionContext,
    PipelineContext,
)
from engines.interpretation_engine.pipeline.execution_policy import ExecutionPolicy
from engines.interpretation_engine.pipeline.execution_result import (
    ExecutionResult,
    StageOutcome,
)
from engines.interpretation_engine.pipeline.execution_state import (
    ExecutionState,
    ExecutionStatus,
)
from engines.interpretation_engine.pipeline.hooks import (
    ExecutionHooks,
    NoOpExecutionHooks,
)
from engines.interpretation_engine.pipeline.canonical_interpretation_pipeline import (
    CanonicalInterpretationPipeline,
)
from engines.interpretation_engine.pipeline.pipeline import Pipeline
from engines.interpretation_engine.pipeline.pipeline_executor import PipelineExecutor
from engines.interpretation_engine.pipeline.pipeline_interface import (
    InterpretationPipelineInterface,
)
from engines.interpretation_engine.pipeline.pipeline_result import InterpretationPipelineResult
from engines.interpretation_engine.pipeline.stage_base import StageBase
from engines.interpretation_engine.pipeline.stage_executor import StageExecutor
from engines.interpretation_engine.pipeline.stage_interface import InterpretationStageInterface

__all__ = [
    "CanonicalInterpretationPipeline",
    "ExecutionContext",
    "ExecutionHooks",
    "ExecutionPolicy",
    "ExecutionResult",
    "ExecutionState",
    "ExecutionStatus",
    "InterpretationPipeline",
    "InterpretationPipelineInterface",
    "InterpretationPipelineResult",
    "InterpretationStageInterface",
    "NoOpExecutionHooks",
    "Pipeline",
    "PipelineContext",
    "PipelineExecutor",
    "StageBase",
    "StageExecutor",
    "StageOutcome",
]

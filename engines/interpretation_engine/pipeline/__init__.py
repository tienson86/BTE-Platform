"""Interpretation pipeline architecture package.

Re-exports legacy ``InterpretationPipeline`` for backward compatibility.
"""

from __future__ import annotations

from engines.interpretation_engine.legacy_runtime.pipeline import InterpretationPipeline
from engines.interpretation_engine.pipeline.pipeline_interface import (
    InterpretationPipelineInterface,
)
from engines.interpretation_engine.pipeline.pipeline_result import InterpretationPipelineResult
from engines.interpretation_engine.pipeline.stage_interface import InterpretationStageInterface

__all__ = [
    "InterpretationPipeline",
    "InterpretationPipelineInterface",
    "InterpretationPipelineResult",
    "InterpretationStageInterface",
]

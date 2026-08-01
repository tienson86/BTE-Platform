"""Pipeline stage finalizer interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import (
    PipelineResult,
    StageOutcome,
)
from engines.analysis_engine.pipeline.stage_base import StageBase


class StageFinalizer:
    """Public interface for finalizing stage and pipeline outcomes."""

    def finalize_stage(
        self,
        stage: StageBase,
        context: PipelineContext,
        outcome: StageOutcome,
    ) -> None:
        """Finalize a single stage outcome."""
        raise NotImplementedError

    def finalize_pipeline(
        self,
        context: PipelineContext,
        outcomes: tuple[StageOutcome, ...],
    ) -> PipelineResult:
        """Finalize the full pipeline into a public result contract."""
        raise NotImplementedError

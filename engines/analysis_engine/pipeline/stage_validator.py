"""Pipeline stage validator interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.stage_base import StageBase


class StageValidator:
    """Public interface for validating stage contracts and context readiness."""

    def validate_stage(self, stage: StageBase) -> bool:
        """Validate a stage contract."""
        raise NotImplementedError

    def validate_context(self, stage: StageBase, context: PipelineContext) -> bool:
        """Validate that a context is ready for a stage."""
        raise NotImplementedError

    def validate_dependencies(
        self,
        stage: StageBase,
        available_stage_ids: tuple[str, ...],
    ) -> bool:
        """Validate that stage dependencies are satisfied."""
        raise NotImplementedError

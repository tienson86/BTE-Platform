"""Analysis Engine pipeline validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.stage_base import StageBase
from engines.analysis_engine.validators.validator_base import ValidatorBase


class PipelineValidator(ValidatorBase):
    """Public interface for pipeline validation.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the pipeline validator skeleton."""
        super().__init__(validator_id="pipeline_validator")

    def validate(self, payload: Any) -> bool:
        """Validate a pipeline-related payload."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return pipeline validation errors."""
        raise NotImplementedError

    def validate_stage(self, stage: StageBase) -> bool:
        """Validate a pipeline stage contract."""
        raise NotImplementedError

    def validate_context(self, context: PipelineContext) -> bool:
        """Validate a pipeline context contract."""
        raise NotImplementedError

    def validate_stage_order(self, stage_ids: tuple[str, ...]) -> bool:
        """Validate an ordered stage identifier sequence."""
        raise NotImplementedError

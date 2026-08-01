"""Analysis Engine result validator interface."""

from __future__ import annotations

from typing import Any

from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.pipeline.pipeline_result import PipelineResult
from engines.analysis_engine.validators.validator_base import ValidatorBase


class ResultValidator(ValidatorBase):
    """Public interface for analysis and pipeline result validation.

    No validation logic.
    """

    def __init__(self) -> None:
        """Initialize the result validator skeleton."""
        super().__init__(validator_id="result_validator")

    def validate(self, payload: Any) -> bool:
        """Validate a result payload."""
        raise NotImplementedError

    def errors(self) -> tuple[str, ...]:
        """Return result validation errors."""
        raise NotImplementedError

    def validate_analysis_result(self, result: AnalysisResult) -> bool:
        """Validate an analysis result contract."""
        raise NotImplementedError

    def validate_pipeline_result(self, result: PipelineResult) -> bool:
        """Validate a pipeline result contract."""
        raise NotImplementedError

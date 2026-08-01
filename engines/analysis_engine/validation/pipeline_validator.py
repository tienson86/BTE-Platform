"""Pipeline validator interface.

No validation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.models.pipeline_state import PipelineState
from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.stage_base import StageBase
from engines.analysis_engine.validation.validator_contract import ValidatorContract


class PipelineValidator(ValidatorContract, ABC):
    """Public interface for validating pipeline contracts and state."""

    @abstractmethod
    def validate_pipeline_context(self, context: PipelineContext) -> bool:
        """Validate a pipeline context instance."""

    @abstractmethod
    def validate_stage(self, stage: StageBase) -> bool:
        """Validate a pipeline stage contract."""

    @abstractmethod
    def validate_pipeline_state(self, state: PipelineState) -> bool:
        """Validate a pipeline state instance."""

    @abstractmethod
    def validate_stage_order(self, stage_ids: tuple[str, ...]) -> bool:
        """Validate an ordered stage identifier sequence."""

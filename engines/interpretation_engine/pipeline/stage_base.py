"""Interpretation pipeline stage base for orchestration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engines.interpretation_engine.pipeline.execution_context import PipelineContext
    from engines.interpretation_engine.pipeline.execution_result import StageOutcome


class StageBase(ABC):
    """Abstract stage contract for interpretation pipeline orchestration.

    Concrete interpreters inherit this contract.
    Does not contain BaZi or sentence/template logic.
    """

    stage_id: str
    name: str
    version: str
    order: int

    def __init__(
        self,
        *,
        stage_id: str,
        name: str,
        version: str = "0.0.0",
        order: int = 0,
    ) -> None:
        """Initialize stage identity fields."""
        self.stage_id = stage_id
        self.name = name
        self.version = version
        self.order = order

    @abstractmethod
    def prepare(self, context: PipelineContext) -> None:
        """Prepare the stage before execution."""

    @abstractmethod
    def execute(self, context: PipelineContext) -> StageOutcome:
        """Execute the stage and return a stage outcome."""

    @abstractmethod
    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """Finalize the stage after execution."""

    def dependencies(self) -> tuple[str, ...]:
        """Return stage dependency identifiers."""
        return ()

    def validate(self, context: PipelineContext) -> bool:
        """Validate stage readiness for the provided context."""
        return bool(context.context_id and context.pipeline_id)

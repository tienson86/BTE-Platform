"""Pipeline stage base interface skeleton."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome


class StageBase(ABC):
    """Abstract public interface for a pipeline stage.

    Concrete analyzers inherit this contract.
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

    @abstractmethod
    def dependencies(self) -> tuple[str, ...]:
        """Return stage dependency identifiers."""

"""Pipeline orchestration interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import PipelineResult


class Pipeline:
    """Public orchestration interface for the Analysis Engine pipeline.

    Defines the pipeline lifecycle boundary only.
    """

    def __init__(self, pipeline_id: str, name: str = "") -> None:
        """Create a pipeline skeleton instance."""
        self.pipeline_id = pipeline_id
        self.name = name

    def run(self, context: PipelineContext) -> PipelineResult:
        """Execute the pipeline against the provided context."""
        raise NotImplementedError

    def validate(self, context: PipelineContext) -> bool:
        """Validate pipeline readiness for the provided context."""
        raise NotImplementedError

    def describe(self) -> dict[str, str]:
        """Return a public description of the pipeline identity."""
        raise NotImplementedError

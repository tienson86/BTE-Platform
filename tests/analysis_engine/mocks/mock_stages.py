"""Mock analyzers/stages for infrastructure tests.

No real BaZi rules or scoring algorithms.
"""

from __future__ import annotations

from engines.analysis_engine.pipeline.pipeline_context import PipelineContext
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome
from engines.analysis_engine.pipeline.stage_base import StageBase


class MockSuccessStage(StageBase):
    """Mock stage that always succeeds with an opaque payload."""

    def __init__(
        self,
        *,
        stage_id: str = "mock_success",
        name: str = "Mock Success",
        order: int = 1,
        payload: dict | None = None,
    ) -> None:
        """Initialize a successful mock stage."""
        super().__init__(stage_id=stage_id, name=name, version="0.0.0-test", order=order)
        self._payload = dict(payload or {"mock": True})
        self.prepared = False
        self.finalized = False

    def prepare(self, context: PipelineContext) -> None:
        """Mark prepare as called."""
        self.prepared = True

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Return a successful mock outcome."""
        return StageOutcome(
            stage_id=self.stage_id,
            success=True,
            payload=dict(self._payload),
            messages=("mock_success",),
        )

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """Mark finalize as called."""
        self.finalized = True

    def dependencies(self) -> tuple[str, ...]:
        """Return no dependencies."""
        return ()


class MockFailStage(StageBase):
    """Mock stage that returns a failed outcome."""

    def __init__(
        self,
        *,
        stage_id: str = "mock_fail",
        name: str = "Mock Fail",
        order: int = 1,
    ) -> None:
        """Initialize a failing mock stage."""
        super().__init__(stage_id=stage_id, name=name, version="0.0.0-test", order=order)

    def prepare(self, context: PipelineContext) -> None:
        """No-op prepare."""
        return None

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Return a failed mock outcome."""
        return StageOutcome(
            stage_id=self.stage_id,
            success=False,
            payload={},
            messages=("mock_failure",),
        )

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """No-op finalize."""
        return None

    def dependencies(self) -> tuple[str, ...]:
        """Return no dependencies."""
        return ()


class MockErrorStage(StageBase):
    """Mock stage that raises during execute."""

    def __init__(
        self,
        *,
        stage_id: str = "mock_error",
        name: str = "Mock Error",
        order: int = 1,
    ) -> None:
        """Initialize an error-raising mock stage."""
        super().__init__(stage_id=stage_id, name=name, version="0.0.0-test", order=order)

    def prepare(self, context: PipelineContext) -> None:
        """No-op prepare."""
        return None

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Raise a runtime error for orchestration handling."""
        raise RuntimeError("mock_stage_boom")

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """No-op finalize."""
        return None

    def dependencies(self) -> tuple[str, ...]:
        """Return no dependencies."""
        return ()

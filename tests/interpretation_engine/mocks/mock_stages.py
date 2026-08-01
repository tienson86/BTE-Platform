"""Mock stages for Interpretation Engine pipeline infrastructure tests."""

from __future__ import annotations

from engines.interpretation_engine.pipeline.execution_context import PipelineContext
from engines.interpretation_engine.pipeline.execution_result import StageOutcome
from engines.interpretation_engine.pipeline.stage_base import StageBase


class MockSuccessStage(StageBase):
    """Mock stage that always succeeds with an opaque payload."""

    def __init__(
        self,
        *,
        stage_id: str = "mock_success",
        name: str = "Mock Success",
        order: int = 1,
        payload: dict | None = None,
        wrong_stage_id: bool = False,
    ) -> None:
        """Initialize a successful mock stage."""
        super().__init__(stage_id=stage_id, name=name, version="0.0.0-test", order=order)
        self._payload = dict(payload or {"mock": True})
        self._wrong_stage_id = wrong_stage_id
        self.prepared = False
        self.finalized = False

    def prepare(self, context: PipelineContext) -> None:
        """Mark prepare as called."""
        self.prepared = True

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Return a successful mock outcome."""
        return StageOutcome(
            stage_id="other_id" if self._wrong_stage_id else self.stage_id,
            success=True,
            payload=dict(self._payload),
            messages=("mock_success",),
        )

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """Mark finalize as called."""
        self.finalized = True


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


class MockErrorStage(StageBase):
    """Mock stage that raises during execute."""

    def __init__(
        self,
        *,
        stage_id: str = "mock_error",
        name: str = "Mock Error",
        order: int = 1,
        raise_pipeline_error: bool = False,
    ) -> None:
        """Initialize an error-raising mock stage."""
        super().__init__(stage_id=stage_id, name=name, version="0.0.0-test", order=order)
        self._raise_pipeline_error = raise_pipeline_error

    def prepare(self, context: PipelineContext) -> None:
        """No-op prepare."""
        return None

    def execute(self, context: PipelineContext) -> StageOutcome:
        """Raise for orchestration handling."""
        if self._raise_pipeline_error:
            from engines.interpretation_engine.exceptions.pipeline_error import (
                InterpretationPipelineError,
            )

            raise InterpretationPipelineError("mock_pipeline_error")
        raise RuntimeError("mock_stage_boom")

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        """No-op finalize."""
        return None

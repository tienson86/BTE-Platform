"""Interpretation pipeline execution hooks for orchestration."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engines.interpretation_engine.pipeline.execution_context import ExecutionContext
from engines.interpretation_engine.pipeline.execution_result import (
    ExecutionResult,
    StageOutcome,
)
from engines.interpretation_engine.pipeline.execution_state import ExecutionState
from engines.interpretation_engine.pipeline.stage_base import StageBase


class ExecutionHooks(ABC):
    """Public hook interface for interpretation pipeline orchestration lifecycle."""

    @abstractmethod
    def before_pipeline(
        self,
        context: ExecutionContext,
        state: ExecutionState,
    ) -> None:
        """Invoked before pipeline orchestration starts."""

    @abstractmethod
    def after_pipeline(
        self,
        context: ExecutionContext,
        state: ExecutionState,
        result: ExecutionResult,
    ) -> None:
        """Invoked after pipeline orchestration completes."""

    @abstractmethod
    def before_stage(
        self,
        stage: StageBase,
        context: ExecutionContext,
        state: ExecutionState,
    ) -> None:
        """Invoked before a stage is orchestrated."""

    @abstractmethod
    def after_stage(
        self,
        stage: StageBase,
        context: ExecutionContext,
        state: ExecutionState,
        outcome: StageOutcome,
    ) -> None:
        """Invoked after a stage orchestration attempt completes."""

    @abstractmethod
    def on_error(
        self,
        stage: StageBase | None,
        context: ExecutionContext,
        state: ExecutionState,
        error: BaseException,
    ) -> None:
        """Invoked when orchestration encounters an error."""


class NoOpExecutionHooks(ExecutionHooks):
    """Default no-op hooks for interpretation pipeline orchestration."""

    def before_pipeline(
        self,
        context: ExecutionContext,
        state: ExecutionState,
    ) -> None:
        """No-op before pipeline."""
        return None

    def after_pipeline(
        self,
        context: ExecutionContext,
        state: ExecutionState,
        result: ExecutionResult,
    ) -> None:
        """No-op after pipeline."""
        return None

    def before_stage(
        self,
        stage: StageBase,
        context: ExecutionContext,
        state: ExecutionState,
    ) -> None:
        """No-op before stage."""
        return None

    def after_stage(
        self,
        stage: StageBase,
        context: ExecutionContext,
        state: ExecutionState,
        outcome: StageOutcome,
    ) -> None:
        """No-op after stage."""
        return None

    def on_error(
        self,
        stage: StageBase | None,
        context: ExecutionContext,
        state: ExecutionState,
        error: BaseException,
    ) -> None:
        """No-op on error."""
        return None

"""Narrative V2 runtime pipeline.

Evidence, reasoning, knowledge, and rewrite are implemented. Later builder stages remain placeholders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from engines.narrative_v2.runtime.runtime_errors import PipelineError, ValidationError
from engines.narrative_v2.runtime.runtime_events import (
    NarrativeStarted,
    STAGE_EVENTS,
    now,
)
from engines.narrative_v2.runtime.runtime_state import RuntimeState, transition

if TYPE_CHECKING:
    from engines.narrative_v2.runtime.narrative_runtime import NarrativeRuntime

CANONICAL_STAGES: tuple[str, ...] = (
    "initialize",
    "build_evidence",
    "build_reasoning",
    "resolve_knowledge",
    "commercial_rewrite",
    "build_summary",
    "build_interpretation",
    "build_action",
    "build_commercial",
    "validate",
    "publish",
)

PRE_VALIDATE_STAGES: tuple[str, ...] = CANONICAL_STAGES[:-2]
BUILDER_STAGES: tuple[str, ...] = CANONICAL_STAGES[1:-2]


@dataclass(slots=True)
class StageResult:
    """Stage output. Evidence through rewrite are implemented; later builders are placeholders."""

    stage: str
    payload: object = field(default=NotImplemented)
    status: str = "not_implemented"


class RuntimePipeline:
    """Sequential pipeline. Evidence through rewrite are implemented; later builders are placeholders."""

    def __init__(self, runtime: "NarrativeRuntime") -> None:
        self._runtime = runtime

    @property
    def stages(self) -> tuple[str, ...]:
        """Canonical stage order."""
        return CANONICAL_STAGES

    def initialize(self) -> StageResult:
        """Stage: initialize."""
        return self.execute_stage("initialize")

    def build_evidence(self) -> StageResult:
        """Stage: evidence. Extracts published CanonicalAnalysis facts."""
        return self.execute_stage("build_evidence")

    def build_reasoning(self) -> StageResult:
        """Stage: reasoning. Connects published Evidence."""
        return self.execute_stage("build_reasoning")

    def resolve_knowledge(self) -> StageResult:
        """Stage: knowledge. Resolves approved knowledge for reasoning semantics."""
        return self.execute_stage("resolve_knowledge")

    def commercial_rewrite(self) -> StageResult:
        """Stage: commercial rewrite. Customer-language units from approved meaning."""
        return self.execute_stage("commercial_rewrite")

    def build_summary(self) -> StageResult:
        """Stage: summary. Not implemented."""
        return self.execute_stage("build_summary")

    def build_interpretation(self) -> StageResult:
        """Stage: interpretation. Not implemented."""
        return self.execute_stage("build_interpretation")

    def build_action(self) -> StageResult:
        """Stage: action. Not implemented."""
        return self.execute_stage("build_action")

    def build_commercial(self) -> StageResult:
        """Stage: commercial. Not implemented."""
        return self.execute_stage("build_commercial")

    def validate(self) -> StageResult:
        """Stage: validate. Ordering check only."""
        return self.execute_stage("validate")

    def publish(self) -> StageResult:
        """Stage: publish. Freeze skeleton result."""
        return self.execute_stage("publish")

    def execute_stage(self, stage: str) -> StageResult:
        """Execute one canonical stage in order."""
        self._assert_next_stage(stage)
        started = now()
        self._on_stage_start(stage, started)
        status = "failed"
        try:
            result = self._run_stage_body(stage)
            status = result.status
            return result
        finally:
            self._on_stage_finish(stage, started, now(), status=status)

    def _assert_next_stage(self, stage: str) -> None:
        executed = self._runtime.executed_stages
        if len(executed) >= len(CANONICAL_STAGES):
            raise PipelineError("Pipeline already complete")
        expected = CANONICAL_STAGES[len(executed)]
        if stage != expected:
            raise PipelineError(
                f"Invalid pipeline order: expected {expected}, got {stage}"
            )

    def _on_stage_start(self, stage: str, started: float) -> None:
        context = self._runtime.require_context()
        context.trace.start(stage, started)
        self._apply_start_state(stage)
        self._emit_start(stage, started)

    def _on_stage_finish(
        self,
        stage: str,
        started: float,
        finished: float,
        *,
        status: str,
    ) -> None:
        context = self._runtime.require_context()
        context.trace.entries[-1].complete(finished=finished, status=status)
        self._runtime.metrics.record_stage(stage, finished - started)
        self._runtime.record_stage(stage)
        self._emit_finish(stage, finished)
        if stage == "publish" and status != "failed":
            context.runtime_state = transition(
                context.runtime_state,
                RuntimeState.PUBLISHED,
            )

    def _apply_start_state(self, stage: str) -> None:
        context = self._runtime.require_context()
        target = _start_state_for(stage)
        context.runtime_state = transition(context.runtime_state, target)

    def _emit_start(self, stage: str, timestamp: float) -> None:
        if stage == "initialize":
            self._runtime.emit(NarrativeStarted(timestamp=timestamp))
            return
        started_cls, _ = STAGE_EVENTS[stage]
        self._runtime.emit(started_cls(timestamp=timestamp, stage=stage))

    def _emit_finish(self, stage: str, timestamp: float) -> None:
        if stage == "initialize":
            return
        _, finished_cls = STAGE_EVENTS[stage]
        self._runtime.emit(finished_cls(timestamp=timestamp, stage=stage))

    def _run_stage_body(self, stage: str) -> StageResult:
        if stage == "build_evidence":
            return self._run_evidence()
        if stage == "build_reasoning":
            return self._run_reasoning()
        if stage == "resolve_knowledge":
            return self._run_knowledge()
        if stage == "commercial_rewrite":
            return self._run_rewrite()
        if stage == "validate":
            return self._run_validate()
        if stage == "publish":
            return StageResult(stage=stage, payload=None, status="placeholder")
        return StageResult(stage=stage)

    def _run_evidence(self) -> StageResult:
        from engines.narrative_v2.evidence import EvidenceBuilder, EvidenceError
        from engines.narrative_v2.runtime.runtime_errors import BuilderError

        context = self._runtime.require_context()
        try:
            evidence = EvidenceBuilder().build(context.canonical_analysis)
        except EvidenceError as exc:
            raise BuilderError(str(exc)) from exc
        context.evidence = evidence
        return StageResult(
            stage="build_evidence",
            payload=evidence,
            status="implemented",
        )

    def _run_reasoning(self) -> StageResult:
        from engines.narrative_v2.reasoning import ReasoningBuilder, ReasoningError
        from engines.narrative_v2.runtime.runtime_errors import BuilderError

        context = self._runtime.require_context()
        try:
            reasoning = ReasoningBuilder().build(context.evidence)
        except ReasoningError as exc:
            raise BuilderError(str(exc)) from exc
        context.reasoning = reasoning
        return StageResult(
            stage="build_reasoning",
            payload=reasoning,
            status="implemented",
        )

    def _run_knowledge(self) -> StageResult:
        from engines.narrative_v2.knowledge import KnowledgeError, KnowledgeResolver
        from engines.narrative_v2.runtime.runtime_errors import BuilderError

        context = self._runtime.require_context()
        try:
            knowledge = KnowledgeResolver().resolve(context.reasoning, context.evidence)
        except KnowledgeError as exc:
            raise BuilderError(str(exc)) from exc
        context.knowledge = knowledge
        return StageResult(
            stage="resolve_knowledge",
            payload=knowledge,
            status="implemented",
        )

    def _run_rewrite(self) -> StageResult:
        from engines.narrative_v2.rewrite import RewriteEngine, RewriteError
        from engines.narrative_v2.runtime.runtime_errors import BuilderError

        context = self._runtime.require_context()
        try:
            rewrite = RewriteEngine().rewrite(
                context.knowledge,
                context.reasoning,
                context.evidence,
            )
        except RewriteError as exc:
            raise BuilderError(str(exc)) from exc
        context.rewrite = rewrite
        return StageResult(
            stage="commercial_rewrite",
            payload=rewrite,
            status="implemented",
        )

    def _run_validate(self) -> StageResult:
        outcome = self._runtime.validator.validate(
            self._runtime.executed_stages,
            expected=PRE_VALIDATE_STAGES,
        )
        if not outcome.passed:
            raise ValidationError(outcome.reason)
        return StageResult(
            stage="validate",
            payload=outcome,
            status="pass",
        )


def _start_state_for(stage: str) -> RuntimeState:
    if stage == "initialize":
        return RuntimeState.INITIALIZED
    if stage == "validate":
        return RuntimeState.VALIDATING
    if stage == "publish":
        return RuntimeState.VALIDATING
    return RuntimeState.RUNNING

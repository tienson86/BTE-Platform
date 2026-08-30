"""Tests for Narrative V2 runtime skeleton (N-IMP-01).

No builder tests. No narrative generation tests.
"""

from __future__ import annotations

import pytest

from engines.narrative_v2.runtime import (
    BUILDER_STAGES,
    CANONICAL_STAGES,
    PRE_VALIDATE_STAGES,
    BuilderError,
    NarrativeRuntime,
    NarrativeRuntimeContext,
    NarrativeRuntimeResult,
    PipelineError,
    RuntimeRegistry,
    RuntimeState,
    RuntimeValidator,
    StageResult,
    can_transition,
    transition,
)
from engines.narrative_v2.runtime.runtime_state import ALLOWED_TRANSITIONS


def _opaque_analysis() -> dict[str, str]:
    return {"source": "canonical_analysis_placeholder"}


# --- Runtime initialization ---


def test_runtime_starts_not_started() -> None:
    runtime = NarrativeRuntime()
    assert runtime.context is None
    assert runtime.executed_stages == ()


def test_initialize_creates_context_without_interpreting_analysis() -> None:
    analysis = _opaque_analysis()
    runtime = NarrativeRuntime()
    context = runtime.initialize(analysis)
    assert isinstance(context, NarrativeRuntimeContext)
    assert context.canonical_analysis is analysis
    assert context.runtime_state is RuntimeState.INITIALIZED
    assert runtime.executed_stages == ("initialize",)
    assert context.metadata["generates_narrative"] is False


def test_initialize_twice_raises() -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(_opaque_analysis())
    with pytest.raises(PipelineError):
        runtime.initialize(_opaque_analysis())


# --- Pipeline ordering ---


def test_full_run_executes_canonical_order() -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(_opaque_analysis())
    assert runtime.executed_stages == CANONICAL_STAGES
    assert result.pipeline_trace.stages() == CANONICAL_STAGES
    assert result.status == RuntimeState.PUBLISHED.value


def test_stage_methods_follow_canonical_order() -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(_opaque_analysis())
    for stage in CANONICAL_STAGES[1:]:
        output = runtime.pipeline.execute_stage(stage)
        assert isinstance(output, StageResult)
        assert output.stage == stage
    assert runtime.executed_stages == CANONICAL_STAGES


def test_skipping_a_stage_raises_pipeline_error() -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(_opaque_analysis())
    with pytest.raises(PipelineError, match="Invalid pipeline order"):
        runtime.pipeline.build_summary()


def test_builder_stages_return_not_implemented_placeholder() -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(_opaque_analysis())
    later_stages = tuple(
        stage for stage in BUILDER_STAGES if stage != "build_evidence"
    )
    runtime.pipeline.build_evidence()
    for stage in later_stages:
        output = runtime.pipeline.execute_stage(stage)
        assert output.payload is NotImplemented
        assert output.status == "not_implemented"


# --- State transitions ---


def test_happy_path_state_machine() -> None:
    runtime = NarrativeRuntime()
    assert can_transition(RuntimeState.NOT_STARTED, RuntimeState.INITIALIZED)
    context = runtime.initialize(_opaque_analysis())
    assert context.runtime_state is RuntimeState.INITIALIZED
    runtime.pipeline.build_evidence()
    assert context.runtime_state is RuntimeState.RUNNING
    for stage in CANONICAL_STAGES[2:-2]:
        runtime.pipeline.execute_stage(stage)
    assert context.runtime_state is RuntimeState.RUNNING
    runtime.pipeline.validate()
    assert context.runtime_state is RuntimeState.VALIDATING
    runtime.pipeline.publish()
    assert context.runtime_state is RuntimeState.PUBLISHED


def test_illegal_transition_raises() -> None:
    with pytest.raises(PipelineError, match="Illegal state transition"):
        transition(RuntimeState.NOT_STARTED, RuntimeState.RUNNING)
    with pytest.raises(PipelineError, match="Illegal state transition"):
        transition(RuntimeState.PUBLISHED, RuntimeState.RUNNING)
    with pytest.raises(PipelineError, match="Illegal state transition"):
        transition(RuntimeState.FAILED, RuntimeState.INITIALIZED)


def test_failed_is_reachable_from_active_states() -> None:
    for state in (
        RuntimeState.NOT_STARTED,
        RuntimeState.INITIALIZED,
        RuntimeState.RUNNING,
        RuntimeState.VALIDATING,
    ):
        assert RuntimeState.FAILED in ALLOWED_TRANSITIONS[state]
    assert ALLOWED_TRANSITIONS[RuntimeState.PUBLISHED] == frozenset()
    assert ALLOWED_TRANSITIONS[RuntimeState.FAILED] == frozenset()


def test_out_of_order_stage_does_not_advance_state() -> None:
    runtime = NarrativeRuntime()
    context = runtime.initialize(_opaque_analysis())
    with pytest.raises(PipelineError):
        runtime.pipeline.build_action()
    assert context.runtime_state is RuntimeState.INITIALIZED
    assert runtime.executed_stages == ("initialize",)


def test_run_records_failed_when_validator_rejects_order() -> None:
    class RejectingValidator(RuntimeValidator):
        def validate(self, executed_stages, *, expected):  # type: ignore[no-untyped-def]
            from engines.narrative_v2.runtime.runtime_validator import ValidationOutcome

            return ValidationOutcome(passed=False, reason="pipeline ordering invalid")

    runtime = NarrativeRuntime(validator=RejectingValidator())
    result = runtime.run(_opaque_analysis())
    assert result.status == RuntimeState.FAILED.value
    assert result.errors
    assert any(event.name == "RuntimeFailed" for event in runtime.events)


# --- Registry ---


def test_registry_registers_builder_identity_only() -> None:
    registry = RuntimeRegistry()
    registry.register("evidence")
    registry.register("reasoning", builder=None)
    assert registry.builder_count == 2
    assert registry.registered_ids() == ("evidence", "reasoning")
    assert registry.get("evidence") is not None
    assert registry.get("evidence").builder is None
    assert registry.contains("reasoning")
    assert not registry.contains("summary")


def test_registry_rejects_duplicate_and_empty_id() -> None:
    registry = RuntimeRegistry()
    registry.register("evidence")
    with pytest.raises(BuilderError):
        registry.register("evidence")
    with pytest.raises(BuilderError):
        registry.register("")


def test_runtime_uses_injected_registry() -> None:
    registry = RuntimeRegistry()
    registry.register("evidence")
    runtime = NarrativeRuntime(registry=registry)
    result = runtime.run(_opaque_analysis())
    assert result.runtime_metadata["generates_narrative"] is False
    assert runtime.metrics.builder_count == 1


# --- Events ---


EXPECTED_EVENT_NAMES: tuple[str, ...] = (
    "NarrativeStarted",
    "EvidenceStarted",
    "EvidenceFinished",
    "ReasoningStarted",
    "ReasoningFinished",
    "KnowledgeStarted",
    "KnowledgeFinished",
    "RewriteStarted",
    "RewriteFinished",
    "SummaryStarted",
    "SummaryFinished",
    "InterpretationStarted",
    "InterpretationFinished",
    "ActionStarted",
    "ActionFinished",
    "CommercialStarted",
    "CommercialFinished",
    "ValidationStarted",
    "ValidationFinished",
    "PublishStarted",
    "PublishFinished",
)


def test_full_run_emits_runtime_events_in_order() -> None:
    runtime = NarrativeRuntime()
    runtime.run(_opaque_analysis())
    names = tuple(event.name for event in runtime.events)
    assert names == EXPECTED_EVENT_NAMES


# --- Trace ---


def test_pipeline_trace_records_stage_spans() -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(_opaque_analysis())
    entries = result.pipeline_trace.entries
    assert [entry.stage for entry in entries] == list(CANONICAL_STAGES)
    for entry in entries:
        assert entry.started <= (entry.finished or entry.started)
        assert entry.status in {
            "placeholder",
            "not_implemented",
            "pass",
            "implemented",
        }
        assert entry.finished is not None


# --- Result object ---


def test_result_object_has_skeleton_fields_and_no_narrative() -> None:
    result = NarrativeRuntime().run(_opaque_analysis())
    assert isinstance(result, NarrativeRuntimeResult)
    assert result.status == RuntimeState.PUBLISHED.value
    assert result.presentation is None
    assert result.errors == ()
    assert "shadow_mode" in result.runtime_metadata
    assert result.runtime_metadata["shadow_mode"] is True
    assert not hasattr(result, "overview")
    assert not hasattr(result, "interpretation")
    assert not hasattr(result, "action_plan")


# --- Validator ---


def test_validator_passes_canonical_pre_validate_order() -> None:
    outcome = RuntimeValidator().validate(
        PRE_VALIDATE_STAGES,
        expected=PRE_VALIDATE_STAGES,
    )
    assert outcome.passed is True
    assert outcome.status == "PASS"


def test_validator_fails_invalid_ordering() -> None:
    outcome = RuntimeValidator().validate(
        ("initialize", "build_summary"),
        expected=PRE_VALIDATE_STAGES,
    )
    assert outcome.passed is False
    assert outcome.status == "FAIL"
    assert outcome.reason == "pipeline ordering invalid"


def test_pipeline_validate_passes_after_builder_placeholders() -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(_opaque_analysis())
    for stage in BUILDER_STAGES:
        runtime.pipeline.execute_stage(stage)
    output = runtime.pipeline.validate()
    assert output.status == "pass"


# --- Metrics ---


def test_metrics_collect_duration_and_counts() -> None:
    registry = RuntimeRegistry()
    registry.register("evidence")
    registry.register("reasoning")
    runtime = NarrativeRuntime(registry=registry)
    result = runtime.run(_opaque_analysis())
    metrics = runtime.metrics
    assert metrics.runtime_duration >= 0.0
    assert set(metrics.stage_duration) == set(CANONICAL_STAGES)
    assert all(duration >= 0.0 for duration in metrics.stage_duration.values())
    assert metrics.builder_count == 2
    assert metrics.error_count == 0
    assert result.errors == ()


def test_metrics_error_count_on_failure() -> None:
    class RejectingValidator(RuntimeValidator):
        def validate(self, executed_stages, *, expected):  # type: ignore[no-untyped-def]
            from engines.narrative_v2.runtime.runtime_validator import ValidationOutcome

            return ValidationOutcome(passed=False, reason="pipeline ordering invalid")

    runtime = NarrativeRuntime(validator=RejectingValidator())
    result = runtime.run(_opaque_analysis())
    assert runtime.metrics.error_count >= 1
    assert result.status == RuntimeState.FAILED.value
    assert result.errors

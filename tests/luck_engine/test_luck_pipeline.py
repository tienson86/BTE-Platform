"""AX-4 Canonical Luck Pipeline integration tests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.pipeline.canonical_luck_pipeline import CanonicalLuckPipeline
from engines.luck_engine.pipeline.diagnostics import (
    DIAG_ANALYSIS_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_DECISION_MISSING,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_TIMELINE_MISSING,
)
from engines.luck_engine.pipeline.pipeline_executor import LuckPipelineContext
from engines.luck_engine.pipeline.stage_registry import ACTIVE_LUCK_STAGES, PIPELINE_VERSION


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _codes(result: Any) -> list[str]:
    return [item.code for item in result.luck_diagnostics]


def test_normal_execution(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Timeline → Analysis → Decision publishes the canonical luck result."""
    upstream_analysis = dict(analysis_snapshot)
    upstream_decision = dict(decision_snapshot)
    result = CanonicalLuckPipeline(clock=_clock).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is True
    assert result.luck_pipeline_version == PIPELINE_VERSION
    assert result.timeline_result is not None
    assert result.analysis_result is not None
    assert result.decision_result is not None
    assert result.overall_luck_result["timeline_version"] == "1.0.0"
    assert result.overall_luck_result["analysis_version"] == "1.0.0"
    assert result.overall_luck_result["decision_version"] == "1.0.0"
    assert result.luck_confidence is not None
    assert result.component_versions["bz_09_luck_foundation"] == "1.0.0"
    assert result.luck_trace is not None
    assert result.luck_trace.timeline_execution["executed"] is True
    assert result.luck_trace.analysis_execution["executed"] is True
    assert result.luck_trace.decision_execution["executed"] is True
    assert result.luck_audit is not None
    assert result.luck_audit.contract_validation == "pass"
    assert result.luck_audit.dependency_validation == "pass"
    assert result.luck_audit.timeline_legality == "pass"
    assert result.luck_audit.analysis_legality == "pass"
    assert result.luck_audit.decision_legality == "pass"
    assert DIAG_PIPE_OK in _codes(result)
    assert analysis_snapshot == upstream_analysis
    assert decision_snapshot == upstream_decision


def test_missing_timeline(
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Missing timeline stops without raising."""
    result = CanonicalLuckPipeline(clock=_clock).run(
        timeline=None,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is False
    assert DIAG_TIMELINE_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.timeline_result is None
    assert result.analysis_result is None


def test_missing_analysis(
    continuous_timeline_payload: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Missing AX-2 snapshot stops after timeline."""
    result = CanonicalLuckPipeline(clock=_clock).run(
        timeline=continuous_timeline_payload,
        analysis_result=None,
        decision_result=decision_snapshot,
    )
    assert result.success is False
    assert DIAG_ANALYSIS_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.timeline_result is not None
    assert result.analysis_result is None
    assert result.decision_result is None


def test_missing_decision(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
) -> None:
    """Missing AX-3 snapshot stops before luck analysis publication."""
    result = CanonicalLuckPipeline(clock=_clock).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=None,
    )
    assert result.success is False
    assert DIAG_DECISION_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.decision_result is None


def test_dependency_violation(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Analysis cannot run without timeline in the active set."""
    result = CanonicalLuckPipeline(
        clock=_clock,
        active_stages=("analysis", "decision"),
    ).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is False
    assert DIAG_DEP_VIOLATION in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)


def test_contract_violation(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Incompatible foundation constraint stops execution."""
    result = CanonicalLuckPipeline(
        clock=_clock,
        version_constraints={"bz_09_luck_foundation": "^9.0.0"},
    ).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is False
    assert DIAG_CONTRACT_VIOLATION in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)


def test_duplicate_publication_prevented(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Reusing a published context must stop without raising."""
    context = LuckPipelineContext(
        timeline_input=continuous_timeline_payload,
        analysis_input=analysis_snapshot,
        decision_input=decision_snapshot,
    )
    pipeline = CanonicalLuckPipeline(clock=_clock)
    first = pipeline.run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
        context=context,
    )
    assert first.success is True
    second = pipeline.run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
        context=context,
    )
    assert second.success is False
    assert DIAG_OUT_DUPLICATE in _codes(second)
    assert any("duplicate_execution" in error for error in second.errors)


def test_future_stages_registered_disabled() -> None:
    """Interpretation and Report remain catalogued and inactive."""
    from engines.luck_engine.pipeline.stage_registry import LuckStageRegistry

    registry = LuckStageRegistry.default()
    assert registry.get("interpretation").enabled is False
    assert registry.get("report").enabled is False
    assert registry.resolve_order(ACTIVE_LUCK_STAGES) == ACTIVE_LUCK_STAGES

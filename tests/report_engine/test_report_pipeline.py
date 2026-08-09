"""RX-1 Canonical Report Pipeline integration tests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.report_engine.layout.layout_engine import ReportLayoutEngine
from engines.report_engine.pipeline.canonical_report_pipeline import CanonicalReportPipeline
from engines.report_engine.pipeline.diagnostics import (
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_FOUNDATION_MISSING,
    DIAG_LAYOUT_MISSING,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_RENDERER_MISSING,
)
from engines.report_engine.pipeline.pipeline_executor import ReportPipelineContext
from engines.report_engine.pipeline.stage_registry import ACTIVE_REPORT_STAGES, PIPELINE_VERSION
from tests.report_engine.re1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot
from tests.report_engine.re2_support import assemble_layout_inputs, frozen_clock


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _codes(result: Any) -> list[str]:
    return [item.code for item in result.report_diagnostics]


def test_normal_execution() -> None:
    """Foundation → Layout → Rendering publishes the canonical report result."""
    payload = assemble_layout_inputs()
    analysis = payload["analysis_result"]
    decision = payload["decision_result"]
    luck = payload["luck_result"]
    interpretation = payload["interpretation_result"]
    upstream_analysis = dict(analysis)
    result = CanonicalReportPipeline(clock=_clock).run(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        interpretation_result=interpretation,
    )
    assert result.success is True
    assert result.report_pipeline_version == PIPELINE_VERSION
    assert result.foundation_result is not None
    assert result.layout_result is not None
    assert result.rendering_result is not None
    assert result.canonical_report_artifact == result.rendering_result
    assert result.canonical_report_artifact["artifact_id"] == "ART-json-1"
    assert result.component_versions["report_foundation"] == "1.0.0"
    assert result.component_versions["report_layout_engine"] == "1.0.0"
    assert result.component_versions["report_rendering_engine"] == "1.0.0"
    assert result.report_trace is not None
    assert result.report_trace.foundation_execution["executed"] is True
    assert result.report_trace.layout_execution["executed"] is True
    assert result.report_trace.render_execution["executed"] is True
    assert result.report_trace.artifact_creation["artifact_id"] == "ART-json-1"
    assert result.report_audit is not None
    assert result.report_audit.contract_validation == "pass"
    assert result.report_audit.dependency_validation == "pass"
    assert result.report_audit.foundation_legality == "pass"
    assert result.report_audit.layout_legality == "pass"
    assert result.report_audit.render_legality == "pass"
    assert DIAG_PIPE_OK in _codes(result)
    assert analysis == upstream_analysis


def test_missing_foundation() -> None:
    """Missing AX / IX snapshots stop before foundation publication."""
    result = CanonicalReportPipeline(clock=_clock).run()
    assert result.success is False
    assert DIAG_FOUNDATION_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.foundation_result is None
    assert result.layout_result is None
    assert result.rendering_result is None


def test_missing_layout() -> None:
    """Prebuilt foundation without live layout inputs stops at RE-2."""
    payload = assemble_layout_inputs()
    result = CanonicalReportPipeline(clock=_clock).run(
        foundation_result=payload["report_context"],
    )
    assert result.success is False
    assert DIAG_LAYOUT_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.foundation_result is not None
    assert result.layout_result is None
    assert result.rendering_result is None


def test_missing_renderer() -> None:
    """Prebuilt foundation and layout with a disabled renderer stops at RE-3."""
    payload = assemble_layout_inputs()
    layout = ReportLayoutEngine(clock=frozen_clock).run(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    result = CanonicalReportPipeline(clock=_clock).run(
        foundation_result=payload["report_context"],
        layout_result=layout,
        renderer="xlsx",
    )
    assert result.success is False
    assert DIAG_RENDERER_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.foundation_result is not None
    assert result.layout_result is not None
    assert result.rendering_result is None


def test_dependency_violation() -> None:
    """Layout cannot run without foundation in the active set."""
    payload = assemble_layout_inputs()
    result = CanonicalReportPipeline(
        clock=_clock,
        active_stages=("layout", "rendering"),
    ).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
    )
    assert result.success is False
    assert DIAG_DEP_VIOLATION in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)


def test_contract_violation() -> None:
    """Incompatible analysis pipeline constraint stops execution."""
    payload = assemble_layout_inputs()
    result = CanonicalReportPipeline(
        clock=_clock,
        version_constraints={"canonical_analysis_pipeline": "^9.0.0"},
    ).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
    )
    assert result.success is False
    assert DIAG_CONTRACT_VIOLATION in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)


def test_duplicate_publication_prevented() -> None:
    """Reusing a published context must stop without raising."""
    payload = assemble_layout_inputs()
    context = ReportPipelineContext(
        analysis_input=payload["analysis_result"],
        decision_input=payload["decision_result"],
        luck_input=payload["luck_result"],
        interpretation_input=payload["interpretation_result"],
    )
    pipeline = CanonicalReportPipeline(clock=_clock)
    first = pipeline.run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
        context=context,
    )
    assert first.success is True
    second = pipeline.run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
        context=context,
    )
    assert second.success is False
    assert DIAG_OUT_DUPLICATE in _codes(second)
    assert any("duplicate_execution" in error for error in second.errors)


def test_future_stages_registered_disabled() -> None:
    """Publisher, delivery, and print remain catalogued and inactive."""
    from engines.report_engine.pipeline.stage_registry import ReportStageRegistry

    registry = ReportStageRegistry.default()
    assert registry.get("publisher").enabled is False
    assert registry.get("delivery").enabled is False
    assert registry.get("print").enabled is False
    assert registry.resolve_order(ACTIVE_REPORT_STAGES) == ACTIVE_REPORT_STAGES

"""IX-1 Canonical Interpretation Pipeline integration tests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.interpretation_engine.pipeline.canonical_interpretation_pipeline import (
    CanonicalInterpretationPipeline,
)
from engines.interpretation_engine.pipeline.canonical_pipeline_executor import (
    InterpretationPipelineContext,
)
from engines.interpretation_engine.pipeline.diagnostics import (
    DIAG_COMPOSITION_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_FOUNDATION_MISSING,
    DIAG_KNOWLEDGE_MISSING,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
)
from engines.interpretation_engine.pipeline.stage_registry import (
    ACTIVE_INTERPRETATION_STAGES,
    PIPELINE_VERSION,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot
from tests.interpretation_engine.ie3_support import assemble_inputs


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _codes(result: Any) -> list[str]:
    return [item.code for item in result.interpretation_diagnostics]


def test_normal_execution() -> None:
    """Foundation → Knowledge → Composition publishes the canonical result."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    upstream_analysis = dict(analysis)
    upstream_decision = dict(decision)
    upstream_luck = dict(luck)
    result = CanonicalInterpretationPipeline(clock=_clock).run(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
    )
    assert result.success is True
    assert result.interpretation_pipeline_version == PIPELINE_VERSION
    assert result.foundation_result is not None
    assert result.knowledge_result is not None
    assert result.composition_result is not None
    assert result.canonical_interpretation == result.composition_result
    assert result.canonical_interpretation["assembly_version"] == "1.0.0"
    assert result.canonical_interpretation["sections"]
    assert result.component_versions["interpretation_foundation"] == "1.0.0"
    assert result.component_versions["knowledge_selection_engine"] == "1.0.0"
    assert result.component_versions["interpretation_composition_engine"] == "1.0.0"
    assert result.interpretation_trace is not None
    assert result.interpretation_trace.foundation_execution["executed"] is True
    assert result.interpretation_trace.knowledge_execution["executed"] is True
    assert result.interpretation_trace.composition_execution["executed"] is True
    assert result.interpretation_audit is not None
    assert result.interpretation_audit.contract_validation == "pass"
    assert result.interpretation_audit.dependency_validation == "pass"
    assert result.interpretation_audit.foundation_legality == "pass"
    assert result.interpretation_audit.knowledge_legality == "pass"
    assert result.interpretation_audit.composition_legality == "pass"
    assert DIAG_PIPE_OK in _codes(result)
    assert analysis == upstream_analysis
    assert decision == upstream_decision
    assert luck == upstream_luck


def test_missing_foundation() -> None:
    """Missing AX snapshots stop before foundation publication."""
    result = CanonicalInterpretationPipeline(clock=_clock).run()
    assert result.success is False
    assert DIAG_FOUNDATION_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.foundation_result is None
    assert result.knowledge_result is None
    assert result.composition_result is None


def test_missing_knowledge() -> None:
    """Prebuilt foundation without AX or knowledge selection stops at IE-2."""
    payload = assemble_inputs()
    result = CanonicalInterpretationPipeline(clock=_clock).run(
        foundation_result=payload["interpretation_context"],
    )
    assert result.success is False
    assert DIAG_KNOWLEDGE_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.foundation_result is not None
    assert result.knowledge_result is None
    assert result.composition_result is None


def test_missing_composition() -> None:
    """Prebuilt foundation and knowledge without AX stop at IE-3."""
    payload = assemble_inputs()
    result = CanonicalInterpretationPipeline(clock=_clock).run(
        foundation_result=payload["interpretation_context"],
        knowledge_result=payload["composition_result"],
    )
    assert result.success is False
    assert DIAG_COMPOSITION_MISSING in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)
    assert result.foundation_result is not None
    assert result.knowledge_result is not None
    assert result.composition_result is None


def test_dependency_violation() -> None:
    """Knowledge cannot run without foundation in the active set."""
    result = CanonicalInterpretationPipeline(
        clock=_clock,
        active_stages=("knowledge_selection", "composition"),
    ).run(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    assert result.success is False
    assert DIAG_DEP_VIOLATION in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)


def test_contract_violation() -> None:
    """Incompatible analysis pipeline constraint stops execution."""
    result = CanonicalInterpretationPipeline(
        clock=_clock,
        version_constraints={"canonical_analysis_pipeline": "^9.0.0"},
    ).run(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    assert result.success is False
    assert DIAG_CONTRACT_VIOLATION in _codes(result)
    assert DIAG_PIPE_FAIL in _codes(result)


def test_duplicate_publication_prevented() -> None:
    """Reusing a published context must stop without raising."""
    analysis = ax2_snapshot()
    decision = ax3_snapshot()
    luck = ax4_snapshot()
    context = InterpretationPipelineContext(
        analysis_input=analysis,
        decision_input=decision,
        luck_input=luck,
    )
    pipeline = CanonicalInterpretationPipeline(clock=_clock)
    first = pipeline.run(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        context=context,
    )
    assert first.success is True
    second = pipeline.run(
        analysis_result=analysis,
        decision_result=decision,
        luck_result=luck,
        context=context,
    )
    assert second.success is False
    assert DIAG_OUT_DUPLICATE in _codes(second)
    assert any("duplicate_execution" in error for error in second.errors)


def test_future_stages_registered_disabled() -> None:
    """Report and AI Rewrite remain catalogued and inactive."""
    from engines.interpretation_engine.pipeline.stage_registry import InterpretationStageRegistry

    registry = InterpretationStageRegistry.default()
    assert registry.get("report").enabled is False
    assert registry.get("ai_rewrite").enabled is False
    assert registry.resolve_order(ACTIVE_INTERPRETATION_STAGES) == ACTIVE_INTERPRETATION_STAGES

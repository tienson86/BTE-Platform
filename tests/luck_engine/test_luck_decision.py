"""Luck Decision Engine construction, validation, and serialization tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis import LuckAnalysisEngine
from engines.luck_engine.decision import LuckDecisionEngine
from engines.luck_engine.decision.validation import validate_contract_integrity
from engines.luck_engine.decision_constants import (
    DIAG_ANALYSIS_MISSING,
    DIAG_DECISION_MISSING,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_TIMELINE_MISSING,
    PUBLISHED_OUTPUTS,
)
from engines.luck_engine.timeline import construct_timeline


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _analysis_result(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> tuple[Any, Any]:
    timeline = construct_timeline(**continuous_timeline_payload)
    analysis = LuckAnalysisEngine(clock=_clock).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    return timeline, analysis


def test_decision_construction(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Five stages publish without mutating upstream snapshots."""
    timeline, luck_analysis = _analysis_result(
        continuous_timeline_payload, analysis_snapshot, decision_snapshot
    )
    upstream_analysis = dict(analysis_snapshot)
    upstream_decision = dict(decision_snapshot)
    luck_copy = luck_analysis.to_dict()
    result = LuckDecisionEngine(clock=_clock).run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is True
    assert result.decision_version == "1.0.0"
    assert result.opportunity_score is not None
    assert result.risk_score is not None
    assert result.luck_priority["value"] in {
        "opportunity_first",
        "risk_first",
        "balanced",
        "withheld",
    }
    assert result.decision_reasoning
    assert all("code" in item for item in result.decision_reasoning)
    assert result.overall_luck_decision["decision_version"] == "1.0.0"
    assert analysis_snapshot == upstream_analysis
    assert decision_snapshot == upstream_decision
    assert luck_analysis.to_dict() == luck_copy
    assert any(item.code == DIAG_PIPE_OK for item in result.diagnostics)


def test_missing_inputs_emit_diagnostics(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Missing inputs never raise."""
    timeline, luck_analysis = _analysis_result(
        continuous_timeline_payload, analysis_snapshot, decision_snapshot
    )
    engine = LuckDecisionEngine(clock=_clock)
    missing_timeline = engine.run(
        timeline_result=None,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert missing_timeline.success is False
    assert any(item.code == DIAG_TIMELINE_MISSING for item in missing_timeline.diagnostics)
    missing_analysis = engine.run(
        timeline_result=timeline,
        luck_analysis_result=None,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert any(item.code == DIAG_ANALYSIS_MISSING for item in missing_analysis.diagnostics)
    missing_decision = engine.run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=None,
    )
    assert any(item.code == DIAG_DECISION_MISSING for item in missing_decision.diagnostics)
    assert any(item.code == DIAG_PIPE_FAIL for item in missing_timeline.diagnostics)


def test_serialization_and_validation(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Serialized result satisfies the published contract."""
    timeline, luck_analysis = _analysis_result(
        continuous_timeline_payload, analysis_snapshot, decision_snapshot
    )
    result = LuckDecisionEngine(clock=_clock).run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    payload = result.to_dict()
    for name in PUBLISHED_OUTPUTS:
        assert name in payload
    validate_contract_integrity(payload)
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    assert "narrative" not in encoded
    assert "interpretation" not in encoded
    assert "report_text" not in encoded

"""Luck Analysis Engine construction, validation, and serialization tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis import LuckAnalysisEngine
from engines.luck_engine.analysis_constants import (
    DIAG_ANALYSIS_MISSING,
    DIAG_DECISION_MISSING,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_TIMELINE_MISSING,
    PUBLISHED_OUTPUTS,
)
from engines.luck_engine.analysis.validation import validate_contract_integrity
from engines.luck_engine.timeline import construct_timeline


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_analysis_construction(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Six impact stages publish without mutating upstream snapshots."""
    timeline = construct_timeline(**continuous_timeline_payload)
    upstream_analysis = dict(analysis_snapshot)
    upstream_decision = dict(decision_snapshot)
    result = LuckAnalysisEngine(clock=_clock).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is True
    assert result.analysis_version == "1.0.0"
    assert result.seasonal_impact is not None
    assert result.useful_god_impact is not None
    assert result.overall_analysis_impact["stage_count"] == 6
    assert analysis_snapshot == upstream_analysis
    assert decision_snapshot == upstream_decision
    codes = [item.code for item in result.analysis_diagnostics]
    assert DIAG_PIPE_OK in codes


def test_missing_inputs_emit_diagnostics(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Missing timeline / analysis / decision never raise."""
    engine = LuckAnalysisEngine(clock=_clock)
    timeline = construct_timeline(**continuous_timeline_payload)
    missing_timeline = engine.run(
        timeline=None,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert missing_timeline.success is False
    assert any(item.code == DIAG_TIMELINE_MISSING for item in missing_timeline.analysis_diagnostics)
    missing_analysis = engine.run(
        timeline=timeline,
        analysis_result=None,
        decision_result=decision_snapshot,
    )
    assert any(item.code == DIAG_ANALYSIS_MISSING for item in missing_analysis.analysis_diagnostics)
    missing_decision = engine.run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=None,
    )
    assert any(item.code == DIAG_DECISION_MISSING for item in missing_decision.analysis_diagnostics)
    assert any(item.code == DIAG_PIPE_FAIL for item in missing_timeline.analysis_diagnostics)


def test_serialization_and_validation(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Serialized result satisfies the published contract."""
    timeline = construct_timeline(**continuous_timeline_payload)
    result = LuckAnalysisEngine(clock=_clock).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    payload = result.to_dict()
    for name in PUBLISHED_OUTPUTS:
        assert name in payload
    validate_contract_integrity(payload)
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    assert "auspicious" not in encoded
    assert "fortune_quality" not in encoded
    assert json.loads(encoded)["analysis_version"] == "1.0.0"

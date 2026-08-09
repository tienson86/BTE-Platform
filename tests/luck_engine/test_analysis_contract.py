"""Published Luck Analysis contract tests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis import luck_analysis_contract
from engines.luck_engine.analysis.luck_analysis_engine import LuckAnalysisEngine
from engines.luck_engine.analysis_constants import PUBLISHED_OUTPUTS
from engines.luck_engine.timeline import construct_timeline


def test_luck_analysis_contract_surface() -> None:
    """Contract lists LE-3 inputs and forbids fortune decisions."""
    contract = luck_analysis_contract()
    assert contract["analysis_version"] == "1.0.0"
    assert contract["outputs"] == list(PUBLISHED_OUTPUTS)
    assert contract["fortune_scores"] is False
    assert contract["decisions"] is False
    assert contract["interpretation"] is False


def test_result_trace_consumes_upstream_identities(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Trace records consumed timeline / analysis / decision identities."""
    timeline = construct_timeline(**continuous_timeline_payload)
    result = LuckAnalysisEngine(
        clock=lambda: datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)
    ).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    trace = result.analysis_trace
    assert trace is not None
    assert trace.timeline_consumed["timeline_version"] == "1.0.0"
    assert trace.analysis_consumed["pipeline_version"] == "2.0.0"
    assert trace.decision_consumed["decision_pipeline_version"] == "1.0.0"
    assert list(trace.impact_stages_executed) == list(PUBLISHED_OUTPUTS[:6])
    assert "seasonal_impact" in trace.outputs_published
    assert result.useful_god_impact["evidence"]["consumed_fields"]
    assert "final_useful_god" in str(result.useful_god_impact["evidence"]["consumed_fields"]) or any(
        "useful_god" in name for name in result.useful_god_impact["evidence"]["consumed_fields"]
    )

"""Published Luck Decision contract tests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis import LuckAnalysisEngine
from engines.luck_engine.decision import LuckDecisionEngine, luck_decision_contract
from engines.luck_engine.decision_constants import PUBLISHED_OUTPUTS
from engines.luck_engine.timeline import construct_timeline


def test_luck_decision_contract_surface() -> None:
    """Contract lists AX-4 / Interpretation inputs and forbids reports."""
    contract = luck_decision_contract()
    assert contract["decision_version"] == "1.0.0"
    assert contract["outputs"] == list(PUBLISHED_OUTPUTS)
    assert contract["interpretation"] is False
    assert contract["reports"] is False


def test_trace_and_audit_are_machine_readable(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Trace and audit carry consumed identities and legality flags."""
    timeline = construct_timeline(**continuous_timeline_payload)
    luck_analysis = LuckAnalysisEngine(
        clock=lambda: datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)
    ).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    result = LuckDecisionEngine(
        clock=lambda: datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)
    ).run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    trace = result.decision_trace
    audit = result.decision_audit
    assert trace is not None
    assert audit is not None
    assert trace.timeline_consumed["timeline_version"] == "1.0.0"
    assert trace.analysis_consumed["luck_analysis_version"] == "1.0.0"
    assert trace.decision_consumed["decision_pipeline_version"] == "1.0.0"
    assert list(trace.decision_stages_executed) == [
        "opportunity_evaluation",
        "risk_evaluation",
        "confidence_evaluation",
        "priority_resolution",
        "decision_publication",
    ]
    assert audit.contract_validation == "pass"
    assert audit.dependency_validation == "pass"
    assert audit.priority_legality == "pass"
    assert audit.confidence_validation == "pass"
    assert audit.deterministic_execution is True
    assert audit.version_compatibility == "pass"

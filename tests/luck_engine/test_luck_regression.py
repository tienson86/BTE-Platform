"""Regression: LE-1 / LE-2 / LE-3 remain unchanged after AX-4."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engines.luck_engine.analysis import LuckAnalysisEngine, luck_analysis_contract
from engines.luck_engine.analysis_constants import PUBLISHED_OUTPUTS as ANALYSIS_OUTPUTS
from engines.luck_engine.contracts.timeline_contract import timeline_contract
from engines.luck_engine.decision import LuckDecisionEngine, luck_decision_contract
from engines.luck_engine.decision_constants import PUBLISHED_OUTPUTS as DECISION_OUTPUTS
from engines.luck_engine.pipeline.luck_audit import AUDIT_SCHEMA_KEYS
from engines.luck_engine.pipeline.luck_trace import STEP_SCHEMA_KEYS, TRACE_SCHEMA_KEYS
from engines.luck_engine.timeline import LuckPackageLoader, construct_timeline
from engines.luck_engine.timeline_constants import PUBLISHED_OUTPUTS as TIMELINE_OUTPUTS

REPO = Path(__file__).resolve().parents[2]

BZ09_CHECKSUM = "57933cd47f469c283af88cbf8fa1f57877becc560b57400a5c26b80ac6aa41cd"


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_le1_timeline_checksum_and_contract_unchanged() -> None:
    """bz_09 checksum, schema, and published timeline contract stay sealed."""
    package = LuckPackageLoader().load()
    assert package.package_id == "bz_09_luck_foundation"
    assert package.package_version == "1.0.0"
    assert package.schema_version == "2.0.0"
    assert package.package_type == "reference"
    assert package.checksum == BZ09_CHECKSUM
    root = REPO / "knowledge" / "packages" / "luck" / "foundation"
    identity = json.loads((root / "PACKAGE.json").read_text(encoding="utf-8"))
    assert identity["checksum"]["value"] == BZ09_CHECKSUM
    contract = timeline_contract()
    assert contract["outputs"] == list(TIMELINE_OUTPUTS)
    assert contract["inputs"] == list(package.published_inputs)
    assert contract["scores"] is False


def test_le2_analysis_contract_and_outputs_unchanged(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """LE-2 published contract and outputs remain independently executable."""
    contract = luck_analysis_contract()
    assert contract["analysis_version"] == "1.0.0"
    assert contract["outputs"] == list(ANALYSIS_OUTPUTS)
    timeline = construct_timeline(**continuous_timeline_payload)
    result = LuckAnalysisEngine(clock=_clock).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is True
    payload = result.to_dict()
    for name in ANALYSIS_OUTPUTS:
        assert name in payload
    trace = result.analysis_trace
    assert trace is not None
    assert set(trace.to_dict()) >= {
        "analysis_engine_id",
        "analysis_version",
        "impact_stages_executed",
        "outputs_published",
        "started_at",
        "completed_at",
    }


def test_le3_decision_contract_trace_and_audit_unchanged(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """LE-3 published contract, trace, and audit remain independently executable."""
    contract = luck_decision_contract()
    assert contract["decision_version"] == "1.0.0"
    assert contract["outputs"] == list(DECISION_OUTPUTS)
    timeline = construct_timeline(**continuous_timeline_payload)
    luck_analysis = LuckAnalysisEngine(clock=_clock).run(
        timeline=timeline,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    result = LuckDecisionEngine(clock=_clock).run(
        timeline_result=timeline,
        luck_analysis_result=luck_analysis,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.success is True
    payload = result.to_dict()
    for name in DECISION_OUTPUTS:
        assert name in payload
    assert result.decision_trace is not None
    assert result.decision_audit is not None
    assert result.decision_audit.contract_validation == "pass"
    assert set(result.decision_trace.to_dict()) >= {
        "decision_engine_id",
        "decision_version",
        "decision_stages_executed",
        "outputs_published",
        "started_at",
        "completed_at",
    }
    assert set(result.decision_audit.to_dict()) >= {
        "contract_validation",
        "dependency_validation",
        "priority_legality",
        "confidence_validation",
        "deterministic_execution",
        "version_compatibility",
    }


def test_ax4_trace_and_audit_schemas_stable(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """AX-4 trace and audit schemas publish the frozen key sets."""
    from engines.luck_engine.pipeline.canonical_luck_pipeline import CanonicalLuckPipeline

    result = CanonicalLuckPipeline(clock=_clock).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    assert result.luck_trace is not None
    assert result.luck_audit is not None
    assert tuple(result.luck_trace.to_dict()) == TRACE_SCHEMA_KEYS
    assert tuple(result.luck_audit.to_dict()) == AUDIT_SCHEMA_KEYS
    assert tuple(result.luck_trace.steps[0].to_dict()) == STEP_SCHEMA_KEYS


def test_ax4_loader_does_not_rewrite_bz09() -> None:
    """Luck pipeline package admission remains read-only."""
    root = REPO / "knowledge" / "packages" / "luck" / "foundation" / "PACKAGE.json"
    before = root.read_bytes()
    LuckPackageLoader().load()
    after = root.read_bytes()
    assert before == after

"""Canonical Luck Pipeline contract tests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.analysis import luck_analysis_contract
from engines.luck_engine.contracts.luck_contract import luck_pipeline_contract
from engines.luck_engine.contracts.timeline_contract import timeline_contract
from engines.luck_engine.decision import luck_decision_contract
from engines.luck_engine.pipeline.canonical_luck_pipeline import CanonicalLuckPipeline
from engines.luck_engine.pipeline.luck_result import RESULT_FIELDS
from engines.luck_engine.pipeline.stage_registry import (
    ACTIVE_LUCK_STAGES,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_luck_pipeline_contract_surface() -> None:
    """Pipeline contract lists official outputs and withholds Interpretation."""
    contract = luck_pipeline_contract()
    assert contract["pipeline_id"] == PIPELINE_ID
    assert contract["luck_pipeline_version"] == PIPELINE_VERSION
    assert contract["active_stages"] == list(ACTIVE_LUCK_STAGES)
    assert contract["future_stages"] == list(INACTIVE_FUTURE_STAGES)
    assert contract["outputs"] == list(RESULT_FIELDS)
    assert contract["interpretation"] is False
    assert contract["reports"] is False


def test_upstream_contracts_remain_isolated() -> None:
    """AX-4 does not rewrite LE-1 / LE-2 / LE-3 published contracts."""
    assert timeline_contract()["timeline_version"] == "1.0.0"
    assert luck_analysis_contract()["analysis_version"] == "1.0.0"
    assert luck_decision_contract()["decision_version"] == "1.0.0"
    assert timeline_contract()["interpretation"] is False
    assert luck_analysis_contract()["decisions"] is False
    assert luck_decision_contract()["reports"] is False


def test_result_exposes_declared_contract_fields(
    continuous_timeline_payload: dict[str, Any],
    analysis_snapshot: dict[str, Any],
    decision_snapshot: dict[str, Any],
) -> None:
    """Serialized canonical result includes every declared pipeline output."""
    result = CanonicalLuckPipeline(clock=_clock).run(
        timeline=continuous_timeline_payload,
        analysis_result=analysis_snapshot,
        decision_result=decision_snapshot,
    )
    payload = result.to_dict()
    for name in RESULT_FIELDS:
        assert name in payload
    assert payload["luck_pipeline_version"] == "1.0.0"
    assert payload["luck_trace"]["pipeline_id"] == PIPELINE_ID
    assert payload["luck_audit"]["deterministic_execution"] is True

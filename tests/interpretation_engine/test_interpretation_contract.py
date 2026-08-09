"""Canonical Interpretation Pipeline contract tests."""

from __future__ import annotations

from datetime import datetime, timezone

from engines.interpretation_engine.contracts.interpretation_contract import (
    interpretation_pipeline_contract,
)
from engines.interpretation_engine.contracts.interpretation_contracts import (
    interpretation_foundation_contract,
)
from engines.interpretation_engine.knowledge.composition_context import COMPOSITION_VERSION
from engines.interpretation_engine.composition.composition_context import ASSEMBLY_VERSION
from engines.interpretation_engine.pipeline.canonical_interpretation_pipeline import (
    CanonicalInterpretationPipeline,
)
from engines.interpretation_engine.pipeline.interpretation_result import RESULT_FIELDS
from engines.interpretation_engine.pipeline.stage_registry import (
    ACTIVE_INTERPRETATION_STAGES,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)
from tests.interpretation_engine.ie1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_interpretation_pipeline_contract_surface() -> None:
    """Pipeline contract lists official outputs and withholds Report / AI."""
    contract = interpretation_pipeline_contract()
    assert contract["pipeline_id"] == PIPELINE_ID
    assert contract["interpretation_pipeline_version"] == PIPELINE_VERSION
    assert contract["active_stages"] == list(ACTIVE_INTERPRETATION_STAGES)
    assert contract["future_stages"] == list(INACTIVE_FUTURE_STAGES)
    assert contract["outputs"] == list(RESULT_FIELDS)
    assert contract["reports"] is False
    assert contract["ai_rewrite"] is False


def test_upstream_contracts_remain_isolated() -> None:
    """IX-1 does not rewrite IE-1 / IE-2 / IE-3 published versions."""
    assert interpretation_foundation_contract()["interpretation_version"] == "1.0.0"
    assert interpretation_foundation_contract()["text_generation"] is False
    assert COMPOSITION_VERSION == "1.0.0"
    assert ASSEMBLY_VERSION == "1.0.0"


def test_result_exposes_declared_contract_fields() -> None:
    """Serialized canonical result includes every declared pipeline output."""
    result = CanonicalInterpretationPipeline(clock=_clock).run(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
    )
    payload = result.to_dict()
    for name in RESULT_FIELDS:
        assert name in payload
    assert payload["interpretation_pipeline_version"] == "1.0.0"
    assert payload["interpretation_trace"]["pipeline_id"] == PIPELINE_ID
    assert payload["interpretation_audit"]["deterministic_execution"] is True

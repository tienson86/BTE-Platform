"""Canonical Report Pipeline contract tests."""

from __future__ import annotations

from datetime import datetime, timezone

from engines.report_engine.contracts.report_contracts import report_foundation_contract
from engines.report_engine.contracts.report_pipeline_contract import report_pipeline_contract
from engines.report_engine.layout.layout_context import LAYOUT_VERSION
from engines.report_engine.pipeline.canonical_report_pipeline import CanonicalReportPipeline
from engines.report_engine.pipeline.report_result import RESULT_FIELDS
from engines.report_engine.pipeline.stage_registry import (
    ACTIVE_REPORT_STAGES,
    INACTIVE_FUTURE_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
)
from engines.report_engine.rendering.rendering_context import RENDER_VERSION
from tests.report_engine.re2_support import assemble_layout_inputs


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_report_pipeline_contract_surface() -> None:
    """Pipeline contract lists official outputs and withholds publisher/print."""
    contract = report_pipeline_contract()
    assert contract["pipeline_id"] == PIPELINE_ID
    assert contract["report_pipeline_version"] == PIPELINE_VERSION
    assert contract["active_stages"] == list(ACTIVE_REPORT_STAGES)
    assert contract["future_stages"] == list(INACTIVE_FUTURE_STAGES)
    assert contract["outputs"] == list(RESULT_FIELDS)
    assert contract["publisher"] is False
    assert contract["delivery"] is False
    assert contract["print"] is False


def test_upstream_contracts_remain_isolated() -> None:
    """RX-1 does not rewrite RE-1 / RE-2 / RE-3 published versions."""
    assert report_foundation_contract()["report_version"] == "1.0.0"
    assert report_foundation_contract()["rendering"] is False
    assert LAYOUT_VERSION == "1.0.0"
    assert RENDER_VERSION == "1.0.0"


def test_result_exposes_declared_contract_fields() -> None:
    """Serialized canonical result includes every declared pipeline output."""
    payload = assemble_layout_inputs()
    result = CanonicalReportPipeline(clock=_clock).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
    )
    serialized = result.to_dict()
    for name in RESULT_FIELDS:
        assert name in serialized
    assert serialized["report_pipeline_version"] == "1.0.0"
    assert serialized["report_trace"]["pipeline_id"] == PIPELINE_ID
    assert serialized["report_audit"]["deterministic_execution"] is True

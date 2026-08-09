"""Deterministic Canonical Report Pipeline execution tests."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from engines.report_engine.pipeline.canonical_report_pipeline import CanonicalReportPipeline
from tests.report_engine.re2_support import assemble_layout_inputs


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def test_two_runs_are_byte_identical() -> None:
    """Same inputs and clock yield identical published JSON."""
    payload = assemble_layout_inputs()
    first = CanonicalReportPipeline(clock=_clock).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
    )
    second = CanonicalReportPipeline(clock=_clock).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
    )
    encoded_first = json.dumps(first.to_dict(), sort_keys=True, ensure_ascii=False)
    encoded_second = json.dumps(second.to_dict(), sort_keys=True, ensure_ascii=False)
    assert encoded_first == encoded_second
    assert first.report_trace.started_at == "2026-08-09T12:00:00Z"
    assert first.layout_result["document"]["document_id"] == second.layout_result["document"]["document_id"]
    assert first.rendering_result["content"] == second.rendering_result["content"]

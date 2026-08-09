"""RE-2 layout engine integration, serialization, and determinism tests."""

from __future__ import annotations

import json

from engines.report_engine.layout.layout_engine import ReportLayoutEngine
from engines.report_engine.layout.layout_result import DIAG_PIPE_OK, CanonicalReportLayout
from tests.report_engine.re2_support import assemble_layout_inputs, frozen_clock


def test_layout_engine_assembles_canonical_report_layout() -> None:
    """Engine publishes document, sections, blocks, theme, layout, assets, TOC."""
    payload = assemble_layout_inputs()
    result = ReportLayoutEngine(clock=frozen_clock).run(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    assert isinstance(result, CanonicalReportLayout)
    assert result.success is True
    assert result.layout_version == "1.0.0"
    assert result.document is not None
    assert len(result.sections) == 9
    assert result.blocks
    assert result.theme is not None
    assert result.layout is not None
    assert result.assets
    assert result.toc is not None
    assert result.layout_trace is not None
    assert result.layout_trace.started_at == "2026-08-09T12:00:00Z"
    assert result.layout_trace.document_created == result.document.document_id
    assert result.layout_audit is not None
    assert result.layout_audit.contract_validation == "pass"
    assert result.layout_audit.layout_legality == "pass"
    assert result.layout_audit.theme_legality == "pass"
    assert result.layout_audit.asset_legality == "pass"
    assert any(item.code == DIAG_PIPE_OK for item in result.layout_diagnostics)
    assert result.metadata is not None
    assert result.metadata["rendering"] is False
    assert result.metadata["pdf"] is False


def test_serialization_and_determinism() -> None:
    """Repeated runs with a frozen clock yield identical JSON."""
    payload = assemble_layout_inputs()
    first = json.dumps(
        ReportLayoutEngine(clock=frozen_clock).run(
            report_context=payload["report_context"],
            interpretation_result=payload["interpretation_result"],
        ).to_dict(),
        sort_keys=True,
        ensure_ascii=False,
    )
    second = json.dumps(
        ReportLayoutEngine(clock=frozen_clock).run(
            report_context=payload["report_context"],
            interpretation_result=payload["interpretation_result"],
        ).to_dict(),
        sort_keys=True,
        ensure_ascii=False,
    )
    assert first == second
    decoded = json.loads(first)
    assert "html" not in decoded
    assert "markdown" not in decoded
    assert "pdf" not in decoded
    assert decoded["sections"]
    assert decoded["layout_trace"]["theme_resolved"] == "bte.report.theme.v1"


def test_missing_interpretation_fails_without_raising() -> None:
    """Missing IX-1 result becomes PIPE-FAIL diagnostics only."""
    payload = assemble_layout_inputs()
    result = ReportLayoutEngine(clock=frozen_clock).run(
        report_context=payload["report_context"],
        interpretation_result=None,
    )
    assert result.success is False
    assert any(item.code == "PIPE-FAIL" for item in result.layout_diagnostics)
    assert result.errors

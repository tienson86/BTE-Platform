"""Regression: RE-1 / RE-2 / RE-3 remain unchanged after RX-1."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from engines.report_engine.context.canonical_report_context import build_report_context
from engines.report_engine.contracts.report_contracts import (
    empty_report_result,
    report_foundation_contract,
)
from engines.report_engine.layout.layout_engine import ReportLayoutEngine
from engines.report_engine.pipeline.canonical_report_pipeline import CanonicalReportPipeline
from engines.report_engine.pipeline.report_audit import AUDIT_SCHEMA_KEYS
from engines.report_engine.pipeline.report_trace import STEP_SCHEMA_KEYS, TRACE_SCHEMA_KEYS
from engines.report_engine.rendering.rendering_engine import ReportRenderingEngine
from tests.report_engine.re1_snapshots import ax2_snapshot, ax3_snapshot, ax4_snapshot
from tests.report_engine.re2_support import assemble_layout_inputs, frozen_clock
from tests.report_engine.re3_support import frozen_render_clock

RE1_FOUNDATION_CONTRACT_CHECKSUM = (
    "8a08a585c9bef57c33f2dffc245325cf7ebeff0644500ab4753082502131c8c4"
)

RE2_TRACE_KEYS: tuple[str, ...] = (
    "layout_version",
    "document_created",
    "sections_created",
    "blocks_created",
    "theme_resolved",
    "layout_resolved",
    "assets_resolved",
    "toc_built",
    "started_at",
    "completed_at",
    "stage_order",
)

RE2_AUDIT_KEYS: tuple[str, ...] = (
    "contract_validation",
    "layout_legality",
    "theme_legality",
    "asset_legality",
    "registry_validation",
    "version_compatibility",
    "reason_codes",
)

RE3_TRACE_KEYS: tuple[str, ...] = (
    "render_version",
    "renderer_selected",
    "layout_consumed",
    "assets_resolved",
    "artifact_created",
    "started_at",
    "completed_at",
)

RE3_AUDIT_KEYS: tuple[str, ...] = (
    "contract_validation",
    "renderer_legality",
    "layout_legality",
    "asset_legality",
    "deterministic_rendering",
    "version_compatibility",
    "reason_codes",
)


def _clock() -> datetime:
    return datetime(2026, 8, 9, 12, 0, 0, tzinfo=timezone.utc)


def _checksum(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def test_re1_foundation_checksum_and_contract_unchanged() -> None:
    """RE-1 foundation contract, empty shell, and independent context stay sealed."""
    contract = report_foundation_contract()
    assert contract["report_version"] == "1.0.0"
    assert contract["rendering"] is False
    assert contract["export"] is False
    assert contract["packages_loaded"] is False
    assert _checksum(contract) == RE1_FOUNDATION_CONTRACT_CHECKSUM
    shell = empty_report_result()
    payload = shell.to_dict()
    assert payload["status"] == "empty"
    assert payload["sections"] == []
    assert "RE1-EMPTY-SHELL" in payload["diagnostics"]
    context = build_report_context(
        analysis_result=ax2_snapshot(),
        decision_result=ax3_snapshot(),
        luck_result=ax4_snapshot(),
        interpretation_result={"interpretation_pipeline_version": "1.0.0"},
    )
    assert context.to_dict()["report_version"] == "1.0.0"


def test_re2_layout_trace_and_audit_unchanged() -> None:
    """RE-2 published layout, trace, and audit remain independently executable."""
    payload = assemble_layout_inputs()
    result = ReportLayoutEngine(clock=frozen_clock).run(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    assert result.success is True
    assert result.layout_version == "1.0.0"
    serialized = result.to_dict()
    for name in ("document", "sections", "blocks", "theme", "layout", "assets", "toc"):
        assert name in serialized
    assert result.layout_trace is not None
    assert result.layout_audit is not None
    assert tuple(result.layout_trace.to_dict()) == RE2_TRACE_KEYS
    assert tuple(result.layout_audit.to_dict()) == RE2_AUDIT_KEYS
    assert result.layout_audit.contract_validation == "pass"


def test_re3_rendering_trace_and_audit_unchanged() -> None:
    """RE-3 published artifact, trace, and audit remain independently executable."""
    payload = assemble_layout_inputs()
    layout = ReportLayoutEngine(clock=frozen_clock).run(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    result = ReportRenderingEngine(clock=frozen_render_clock).run(layout=layout, renderer="json")
    assert result.success is True
    assert result.render_version == "1.0.0"
    serialized = result.to_dict()
    for name in ("artifact_id", "renderer", "mime_type", "content", "render_trace", "render_audit"):
        assert name in serialized
    assert result.render_trace is not None
    assert result.render_audit is not None
    assert tuple(result.render_trace.to_dict()) == RE3_TRACE_KEYS
    assert tuple(result.render_audit.to_dict()) == RE3_AUDIT_KEYS
    assert result.render_audit.deterministic_rendering is True


def test_rx1_trace_and_audit_schemas_stable() -> None:
    """RX-1 trace and audit schemas publish the frozen key sets."""
    payload = assemble_layout_inputs()
    result = CanonicalReportPipeline(clock=_clock).run(
        analysis_result=payload["analysis_result"],
        decision_result=payload["decision_result"],
        luck_result=payload["luck_result"],
        interpretation_result=payload["interpretation_result"],
    )
    assert result.report_trace is not None
    assert result.report_audit is not None
    assert tuple(result.report_trace.to_dict()) == TRACE_SCHEMA_KEYS
    assert tuple(result.report_audit.to_dict()) == AUDIT_SCHEMA_KEYS
    assert tuple(result.report_trace.steps[0].to_dict()) == STEP_SCHEMA_KEYS

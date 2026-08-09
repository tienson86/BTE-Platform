"""RE-3 rendering engine integration, serialization, and determinism tests."""

from __future__ import annotations

import json

from engines.report_engine.rendering.renderer_registry import ACTIVE_RENDERERS
from engines.report_engine.rendering.rendering_engine import ReportRenderingEngine
from engines.report_engine.rendering.rendering_result import (
    DIAG_ASSET_MISSING,
    DIAG_LAYOUT_MISSING,
    DIAG_PIPE_OK,
    DIAG_RENDERER_MISSING,
    CanonicalReportArtifact,
)
from tests.report_engine.re3_support import (
    assemble_canonical_layout,
    frozen_render_clock,
    layout_without_assets,
)


def test_rendering_engine_exports_all_enabled_renderers() -> None:
    """Each enabled renderer produces a successful canonical artifact."""
    layout = assemble_canonical_layout()
    for renderer_id in ACTIVE_RENDERERS:
        result = ReportRenderingEngine(clock=frozen_render_clock).run(
            layout=layout,
            renderer=renderer_id,
        )
        assert isinstance(result, CanonicalReportArtifact)
        assert result.success is True
        assert result.render_version == "1.0.0"
        assert result.renderer == renderer_id
        assert result.content
        assert result.artifact_id == f"ART-{renderer_id}-1"
        assert any(item.code == DIAG_PIPE_OK for item in result.render_diagnostics)
        assert result.render_audit is not None
        assert result.render_audit.deterministic_rendering is True
        assert result.render_trace is not None
        assert result.render_trace.started_at == "2026-08-09T12:00:00Z"
        assert result.metadata["filesystem"] is False


def test_serialization_and_determinism() -> None:
    """Repeated JSON renders with a frozen clock yield identical output."""
    layout = assemble_canonical_layout()
    first = json.dumps(
        ReportRenderingEngine(clock=frozen_render_clock).run(layout=layout, renderer="json").to_dict(),
        sort_keys=True,
        ensure_ascii=False,
    )
    second = json.dumps(
        ReportRenderingEngine(clock=frozen_render_clock).run(layout=layout, renderer="json").to_dict(),
        sort_keys=True,
        ensure_ascii=False,
    )
    assert first == second
    decoded = json.loads(first)
    assert decoded["mime_type"] == "application/json"
    assert "html" not in decoded["content"] or decoded["renderer"] == "json"


def test_missing_layout_fails_without_raising() -> None:
    """Missing CanonicalReportLayout becomes LAYOUT-MISSING diagnostics only."""
    result = ReportRenderingEngine(clock=frozen_render_clock).run(layout=None)
    assert result.success is False
    assert any(item.code == DIAG_LAYOUT_MISSING for item in result.render_diagnostics)
    assert any(item.code == "PIPE-FAIL" for item in result.render_diagnostics)
    assert result.errors


def test_missing_renderer_fails_without_raising() -> None:
    """Unknown or disabled renderer becomes RENDERER-MISSING diagnostics only."""
    layout = assemble_canonical_layout()
    result = ReportRenderingEngine(clock=frozen_render_clock).run(
        layout=layout,
        renderer="xlsx",
    )
    assert result.success is False
    assert any(item.code == DIAG_RENDERER_MISSING for item in result.render_diagnostics)


def test_missing_assets_fail_without_raising() -> None:
    """Layout blocks with unresolved assets become ASSET-MISSING."""
    result = ReportRenderingEngine(clock=frozen_render_clock).run(
        layout=layout_without_assets(),
        renderer="json",
    )
    assert result.success is False
    assert any(item.code == DIAG_ASSET_MISSING for item in result.render_diagnostics)

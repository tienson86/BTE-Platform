"""RE-3 Rendering & Export Engine. Never raises to API."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.export_manager import ExportManager
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.renderer_registry import RENDERER_JSON, RendererRegistry
from engines.report_engine.rendering.rendering_context import (
    RENDER_ENGINE_ID,
    RENDER_VERSION,
    RenderingError,
    build_rendering_context,
)
from engines.report_engine.rendering.rendering_result import (
    DIAG_ASSET_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_EXPORT_FAILED,
    DIAG_LAYOUT_MISSING,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_RENDERER_MISSING,
    CanonicalReportArtifact,
    RenderDiagnostic,
    build_audit,
    build_trace,
)
from engines.report_engine.rendering.validation import validate_rendering

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ReportRenderingEngine:
    """Render CanonicalReportLayout into an in-memory CanonicalReportArtifact."""

    engine_id: str = RENDER_ENGINE_ID
    render_version: str = RENDER_VERSION

    def __init__(
        self,
        *,
        registry: RendererRegistry | None = None,
        embedder: AssetEmbedder | None = None,
        exporter: ExportManager | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize deterministic rendering collaborators."""
        self._registry = registry or RendererRegistry.default()
        self._embedder = embedder or AssetEmbedder()
        self._exporter = exporter or ExportManager(registry=self._registry)
        self._clock = clock or _utc_now

    def run(
        self,
        *,
        layout: Any = None,
        renderer: str = RENDERER_JSON,
        context: Any = None,
    ) -> CanonicalReportArtifact:
        """Render one layout with one renderer. Failures become diagnostics."""
        started_at = _iso(self._clock())
        diagnostics: list[RenderDiagnostic] = []
        errors: list[str] = []
        artifact = None
        model = None
        assets = ()
        success = False
        render_context = context
        renderer_id = renderer
        try:
            if layout is None and context is None:
                raise RenderingError(DIAG_LAYOUT_MISSING)
            render_context = context or build_rendering_context(
                layout=layout,
                renderer_id=renderer_id,
            )
            renderer_id = render_context.renderer_id
            self._registry.require_enabled(renderer_id)
            assets = self._embedder.embed(render_context)
            render_context.publish("assets", [item.to_dict() for item in assets])
            model = build_render_model(render_context, assets=assets)
            render_context.publish("render_model", model.to_dict())
            artifact = self._exporter.export(renderer_id=renderer_id, model=model)
            render_context.publish("artifact", artifact.to_dict())
            report = validate_rendering(
                context=render_context,
                registry=self._registry,
                model=model,
                artifact=artifact,
            )
            diagnostics.extend(report.diagnostics)
            if report.success:
                diagnostics.append(
                    RenderDiagnostic(DIAG_PIPE_OK, "Report rendering passed", "info")
                )
                success = True
            else:
                diagnostics.append(RenderDiagnostic(DIAG_PIPE_FAIL, "Report rendering failed"))
                errors.append(str(report.details.get("error") or "render_failed"))
        except RenderingError as exc:
            logger.warning("report_rendering_failed %s", exc)
            code = _map_error(str(exc))
            diagnostics.append(RenderDiagnostic(code, str(exc)))
            diagnostics.append(RenderDiagnostic(DIAG_PIPE_FAIL, str(exc)))
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("report_rendering_unexpected")
            diagnostics.append(RenderDiagnostic(DIAG_PIPE_FAIL, DIAG_PIPE_FAIL))
            errors.append(str(exc))

        completed_at = _iso(self._clock())
        layout_id = None
        if render_context is not None:
            document = render_context.layout_snapshot().get("document") or {}
            if isinstance(document, dict):
                layout_id = document.get("document_id")
        metadata = {
            "render_version": RENDER_VERSION,
            "engine_id": RENDER_ENGINE_ID,
            "filesystem": False,
            "persistence": False,
            "printing": False,
        }
        if artifact is not None:
            metadata.update(artifact.metadata)
        return CanonicalReportArtifact(
            success=success,
            artifact_id=None if artifact is None else artifact.artifact_id,
            renderer=None if artifact is None else artifact.renderer,
            mime_type=None if artifact is None else artifact.mime_type,
            content=None if artifact is None else artifact.content,
            metadata=metadata,
            assets=tuple(item.to_dict() for item in assets),
            render_trace=build_trace(
                renderer_id=renderer_id,
                layout_id=layout_id,
                assets=tuple(item.asset_id for item in assets),
                artifact=artifact,
                started_at=started_at,
                completed_at=completed_at,
            ),
            render_audit=build_audit(diagnostics),
            render_diagnostics=tuple(diagnostics),
            errors=tuple(errors),
        )


def _map_error(message: str) -> str:
    if message.startswith("missing_canonical_report_layout") or message == DIAG_LAYOUT_MISSING:
        return DIAG_LAYOUT_MISSING
    if "renderer" in message:
        return DIAG_RENDERER_MISSING
    if "asset" in message:
        return DIAG_ASSET_MISSING
    if "export" in message or "mime_mismatch" in message:
        return DIAG_EXPORT_FAILED
    if "contract" in message:
        return DIAG_CONTRACT_VIOLATION
    return DIAG_EXPORT_FAILED

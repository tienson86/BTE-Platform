"""RE-3 rendering validation. No business-rule checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import (
    ACTIVE_RENDERERS,
    FUTURE_RENDERERS,
    RendererRegistry,
)
from engines.report_engine.rendering.rendering_context import (
    REQUIRED_LAYOUT_VERSION,
    RenderingContext,
)
from engines.report_engine.rendering.rendering_result import (
    DIAG_ASSET_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_EXPORT_FAILED,
    DIAG_LAYOUT_MISSING,
    DIAG_RENDERER_MISSING,
    RenderDiagnostic,
)


@dataclass(slots=True)
class RenderingValidationReport:
    """Machine-readable RE-3 validation report."""

    success: bool
    diagnostics: tuple[RenderDiagnostic, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the validation report."""
        return {
            "success": self.success,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "details": dict(self.details),
        }


def _diagnostic(code: str, message: str, **details: Any) -> RenderDiagnostic:
    return RenderDiagnostic(code=code, message=message, details=dict(details))


def validate_registry(registry: RendererRegistry) -> None:
    """Require active renderers enabled and future renderers disabled."""
    if registry.enabled_ids() != ACTIVE_RENDERERS:
        raise ValueError("registry_renderer_mismatch")
    if registry.disabled_ids() != FUTURE_RENDERERS:
        raise ValueError("registry_future_mismatch")


def validate_layout_compatibility(context: RenderingContext) -> None:
    """Require a successful RE-2 layout snapshot at version 1.0.0."""
    layout = context.layout_snapshot()
    if not layout:
        raise ValueError(DIAG_LAYOUT_MISSING)
    if layout.get("success") is False:
        raise ValueError(DIAG_LAYOUT_MISSING)
    if str(layout.get("layout_version") or "") != REQUIRED_LAYOUT_VERSION:
        raise ValueError(f"layout_version_incompatible:{layout.get('layout_version')}")
    if not layout.get("document"):
        raise ValueError(DIAG_LAYOUT_MISSING)


def validate_renderer_compatibility(registry: RendererRegistry, renderer_id: str) -> None:
    """Require an enabled renderer with a declared mime type."""
    try:
        record = registry.require_enabled(renderer_id)
    except Exception as exc:
        raise ValueError(DIAG_RENDERER_MISSING) from exc
    if not record.mime_type:
        raise ValueError(DIAG_CONTRACT_VIOLATION)


def validate_mime_type(artifact: RenderArtifact, registry: RendererRegistry) -> None:
    """Require artifact mime type to match the registry."""
    record = registry.get(artifact.renderer)
    if artifact.mime_type != record.mime_type:
        raise ValueError(f"mime_mismatch:{artifact.mime_type}")


def validate_assets(model: RenderModel) -> None:
    """Require unique assets and block asset ids to resolve."""
    ids = [item.asset_id for item in model.assets]
    if len(ids) != len(set(ids)):
        raise ValueError(DIAG_ASSET_MISSING)
    pool = set(ids)
    for block in model.blocks:
        for asset_id in block.asset_ids:
            if asset_id not in pool:
                raise ValueError(DIAG_ASSET_MISSING)


def validate_rendering(
    *,
    context: RenderingContext,
    registry: RendererRegistry,
    model: RenderModel,
    artifact: RenderArtifact,
) -> RenderingValidationReport:
    """Run the RE-3 validation suite and map failures to diagnostics."""
    diagnostics: list[RenderDiagnostic] = []
    try:
        validate_registry(registry)
        validate_layout_compatibility(context)
        validate_renderer_compatibility(registry, context.renderer_id)
        validate_mime_type(artifact, registry)
        validate_assets(model)
        if artifact.renderer != context.renderer_id:
            raise ValueError(DIAG_EXPORT_FAILED)
        return RenderingValidationReport(success=True, diagnostics=tuple(diagnostics))
    except ValueError as exc:
        message = str(exc)
        if message == DIAG_LAYOUT_MISSING:
            diagnostics.append(_diagnostic(DIAG_LAYOUT_MISSING, "CanonicalReportLayout missing"))
        elif message == DIAG_RENDERER_MISSING:
            diagnostics.append(_diagnostic(DIAG_RENDERER_MISSING, "Renderer missing or disabled"))
        elif message == DIAG_ASSET_MISSING:
            diagnostics.append(_diagnostic(DIAG_ASSET_MISSING, "Missing asset reference"))
        elif message == DIAG_EXPORT_FAILED:
            diagnostics.append(_diagnostic(DIAG_EXPORT_FAILED, "Export failed"))
        else:
            diagnostics.append(
                _diagnostic(DIAG_CONTRACT_VIOLATION, "Rendering contract failed", error=message)
            )
        return RenderingValidationReport(
            success=False,
            diagnostics=tuple(diagnostics),
            details={"error": message},
        )

"""Canonical Report Artifact. The only official RE-3 rendering output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.report_engine.rendering.render_model import RenderArtifact
from engines.report_engine.rendering.rendering_context import RENDER_ENGINE_ID, RENDER_VERSION

DIAG_RENDERER_MISSING = "RENDERER-MISSING"
DIAG_LAYOUT_MISSING = "LAYOUT-MISSING"
DIAG_ASSET_MISSING = "ASSET-MISSING"
DIAG_EXPORT_FAILED = "EXPORT-FAILED"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"


@dataclass(slots=True)
class RenderDiagnostic:
    """Structured rendering diagnostic. No exception payload."""

    code: str
    message: str
    severity: str = "error"
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize one diagnostic."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "details": dict(self.details),
        }


@dataclass(slots=True)
class RenderTrace:
    """Machine-readable RE-3 execution trace."""

    render_version: str = RENDER_VERSION
    renderer_selected: str | None = None
    layout_consumed: str | None = None
    assets_resolved: tuple[str, ...] = ()
    artifact_created: str | None = None
    started_at: str | None = None
    completed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the render trace."""
        return {
            "render_version": self.render_version,
            "renderer_selected": self.renderer_selected,
            "layout_consumed": self.layout_consumed,
            "assets_resolved": list(self.assets_resolved),
            "artifact_created": self.artifact_created,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass(slots=True)
class RenderAudit:
    """Machine-readable RE-3 legality audit."""

    contract_validation: str
    renderer_legality: str
    layout_legality: str
    asset_legality: str
    deterministic_rendering: bool
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the render audit."""
        return {
            "contract_validation": self.contract_validation,
            "renderer_legality": self.renderer_legality,
            "layout_legality": self.layout_legality,
            "asset_legality": self.asset_legality,
            "deterministic_rendering": self.deterministic_rendering,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(slots=True)
class CanonicalReportArtifact:
    """Official rendering output produced by the Rendering & Export Engine."""

    render_version: str = RENDER_VERSION
    engine_id: str = RENDER_ENGINE_ID
    success: bool = True
    artifact_id: str | None = None
    renderer: str | None = None
    mime_type: str | None = None
    content: str | None = None
    metadata: dict[str, Any] | None = None
    assets: tuple[dict[str, Any], ...] = ()
    render_trace: RenderTrace | None = None
    render_audit: RenderAudit | None = None
    render_diagnostics: tuple[RenderDiagnostic, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical report artifact."""
        return {
            "render_version": self.render_version,
            "engine_id": self.engine_id,
            "success": self.success,
            "artifact_id": self.artifact_id,
            "renderer": self.renderer,
            "mime_type": self.mime_type,
            "content": self.content,
            "metadata": dict(self.metadata or {}),
            "assets": [dict(item) for item in self.assets],
            "render_trace": None if self.render_trace is None else self.render_trace.to_dict(),
            "render_audit": None if self.render_audit is None else self.render_audit.to_dict(),
            "render_diagnostics": [item.to_dict() for item in self.render_diagnostics],
            "errors": list(self.errors),
        }


def build_audit(diagnostics: Sequence[RenderDiagnostic]) -> RenderAudit:
    """Derive audit flags from diagnostic codes."""
    codes = {item.code for item in diagnostics if item.severity == "error"}
    info_codes = tuple(item.code for item in diagnostics)

    def flag(error_code: str) -> str:
        return "fail" if error_code in codes else "pass"

    version_fail = DIAG_CONTRACT_VIOLATION in codes and any(
        "version" in str(item.details.get("error", item.message)) for item in diagnostics
    )
    return RenderAudit(
        contract_validation=flag(DIAG_CONTRACT_VIOLATION),
        renderer_legality=flag(DIAG_RENDERER_MISSING),
        layout_legality=flag(DIAG_LAYOUT_MISSING),
        asset_legality=flag(DIAG_ASSET_MISSING),
        deterministic_rendering=True,
        version_compatibility="fail" if version_fail else "pass",
        reason_codes=info_codes,
    )


def build_trace(
    *,
    renderer_id: str | None,
    layout_id: str | None,
    assets: Sequence[str],
    artifact: RenderArtifact | None,
    started_at: str | None,
    completed_at: str | None,
) -> RenderTrace:
    """Assemble the machine-readable render trace."""
    return RenderTrace(
        renderer_selected=renderer_id,
        layout_consumed=layout_id,
        assets_resolved=tuple(assets),
        artifact_created=None if artifact is None else artifact.artifact_id,
        started_at=started_at,
        completed_at=completed_at,
    )

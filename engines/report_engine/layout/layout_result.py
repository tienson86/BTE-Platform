"""Canonical Report Layout result. No presentation formats."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.report_engine.layout.asset_resolver import LayoutAsset
from engines.report_engine.layout.block_builder import LayoutBlock
from engines.report_engine.layout.document_builder import DocumentLayout
from engines.report_engine.layout.layout_context import LAYOUT_ENGINE_ID, LAYOUT_VERSION
from engines.report_engine.layout.layout_resolver import LayoutResolution
from engines.report_engine.layout.section_builder import LayoutSection
from engines.report_engine.layout.theme_resolver import ThemeResolution
from engines.report_engine.layout.toc_builder import TableOfContents

DIAG_BLOCK_DUPLICATE = "BLOCK-DUPLICATE"
DIAG_SECTION_DUPLICATE = "SECTION-DUPLICATE"
DIAG_ASSET_MISSING = "ASSET-MISSING"
DIAG_LAYOUT_VIOLATION = "LAYOUT-VIOLATION"
DIAG_THEME_VIOLATION = "THEME-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"


@dataclass(slots=True)
class LayoutDiagnostic:
    """Structured layout diagnostic. No exception payload."""

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
class LayoutTrace:
    """Machine-readable RE-2 execution trace."""

    layout_version: str = LAYOUT_VERSION
    document_created: str | None = None
    sections_created: tuple[str, ...] = ()
    blocks_created: tuple[str, ...] = ()
    theme_resolved: str | None = None
    layout_resolved: dict[str, Any] = field(default_factory=dict)
    assets_resolved: tuple[str, ...] = ()
    toc_built: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    stage_order: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the layout trace."""
        return {
            "layout_version": self.layout_version,
            "document_created": self.document_created,
            "sections_created": list(self.sections_created),
            "blocks_created": list(self.blocks_created),
            "theme_resolved": self.theme_resolved,
            "layout_resolved": dict(self.layout_resolved),
            "assets_resolved": list(self.assets_resolved),
            "toc_built": self.toc_built,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "stage_order": list(self.stage_order),
        }


@dataclass(slots=True)
class LayoutAudit:
    """Machine-readable RE-2 legality audit."""

    contract_validation: str
    layout_legality: str
    theme_legality: str
    asset_legality: str
    registry_validation: str
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the layout audit."""
        return {
            "contract_validation": self.contract_validation,
            "layout_legality": self.layout_legality,
            "theme_legality": self.theme_legality,
            "asset_legality": self.asset_legality,
            "registry_validation": self.registry_validation,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(slots=True)
class CanonicalReportLayout:
    """Official layout model produced by the Layout & Theme Composition Engine."""

    layout_version: str = LAYOUT_VERSION
    engine_id: str = LAYOUT_ENGINE_ID
    success: bool = True
    document: DocumentLayout | None = None
    sections: tuple[LayoutSection, ...] = ()
    blocks: tuple[LayoutBlock, ...] = ()
    theme: ThemeResolution | None = None
    layout: LayoutResolution | None = None
    assets: tuple[LayoutAsset, ...] = ()
    toc: TableOfContents | None = None
    metadata: dict[str, Any] | None = None
    layout_trace: LayoutTrace | None = None
    layout_audit: LayoutAudit | None = None
    layout_diagnostics: tuple[LayoutDiagnostic, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical report layout."""
        return {
            "layout_version": self.layout_version,
            "engine_id": self.engine_id,
            "success": self.success,
            "document": None if self.document is None else self.document.to_dict(),
            "sections": [item.to_dict() for item in self.sections],
            "blocks": [item.to_dict() for item in self.blocks],
            "theme": None if self.theme is None else self.theme.to_dict(),
            "layout": None if self.layout is None else self.layout.to_dict(),
            "assets": [item.to_dict() for item in self.assets],
            "toc": None if self.toc is None else self.toc.to_dict(),
            "metadata": dict(self.metadata or {}),
            "layout_trace": None if self.layout_trace is None else self.layout_trace.to_dict(),
            "layout_audit": None if self.layout_audit is None else self.layout_audit.to_dict(),
            "layout_diagnostics": [item.to_dict() for item in self.layout_diagnostics],
            "errors": list(self.errors),
        }


def build_audit(diagnostics: Sequence[LayoutDiagnostic]) -> LayoutAudit:
    """Derive audit flags from diagnostic codes."""
    codes = {item.code for item in diagnostics if item.severity == "error"}
    info_codes = tuple(item.code for item in diagnostics)

    def flag(error_code: str) -> str:
        return "fail" if error_code in codes else "pass"

    version_fail = DIAG_CONTRACT_VIOLATION in codes and any(
        "version" in str(item.details.get("error", item.message)) for item in diagnostics
    )
    return LayoutAudit(
        contract_validation=flag(DIAG_CONTRACT_VIOLATION),
        layout_legality=flag(DIAG_LAYOUT_VIOLATION),
        theme_legality=flag(DIAG_THEME_VIOLATION),
        asset_legality=flag(DIAG_ASSET_MISSING),
        registry_validation="fail" if DIAG_CONTRACT_VIOLATION in codes else "pass",
        version_compatibility="fail" if version_fail else "pass",
        reason_codes=info_codes,
    )


def build_trace(
    *,
    document: DocumentLayout | None,
    sections: Sequence[LayoutSection],
    blocks: Sequence[LayoutBlock],
    theme: ThemeResolution | None,
    layout: LayoutResolution | None,
    assets: Sequence[LayoutAsset],
    toc: TableOfContents | None,
    started_at: str | None,
    completed_at: str | None,
    stage_order: Sequence[str],
) -> LayoutTrace:
    """Assemble the machine-readable layout trace."""
    return LayoutTrace(
        document_created=None if document is None else document.document_id,
        sections_created=tuple(item.section_id for item in sections),
        blocks_created=tuple(item.block_id for item in blocks),
        theme_resolved=None if theme is None else theme.theme_id,
        layout_resolved={} if layout is None else layout.to_dict(),
        assets_resolved=tuple(item.asset_id for item in assets),
        toc_built=None if toc is None else toc.toc_id,
        started_at=started_at,
        completed_at=completed_at,
        stage_order=tuple(stage_order),
    )

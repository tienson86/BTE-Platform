"""RE-2 layout validation. No presentation checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.report_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    MODULE_COVER,
    MODULE_SUMMARY,
    REPORT_VERSION,
    REQUIRED_ANALYSIS_PIPELINE_VERSION,
    REQUIRED_DECISION_PIPELINE_VERSION,
    REQUIRED_INTERPRETATION_PIPELINE_VERSION,
    REQUIRED_LUCK_PIPELINE_VERSION,
)
from engines.report_engine.layout.asset_resolver import LayoutAsset
from engines.report_engine.layout.block_builder import SUPPORTED_BLOCK_TYPES, LayoutBlock
from engines.report_engine.layout.document_builder import DocumentLayout
from engines.report_engine.layout.layout_context import LAYOUT_VERSION, LayoutContext
from engines.report_engine.layout.layout_registry import CANONICAL_STAGE_ORDER, LayoutRegistry
from engines.report_engine.layout.layout_resolver import LayoutResolution
from engines.report_engine.layout.layout_result import (
    DIAG_ASSET_MISSING,
    DIAG_BLOCK_DUPLICATE,
    DIAG_CONTRACT_VIOLATION,
    DIAG_LAYOUT_VIOLATION,
    DIAG_SECTION_DUPLICATE,
    DIAG_THEME_VIOLATION,
    LayoutDiagnostic,
)
from engines.report_engine.layout.section_builder import LayoutSection
from engines.report_engine.layout.theme_resolver import THEME_ID, ThemeResolution


@dataclass(slots=True)
class LayoutValidationReport:
    """Machine-readable RE-2 validation report."""

    success: bool
    diagnostics: tuple[LayoutDiagnostic, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the validation report."""
        return {
            "success": self.success,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "details": dict(self.details),
        }


def _diagnostic(code: str, message: str, **details: Any) -> LayoutDiagnostic:
    return LayoutDiagnostic(code=code, message=message, details=dict(details))


def validate_versions(context: LayoutContext) -> None:
    """Require RE-1 / AX-2 / AX-3 / AX-4 / IX-1 / RE-2 versions."""
    analysis = str(context.analysis_snapshot().get("pipeline_version") or "")
    decision = str(context.decision_snapshot().get("decision_pipeline_version") or "")
    luck = str(context.luck_snapshot().get("luck_pipeline_version") or "")
    interpretation = context.interpretation_snapshot()
    interp_version = str(
        interpretation.get("interpretation_pipeline_version")
        or interpretation.get("interpretation_version")
        or ""
    )
    if context.layout_version != LAYOUT_VERSION:
        raise ValueError(f"layout_version_incompatible:{context.layout_version}")
    if context.report_version != REPORT_VERSION:
        raise ValueError(f"report_version_incompatible:{context.report_version}")
    if analysis != REQUIRED_ANALYSIS_PIPELINE_VERSION:
        raise ValueError(f"analysis_pipeline_incompatible:{analysis}")
    if decision != REQUIRED_DECISION_PIPELINE_VERSION:
        raise ValueError(f"decision_pipeline_incompatible:{decision}")
    if luck != REQUIRED_LUCK_PIPELINE_VERSION:
        raise ValueError(f"luck_pipeline_incompatible:{luck}")
    if interp_version != REQUIRED_INTERPRETATION_PIPELINE_VERSION:
        raise ValueError(f"interpretation_pipeline_incompatible:{interp_version}")


def validate_registry(registry: LayoutRegistry) -> None:
    """Require the canonical deterministic layout catalog."""
    if registry.registered_ids() != CANONICAL_STAGE_ORDER:
        raise ValueError("registry_stage_mismatch")
    if registry.resolve_order() != CANONICAL_STAGE_ORDER:
        raise ValueError("registry_order_mismatch")


def validate_section_integrity(sections: Sequence[LayoutSection]) -> None:
    """Reject duplicate section ids and unknown modules."""
    ids = [item.section_id for item in sections]
    if len(ids) != len(set(ids)):
        raise ValueError(DIAG_SECTION_DUPLICATE)
    for item in sections:
        if item.module_id not in CANONICAL_MODULE_ORDER:
            raise ValueError(f"unknown_section_module:{item.module_id}")
    module_ids = [item.module_id for item in sections]
    if module_ids != list(CANONICAL_MODULE_ORDER):
        raise ValueError(DIAG_LAYOUT_VIOLATION)


def validate_block_hierarchy(
    blocks: Sequence[LayoutBlock],
    sections: Sequence[LayoutSection],
) -> None:
    """Require unique blocks that belong to known sections and types."""
    ids = [item.block_id for item in blocks]
    if len(ids) != len(set(ids)):
        raise ValueError(DIAG_BLOCK_DUPLICATE)
    section_ids = {item.section_id for item in sections}
    for item in blocks:
        if item.section_id not in section_ids:
            raise ValueError(DIAG_LAYOUT_VIOLATION)
        if item.block_type not in SUPPORTED_BLOCK_TYPES:
            raise ValueError(DIAG_LAYOUT_VIOLATION)


def validate_layout_hierarchy(
    document: DocumentLayout,
    sections: Sequence[LayoutSection],
    layout: LayoutResolution,
) -> None:
    """Require cover-first page hierarchy matching document pages."""
    section_ids = [item.section_id for item in sections]
    page_ids = [page.page_id for page in document.pages]
    if list(layout.page_hierarchy) != page_ids:
        raise ValueError(DIAG_LAYOUT_VIOLATION)
    if sections and sections[0].module_id != MODULE_COVER:
        raise ValueError(DIAG_LAYOUT_VIOLATION)
    if sections and sections[-1].module_id != MODULE_SUMMARY:
        raise ValueError(DIAG_LAYOUT_VIOLATION)
    known_pages = set(page_ids)
    for section in sections:
        if section.page_id not in known_pages:
            raise ValueError(DIAG_LAYOUT_VIOLATION)
        if section.section_id not in section_ids:
            raise ValueError(DIAG_LAYOUT_VIOLATION)


def validate_assets(
    assets: Sequence[LayoutAsset],
    blocks: Sequence[LayoutBlock],
) -> None:
    """Require unique assets and declared block references to exist."""
    ids = [item.asset_id for item in assets]
    if len(ids) != len(set(ids)):
        raise ValueError(DIAG_ASSET_MISSING)
    pool = {item.asset_id: item for item in assets}
    for block in blocks:
        for asset_id in block.asset_ids:
            asset = pool.get(asset_id)
            if asset is None or asset.status == "missing":
                raise ValueError(DIAG_ASSET_MISSING)
    if any(item.status == "missing" for item in assets):
        raise ValueError(DIAG_ASSET_MISSING)


def validate_theme(theme: ThemeResolution) -> None:
    """Admit only the frozen Foundation v1 theme identifiers."""
    ids = (theme.theme_id, theme.palette_id, theme.spacing_id, theme.typography_id, theme.icon_set_id)
    if theme.theme_id != THEME_ID or theme.status != "resolved":
        raise ValueError(DIAG_THEME_VIOLATION)
    if any(not item.startswith("bte.report.") or not item.endswith(".v1") for item in ids):
        raise ValueError(DIAG_THEME_VIOLATION)


def validate_layout(
    *,
    context: LayoutContext,
    registry: LayoutRegistry,
    document: DocumentLayout,
    sections: Sequence[LayoutSection],
    blocks: Sequence[LayoutBlock],
    theme: ThemeResolution,
    layout: LayoutResolution,
    assets: Sequence[LayoutAsset],
) -> LayoutValidationReport:
    """Run the RE-2 validation suite and map failures to diagnostics."""
    diagnostics: list[LayoutDiagnostic] = []
    try:
        validate_versions(context)
        validate_registry(registry)
        validate_section_integrity(sections)
        validate_block_hierarchy(blocks, sections)
        validate_layout_hierarchy(document, sections, layout)
        validate_theme(theme)
        validate_assets(assets, blocks)
        return LayoutValidationReport(success=True, diagnostics=tuple(diagnostics))
    except ValueError as exc:
        message = str(exc)
        if message == DIAG_SECTION_DUPLICATE:
            diagnostics.append(_diagnostic(DIAG_SECTION_DUPLICATE, "Duplicate section id"))
        elif message == DIAG_BLOCK_DUPLICATE:
            diagnostics.append(_diagnostic(DIAG_BLOCK_DUPLICATE, "Duplicate block id"))
        elif message == DIAG_ASSET_MISSING:
            diagnostics.append(_diagnostic(DIAG_ASSET_MISSING, "Missing asset reference"))
        elif message == DIAG_LAYOUT_VIOLATION:
            diagnostics.append(_diagnostic(DIAG_LAYOUT_VIOLATION, "Illegal layout hierarchy"))
        elif message == DIAG_THEME_VIOLATION:
            diagnostics.append(_diagnostic(DIAG_THEME_VIOLATION, "Illegal theme identifiers"))
        else:
            diagnostics.append(
                _diagnostic(DIAG_CONTRACT_VIOLATION, "Layout contract failed", error=message)
            )
        return LayoutValidationReport(
            success=False,
            diagnostics=tuple(diagnostics),
            details={"error": message},
        )

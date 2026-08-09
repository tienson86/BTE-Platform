"""RE-2 Layout & Theme Composition Engine. Never raises to API."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable

from engines.report_engine.foundation_constants import CANONICAL_MODULE_ORDER, REPORT_VERSION
from engines.report_engine.layout.asset_resolver import AssetResolver
from engines.report_engine.layout.block_builder import BlockBuilder
from engines.report_engine.layout.document_builder import DocumentBuilder
from engines.report_engine.layout.layout_context import (
    LAYOUT_ENGINE_ID,
    LAYOUT_VERSION,
    LayoutError,
    build_layout_context,
)
from engines.report_engine.layout.layout_registry import (
    STAGE_ASSET,
    STAGE_ASSEMBLY,
    STAGE_BLOCK,
    STAGE_DOCUMENT,
    STAGE_LAYOUT,
    STAGE_SECTION,
    STAGE_THEME,
    STAGE_TOC,
    LayoutRegistry,
)
from engines.report_engine.layout.layout_resolver import LayoutResolver
from engines.report_engine.layout.layout_result import (
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    CanonicalReportLayout,
    LayoutDiagnostic,
    build_audit,
    build_trace,
)
from engines.report_engine.layout.section_builder import SectionBuilder
from engines.report_engine.layout.theme_resolver import ThemeResolver
from engines.report_engine.layout.toc_builder import TocBuilder
from engines.report_engine.layout.validation import validate_layout

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ReportLayoutEngine:
    """Compose CanonicalInterpretationResult into CanonicalReportLayout."""

    engine_id: str = LAYOUT_ENGINE_ID
    layout_version: str = LAYOUT_VERSION

    def __init__(
        self,
        *,
        registry: LayoutRegistry | None = None,
        document_builder: DocumentBuilder | None = None,
        section_builder: SectionBuilder | None = None,
        block_builder: BlockBuilder | None = None,
        theme_resolver: ThemeResolver | None = None,
        layout_resolver: LayoutResolver | None = None,
        asset_resolver: AssetResolver | None = None,
        toc_builder: TocBuilder | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize deterministic layout collaborators."""
        self._registry = registry or LayoutRegistry.default()
        self._document = document_builder or DocumentBuilder()
        self._sections = section_builder or SectionBuilder()
        self._blocks = block_builder or BlockBuilder()
        self._theme = theme_resolver or ThemeResolver()
        self._layout = layout_resolver or LayoutResolver()
        self._assets = asset_resolver or AssetResolver()
        self._toc = toc_builder or TocBuilder()
        self._clock = clock or _utc_now

    def run(
        self,
        *,
        report_context: Any = None,
        interpretation_result: Any = None,
        analysis_result: Any = None,
        decision_result: Any = None,
        luck_result: Any = None,
        context: Any = None,
    ) -> CanonicalReportLayout:
        """Assemble the official report layout. Failures become diagnostics."""
        started_at = _iso(self._clock())
        diagnostics: list[LayoutDiagnostic] = []
        errors: list[str] = []
        document = None
        sections = ()
        blocks = ()
        theme = None
        layout = None
        assets = ()
        toc = None
        stage_order: tuple[str, ...] = ()
        success = False
        layout_context = context
        try:
            layout_context = context or build_layout_context(
                report_context=report_context,
                interpretation_result=interpretation_result,
                analysis_result=analysis_result,
                decision_result=decision_result,
                luck_result=luck_result,
            )
            stage_order = self._registry.resolve_order()
            document = self._document.build(layout_context)
            layout_context.publish(STAGE_DOCUMENT, document.to_dict())
            sections = self._sections.build(layout_context)
            layout_context.publish(STAGE_SECTION, [item.to_dict() for item in sections])
            blocks = self._blocks.build(sections)
            layout_context.publish(STAGE_BLOCK, [item.to_dict() for item in blocks])
            theme = self._theme.resolve(layout_context)
            layout_context.publish(STAGE_THEME, theme.to_dict())
            layout = self._layout.resolve(document, sections, blocks)
            layout_context.publish(STAGE_LAYOUT, layout.to_dict())
            assets = self._assets.resolve(layout_context, blocks)
            layout_context.publish(STAGE_ASSET, [item.to_dict() for item in assets])
            toc = self._toc.build(sections)
            layout_context.publish(STAGE_TOC, toc.to_dict())
            report = validate_layout(
                context=layout_context,
                registry=self._registry,
                document=document,
                sections=sections,
                blocks=blocks,
                theme=theme,
                layout=layout,
                assets=assets,
            )
            diagnostics.extend(report.diagnostics)
            if report.success:
                diagnostics.append(
                    LayoutDiagnostic(DIAG_PIPE_OK, "Report layout composition passed", "info")
                )
                success = True
            else:
                diagnostics.append(LayoutDiagnostic(DIAG_PIPE_FAIL, "Report layout composition failed"))
                errors.append(str(report.details.get("error") or "layout_failed"))
            layout_context.publish(STAGE_ASSEMBLY, {"success": success})
        except LayoutError as exc:
            logger.warning("report_layout_failed %s", exc)
            diagnostics.append(LayoutDiagnostic(DIAG_PIPE_FAIL, str(exc)))
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("report_layout_unexpected")
            diagnostics.append(LayoutDiagnostic(DIAG_PIPE_FAIL, DIAG_PIPE_FAIL))
            errors.append(str(exc))

        completed_at = _iso(self._clock())
        metadata = {
            "report_version": REPORT_VERSION,
            "layout_version": LAYOUT_VERSION,
            "engine_id": LAYOUT_ENGINE_ID,
            "module_ids": list(CANONICAL_MODULE_ORDER),
            "rendering": False,
            "export": False,
            "html": False,
            "pdf": False,
            "docx": False,
            "markdown": False,
        }
        return CanonicalReportLayout(
            success=success,
            document=document,
            sections=sections,
            blocks=blocks,
            theme=theme,
            layout=layout,
            assets=assets,
            toc=toc,
            metadata=metadata,
            layout_trace=build_trace(
                document=document,
                sections=sections,
                blocks=blocks,
                theme=theme,
                layout=layout,
                assets=assets,
                toc=toc,
                started_at=started_at,
                completed_at=completed_at,
                stage_order=stage_order,
            ),
            layout_audit=build_audit(diagnostics),
            layout_diagnostics=tuple(diagnostics),
            errors=tuple(errors),
        )

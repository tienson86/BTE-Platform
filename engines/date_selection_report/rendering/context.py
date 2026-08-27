"""DateSelectionRenderContext — presentation/runtime state only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.tokens import (
    SECTION_ORDER,
    TEMPLATE_ID,
    TEMPLATE_VERSION,
    THEME_REF,
)


@dataclass(frozen=True, slots=True)
class PageConfiguration:
    """Paper hints. Exporters own actual pagination."""

    paper: str = "A4"
    orientation: str = "portrait"
    keep_recommendation_together: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize page configuration."""
        return {
            "paper": self.paper,
            "orientation": self.orientation,
            "keep_recommendation_together": self.keep_recommendation_together,
        }


@dataclass(frozen=True, slots=True)
class LayoutConfiguration:
    """Logical section order and template identity."""

    template_id: str = TEMPLATE_ID
    template_version: str = TEMPLATE_VERSION
    section_order: tuple[str, ...] = SECTION_ORDER

    def to_dict(self) -> dict[str, Any]:
        """Serialize layout configuration."""
        return {
            "template_id": self.template_id,
            "template_version": self.template_version,
            "section_order": list(self.section_order),
        }


@dataclass(frozen=True, slots=True)
class DateSelectionRenderContext:
    """Runtime presentation state. Holds the report by reference."""

    report: DateSelectionReportModel
    locale: str
    theme_id: str
    palette_id: str
    spacing_id: str
    typography_id: str
    icon_set_id: str
    page: PageConfiguration
    layout: LayoutConfiguration
    template_version: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize context identity. Does not copy analytical fields."""
        return {
            "locale": self.locale,
            "theme_id": self.theme_id,
            "palette_id": self.palette_id,
            "spacing_id": self.spacing_id,
            "typography_id": self.typography_id,
            "icon_set_id": self.icon_set_id,
            "page": self.page.to_dict(),
            "layout": self.layout.to_dict(),
            "template_version": self.template_version,
            "report_id": self.report.metadata.report_id,
        }


def create_render_context(
    report: DateSelectionReportModel,
    *,
    locale: str | None = None,
    page: PageConfiguration | None = None,
    layout: LayoutConfiguration | None = None,
) -> DateSelectionRenderContext:
    """Build render context without copying or mutating the report model."""
    resolved_layout = layout or LayoutConfiguration()
    return DateSelectionRenderContext(
        report=report,
        locale=locale or report.metadata.locale,
        theme_id=THEME_REF["theme_id"],
        palette_id=THEME_REF["palette_id"],
        spacing_id=THEME_REF["spacing_id"],
        typography_id=THEME_REF["typography_id"],
        icon_set_id=THEME_REF["icon_set_id"],
        page=page or PageConfiguration(),
        layout=resolved_layout,
        template_version=resolved_layout.template_version,
    )

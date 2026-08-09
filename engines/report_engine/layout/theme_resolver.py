"""Resolve theme identifiers only. No CSS or stylesheets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.report_engine.layout.layout_context import LAYOUT_VERSION, LayoutContext

THEME_ID = "bte.report.theme.v1"
PALETTE_ID = "bte.report.palette.foundation.v1"
SPACING_ID = "bte.report.spacing.foundation.v1"
TYPOGRAPHY_ID = "bte.report.typography.foundation.v1"
ICON_SET_ID = "bte.report.icons.foundation.v1"


@dataclass(slots=True)
class ThemeResolution:
    """Resolved theme identity set. Identifiers only."""

    theme_id: str
    palette_id: str
    spacing_id: str
    typography_id: str
    icon_set_id: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize theme identifiers."""
        return {
            "theme_id": self.theme_id,
            "palette_id": self.palette_id,
            "spacing_id": self.spacing_id,
            "typography_id": self.typography_id,
            "icon_set_id": self.icon_set_id,
            "status": self.status,
        }


class ThemeResolver:
    """Bind the frozen Foundation v1 theme identifiers."""

    def resolve(self, context: LayoutContext) -> ThemeResolution:
        """Return version-aware theme ids. Layout version must stay 1.0.0."""
        status = "resolved" if context.layout_version == LAYOUT_VERSION else "incompatible"
        return ThemeResolution(
            theme_id=THEME_ID,
            palette_id=PALETTE_ID,
            spacing_id=SPACING_ID,
            typography_id=TYPOGRAPHY_ID,
            icon_set_id=ICON_SET_ID,
            status=status,
        )

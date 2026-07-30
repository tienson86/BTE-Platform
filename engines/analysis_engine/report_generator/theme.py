"""Report themes for presentation rendering."""

from __future__ import annotations

from engines.analysis_engine.report_generator.exceptions import ReportFormatProfileError
from engines.analysis_engine.report_generator.models import ReportTheme

DEFAULT_THEME_ID = "default"

_THEMES: dict[str, ReportTheme] = {
    DEFAULT_THEME_ID: ReportTheme(
        theme_id=DEFAULT_THEME_ID,
        name="BTE Default",
        font_family="Georgia, 'Times New Roman', serif",
        css_variables={
            "--bg": "#f7f4ef",
            "--fg": "#1f1a14",
            "--accent": "#8b5a2b",
            "--muted": "#6b635a",
            "--border": "#d9d0c3",
            "--section-gap": "1.5rem",
        },
        metadata={"version": "1.0.0"},
    ),
    "compact": ReportTheme(
        theme_id="compact",
        name="BTE Compact",
        font_family="'Segoe UI', Tahoma, sans-serif",
        css_variables={
            "--bg": "#ffffff",
            "--fg": "#111111",
            "--accent": "#334155",
            "--muted": "#64748b",
            "--border": "#e2e8f0",
            "--section-gap": "1rem",
        },
        metadata={"version": "1.0.0"},
    ),
}


class ThemeRegistry:
    """Resolve presentation themes by id."""

    def __init__(self, themes: dict[str, ReportTheme] | None = None) -> None:
        self._themes = dict(themes or _THEMES)

    def get(self, theme_id: str) -> ReportTheme:
        """Return a theme or raise FormatProfileError."""
        theme = self._themes.get(theme_id)
        if theme is None:
            raise ReportFormatProfileError(
                f"Unknown theme_id: {theme_id}",
                details={"theme_id": theme_id, "available": sorted(self._themes)},
            )
        return theme

    def list_ids(self) -> tuple[str, ...]:
        """Return registered theme ids."""
        return tuple(sorted(self._themes))

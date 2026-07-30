"""Report themes and Theme Manager for presentation rendering."""

from __future__ import annotations

from engines.analysis_engine.report_generator.exceptions import ReportFormatProfileError
from engines.analysis_engine.report_generator.models import ReportTheme

DEFAULT_THEME_ID = "default"

# Sprint 2 catalog themes (plus legacy default/compact for compatibility).
CATALOG_THEME_IDS: tuple[str, ...] = (
    "classic",
    "modern",
    "professional",
    "dark",
)

_PRINT_CSS = """
@media print {
  body {
    background: #ffffff !important;
    color: #000000 !important;
    padding: 0.5in;
  }
  a { color: inherit; text-decoration: none; }
  .no-print { display: none !important; }
  .data-block, .chart-block, table {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  h1, h2, h3 {
    break-after: avoid;
    page-break-after: avoid;
  }
}
""".strip()


def _theme(
    theme_id: str,
    name: str,
    *,
    font_family: str,
    css_variables: dict[str, str],
    family: str,
) -> ReportTheme:
    return ReportTheme(
        theme_id=theme_id,
        name=name,
        font_family=font_family,
        css_variables=css_variables,
        metadata={
            "version": "1.0.0",
            "family": family,
            "print_css": _PRINT_CSS,
        },
    )


_THEMES: dict[str, ReportTheme] = {
    DEFAULT_THEME_ID: _theme(
        DEFAULT_THEME_ID,
        "BTE Default",
        font_family="Georgia, 'Times New Roman', serif",
        css_variables={
            "--bg": "#f7f4ef",
            "--fg": "#1f1a14",
            "--accent": "#8b5a2b",
            "--muted": "#6b635a",
            "--border": "#d9d0c3",
            "--section-gap": "1.5rem",
            "--surface": "#fffdf9",
            "--table-header-bg": "#efe7db",
            "--chart-bar": "#8b5a2b",
            "--chart-track": "#e8dfd2",
        },
        family="classic",
    ),
    "compact": _theme(
        "compact",
        "BTE Compact",
        font_family="'Segoe UI', Tahoma, sans-serif",
        css_variables={
            "--bg": "#ffffff",
            "--fg": "#111111",
            "--accent": "#334155",
            "--muted": "#64748b",
            "--border": "#e2e8f0",
            "--section-gap": "1rem",
            "--surface": "#f8fafc",
            "--table-header-bg": "#e2e8f0",
            "--chart-bar": "#334155",
            "--chart-track": "#e2e8f0",
        },
        family="modern",
    ),
    "classic": _theme(
        "classic",
        "Classic",
        font_family="Georgia, 'Times New Roman', serif",
        css_variables={
            "--bg": "#faf6ef",
            "--fg": "#2a2118",
            "--accent": "#7a4e2d",
            "--muted": "#6e6256",
            "--border": "#d4c4b0",
            "--section-gap": "1.75rem",
            "--surface": "#fffaf2",
            "--table-header-bg": "#eadfcf",
            "--chart-bar": "#7a4e2d",
            "--chart-track": "#e8dccb",
        },
        family="classic",
    ),
    "modern": _theme(
        "modern",
        "Modern",
        font_family="'Segoe UI', 'Helvetica Neue', sans-serif",
        css_variables={
            "--bg": "#f5f7fa",
            "--fg": "#0f172a",
            "--accent": "#0f766e",
            "--muted": "#64748b",
            "--border": "#cbd5e1",
            "--section-gap": "1.25rem",
            "--surface": "#ffffff",
            "--table-header-bg": "#e2e8f0",
            "--chart-bar": "#0f766e",
            "--chart-track": "#e2e8f0",
        },
        family="modern",
    ),
    "professional": _theme(
        "professional",
        "Professional",
        font_family="'Segoe UI', Calibri, sans-serif",
        css_variables={
            "--bg": "#f3f5f8",
            "--fg": "#1e293b",
            "--accent": "#1e3a5f",
            "--muted": "#475569",
            "--border": "#c5ced9",
            "--section-gap": "1.5rem",
            "--surface": "#ffffff",
            "--table-header-bg": "#dbe3ee",
            "--chart-bar": "#1e3a5f",
            "--chart-track": "#dbe3ee",
        },
        family="professional",
    ),
    "dark": _theme(
        "dark",
        "Dark",
        font_family="'Segoe UI', Tahoma, sans-serif",
        css_variables={
            "--bg": "#0f1419",
            "--fg": "#e7ecf3",
            "--accent": "#5b9bd5",
            "--muted": "#9aa7b8",
            "--border": "#2a3441",
            "--section-gap": "1.25rem",
            "--surface": "#171e27",
            "--table-header-bg": "#243041",
            "--chart-bar": "#5b9bd5",
            "--chart-track": "#243041",
        },
        family="dark",
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

    def register(self, theme: ReportTheme) -> None:
        """Register or replace a theme (extension hook)."""
        self._themes[theme.theme_id] = theme


class ThemeManager:
    """Sprint 2 Theme Manager over ThemeRegistry.

    Provides catalog helpers for Classic / Modern / Professional / Dark
    while preserving ThemeRegistry resolution for all registered themes.
    """

    def __init__(self, registry: ThemeRegistry | None = None) -> None:
        self._registry = registry or ThemeRegistry()

    @property
    def registry(self) -> ThemeRegistry:
        """Return the underlying theme registry."""
        return self._registry

    def get(self, theme_id: str) -> ReportTheme:
        """Resolve a theme by id."""
        return self._registry.get(theme_id)

    def resolve(self, theme_id: str) -> ReportTheme:
        """Alias of :meth:`get`."""
        return self.get(theme_id)

    def list_ids(self) -> tuple[str, ...]:
        """Return all registered theme ids."""
        return self._registry.list_ids()

    def list_catalog(self) -> tuple[ReportTheme, ...]:
        """Return Sprint 2 catalog themes in canonical order."""
        themes: list[ReportTheme] = []
        for theme_id in CATALOG_THEME_IDS:
            if theme_id in self._registry.list_ids():
                themes.append(self._registry.get(theme_id))
        return tuple(themes)

    def register(self, theme: ReportTheme) -> None:
        """Register a theme through the manager."""
        self._registry.register(theme)

    def print_css(self, theme_id: str) -> str:
        """Return print stylesheet fragment for a theme."""
        theme = self.get(theme_id)
        return str(theme.metadata.get("print_css") or _PRINT_CSS)

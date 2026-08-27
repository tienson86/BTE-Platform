"""Presentation-only formatters. No analytical calculation."""

from __future__ import annotations

from engines.date_selection_report.rendering.labels import LABELS
from engines.date_selection_report.rendering.tokens import ELEMENT_COLOR_TOKEN


def format_cung(cung: str, element: str) -> str:
    """Combine Cung and element for display. Internal fields stay separate."""
    name = cung.strip()
    action = element.strip()
    if action:
        return f"{name} ({action})"
    return name


def format_lunar_date(lunar_date: str) -> str:
    """Append the customer-facing lunar suffix."""
    return f"{lunar_date.strip()} {LABELS['lunar_suffix']}"


def format_compatible_hour_row(branch: str, time_range: str, cung_display: str) -> str:
    """Render one compatible-hour line."""
    prefix = LABELS["hour_prefix"]
    return f"{prefix} {branch} ({time_range}) · {cung_display}"


def format_hour_branch(branch: str) -> str:
    """Render the hour-branch label used in positive-time rows."""
    return f"{LABELS['hour_prefix']} {branch.strip()}"


def element_color_token(element: str) -> str | None:
    """Return the semantic Five-Element color token when known."""
    return ELEMENT_COLOR_TOKEN.get(element.strip())

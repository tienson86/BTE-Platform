"""Shared UI components (markup snippets)."""

from __future__ import annotations

from applications.customer_portal.i18n import DEFAULT_LOCALE, load_catalog, t


def stage_tabs(locale: str = DEFAULT_LOCALE) -> str:
    """Result stage tab buttons (labels from i18n)."""
    catalog = load_catalog(locale)
    stages = (
        "calendar",
        "bazi",
        "pattern",
        "score",
        "interpretation",
        "narrative",
    )
    parts: list[str] = []
    for index, stage in enumerate(stages):
        active = " active" if index == 0 else ""
        label = t(catalog, f"stages.{stage}")
        parts.append(
            f'<button type="button" class="tab{active}" data-stage="{stage}" '
            f'data-i18n="stages.{stage}">{label}</button>'
        )
    return "".join(parts)

"""RE-2 theme resolver tests."""

from __future__ import annotations

from engines.report_engine.layout.layout_context import build_layout_context
from engines.report_engine.layout.theme_resolver import (
    ICON_SET_ID,
    PALETTE_ID,
    SPACING_ID,
    THEME_ID,
    TYPOGRAPHY_ID,
    ThemeResolver,
)
from tests.report_engine.re2_support import assemble_layout_inputs


def test_theme_resolver_returns_identifiers_only() -> None:
    """Theme resolution publishes ids and never CSS."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    theme = ThemeResolver().resolve(context)
    assert theme.theme_id == THEME_ID
    assert theme.palette_id == PALETTE_ID
    assert theme.spacing_id == SPACING_ID
    assert theme.typography_id == TYPOGRAPHY_ID
    assert theme.icon_set_id == ICON_SET_ID
    encoded = theme.to_dict()
    assert "css" not in encoded
    assert "stylesheet" not in encoded
    assert encoded["status"] == "resolved"

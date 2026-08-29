"""UI-10R1 — Luck compact header is presentation-only."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src" / "screens" / "commercial_dashboard"
_CARD = _SRC / "LuckCard.tsx"
_CSS = _SRC / "commercial-dashboard.css"
_ADAPTER = _SRC / "luckAdapter.ts"
_GRID = _SRC / "DashboardGrid.tsx"


def test_lp4_compact_value_row_css() -> None:
    css = _CSS.read_text(encoding="utf-8")
    assert ".bte-luck__value-row" in css
    assert "display: flex" in css
    assert ".bte-luck__chronology" in css
    assert ".bte-cdash__card--span-6 { grid-column: span 6; }" in css


def test_lp_card_uses_one_current_row() -> None:
    card = _CARD.read_text(encoding="utf-8")
    assert 'data-luck-current-row="true"' in card
    assert 'data-luck-start-row="true"' in card
    assert "Thuận" not in card
    assert "luckAdapter" not in card


def test_lp_adapter_and_grid_untouched_contract() -> None:
    adapter = _ADAPTER.read_text(encoding="utf-8")
    grid = _GRID.read_text(encoding="utf-8")
    assert "copyCycle" in adapter
    assert 'card.id === "luck"' in grid
    assert "repeat(12, minmax(0, 1fr))" in _CSS.read_text(encoding="utf-8")

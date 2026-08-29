"""UI-11 Card 08 Interpretation — grid freeze, copy-only adapter, routing."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_CSS = _SRC / "screens" / "commercial_dashboard" / "commercial-dashboard.css"
_GRID = _SRC / "screens" / "commercial_dashboard" / "DashboardGrid.tsx"
_ADAPTER = _SRC / "screens" / "commercial_dashboard" / "interpretationAdapter.ts"
_CARD = _SRC / "screens" / "commercial_dashboard" / "InterpretationCard.tsx"
_RESULT_APP = _SRC / "entries" / "resultApp.tsx"
_BOOT = _SRC / "entries" / "resultBoot.ts"


def _client() -> TestClient:
    return TestClient(create_app())


def test_i2_i16_grid_spans_unchanged() -> None:
    css = _CSS.read_text(encoding="utf-8")
    assert "repeat(12, minmax(0, 1fr))" in css
    assert ".bte-cdash__card--span-12 { grid-column: span 12; }" in css
    grid = _GRID.read_text(encoding="utf-8")
    assert 'card.id === "interpretation"' in grid
    assert 'card.id === "action-plan"' in grid
    assert "ActionPlanCard" in grid
    assert "repeat(12" not in grid


def test_i8_i15_adapter_does_not_reason() -> None:
    adapter = _ADAPTER.read_text(encoding="utf-8")
    card = _CARD.read_text(encoding="utf-8")
    for source in (adapter, card):
        assert "engines." not in source
        assert "InterpretationEngine" not in source
        assert "CASE-0001" not in source
        assert "${strength}" not in source
        assert "vận tốt" not in source


def test_i_result_store_and_routing_remain() -> None:
    html = _client().get("/result").text
    assert html.count('id="canonical-desktop-root"') == 1
    assert "/static/js/result_store.js" in html
    assert "/static/dist/result.js" in html
    source = _RESULT_APP.read_text(encoding="utf-8")
    assert "CommercialDashboardPage" in source
    boot = _BOOT.read_text(encoding="utf-8")
    assert "layoutMode" in boot

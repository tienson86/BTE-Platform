"""UI-10 Card 07 Luck — grid freeze, copy-only adapter, routing."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_CSS = _SRC / "screens" / "commercial_dashboard" / "commercial-dashboard.css"
_GRID = _SRC / "screens" / "commercial_dashboard" / "DashboardGrid.tsx"
_ADAPTER = _SRC / "screens" / "commercial_dashboard" / "luckAdapter.ts"
_CARD = _SRC / "screens" / "commercial_dashboard" / "LuckCard.tsx"
_RESULT_APP = _SRC / "entries" / "resultApp.tsx"
_BOOT = _SRC / "entries" / "resultBoot.ts"


def _client() -> TestClient:
    return TestClient(create_app())


def test_l2_l20_grid_spans_unchanged() -> None:
    css = _CSS.read_text(encoding="utf-8")
    assert "repeat(12, minmax(0, 1fr))" in css
    assert ".bte-cdash__card--span-6 { grid-column: span 6; }" in css
    grid = _GRID.read_text(encoding="utf-8")
    assert 'card.id === "luck"' in grid
    assert 'card.id === "shensha"' in grid
    assert "SkeletonCard" in grid


def test_l12_l19_luck_does_not_calculate() -> None:
    adapter = _ADAPTER.read_text(encoding="utf-8")
    card = _CARD.read_text(encoding="utf-8")
    for source in (adapter, card):
        assert "engines." not in source
        assert "LuckEngine" not in source
        assert "CASE-0001" not in source
        assert "Date.now" not in source
        assert "birth_year" not in source


def test_l25_result_store_and_routing_remain() -> None:
    html = _client().get("/result").text
    assert html.count('id="canonical-desktop-root"') == 1
    assert "/static/js/result_store.js" in html
    assert "/static/dist/result.js" in html
    source = _RESULT_APP.read_text(encoding="utf-8")
    assert "CommercialDashboardPage" in source
    assert "resolveResultBoot" in source
    boot = _BOOT.read_text(encoding="utf-8")
    assert "layoutMode" in boot

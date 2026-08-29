"""UI-04 Card 01 Overview — grid freeze, routing, no customer visual control."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_CSS = _SRC / "screens" / "commercial_dashboard" / "commercial-dashboard.css"
_GRID = _SRC / "screens" / "commercial_dashboard" / "DashboardGrid.tsx"
_RESULT_APP = _SRC / "entries" / "resultApp.tsx"
_BOOT = _SRC / "entries" / "resultBoot.ts"


def _client() -> TestClient:
    return TestClient(create_app())


def test_o2_o13_grid_spans_unchanged() -> None:
    css = _CSS.read_text(encoding="utf-8")
    assert "repeat(12, minmax(0, 1fr))" in css
    assert ".bte-cdash__card--span-4 { grid-column: span 4; }" in css
    assert ".bte-cdash__card--span-8 { grid-column: span 8; }" in css
    grid = _GRID.read_text(encoding="utf-8")
    assert 'card.id === "overview"' in grid
    assert "SkeletonCard" in grid


def test_o10_overview_does_not_import_engines() -> None:
    adapter = (_SRC / "screens" / "commercial_dashboard" / "overviewAdapter.ts").read_text(
        encoding="utf-8"
    )
    assert "engines." not in adapter
    assert "CASE-0001" not in adapter


def test_o15_result_store_and_routing_remain() -> None:
    html = _client().get("/result").text
    assert html.count('id="canonical-desktop-root"') == 1
    assert "/static/js/result_store.js" in html
    assert "/static/dist/result.js" in html
    source = _RESULT_APP.read_text(encoding="utf-8")
    assert "CommercialDashboardPage" in source
    assert "resolveResultBoot" in source
    boot = _BOOT.read_text(encoding="utf-8")
    assert "layoutMode" in boot


def test_visual_harness_is_not_customer_facing() -> None:
    analyze = (PORTAL_ROOT / "templates" / "analyze.html").read_text(encoding="utf-8")
    layout = (PORTAL_ROOT / "templates" / "_layout.html").read_text(encoding="utf-8")
    assert "layout=visual" not in analyze
    assert "layout=skeleton" not in analyze
    assert "layout=visual" not in layout

"""UI-03R1 Tứ Trụ summary vs Bát Tự detail — frozen spans, copy-only, routing."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_CSS = _SRC / "screens" / "commercial_dashboard" / "commercial-dashboard.css"
_FOUR = _SRC / "screens" / "commercial_dashboard" / "FourPillars.tsx"
_BAZI = _SRC / "screens" / "commercial_dashboard" / "BaziCard.tsx"
_ADAPTER = _SRC / "screens" / "commercial_dashboard" / "adapter.ts"
_RESULT_APP = _SRC / "entries" / "resultApp.tsx"


def _client() -> TestClient:
    return TestClient(create_app())


def test_r12_uses_shared_tu_tru_panel() -> None:
    source = _FOUR.read_text(encoding="utf-8")
    assert "TuTruPanel" in source
    assert "Thiên Can" not in source
    assert "Địa Chi" not in source


def test_r14_outer_grid_spans_unchanged() -> None:
    css = _CSS.read_text(encoding="utf-8")
    assert "repeat(12, minmax(0, 1fr))" in css
    assert ".bte-cdash__card--span-4 { grid-column: span 4; }" in css
    assert ".bte-cdash__card--span-8 { grid-column: span 8; }" in css


def test_r13_no_astrology_computation() -> None:
    for path in (_ADAPTER, _FOUR, _BAZI):
        source = path.read_text(encoding="utf-8")
        assert "engines." not in source
        assert "cung_for_ganzhi" not in source
        assert "pillar_contract" not in source


def test_result_route_still_hosts_commercial_dashboard() -> None:
    html = _client().get("/result").text
    assert html.count('id="canonical-desktop-root"') == 1
    assert "/static/dist/result.js" in html
    assert "CommercialDashboardPage" in _RESULT_APP.read_text(encoding="utf-8")

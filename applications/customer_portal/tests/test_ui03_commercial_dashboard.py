"""UI-03 Identity Header + canonical Commercial Dashboard grid."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_RESULT_APP = _SRC / "entries" / "resultApp.tsx"
_DASHBOARD_CSS = _SRC / "screens" / "commercial_dashboard" / "commercial-dashboard.css"
_CARDS = _SRC / "screens" / "commercial_dashboard" / "cards.ts"


def _client() -> TestClient:
    return TestClient(create_app())


def test_g1_result_route_still_hosts_canonical_result_js() -> None:
    html = _client().get("/result").text
    assert html.count('id="canonical-desktop-root"') == 1
    assert "/static/dist/result.js" in html
    source = _RESULT_APP.read_text(encoding="utf-8")
    assert "CommercialDashboardPage" in source
    assert 'pathname === "/result"' in source


def test_g2_single_result_mount_node() -> None:
    html = _client().get("/result").text
    assert html.count('id="canonical-desktop-root"') == 1
    assert html.count('data-mount="PortalPage"') == 1


def test_g11_desktop_span_css_is_twelve_column_grid() -> None:
    css = _DASHBOARD_CSS.read_text(encoding="utf-8")
    assert "repeat(12, minmax(0, 1fr))" in css
    assert ".bte-cdash__card--span-4 { grid-column: span 4; }" in css
    assert ".bte-cdash__card--span-8 { grid-column: span 8; }" in css
    assert ".bte-cdash__card--span-6 { grid-column: span 6; }" in css
    assert ".bte-cdash__card--span-12 { grid-column: span 12; }" in css


def test_g10_customer_facing_card_titles_are_vietnamese() -> None:
    cards = _CARDS.read_text(encoding="utf-8")
    for title in (
        "TỔNG QUAN LÁ SỐ",
        "BÁT TỰ",
        "NGŨ HÀNH",
        "THẬP THẦN",
        "MỆNH CỤC",
        "THẦN SÁT",
        "ĐẠI VẬN",
        "LUẬN GIẢI TỔNG THỂ",
        "KẾ HOẠCH HÀNH ĐỘNG",
    ):
        assert title in cards


def test_g14_skeleton_query_is_not_customer_facing() -> None:
    analyze = (PORTAL_ROOT / "templates" / "analyze.html").read_text(encoding="utf-8")
    layout = (PORTAL_ROOT / "templates" / "_layout.html").read_text(encoding="utf-8")
    assert "layout=skeleton" not in analyze
    assert "layout=skeleton" not in layout
    assert "Skeleton mode" not in analyze


def test_g15_result_store_and_routing_remain() -> None:
    html = _client().get("/result").text
    assert html.count("/static/js/result_store.js") == 1
    assert 'data-result-ui="canonical-desktop-v2"' in html
    assert _client().get("/result").status_code == 200
    interpretation = _client().get("/interpretation")
    assert interpretation.status_code == 200
    assert 'data-mount="PortalPage"' in interpretation.text
    source = _RESULT_APP.read_text(encoding="utf-8")
    assert "PortalPage" in source
    assert "resolveResultBoot" in source
    assert "ResultStore" in source


def test_adapter_does_not_hard_code_case_0001() -> None:
    adapter = (_SRC / "screens" / "commercial_dashboard" / "adapter.ts").read_text(
        encoding="utf-8"
    )
    assert "Nguyễn Tiến Sơn" not in adapter
    assert "CASE-0001" not in adapter
    assert "1987-01-21" not in adapter

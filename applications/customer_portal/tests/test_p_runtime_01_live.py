"""P-RUNTIME-01 production /result routing and cache-bust checks."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT


def test_live_result_html_serves_pruntime01_bundle() -> None:
    html = TestClient(create_app()).get("/result").text
    assert 'data-result-ui="canonical-desktop-v2"' in html
    assert "/static/dist/result.js?v=PRUNTIME01" in html
    assert "/static/dist/result.css?v=PRUNTIME01" in html
    assert "result.js?v=P004R" not in html
    assert 'id="canonical-desktop-root"' in html


def test_live_result_template_is_not_legacy_default() -> None:
    html = TestClient(create_app()).get("/result").text
    assert "result_legacy.html" not in html
    desktop = (PORTAL_ROOT / "templates" / "result_desktop.html").read_text(encoding="utf-8")
    assert "CommercialDashboardPage" not in desktop
    entry = (PORTAL_ROOT / "src" / "entries" / "resultApp.tsx").read_text(encoding="utf-8")
    assert "CommercialDashboardPage" in entry
    assert "isCanonicalResultPath" in entry
    page = (
        PORTAL_ROOT / "src" / "screens" / "commercial_dashboard" / "CommercialDashboardPage.tsx"
    ).read_text(encoding="utf-8")
    assert "CanXuongDetail" not in page
    grid = (
        PORTAL_ROOT / "src" / "screens" / "commercial_dashboard" / "DashboardGrid.tsx"
    ).read_text(encoding="utf-8")
    assert "LifeConsultingSection" in grid

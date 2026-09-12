"""Number Energy V1 customer portal page."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import _proxy_upstream_url, create_app
from applications.customer_portal.config import PORTAL_ROOT, settings
from applications.customer_portal.pages import (
    CUSTOMER_NAV_ITEMS,
    NUMBER_ENERGY_API_PROXY_PREFIX,
    NUMBER_ENERGY_PATH,
)

_PRODUCT_LABELS = (
    "Trang chủ",
    "Chọn ngày tốt",
    "Xem lá số",
    "Tư vấn năng lượng số",
    "Tư vấn hôn nhân",
)


def _client() -> TestClient:
    return TestClient(create_app())


def _primary_nav(html: str) -> str:
    nav_start = html.index('data-customer-nav="primary"')
    return html[nav_start : html.index("</nav>", nav_start)]


def test_number_energy_route_loads() -> None:
    response = _client().get(NUMBER_ENERGY_PATH)
    assert response.status_code == 200
    assert "Tư vấn năng lượng số" in response.text
    assert 'id="number-energy-root"' in response.text
    assert "/static/dist/numberEnergy.js" in response.text
    assert "/backend/api/v1/number-energy/analyze" in response.text
    assert 'data-customer-nav="primary"' in response.text
    nav_html = _primary_nav(response.text)
    assert 'href="/number-energy"' in nav_html
    assert 'data-nav-id="number-energy"' in nav_html
    assert 'aria-current="page"' in nav_html


def test_number_energy_proxy_targets_applications_api() -> None:
    path = f"{NUMBER_ENERGY_API_PROXY_PREFIX}/analyze"
    url = _proxy_upstream_url(path)
    assert url == f"{settings.api_base_url.rstrip('/')}/{path}"
    assert "consulting/marriage" not in url


def test_number_energy_is_visible_in_primary_nav() -> None:
    html = _client().get("/good-date").text
    assert len(CUSTOMER_NAV_ITEMS) == 5
    assert [item.path for item in CUSTOMER_NAV_ITEMS] == [
        "/good-date",
        "/choose-date",
        "/analyze",
        "/number-energy",
        "/marriage-consulting",
    ]
    nav_html = _primary_nav(html)
    assert "Tư vấn năng lượng số" in nav_html
    assert 'href="/number-energy"' in nav_html
    assert CUSTOMER_NAV_ITEMS[-1].path == "/marriage-consulting"


def test_analyze_page_links_to_number_energy() -> None:
    html = _client().get("/analyze").text
    assert 'id="analyzeForm"' in html
    assert 'data-testid="number-energy-entry"' in html
    assert 'href="/number-energy"' in html
    assert "Năng lượng số (Bát Cực Linh Số)" in html


def test_existing_product_routes_still_load() -> None:
    client = _client()
    for path in ("/good-date", "/choose-date", "/analyze", "/marriage-consulting"):
        assert client.get(path).status_code == 200


def test_number_energy_bundle_keeps_freeze_marker() -> None:
    """Public runtime bundle still carries the frozen UI marker."""
    bundle = (PORTAL_ROOT / "static" / "dist" / "numberEnergy.js").read_text(encoding="utf-8")
    assert "NUMBER_ENERGY_STATIC_UI_V1" in bundle
    assert "analyzeNumberEnergy" not in bundle

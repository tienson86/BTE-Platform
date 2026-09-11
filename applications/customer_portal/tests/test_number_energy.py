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


def _client() -> TestClient:
    return TestClient(create_app())


def test_number_energy_route_loads() -> None:
    response = _client().get(NUMBER_ENERGY_PATH)
    assert response.status_code == 200
    assert "Năng lượng số" in response.text
    assert 'id="number-energy-root"' in response.text
    assert "/static/dist/numberEnergy.js" in response.text
    assert "/backend/api/v1/number-energy/analyze" in response.text
    assert 'data-customer-nav="primary"' in response.text


def test_number_energy_proxy_targets_applications_api() -> None:
    path = f"{NUMBER_ENERGY_API_PROXY_PREFIX}/analyze"
    url = _proxy_upstream_url(path)
    assert url == f"{settings.api_base_url.rstrip('/')}/{path}"
    assert "consulting/marriage" not in url


def test_number_energy_is_not_a_fifth_primary_nav_item() -> None:
    html = _client().get("/good-date").text
    assert len(CUSTOMER_NAV_ITEMS) == 4
    nav_start = html.index('data-customer-nav="primary"')
    nav_html = html[nav_start : html.index("</nav>", nav_start)]
    assert "Năng lượng số" not in nav_html
    assert 'href="/number-energy"' not in nav_html


def test_analyze_page_links_to_number_energy() -> None:
    html = _client().get("/analyze").text
    assert 'id="analyzeForm"' in html
    assert 'data-testid="number-energy-entry"' in html
    assert 'href="/number-energy"' in html
    assert "Năng lượng số (Bát Cực Linh Số)" in html


def test_number_energy_static_bundle_is_frozen() -> None:
    """Lock the static Golden UI bundle: freeze marker present, no analyze fetch."""
    bundle = (PORTAL_ROOT / "static" / "dist" / "numberEnergy.js").read_text(encoding="utf-8")
    assert "NUMBER_ENERGY_STATIC_UI_V1" in bundle
    assert "fetch(" not in bundle
    assert "/number-energy/analyze" not in bundle
    assert "analyzeNumberEnergy" not in bundle

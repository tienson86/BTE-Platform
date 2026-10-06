"""Business partnership and career consulting customer page."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.pages import (
    BUSINESS_CONSULTING_PATH,
    CHILDBIRTH_CONSULTING_PATH,
    CUSTOMER_NAV_ITEMS,
)


def _client() -> TestClient:
    return TestClient(create_app())


def test_business_consulting_route_loads() -> None:
    response = _client().get(BUSINESS_CONSULTING_PATH)
    assert response.status_code == 200
    assert "Tư vấn hợp tác" in response.text
    assert 'id="business-consulting-root"' in response.text
    assert "/static/dist/business.js" in response.text


def test_business_consulting_is_primary_nav_item() -> None:
    html = _client().get("/good-date").text
    assert CUSTOMER_NAV_ITEMS[-2].path == "/business-consulting"
    assert CUSTOMER_NAV_ITEMS[-1].path == CHILDBIRTH_CONSULTING_PATH
    assert 'href="/business-consulting"' in html
    assert "Tư vấn hợp tác" in html


def test_business_consulting_route_sets_active_nav() -> None:
    response = _client().get(BUSINESS_CONSULTING_PATH)
    assert response.status_code == 200
    nav_start = response.text.index('data-customer-nav="primary"')
    nav_html = response.text[nav_start : response.text.index("</nav>", nav_start)]
    assert 'data-nav-id="business-consulting"' in nav_html
    assert 'aria-current="page"' in nav_html

"""TV1-B07 customer Marriage Consulting UI."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.pages import CUSTOMER_NAV_ITEMS, MARRIAGE_CONSULTING_PATH


def _client() -> TestClient:
    return TestClient(create_app())


def test_marriage_consulting_route_loads() -> None:
    """Customer route renders the TV-01 page inside the portal shell."""
    response = _client().get(MARRIAGE_CONSULTING_PATH)
    assert response.status_code == 200
    assert "Tư vấn hôn nhân" in response.text
    assert 'id="marriage-consulting-root"' in response.text
    assert 'data-customer-nav="primary"' in response.text


def test_primary_nav_includes_approved_fourth_item() -> None:
    """TV1-B07A + RB18: Tư vấn hôn nhân remains the last live primary nav item."""
    html = _client().get("/good-date").text
    assert len(CUSTOMER_NAV_ITEMS) == 5
    assert CUSTOMER_NAV_ITEMS[-1].path == "/marriage-consulting"
    assert html.count('data-customer-nav="primary"') == 1
    nav_start = html.index('data-customer-nav="primary"')
    nav_html = html[nav_start : html.index("</nav>", nav_start)]
    assert "Trang chủ" in nav_html
    assert "Chọn ngày tốt" in nav_html
    assert "Xem lá số" in nav_html
    assert "Tư vấn hôn nhân" in nav_html
    assert 'href="/marriage-consulting"' in nav_html
    assert 'data-nav-family="consulting"' not in html


def test_consulting_entry_is_mounted_in_primary_nav() -> None:
    """Marriage is reachable from live primary chrome, not a hidden header-action."""
    html = _client().get(MARRIAGE_CONSULTING_PATH).text
    nav_start = html.index('data-customer-nav="primary"')
    nav_html = html[nav_start : html.index("</nav>", nav_start)]
    assert 'href="/marriage-consulting"' in nav_html
    assert 'data-nav-id="marriage-consulting"' in nav_html
    assert 'aria-current="page"' in nav_html
    assert 'id="marriage-consulting-root"' in html
    assert _client().get("/good-date").status_code == 200
    assert _client().get("/analyze").status_code == 200
    assert _client().get("/choose-date").status_code == 200


def test_existing_customer_routes_still_render() -> None:
    """B07 does not break Xem ngày tốt / Chọn ngày tốt / Xem lá số."""
    client = _client()
    assert client.get("/good-date").status_code == 200
    assert client.get("/choose-date").status_code == 200
    assert client.get("/analyze").status_code == 200
    assert client.get("/result").status_code == 200


def test_marriage_proxy_does_not_import_consulting() -> None:
    """Portal talks to Marriage API over HTTP only."""
    source = Path(__file__).resolve().parents[1] / "app.py"
    assert "consulting.marriage" not in source.read_text(encoding="utf-8")


def test_marriage_proxy_returns_customer_error_when_upstream_down() -> None:
    """Transport failure is a customer-safe retryable error, not a traceback."""
    request = httpx.Request("POST", "http://127.0.0.1:8082/api/v1/consulting/marriage")
    with patch("applications.customer_portal.app.httpx.AsyncClient") as client_cls:
        instance = AsyncMock()
        instance.__aenter__.return_value = instance
        instance.request.side_effect = httpx.ConnectError("down", request=request)
        client_cls.return_value = instance
        response = _client().post("/backend/api/v1/consulting/marriage", json={})
    assert response.status_code == 503
    payload = response.json()
    assert payload["status"] == "FAILED"
    assert payload["errors"][0]["retryable"] is True
    assert "traceback" not in response.text.lower()

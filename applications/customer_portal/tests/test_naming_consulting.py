from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from applications.customer_portal.app import _proxy_upstream_url, create_app
from applications.customer_portal.config import settings


def test_naming_menu_page_and_assets_are_reachable():
    client = TestClient(create_app())
    response = client.get("/naming-consulting")
    assert response.status_code == 200
    assert 'data-nav-id="naming-consulting" aria-current="page"' in response.text
    assert 'data-testid="naming-form"' in response.text
    assert 'name="current_name"' in response.text
    assert 'name="birth_time"' in response.text
    for path in ("/static/js/naming_consulting.js", "/static/css/naming_consulting.css"):
        assert client.get(path).status_code == 200
    for path in ("/good-date", "/analyze", "/result", "/marriage-consulting", "/childbirth-consulting"):
        assert 'href="/naming-consulting"' in client.get(path).text


def test_naming_proxy_uses_consulting_origin_and_forwards_authorization():
    path = "api/v1/consulting/naming/analyze"
    assert _proxy_upstream_url(path) == settings.marriage_api_base_url.rstrip("/") + "/" + path
    upstream = httpx.Response(200, json={"status": "SUCCESS", "data": {"recommendations": []}})
    with patch("applications.customer_portal.app.httpx.AsyncClient") as factory:
        requester = AsyncMock(return_value=upstream)
        factory.return_value.__aenter__.return_value.request = requester
        response = TestClient(create_app()).post("/backend/" + path, json={"count": 5}, headers={"Authorization": "Bearer example"})
    assert response.status_code == 200
    arguments = requester.call_args
    assert arguments.args[1] == _proxy_upstream_url(path)
    assert arguments.kwargs["headers"]["authorization"] == "Bearer example"


def test_naming_upstream_failure_has_a_readable_response():
    with patch("applications.customer_portal.app.httpx.AsyncClient") as factory:
        factory.return_value.__aenter__.return_value.request = AsyncMock(side_effect=httpx.ConnectError("offline"))
        response = TestClient(create_app()).post("/backend/api/v1/consulting/naming/analyze", json={})
    assert response.status_code == 503
    assert response.json()["status"] == "FAILED"
    assert response.json()["errors"][0]["retryable"] is True

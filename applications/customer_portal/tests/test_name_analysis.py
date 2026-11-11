from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from applications.customer_portal.app import _proxy_upstream_url, create_app
from applications.customer_portal.config import settings


def test_guest_name_page_and_entries_are_available():
    client = TestClient(create_app())
    page = client.get("/name-analysis")
    assert page.status_code == 200
    assert 'data-nav-id="name-analysis" aria-current="page"' in page.text
    assert 'data-testid="name-analysis-form"' in page.text
    assert 'name="full_name"' in page.text
    assert 'name="gender"' in page.text
    assert 'name="birth_date"' in page.text
    assert '<select name="birth_time" required' in page.text
    assert "Giờ Tý · 23h01 – 01h00" in page.text
    assert "Giờ Sửu · 01h01 – 03h00" in page.text
    assert "Giờ Hợi · 21h01 – 23h00" in page.text
    assert 'name="timezone"' in page.text
    assert "Ngày sinh dương lịch" in page.text
    assert "Không cần đăng nhập" in page.text
    for route in ("/good-date", "/naming-consulting"):
        assert 'href="/name-analysis"' in client.get(route).text
    for route in ("/static/js/name_analysis.js", "/static/css/name_analysis.css"):
        assert client.get(route).status_code == 200


def test_public_name_proxy_uses_consulting_origin_without_token_requirement():
    path = "api/v1/public/naming/analyze-current-birth"
    assert _proxy_upstream_url(path) == settings.marriage_api_base_url.rstrip("/") + "/" + path
    upstream = httpx.Response(200, json={"status": "SUCCESS", "data": {"full_name": "Nguyễn Tiến Sơn"}})
    with patch("applications.customer_portal.app.httpx.AsyncClient") as factory:
        requester = AsyncMock(return_value=upstream)
        factory.return_value.__aenter__.return_value.request = requester
        response = TestClient(create_app()).post("/backend/" + path, json={
            "full_name": "Nguyễn Tiến Sơn", "gender": "male", "birth_date": "1987-01-21", "birth_time": "04:30",
        })
    assert response.status_code == 200
    assert requester.call_args.args[1] == _proxy_upstream_url(path)
    assert "authorization" not in requester.call_args.kwargs["headers"]


def test_public_name_upstream_failure_remains_readable():
    with patch("applications.customer_portal.app.httpx.AsyncClient") as factory:
        factory.return_value.__aenter__.return_value.request = AsyncMock(side_effect=httpx.ConnectError("offline"))
        response = TestClient(create_app()).post("/backend/api/v1/public/naming/analyze-current-birth", json={})
    assert response.status_code == 503
    assert response.json()["errors"][0]["retryable"] is True

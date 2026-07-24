"""Customer Portal UI tests."""

from __future__ import annotations

import httpx
from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.config import PORTAL_ROOT
from applications.customer_portal.pages import LOGIN_ITEM, NAV_ITEMS


def test_required_pages_registered() -> None:
    keys = {item.key for item in NAV_ITEMS} | {LOGIN_ITEM.key}
    assert keys == {
        "login",
        "analyze",
        "result",
        "reports",
        "history",
        "profile",
    }


def test_templates_exist() -> None:
    templates = PORTAL_ROOT / "templates"
    assert (templates / "_layout.html").is_file()
    for item in (*NAV_ITEMS, LOGIN_ITEM):
        assert (templates / item.template).is_file()


def test_pages_render() -> None:
    client = TestClient(create_app())
    root = client.get("/", follow_redirects=False)
    assert root.status_code in {302, 307}
    for item in (*NAV_ITEMS, LOGIN_ITEM):
        response = client.get(item.path)
        assert response.status_code == 200, item.path
        assert "BTE" in response.text
        assert "text/html" in response.headers.get("content-type", "")


def test_healthz() -> None:
    client = TestClient(create_app())
    body = client.get("/healthz").json()
    assert body["status"] == "ok"
    assert "/analyze" in body["pages"]


def test_proxy_forwards(monkeypatch) -> None:
    calls: list[str] = []

    class FakeResponse:
        status_code = 200
        content = b'{"success":true}'
        headers = {"content-type": "application/json"}

    class FakeClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def request(self, method, url, headers=None, content=None):
            calls.append(url)
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeClient)
    client = TestClient(create_app())
    response = client.post("/backend/api/v1/analyze", json={"year": 1990, "month": 5, "day": 15})
    assert response.status_code == 200
    assert calls and "/api/v1/analyze" in calls[0]

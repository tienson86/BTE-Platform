"""Web Admin UI tests — pages render; no repository access."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.web_admin.app import create_app
from applications.web_admin.config import WEB_ADMIN_ROOT
from applications.web_admin.nav import NAV_ITEMS


def test_nav_covers_required_pages() -> None:
    keys = {item.key for item in NAV_ITEMS}
    assert keys >= {
        "dashboard",
        "customers",
        "cases",
        "reports",
        "licenses",
        "statistics",
        "settings",
    }


def test_templates_exist() -> None:
    templates = WEB_ADMIN_ROOT / "templates"
    for item in NAV_ITEMS:
        assert (templates / item.template).is_file()
    assert (templates / "_layout.html").is_file()


def test_static_assets_exist() -> None:
    assert (WEB_ADMIN_ROOT / "static" / "css" / "admin.css").is_file()
    assert (WEB_ADMIN_ROOT / "static" / "js" / "api.js").is_file()


def test_pages_render_html() -> None:
    client = TestClient(create_app())
    for item in NAV_ITEMS:
        response = client.get(item.path)
        assert response.status_code == 200, item.path
        assert "text/html" in response.headers.get("content-type", "")
        assert "BTE Admin" in response.text
        assert item.label in response.text


def test_healthz() -> None:
    client = TestClient(create_app())
    response = client.get("/healthz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "/customers" in body["pages"]


def test_proxy_forwards_to_api(monkeypatch) -> None:
    """Proxy path exists and uses configured API base (no business logic)."""
    import httpx

    calls: list[str] = []

    class FakeResponse:
        status_code = 200
        content = b'{"status":"ok"}'
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
    response = client.get("/backend/api/v1/health")
    assert response.status_code == 200
    assert calls and calls[0].endswith("/api/v1/health")

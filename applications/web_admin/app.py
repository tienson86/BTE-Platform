"""
BTE Web Admin UI (WP15)

Serves HTML/CSS/JS only and proxies REST calls to the Applications API.
Does not contain business logic and does not import repositories.

Run (API must already be up on :8000):
  uvicorn applications.web_admin.app:app --port 8080

Or:
  python -m applications.web_admin
"""

from __future__ import annotations

from typing import Mapping

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from applications.web_admin.config import WEB_ADMIN_ROOT, settings
from applications.web_admin.nav import NAV_ITEMS
from applications.web_admin.templates_util import render_page

HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


def create_app() -> FastAPI:
    """Create the Web Admin UI application."""
    app = FastAPI(
        title=settings.title,
        description="BTE Web Admin — UI that calls Applications REST API only.",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
    )

    static_dir = WEB_ADMIN_ROOT / "static"
    assets_dir = WEB_ADMIN_ROOT / "assets"
    assets_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    def page(active: str, template: str) -> HTMLResponse:
        return HTMLResponse(render_page(template, active=active))

    @app.get("/", response_class=HTMLResponse)
    def dashboard_page() -> HTMLResponse:
        """Dashboard page."""
        return page("dashboard", "dashboard.html")

    @app.get("/customers", response_class=HTMLResponse)
    def customers_page() -> HTMLResponse:
        """Customers page."""
        return page("customers", "customers.html")

    @app.get("/cases", response_class=HTMLResponse)
    def cases_page() -> HTMLResponse:
        """Cases page."""
        return page("cases", "cases.html")

    @app.get("/reports", response_class=HTMLResponse)
    def reports_page() -> HTMLResponse:
        """Reports page."""
        return page("reports", "reports.html")

    @app.get("/licenses", response_class=HTMLResponse)
    def licenses_page() -> HTMLResponse:
        """Licenses page."""
        return page("licenses", "licenses.html")

    @app.get("/statistics", response_class=HTMLResponse)
    def statistics_page() -> HTMLResponse:
        """Statistics page."""
        return page("statistics", "statistics.html")

    @app.get("/settings", response_class=HTMLResponse)
    def settings_page() -> HTMLResponse:
        """Settings page."""
        return page("settings", "settings.html")

    @app.api_route(
        "/backend/{path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    async def backend_proxy(path: str, request: Request) -> Response:
        """Transparent proxy to Applications API (avoids CORS; no business logic)."""
        url = f"{settings.api_base_url.rstrip('/')}/{path}"
        if request.url.query:
            url = f"{url}?{request.url.query}"

        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in HOP_BY_HOP
        }
        body = await request.body()

        async with httpx.AsyncClient(timeout=120.0) as client:
            upstream = await client.request(
                request.method,
                url,
                headers=headers,
                content=body,
            )

        excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
        response_headers: Mapping[str, str] = {
            key: value
            for key, value in upstream.headers.items()
            if key.lower() not in excluded
        }
        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            headers=dict(response_headers),
            media_type=upstream.headers.get("content-type"),
        )

    @app.get("/healthz")
    def healthz() -> dict[str, object]:
        """UI process liveness (not the Applications API health)."""
        return {
            "status": "ok",
            "service": "bte-web-admin",
            "api_base_url": settings.api_base_url,
            "pages": [item.path for item in NAV_ITEMS],
        }

    return app


app = create_app()

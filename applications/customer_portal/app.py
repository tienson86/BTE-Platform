"""
BTE Customer Portal (WP16)

Standalone UI for end users. Proxies REST to Applications API.
No business logic / repository / database.

Run:
  uvicorn applications.api.app:app --port 8000
  uvicorn applications.customer_portal.app:app --port 8081
"""

from __future__ import annotations

from typing import Mapping

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from applications.customer_portal.config import PORTAL_ROOT, settings
from applications.customer_portal.pages import LOGIN_ITEM, NAV_ITEMS
from applications.customer_portal.templates_util import render_page

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
    """Create Customer Portal FastAPI app."""
    app = FastAPI(
        title=settings.title,
        description="BTE Customer Portal — REST-only UI.",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
    )

    static_dir = PORTAL_ROOT / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    def page(active: str, template: str) -> HTMLResponse:
        return HTMLResponse(render_page(template, active=active))

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        """Default landing → dashboard."""
        return RedirectResponse(url="/dashboard", status_code=302)

    @app.get(LOGIN_ITEM.path, response_class=HTMLResponse)
    def login_page() -> HTMLResponse:
        """Login page."""
        return page("login", LOGIN_ITEM.template)

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard_page() -> HTMLResponse:
        """Dashboard home."""
        return page("dashboard", "dashboard.html")

    @app.get("/analyze", response_class=HTMLResponse)
    def analyze_page() -> HTMLResponse:
        """Analyze page."""
        return page("analyze", "analyze.html")

    @app.get("/result", response_class=HTMLResponse)
    def result_page() -> HTMLResponse:
        """Result page."""
        return page("result", "result.html")

    @app.get("/reports", response_class=HTMLResponse)
    def reports_page() -> HTMLResponse:
        """Reports page."""
        return page("reports", "reports.html")

    @app.get("/history", response_class=HTMLResponse)
    def history_page() -> HTMLResponse:
        """History page."""
        return page("history", "history.html")

    @app.get("/profile", response_class=HTMLResponse)
    def profile_page() -> HTMLResponse:
        """Profile page."""
        return page("profile", "profile.html")

    @app.api_route(
        "/backend/{path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    async def backend_proxy(path: str, request: Request) -> Response:
        """Proxy to Applications API (no business logic)."""
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
        excluded = {
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        }
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
        """Portal process liveness."""
        return {
            "status": "ok",
            "service": "bte-customer-portal",
            "api_base_url": settings.api_base_url,
            "pages": [LOGIN_ITEM.path, *[i.path for i in NAV_ITEMS]],
        }

    return app


app = create_app()

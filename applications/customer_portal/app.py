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
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from applications.customer_portal.config import PORTAL_ROOT, settings
from applications.customer_portal.pages import (
    HOME_PATH,
    LOGIN_ITEM,
    MARRIAGE_API_PROXY_PREFIX,
    MARRIAGE_CONSULTING_PATH,
    NAV_ITEMS,
)
from applications.customer_portal.templates_util import render_desktop_page, render_page

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


def _proxy_upstream_url(path: str) -> str:
    """HTTP-only composition: marriage Public API is a separate origin."""
    if path == MARRIAGE_API_PROXY_PREFIX or path.startswith(f"{MARRIAGE_API_PROXY_PREFIX}/"):
        return f"{settings.marriage_api_base_url.rstrip('/')}/{path}"
    return f"{settings.api_base_url.rstrip('/')}/{path}"


def create_app() -> FastAPI:
    """Create Customer Portal FastAPI app."""
    app = FastAPI(
        title=settings.title,
        description="BTE Portal — REST-only UI.",
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
        """Default landing → Good Date Home (Xem ngày tốt/xấu)."""
        return RedirectResponse(url=HOME_PATH, status_code=302)

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

    @app.get("/good-date", response_class=HTMLResponse)
    def good_date_page() -> HTMLResponse:
        """General auspicious-date calendar."""
        return page("good-date", "good_date.html")

    @app.get("/choose-date", response_class=HTMLResponse)
    def choose_date_page() -> HTMLResponse:
        """Personalized auspicious-date search."""
        return page("choose-date", "choose_date.html")

    @app.get("/result", response_class=HTMLResponse)
    def result_page(request: Request) -> HTMLResponse:
        """Result page — Canonical Desktop V2 (production).
        `?legacy=1` is EXPLICIT LEGACY ONLY and never shares Desktop precedence.
        """
        if request.query_params.get("legacy") == "1":
            return page("result", "result_legacy.html")
        return HTMLResponse(render_desktop_page("result_desktop.html", active="result"))

    @app.get("/result-workspace", response_class=HTMLResponse)
    def result_workspace_page() -> HTMLResponse:
        """BaZi Result Workspace V2 — layout foundation, no data binding."""
        return HTMLResponse(render_desktop_page("result_workspace.html"))

    @app.get("/interpretation", response_class=HTMLResponse)
    def interpretation_page() -> HTMLResponse:
        """Luận giải — same current result as /result, interpretation zone."""
        return HTMLResponse(render_desktop_page("result_desktop.html", active="interpretation"))

    @app.get("/reports", response_class=HTMLResponse)
    def reports_page() -> HTMLResponse:
        """Reports page."""
        return page("reports", "reports.html")

    @app.get("/report-preview", response_class=HTMLResponse)
    def report_preview_page() -> HTMLResponse:
        """UI-16 executive report HTML preview. Does not replace /reports PDF."""
        return HTMLResponse(render_desktop_page("result_desktop.html", active="result"))

    @app.get("/history", response_class=HTMLResponse)
    def history_page() -> HTMLResponse:
        """History page."""
        return page("history", "history.html")

    @app.get("/profile", response_class=HTMLResponse)
    def profile_page() -> HTMLResponse:
        """Profile page."""
        return page("profile", "profile.html")

    @app.get(MARRIAGE_CONSULTING_PATH, response_class=HTMLResponse)
    def marriage_consulting_page() -> HTMLResponse:
        """TV-01 Marriage Consulting customer page."""
        return page("marriage-consulting", "marriage_consulting.html")

    @app.api_route(
        "/backend/{path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    async def backend_proxy(path: str, request: Request) -> Response:
        """Proxy REST. Marriage routes go to the isolated TV-01 API origin."""
        url = _proxy_upstream_url(path)
        if request.url.query:
            url = f"{url}?{request.url.query}"
        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in HOP_BY_HOP
        }
        body = await request.body()
        marriage_route = path == MARRIAGE_API_PROXY_PREFIX or path.startswith(
            f"{MARRIAGE_API_PROXY_PREFIX}/"
        )
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(120.0, connect=5.0, write=30.0, pool=5.0)
            ) as client:
                upstream = await client.request(
                    request.method,
                    url,
                    headers=headers,
                    content=body,
                )
        except httpx.RequestError:
            if marriage_route:
                return JSONResponse(
                    status_code=503,
                    content={
                        "status": "FAILED",
                        "data": None,
                        "warnings": [],
                        "errors": [
                            {
                                "code": "INTERNAL_ERROR",
                                "stage": "transport",
                                "message": "Không thể hoàn tất phân tích lúc này.",
                                "retryable": True,
                                "consultation_id": None,
                            }
                        ],
                        "version_bundle": {"api_version": "v1"},
                    },
                )
            raise
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
            "pages": [
                LOGIN_ITEM.path,
                *[i.path for i in NAV_ITEMS],
                "/good-date",
                "/choose-date",
                "/result-workspace",
                MARRIAGE_CONSULTING_PATH,
            ],
            "marriage_api_base_url": settings.marriage_api_base_url,
        }

    return app


app = create_app()

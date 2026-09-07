"""Isolated TV-01 customer composition host. Does not import applications."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from consulting.marriage.api.http import create_marriage_api_app
from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.ui.layout import PRODUCT_LABEL, ROUTE_PATH

_UI_STATIC = Path(__file__).resolve().parent / "static"


def create_marriage_customer_app(container: MarriageContainer | None = None) -> FastAPI:
    """Serve the B06 Public API and the isolated customer page on one host."""
    app = create_marriage_api_app(container)
    app.title = f"TV-01 {PRODUCT_LABEL}"

    @app.get(ROUTE_PATH, response_class=HTMLResponse)
    def marriage_consulting_page() -> HTMLResponse:
        """Customer route for the isolated legal composition app."""
        page = _UI_STATIC / "marriage_consulting.html"
        return HTMLResponse(page.read_text(encoding="utf-8"))

    if _UI_STATIC.is_dir():
        app.mount("/tv01-static", StaticFiles(directory=str(_UI_STATIC)), name="tv01-static")
    return app

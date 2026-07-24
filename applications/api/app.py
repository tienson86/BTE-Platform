"""
BTE Applications API (WP8)

Run:
  uvicorn applications.api.app:app --reload --port 8000

Endpoint:
  POST /api/v1/report
"""

from __future__ import annotations

from fastapi import FastAPI

from applications.api.routers import health as health_router
from applications.api.routers import report as report_router


def create_app() -> FastAPI:
    """Create Applications Layer FastAPI app."""
    app = FastAPI(
        title="BTE Applications API",
        description="Applications Layer skeleton — report pipeline entrypoint.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.include_router(health_router.router)
    app.include_router(report_router.router, prefix="/api/v1")
    return app


app = create_app()

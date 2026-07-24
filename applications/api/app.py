"""
BTE Applications API V1 (WP9)

Run:
  uvicorn applications.api.app:app --reload --port 8000

Docs:
  http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from applications.api.config import settings
from applications.api.exceptions import register_exception_handlers
from applications.api.middleware.request_context import register_middleware
from applications.api.routes import health as health_router
from applications.api.routes import v1 as v1_router


def _configure_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def create_app() -> FastAPI:
    """Create Applications API V1 FastAPI application."""
    _configure_logging()
    app = FastAPI(
        title=settings.app_name,
        description=(
            "BTE Platform Applications API V1 — orchestration layer over engines. "
            "Primary endpoint: POST /api/v1/analyze"
        ),
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )
    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(health_router.router)
    app.include_router(v1_router.router, prefix=settings.api_prefix)
    return app


app = create_app()

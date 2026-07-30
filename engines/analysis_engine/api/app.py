"""
BTE Analysis Engine REST API

Run:
  uvicorn engines.analysis_engine.api.app:app --reload --port 8001

Docs (Swagger UI):
  http://127.0.0.1:8001/docs

OpenAPI:
  http://127.0.0.1:8001/openapi.json
"""

from __future__ import annotations

import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from engines.analysis_engine.api.config import settings
from engines.analysis_engine.api.exceptions import register_exception_handlers
from engines.analysis_engine.api.routes import (
    analysis,
    auth,
    charts,
    health,
    interpretation,
    report,
)


def _configure_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach X-Request-ID to request state and response."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def create_app() -> FastAPI:
    """Create Analysis Engine FastAPI application."""
    _configure_logging()
    app = FastAPI(
        title=settings.app_name,
        description=(
            "BTE Analysis Engine REST API — Chart, Analysis, Interpretation, Report. "
            "JWT Ready (BearerAuth) and Role Ready (ADMIN / ANALYST / VIEWER). "
            "Swagger UI at /docs; OpenAPI at /openapi.json."
        ),
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )
    app.openapi_tags = [
        {"name": "health", "description": "Liveness probe"},
        {"name": "Auth", "description": "JWT token issuance (JWT Ready)"},
        {"name": "Charts", "description": "Create / read natal chart snapshots"},
        {"name": "Analysis", "description": "Analysis Runtime execution"},
        {"name": "Interpretation", "description": "Interpretation Engine execution"},
        {"name": "Report", "description": "Report Generator (HTML/MD/PDF/JSON)"},
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:4173",
            "http://localhost:4173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)
    register_exception_handlers(app)

    app.include_router(health.router)
    app.include_router(auth.router, prefix=settings.api_prefix)
    app.include_router(charts.router, prefix=settings.api_prefix)
    app.include_router(analysis.router, prefix=settings.api_prefix)
    app.include_router(interpretation.router, prefix=settings.api_prefix)
    app.include_router(report.router, prefix=settings.api_prefix)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        from fastapi.openapi.utils import get_openapi

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
        )
        schema.setdefault("components", {}).setdefault("securitySchemes", {}).update(
            {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        )
        # Advertise JWT readiness without forcing global security (auth_required toggle).
        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
    return app


app = create_app()

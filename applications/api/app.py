"""
BTE Applications API V1 (WP9 + WP10 Security)

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
from applications.api.middleware import register_middleware
from applications.api.routes import admin as admin_router
from applications.api.routes import auth as auth_router
from applications.api.routes import cases as cases_router
from applications.api.routes import customers as customers_router
from applications.api.routes import health as health_router
from applications.api.routes import license as license_router
from applications.api.routes import user as user_router
from applications.api.routes import v1 as v1_router
from applications.monitoring import register_ops_middleware


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
            "BTE Platform Applications API V1 — orchestration + security foundation. "
            "Primary endpoint: POST /api/v1/analyze. "
            "Auth: POST /api/v1/auth/login "
            "(dev users: admin/admin123, consultant/consultant123, customer/customer123)."
        ),
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
    )
    app.openapi_tags = [
        {"name": "Auth", "description": "JWT / API Key authentication"},
        {"name": "Users", "description": "Current user profile & RBAC demos"},
        {"name": "Customers", "description": "Customer management (WP11)"},
        {"name": "Cases", "description": "Case / analysis history (WP11)"},
        {"name": "Admin", "description": "Administration & operations (WP13)"},
        {"name": "License", "description": "Licensing & product editions (WP14)"},
        {"name": "engines", "description": "Engine orchestration endpoints"},
        {"name": "health", "description": "Liveness"},
    ]
    register_middleware(app)
    register_ops_middleware(app)
    register_exception_handlers(app)
    app.include_router(health_router.router)
    app.include_router(auth_router.router, prefix=settings.api_prefix)
    app.include_router(user_router.router, prefix=settings.api_prefix)
    app.include_router(customers_router.router, prefix=settings.api_prefix)
    app.include_router(cases_router.router, prefix=settings.api_prefix)
    app.include_router(admin_router.router, prefix=settings.api_prefix)
    app.include_router(license_router.router, prefix=settings.api_prefix)
    app.include_router(v1_router.router, prefix=settings.api_prefix)

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
                },
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": settings.api_key_header,
                },
            }
        )
        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
    return app


app = create_app()

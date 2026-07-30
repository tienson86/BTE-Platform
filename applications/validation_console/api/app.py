"""BTE Validation Console API — Golden Dataset Manager.

Run:
  uvicorn applications.validation_console.api.app:app --reload --port 8003

Docs:
  http://127.0.0.1:8003/docs
"""

from __future__ import annotations

import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from applications.validation_console.api.routes import datasets, health, workflow
from applications.validation_console.api.services import seed_demo_datasets


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
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
    """Create Validation Console FastAPI application."""
    _configure_logging()
    app = FastAPI(
        title="BTE Validation Console API",
        description=(
            "Golden Dataset Manager — Create, Import, Compare, Regression, "
            "Approval, Statistics, Coverage."
        ),
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)
    app.include_router(health.router)
    app.include_router(datasets.router, prefix="/api/v1")
    app.include_router(workflow.router, prefix="/api/v1")
    seed_demo_datasets()
    return app


app = create_app()

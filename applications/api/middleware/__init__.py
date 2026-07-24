"""Register all HTTP middlewares (order: outer → inner)."""

from __future__ import annotations

from fastapi import FastAPI

from applications.api.middleware.auth_middleware import register_auth_middleware
from applications.api.middleware.logging import register_logging_middleware
from applications.api.middleware.request_id import register_request_id_middleware
from applications.api.middleware.timing import register_timing_middleware


def register_middleware(app: FastAPI) -> None:
    """
    Register middleware stack.

    FastAPI runs middleware in reverse registration order (last added = outermost).
    Desired outer→inner: logging → timing → request_id → auth → route
    """
    register_auth_middleware(app)
    register_request_id_middleware(app)
    register_timing_middleware(app)
    register_logging_middleware(app)

"""Public service middleware stack."""

from __future__ import annotations

from fastapi import FastAPI

from applications.middleware.api_version import register_api_version_middleware
from applications.middleware.authentication_placeholder import (
    register_authentication_placeholder_middleware,
)
from applications.middleware.correlation_id import register_correlation_id_middleware
from applications.middleware.rate_limit_placeholder import (
    register_rate_limit_placeholder_middleware,
)
from applications.middleware.request_id import register_request_id_middleware


def register_public_middleware(app: FastAPI) -> None:
    """Register pass-through public middleware. Order: last added is outermost."""
    register_authentication_placeholder_middleware(app)
    register_rate_limit_placeholder_middleware(app)
    register_api_version_middleware(app)
    register_correlation_id_middleware(app)
    register_request_id_middleware(app)


__all__ = ["register_public_middleware"]

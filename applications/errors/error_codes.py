"""Canonical public API error codes.

Codes are stable contract identifiers. Messages may be localized later;
codes must not change meaning.
"""

from __future__ import annotations

from typing import Final

VALIDATION_ERROR: Final[str] = "BTE-400-VALIDATION"
UNSUPPORTED_VERSION: Final[str] = "BTE-400-UNSUPPORTED_VERSION"
UNAUTHORIZED: Final[str] = "BTE-401-UNAUTHORIZED"
FORBIDDEN: Final[str] = "BTE-403-FORBIDDEN"
NOT_FOUND: Final[str] = "BTE-404-NOT_FOUND"
CONFLICT: Final[str] = "BTE-409-CONFLICT"
RATE_LIMITED: Final[str] = "BTE-429-RATE_LIMITED"
INTERNAL_ERROR: Final[str] = "BTE-500-INTERNAL"
NOT_IMPLEMENTED: Final[str] = "BTE-501-NOT_IMPLEMENTED"
PIPELINE_UNBOUND: Final[str] = "BTE-503-PIPELINE_UNBOUND"
SERVICE_UNAVAILABLE: Final[str] = "BTE-503-UNAVAILABLE"

HTTP_STATUS_BY_CODE: Final[dict[str, int]] = {
    VALIDATION_ERROR: 400,
    UNSUPPORTED_VERSION: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    CONFLICT: 409,
    RATE_LIMITED: 429,
    INTERNAL_ERROR: 500,
    NOT_IMPLEMENTED: 501,
    PIPELINE_UNBOUND: 503,
    SERVICE_UNAVAILABLE: 503,
}

SAFE_PUBLIC_MESSAGES: Final[dict[str, str]] = {
    VALIDATION_ERROR: "Request validation failed.",
    UNSUPPORTED_VERSION: "Requested API version is not supported.",
    UNAUTHORIZED: "Authentication is required.",
    FORBIDDEN: "The caller is not allowed to perform this operation.",
    NOT_FOUND: "The requested resource was not found.",
    CONFLICT: "The request conflicts with the current resource state.",
    RATE_LIMITED: "Rate limit exceeded. Retry after the indicated interval.",
    INTERNAL_ERROR: "An unexpected error occurred.",
    NOT_IMPLEMENTED: "This endpoint is reserved and not implemented.",
    PIPELINE_UNBOUND: "Canonical pipeline binding is not available.",
    SERVICE_UNAVAILABLE: "The service is temporarily unavailable.",
}

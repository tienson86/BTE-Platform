"""Public service error package."""

from applications.errors.error_codes import (
    INTERNAL_ERROR,
    NOT_FOUND,
    PIPELINE_UNBOUND,
    RATE_LIMITED,
    UNAUTHORIZED,
    VALIDATION_ERROR,
)
from applications.errors.error_response import PublicServiceError, build_error_response
from applications.errors.exception_mapper import map_exception, register_public_exception_handlers

__all__ = [
    "INTERNAL_ERROR",
    "NOT_FOUND",
    "PIPELINE_UNBOUND",
    "PublicServiceError",
    "RATE_LIMITED",
    "UNAUTHORIZED",
    "VALIDATION_ERROR",
    "build_error_response",
    "map_exception",
    "register_public_exception_handlers",
]

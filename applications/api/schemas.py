"""Backward-compatible schema exports (WP8 flat module)."""

from applications.api.schemas.common import (
    APIResponse,
    BirthRequest,
    ReportRequest,
    ReportResponse,
)

__all__ = [
    "APIResponse",
    "BirthRequest",
    "ReportRequest",
    "ReportResponse",
]

"""Rate-limit placeholder.

Documents 429 + Retry-After policy. Does not enforce limits in Beta-2.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, Response

from applications.errors.error_codes import RATE_LIMITED

RETRY_AFTER_HEADER = "Retry-After"
RATE_LIMIT_LIMIT_HEADER = "X-RateLimit-Limit"
RATE_LIMIT_REMAINING_HEADER = "X-RateLimit-Remaining"
PLACEHOLDER_LIMIT = 60
PLACEHOLDER_WINDOW_SECONDS = 60


def register_rate_limit_placeholder_middleware(app: FastAPI) -> None:
    """Expose reserved rate-limit headers without rejecting traffic."""

    @app.middleware("http")
    async def rate_limit_placeholder_middleware(request: Request, call_next) -> Response:
        request.state.rate_limit = {
            "enabled": False,
            "code": RATE_LIMITED,
            "limit": PLACEHOLDER_LIMIT,
            "window_seconds": PLACEHOLDER_WINDOW_SECONDS,
        }
        response = await call_next(request)
        response.headers[RATE_LIMIT_LIMIT_HEADER] = str(PLACEHOLDER_LIMIT)
        response.headers[RATE_LIMIT_REMAINING_HEADER] = str(PLACEHOLDER_LIMIT)
        return response

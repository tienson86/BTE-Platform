"""Access logging middleware."""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request, Response

logger = logging.getLogger("bte.applications.api")


def register_logging_middleware(app: FastAPI) -> None:
    """Log method, path, status, request_id, and elapsed ms."""

    @app.middleware("http")
    async def logging_middleware(
        request: Request,
        call_next,
    ) -> Response:
        response = await call_next(request)
        request_id = getattr(request.state, "request_id", None)
        elapsed_ms = getattr(request.state, "elapsed_ms", None)
        logger.info(
            "request_id=%s method=%s path=%s status=%s elapsed_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            f"{elapsed_ms:.2f}" if isinstance(elapsed_ms, float) else "-",
        )
        return response

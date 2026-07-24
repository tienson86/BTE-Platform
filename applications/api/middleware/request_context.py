"""Request ID + elapsed-time + access logging middleware."""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import FastAPI, Request, Response

from applications.api.config import settings

logger = logging.getLogger("bte.applications.api")


def register_middleware(app: FastAPI) -> None:
    """Register HTTP middlewares for request_id, elapsed ms, and logging."""

    @app.middleware("http")
    async def request_context_middleware(
        request: Request,
        call_next,
    ) -> Response:
        incoming = request.headers.get(settings.request_id_header)
        request_id = (incoming or "").strip() or str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        response.headers[settings.request_id_header] = request_id
        response.headers[settings.elapsed_header] = f"{elapsed_ms:.2f}"

        logger.info(
            "request_id=%s method=%s path=%s status=%s elapsed_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

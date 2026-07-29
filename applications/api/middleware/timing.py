"""Elapsed-time middleware."""

from __future__ import annotations

import time

from fastapi import FastAPI, Request, Response

from applications.api.config import settings


def register_timing_middleware(app: FastAPI) -> None:
    """Measure request duration and set ``X-Elapsed-Ms``."""

    @app.middleware("http")
    async def timing_middleware(
        request: Request,
        call_next,
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        response.headers[settings.elapsed_header] = f"{elapsed_ms:.2f}"
        request.state.elapsed_ms = elapsed_ms
        return response

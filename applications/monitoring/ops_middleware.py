"""Ops monitoring middleware (records metrics without changing auth core)."""

from __future__ import annotations

import time

from fastapi import FastAPI, Request, Response

from applications.audit.activity_logger import ActivityLogger, get_activity_logger
from applications.monitoring.metrics import MetricsCollector, get_metrics


def register_ops_middleware(
    app: FastAPI,
    *,
    metrics: MetricsCollector | None = None,
    activity_logger: ActivityLogger | None = None,
) -> None:
    """
    Register request metrics + path-based audit middleware.

    Does not modify existing auth/request middleware modules.
    """
    collector = metrics or get_metrics()
    logger = activity_logger or get_activity_logger()

    @app.middleware("http")
    async def ops_middleware(request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        user = getattr(request.state, "user", None)
        user_id = getattr(user, "user_id", None) if user is not None else None
        username = getattr(user, "username", None) if user is not None else None

        path = request.url.path.rstrip("/") or "/"
        collector.record_request(
            method=request.method,
            path=path,
            status_code=response.status_code,
            elapsed_ms=elapsed_ms,
            user_id=user_id,
        )
        logger.record_from_request(
            method=request.method,
            path=path,
            status_code=response.status_code,
            user_id=user_id,
            username=username,
        )
        return response

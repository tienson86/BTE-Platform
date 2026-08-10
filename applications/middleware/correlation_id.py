"""Correlation-ID and Idempotency-Key pass-through. No persistence."""

from __future__ import annotations

from fastapi import FastAPI, Request, Response

CORRELATION_ID_HEADER = "Correlation-ID"
CORRELATION_ID_HEADER_ALT = "X-Correlation-ID"
IDEMPOTENCY_KEY_HEADER = "Idempotency-Key"


def resolve_correlation_id(request: Request) -> str | None:
    """Return inbound Correlation-ID when present."""
    value = (
        request.headers.get(CORRELATION_ID_HEADER)
        or request.headers.get(CORRELATION_ID_HEADER_ALT)
        or ""
    ).strip()
    return value or None


def resolve_idempotency_key(request: Request) -> str | None:
    """Return inbound Idempotency-Key when present."""
    value = (request.headers.get(IDEMPOTENCY_KEY_HEADER) or "").strip()
    return value or None


def register_correlation_id_middleware(app: FastAPI) -> None:
    """Propagate Correlation-ID and Idempotency-Key without storing them."""

    @app.middleware("http")
    async def correlation_id_middleware(request: Request, call_next) -> Response:
        correlation_id = resolve_correlation_id(request)
        idempotency_key = resolve_idempotency_key(request)
        request.state.correlation_id = correlation_id
        request.state.idempotency_key = idempotency_key
        response = await call_next(request)
        if correlation_id:
            response.headers[CORRELATION_ID_HEADER] = correlation_id
        if idempotency_key:
            response.headers[IDEMPOTENCY_KEY_HEADER] = idempotency_key
        return response

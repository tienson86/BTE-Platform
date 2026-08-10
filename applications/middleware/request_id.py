"""Request-ID pass-through middleware. No persistence."""

from __future__ import annotations

import uuid

from fastapi import FastAPI, Request, Response

REQUEST_ID_HEADER = "Request-ID"
REQUEST_ID_HEADER_ALT = "X-Request-ID"


def resolve_request_id(request: Request) -> str:
    """Return inbound Request-ID or generate a new identifier."""
    incoming = (
        request.headers.get(REQUEST_ID_HEADER)
        or request.headers.get(REQUEST_ID_HEADER_ALT)
        or ""
    ).strip()
    return incoming or str(uuid.uuid4())


def register_request_id_middleware(app: FastAPI) -> None:
    """Propagate Request-ID on the request state and response headers."""

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next) -> Response:
        request_id = resolve_request_id(request)
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response

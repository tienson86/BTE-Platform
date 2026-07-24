"""Request ID middleware."""

from __future__ import annotations

import uuid

from fastapi import FastAPI, Request, Response

from applications.api.config import settings


def register_request_id_middleware(app: FastAPI) -> None:
    """Attach / propagate ``X-Request-ID``."""

    @app.middleware("http")
    async def request_id_middleware(
        request: Request,
        call_next,
    ) -> Response:
        incoming = request.headers.get(settings.request_id_header)
        request_id = (incoming or "").strip() or str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[settings.request_id_header] = request_id
        return response

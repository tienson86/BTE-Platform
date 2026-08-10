"""Map exceptions to canonical public errors.

Never expose stack traces, Python exception types, or filesystem paths.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from applications.errors.error_codes import (
    HTTP_STATUS_BY_CODE,
    INTERNAL_ERROR,
    UNSUPPORTED_VERSION,
    VALIDATION_ERROR,
)
from applications.errors.error_response import PublicServiceError, build_error_response


def _request_id_from(request: Request) -> str:
    return str(getattr(request.state, "request_id", "") or "unknown")


def map_exception(exc: BaseException, *, request_id: str) -> tuple[int, dict[str, Any]]:
    """Return HTTP status and a JSON-safe canonical error body."""
    if isinstance(exc, PublicServiceError):
        model = exc.to_model(request_id)
        return exc.status_code, model.model_dump(mode="json")

    if isinstance(exc, (RequestValidationError, ValidationError)):
        model = build_error_response(
            code=VALIDATION_ERROR,
            request_id=request_id,
            details={"reason": "Request does not match the public contract."},
        )
        return HTTP_STATUS_BY_CODE[VALIDATION_ERROR], model.model_dump(mode="json")

    if isinstance(exc, ValueError):
        text = str(exc)
        code = UNSUPPORTED_VERSION if "version" in text.lower() else VALIDATION_ERROR
        model = build_error_response(code=code, request_id=request_id)
        return HTTP_STATUS_BY_CODE[code], model.model_dump(mode="json")

    model = build_error_response(code=INTERNAL_ERROR, request_id=request_id)
    return HTTP_STATUS_BY_CODE[INTERNAL_ERROR], model.model_dump(mode="json")


def register_public_exception_handlers(app: FastAPI) -> None:
    """Attach public error handlers to a FastAPI application."""

    @app.exception_handler(PublicServiceError)
    async def public_service_error_handler(
        request: Request,
        exc: PublicServiceError,
    ) -> JSONResponse:
        status_code, payload = map_exception(exc, request_id=_request_id_from(request))
        return JSONResponse(status_code=status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        status_code, payload = map_exception(exc, request_id=_request_id_from(request))
        return JSONResponse(status_code=status_code, content=payload)

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        status_code, payload = map_exception(exc, request_id=_request_id_from(request))
        return JSONResponse(status_code=status_code, content=payload)

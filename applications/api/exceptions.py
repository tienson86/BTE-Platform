"""API exception types and FastAPI handlers."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("bte.applications.api")


class ApplicationsAPIError(Exception):
    """Base Applications API error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        code: str = "api_error",
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details


class ValidationAPIError(ApplicationsAPIError):
    """Invalid client input."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            message,
            status_code=422,
            code="validation_error",
            details=details,
        )


class PipelineAPIError(ApplicationsAPIError):
    """Engine pipeline orchestration failure."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            message,
            status_code=500,
            code="pipeline_error",
            details=details,
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach JSON error handlers."""

    @app.exception_handler(ApplicationsAPIError)
    async def applications_api_error_handler(
        request: Request,
        exc: ApplicationsAPIError,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "API error request_id=%s code=%s path=%s",
            request_id,
            exc.code,
            request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "code": exc.code,
                "details": exc.details,
                "request_id": request_id,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "Unhandled error request_id=%s path=%s",
            request_id,
            request.url.path,
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(exc),
                "code": "internal_error",
                "request_id": request_id,
            },
        )

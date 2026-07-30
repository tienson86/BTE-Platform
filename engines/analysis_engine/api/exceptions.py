"""Analysis Engine API exceptions."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AnalysisAPIError(Exception):
    """Base HTTP-mapped API error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        code: str = "analysis_api_error",
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AnalysisAPIError):
    """Resource not found."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message,
            status_code=404,
            code="not_found",
            details=details,
        )


class AuthenticationError(AnalysisAPIError):
    """Missing or invalid credentials."""

    def __init__(self, message: str = "Not authenticated") -> None:
        super().__init__(message, status_code=401, code="unauthorized")


class AuthorizationError(AnalysisAPIError):
    """Authenticated but missing role/permission."""

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, status_code=403, code="forbidden")


def register_exception_handlers(app: FastAPI) -> None:
    """Register JSON exception handlers."""

    @app.exception_handler(AnalysisAPIError)
    async def _handle_analysis_api_error(
        request: Request,
        exc: AnalysisAPIError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "code": exc.code,
                "details": exc.details,
                "request_id": getattr(request.state, "request_id", None),
            },
        )

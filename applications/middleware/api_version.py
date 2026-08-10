"""API version header negotiation. Does not mount /api/v2."""

from __future__ import annotations

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from applications.errors.error_codes import HTTP_STATUS_BY_CODE, UNSUPPORTED_VERSION
from applications.errors.error_response import PublicServiceError, build_error_response
from applications.versioning.api_versions import CURRENT_API_VERSION
from applications.versioning.version_manager import default_version_manager

API_VERSION_HEADER = "API-Version"
API_VERSION_HEADER_ALT = "X-API-Version"


def resolve_api_version(request: Request) -> str:
    """Negotiate the public API version from header or default to v1."""
    requested = (
        request.headers.get(API_VERSION_HEADER)
        or request.headers.get(API_VERSION_HEADER_ALT)
        or CURRENT_API_VERSION
    )
    try:
        return default_version_manager.negotiate(requested)
    except ValueError as exc:
        raise PublicServiceError(UNSUPPORTED_VERSION, str(exc)) from exc


def register_api_version_middleware(app: FastAPI) -> None:
    """Attach negotiated API version to request state and response headers."""

    @app.middleware("http")
    async def api_version_middleware(request: Request, call_next) -> Response:
        try:
            version = resolve_api_version(request)
        except PublicServiceError as exc:
            request_id = str(getattr(request.state, "request_id", "") or "unknown")
            payload = build_error_response(
                code=exc.code,
                request_id=request_id,
                message=exc.public_message,
            )
            return JSONResponse(
                status_code=HTTP_STATUS_BY_CODE.get(exc.code, 400),
                content=payload.model_dump(mode="json"),
            )
        request.state.api_version = version
        response = await call_next(request)
        response.headers[API_VERSION_HEADER] = version
        return response

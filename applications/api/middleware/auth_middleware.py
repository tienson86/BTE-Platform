"""Optional JWT / API-key authentication middleware."""

from __future__ import annotations

from fastapi import FastAPI, Request, Response

from applications.api.config import settings


def register_auth_middleware(app: FastAPI) -> None:
    """
    Resolve credentials when present and set ``request.state.user``.

    Does not block anonymous access — route dependencies enforce auth.
    Existing public engine endpoints remain unchanged.
    """

    @app.middleware("http")
    async def auth_middleware(
        request: Request,
        call_next,
    ) -> Response:
        request.state.user = None
        try:
            from applications.api.dependencies import get_auth_service

            auth_service = get_auth_service()
            authorization = request.headers.get("Authorization")
            api_key = request.headers.get(settings.api_key_header)
            if authorization or api_key:
                user = auth_service.resolve_user_from_headers(
                    authorization=authorization,
                    api_key=api_key,
                )
                request.state.user = user
        except Exception:
            # Never fail the request in middleware; deps raise 401/403.
            request.state.user = None

        return await call_next(request)

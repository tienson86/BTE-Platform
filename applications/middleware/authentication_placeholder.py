"""Authentication placeholder.

Bearer Token is recognized. API Key, Refresh Token, and Role are reserved.
No login, validation, or session implementation.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, Response

AUTHORIZATION_HEADER = "Authorization"
API_KEY_HEADER = "X-API-Key"
REFRESH_TOKEN_HEADER = "X-Refresh-Token"
ROLE_HEADER = "X-Role"


def _parse_authorization(raw: str | None) -> dict[str, object]:
    value = (raw or "").strip()
    if not value:
        return {"scheme": None, "present": False, "validated": False}
    scheme, _, remainder = value.partition(" ")
    scheme_name = scheme.strip().lower()
    token_present = bool(remainder.strip()) if remainder else scheme_name == "bearer"
    return {
        "scheme": scheme_name or None,
        "present": True,
        "token_present": token_present,
        "validated": False,
    }


def register_authentication_placeholder_middleware(app: FastAPI) -> None:
    """Attach unvalidated auth context. Never blocks requests in Beta-2."""

    @app.middleware("http")
    async def authentication_placeholder_middleware(request: Request, call_next) -> Response:
        auth = _parse_authorization(request.headers.get(AUTHORIZATION_HEADER))
        api_key_present = bool((request.headers.get(API_KEY_HEADER) or "").strip())
        refresh_present = bool((request.headers.get(REFRESH_TOKEN_HEADER) or "").strip())
        role = (request.headers.get(ROLE_HEADER) or "").strip() or None
        request.state.auth = {
            "bearer": auth,
            "api_key": {"present": api_key_present, "reserved": True, "validated": False},
            "refresh_token": {"present": refresh_present, "reserved": True, "validated": False},
            "role": {"value": role, "reserved": True, "validated": False},
        }
        response = await call_next(request)
        return response

"""Auth token issuance (JWT-ready demo)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from engines.analysis_engine.api.auth import (
    JWTManager,
    Permission,
    Role,
    get_jwt_manager,
    require_permission,
)
from engines.analysis_engine.api.auth.dependencies import Principal
from engines.analysis_engine.api.exceptions import AuthorizationError
from engines.analysis_engine.api.schemas import APIEnvelope, TokenRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=APIEnvelope)
def issue_token(
    request: Request,
    body: TokenRequest,
    jwt_manager: JWTManager = Depends(get_jwt_manager),
    principal: Principal = Depends(require_permission(Permission.TOKEN_ISSUE)),
) -> APIEnvelope:
    """Issue a signed access JWT (development / integration)."""
    try:
        role = Role(body.role)
    except ValueError as exc:
        raise AuthorizationError(f"Unknown role: {body.role}") from exc
    # Non-admins may only issue tokens for themselves at equal-or-lower privilege.
    if principal.role != Role.ADMIN and role == Role.ADMIN:
        raise AuthorizationError("Cannot issue ADMIN token")
    pair = jwt_manager.create_access_token(
        subject=body.subject,
        role=role.value,
        username=body.username,
    )
    return APIEnvelope(
        success=True,
        message="Token issued",
        data={
            "access_token": pair.access_token,
            "token_type": pair.token_type,
            "expires_in": pair.expires_in,
            "role": role.value,
            "issued_by": principal.username,
        },
        request_id=getattr(request.state, "request_id", None),
    )

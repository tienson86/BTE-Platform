"""License API routes (WP14)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, Depends, Request

from applications.api.config import settings
from applications.api.exceptions import ApplicationsAPIError, ValidationAPIError
from applications.api.schemas.common import APIResponse
from applications.api.schemas.license import (
    LicenseActivateRequest,
    LicenseIssueRequest,
    LicenseValidateRequest,
)
from applications.license.activation import ActivationError
from applications.license.service import LicenseService

router = APIRouter(prefix="/license", tags=["License"])


@lru_cache(maxsize=1)
def get_license_service() -> LicenseService:
    """Resolve license service rooted at API data_dir."""
    return LicenseService.from_data_dir(Path(settings.data_dir))


def clear_license_cache() -> None:
    """Clear cached license service (tests)."""
    get_license_service.cache_clear()


def _envelope(request: Request, message: str, data: dict) -> APIResponse:
    return APIResponse(
        success=True,
        message=message,
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )


@router.post("/activate", response_model=APIResponse)
def activate_license(
    request: Request,
    body: LicenseActivateRequest,
    service: LicenseService = Depends(get_license_service),
) -> APIResponse:
    """Activate a license key on this machine (offline)."""
    try:
        license_obj = service.activate(body.license_key)
    except ActivationError as exc:
        raise ApplicationsAPIError(
            str(exc),
            status_code=400,
            code="license_activation_failed",
        ) from exc
    return _envelope(
        request,
        "License activated",
        {"license": license_obj.to_dict()},
    )


@router.get("/status", response_model=APIResponse)
def license_status(
    request: Request,
    service: LicenseService = Depends(get_license_service),
) -> APIResponse:
    """Current license status."""
    return _envelope(request, "License status", service.status())


@router.post("/validate", response_model=APIResponse)
def validate_license(
    request: Request,
    body: LicenseValidateRequest,
    service: LicenseService = Depends(get_license_service),
) -> APIResponse:
    """Validate license expiration / feature / usage limits."""
    try:
        result = service.validate(
            license_key=body.license_key,
            feature=body.feature,
            current_users=body.current_users,
            current_cases=body.current_cases,
        )
    except ValueError as exc:
        raise ValidationAPIError(str(exc)) from exc
    return _envelope(request, "License validation", result.to_dict())


@router.get("/features", response_model=APIResponse)
def license_features(
    request: Request,
    service: LicenseService = Depends(get_license_service),
) -> APIResponse:
    """Enabled features for the active license."""
    return _envelope(request, "License features", service.features())


@router.post("/issue", response_model=APIResponse, include_in_schema=True)
def issue_license(
    request: Request,
    body: LicenseIssueRequest,
    service: LicenseService = Depends(get_license_service),
) -> APIResponse:
    """
    Dev helper: issue an offline license (no payment / no online activation).

    Useful for local setup and tests; not a billing endpoint.
    """
    try:
        license_obj = service.issue(
            edition=body.edition,
            customer=body.customer,
            organization=body.organization,
            days_valid=body.days_valid,
            max_users=body.max_users,
            max_cases=body.max_cases,
        )
    except ValueError as exc:
        raise ValidationAPIError(str(exc)) from exc
    return _envelope(
        request,
        "License issued",
        {"license": license_obj.to_dict()},
    )

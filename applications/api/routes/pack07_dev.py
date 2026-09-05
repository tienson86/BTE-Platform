"""Development-only Pack 07 diagnostics routes. Disabled in production."""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException, Request

from applications.api.dependencies import get_orchestrator
from applications.api.routes._helpers import attach_presentation_metadata
from applications.api.schemas.common import APIResponse, BirthRequest
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.result_identity import stamp_customer_result_identity
from engines.detailed_interpretation_engine.diagnostics import (
    build_pack07_diagnostics,
    diagnostics_from_payload,
)
from engines.detailed_interpretation_engine.factories import build_canonical_analysis_context

router = APIRouter(tags=["pack07-dev"])


def pack07_dev_enabled() -> bool:
    """True when Pack 07 developer diagnostics may be exposed."""
    env = (os.getenv("BTE_ENV") or os.getenv("APP_ENV") or "development").strip().lower()
    return env not in {"production", "prod"}


def _require_dev() -> None:
    if not pack07_dev_enabled():
        raise HTTPException(status_code=404, detail="Not Found")


@router.get("/dev/pack07/diagnostics", response_model=APIResponse)
def pack07_diagnostics_foundation() -> APIResponse:
    """Empty-shell Pack 07 diagnostics. No customer payload."""
    _require_dev()
    context = build_canonical_analysis_context("dev-pack07")
    data = build_pack07_diagnostics(context).to_dict()
    return APIResponse(success=True, message="Pack 07 diagnostics OK", data=data)


@router.post("/dev/pack07/diagnostics", response_model=APIResponse)
def pack07_diagnostics_from_analyze(
    request: Request,
    body: BirthRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> APIResponse:
    """Diagnostics after a fresh analyze. Returns states only, not customer cards."""
    _require_dev()
    payload = orchestrator.analyze(
        year=body.year,
        month=body.month,
        day=body.day,
        hour=body.hour,
        minute=body.minute,
        gender=body.gender,
        timezone=body.timezone,
    )
    payload = attach_presentation_metadata(payload, body)
    payload = stamp_customer_result_identity(
        payload,
        getattr(request.state, "request_id", None),
    )
    data = diagnostics_from_payload(payload).to_dict()
    return APIResponse(
        success=True,
        message="Pack 07 diagnostics OK",
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )

"""Interpretation routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from engines.analysis_engine.api.auth import Permission, require_permission
from engines.analysis_engine.api.auth.dependencies import Principal
from engines.analysis_engine.api.dependencies import get_interpretation_service
from engines.analysis_engine.api.schemas import APIEnvelope, InterpretationRequest
from engines.analysis_engine.api.services.interpretation_service import (
    InterpretationService,
)

router = APIRouter(prefix="/interpretation", tags=["Interpretation"])


@router.post("", response_model=APIEnvelope)
def run_interpretation(
    request: Request,
    body: InterpretationRequest,
    service: InterpretationService = Depends(get_interpretation_service),
    _principal: Principal = Depends(
        require_permission(Permission.INTERPRETATION_EXECUTE)
    ),
) -> APIEnvelope:
    """Run Interpretation Engine for an analysis."""
    record = service.interpret(body.analysis_id)
    return APIEnvelope(
        success=True,
        message="Interpretation OK",
        data=dict(record.payload),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{interpretation_id}", response_model=APIEnvelope)
def get_interpretation(
    request: Request,
    interpretation_id: str,
    service: InterpretationService = Depends(get_interpretation_service),
    _principal: Principal = Depends(
        require_permission(Permission.INTERPRETATION_READ)
    ),
) -> APIEnvelope:
    """Read a stored interpretation."""
    record = service.get(interpretation_id)
    return APIEnvelope(
        success=True,
        message="Interpretation OK",
        data=dict(record.payload),
        request_id=getattr(request.state, "request_id", None),
    )

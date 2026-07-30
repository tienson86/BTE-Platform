"""Analysis routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from engines.analysis_engine.api.auth import Permission, require_permission
from engines.analysis_engine.api.auth.dependencies import Principal
from engines.analysis_engine.api.dependencies import get_analysis_service
from engines.analysis_engine.api.schemas import APIEnvelope, AnalysisRequest
from engines.analysis_engine.api.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("", response_model=APIEnvelope)
def run_analysis(
    request: Request,
    body: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),
    _principal: Principal = Depends(require_permission(Permission.ANALYSIS_EXECUTE)),
) -> APIEnvelope:
    """Run Analysis Runtime for a chart."""
    record = service.analyze(body.chart_id)
    return APIEnvelope(
        success=True,
        message="Analysis OK",
        data=dict(record.payload),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{analysis_id}", response_model=APIEnvelope)
def get_analysis(
    request: Request,
    analysis_id: str,
    service: AnalysisService = Depends(get_analysis_service),
    _principal: Principal = Depends(require_permission(Permission.ANALYSIS_READ)),
) -> APIEnvelope:
    """Read a stored analysis."""
    record = service.get(analysis_id)
    return APIEnvelope(
        success=True,
        message="Analysis OK",
        data=dict(record.payload),
        request_id=getattr(request.state, "request_id", None),
    )

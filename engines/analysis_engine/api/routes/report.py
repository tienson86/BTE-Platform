"""Report routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from engines.analysis_engine.api.auth import Permission, require_permission
from engines.analysis_engine.api.auth.dependencies import Principal
from engines.analysis_engine.api.dependencies import get_report_service
from engines.analysis_engine.api.schemas import APIEnvelope, ReportRequest
from engines.analysis_engine.api.services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["Report"])


@router.post("", response_model=APIEnvelope)
def generate_report(
    request: Request,
    body: ReportRequest,
    service: ReportService = Depends(get_report_service),
    _principal: Principal = Depends(require_permission(Permission.REPORT_GENERATE)),
) -> APIEnvelope:
    """Generate multi-format report from interpretation."""
    record = service.generate(body)
    return APIEnvelope(
        success=True,
        message="Report OK",
        data=dict(record.payload),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{report_id}", response_model=APIEnvelope)
def get_report(
    request: Request,
    report_id: str,
    service: ReportService = Depends(get_report_service),
    _principal: Principal = Depends(require_permission(Permission.REPORT_READ)),
) -> APIEnvelope:
    """Read a stored report."""
    record = service.get(report_id)
    return APIEnvelope(
        success=True,
        message="Report OK",
        data=dict(record.payload),
        request_id=getattr(request.state, "request_id", None),
    )

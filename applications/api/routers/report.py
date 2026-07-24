"""POST /api/v1/report — full BTE report pipeline."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from applications.api.schemas import ReportRequest, ReportResponse
from applications.api.services.report_pipeline import ReportPipelineService

router = APIRouter(tags=["Report"])
_service = ReportPipelineService()


@router.post("/report", response_model=ReportResponse)
def create_report(request: ReportRequest) -> ReportResponse:
    """
    Run Calendar → Bazi → Pattern → Score → Interpretation → Report → Narrative.
    """
    try:
        data = _service.run(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            gender=request.gender,
            timezone=request.timezone,
        )
        return ReportResponse(
            success=True,
            message="Report pipeline completed.",
            data=data,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

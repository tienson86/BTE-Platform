"""Chart routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from engines.analysis_engine.api.auth import Permission, require_permission
from engines.analysis_engine.api.auth.dependencies import Principal
from engines.analysis_engine.api.dependencies import get_chart_service
from engines.analysis_engine.api.schemas import APIEnvelope, CreateChartRequest
from engines.analysis_engine.api.services.chart_service import ChartService

router = APIRouter(prefix="/charts", tags=["Charts"])


@router.post("", response_model=APIEnvelope)
def create_chart(
    request: Request,
    body: CreateChartRequest,
    service: ChartService = Depends(get_chart_service),
    _principal: Principal = Depends(require_permission(Permission.CHART_CREATE)),
) -> APIEnvelope:
    """Create Chart — natal chart snapshot for analysis."""
    record = service.create(body)
    return APIEnvelope(
        success=True,
        message="Chart created",
        data={
            "chart_id": record.chart_id,
            "chart": record.chart,
            "calendar": record.calendar,
            "metadata": record.metadata,
        },
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{chart_id}", response_model=APIEnvelope)
def get_chart(
    request: Request,
    chart_id: str,
    service: ChartService = Depends(get_chart_service),
    _principal: Principal = Depends(require_permission(Permission.CHART_READ)),
) -> APIEnvelope:
    """Read a stored chart."""
    record = service.get(chart_id)
    return APIEnvelope(
        success=True,
        message="Chart OK",
        data={
            "chart_id": record.chart_id,
            "chart": record.chart,
            "calendar": record.calendar,
            "metadata": record.metadata,
        },
        request_id=getattr(request.state, "request_id", None),
    )

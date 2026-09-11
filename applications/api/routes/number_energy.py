"""Number Energy API routes — isolated from Bazi analysis."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from applications.api.dependencies import get_number_energy_api_service
from applications.api.exceptions import PipelineAPIError, ValidationAPIError
from applications.api.schemas.common import APIResponse
from applications.api.schemas.number_energy import NumberEnergyRequest
from applications.api.services.number_energy_service import NumberEnergyAPIService
from engines.number_energy.exceptions import (
    NumberEnergyEngineError,
    NumberEnergyValidationError,
)

router = APIRouter(prefix="/number-energy", tags=["number-energy"])


@router.post("/analyze", response_model=APIResponse)
def analyze_number_energy(
    request: Request,
    body: NumberEnergyRequest,
    service: NumberEnergyAPIService = Depends(get_number_energy_api_service),
) -> APIResponse:
    """Analyze a digit string with frozen V1 Bát Cực Linh Số rules."""
    try:
        data = service.analyze(body.number, purpose_context=body.purpose_context)
    except NumberEnergyValidationError as exc:
        raise ValidationAPIError(str(exc)) from exc
    except NumberEnergyEngineError as exc:
        raise PipelineAPIError(str(exc)) from exc
    return APIResponse(
        success=True,
        message="Number Energy OK",
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )

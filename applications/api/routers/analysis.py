"""Public analysis router."""

from __future__ import annotations

from datetime import datetime, timezone
import logging

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.error_response import ApiError, ErrorResponse
from applications.api.contracts.report_response import ReportResponse
from applications.api.dependencies.services import get_analysis_service
from applications.api.exceptions import ApplicationsAPIError
from applications.api.services.analysis_service import AnalysisService

router = APIRouter(tags=["analysis"])
logger = logging.getLogger("bte.applications.api")


def _error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    request_id: str | None,
) -> JSONResponse:
    """Build a contract ErrorResponse without exposing stack traces."""
    payload = ErrorResponse(
        success=False,
        error=ApiError(
            code=code,
            message=message,
            details=None,
            request_id=request_id,
            timestamp=datetime.now(timezone.utc),
        ),
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(mode="json"),
    )


@router.post(
    "/analysis",
    response_model=ReportResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
def create_analysis(
    request: AnalyzeRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> ReportResponse | Response:
    """Run the analysis pipeline and return ReportResponse."""
    try:
        return service.execute(request)
    except ApplicationsAPIError as exc:
        logger.exception(
            "analysis failed request_id=%s code=%s",
            request.request_id,
            exc.code,
        )
        return _error_response(
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            request_id=request.request_id,
        )
    except ValueError as exc:
        logger.exception("analysis validation failed request_id=%s", request.request_id)
        return _error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="validation_error",
            message=str(exc),
            request_id=request.request_id,
        )
    except Exception:
        logger.exception("unexpected analysis failure request_id=%s", request.request_id)
        return _error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="internal_error",
            message="Unexpected analysis failure.",
            request_id=request.request_id,
        )

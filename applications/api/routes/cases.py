"""Case CRUD + export routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request, Response

from applications.api.dependencies import get_case_service
from applications.api.exceptions import ApplicationsAPIError, ValidationAPIError
from applications.api.schemas.case import CaseCreateRequest
from applications.api.schemas.common import APIResponse
from applications.case_management.models import CaseModel
from applications.case_management.service import (
    CaseNotFoundError,
    CaseService,
    CaseServiceError,
)
from applications.customer.service import CustomerNotFoundError

router = APIRouter(prefix="/cases", tags=["Cases"])


def _case_not_found(case_id: str) -> ApplicationsAPIError:
    return ApplicationsAPIError(
        f"Case not found: {case_id}",
        status_code=404,
        code="case_not_found",
    )


@router.get("", response_model=APIResponse)
def list_cases(
    request: Request,
    customer_id: str | None = Query(None),
    service: CaseService = Depends(get_case_service),
) -> APIResponse:
    """List cases (optional customer filter)."""
    cases = service.list(customer_id=customer_id)
    return APIResponse(
        success=True,
        message="OK",
        data={"cases": [c.to_dict() for c in cases], "count": len(cases)},
        request_id=getattr(request.state, "request_id", None),
    )


@router.post("", response_model=APIResponse)
def create_case(
    request: Request,
    body: CaseCreateRequest,
    service: CaseService = Depends(get_case_service),
) -> APIResponse:
    """Create a case record manually."""
    try:
        case = CaseModel.create(
            customer_id=body.customer_id,
            engine_version=body.engine_version or service.engine_version,
            input_snapshot=body.input_snapshot,
            calendar_result=body.calendar_result,
            bazi_result=body.bazi_result,
            pattern_result=body.pattern_result,
            score_result=body.score_result,
            interpretation_result=body.interpretation_result,
            report_result=body.report_result,
            narrative_result=body.narrative_result,
        )
        saved = service.create(case)
    except CustomerNotFoundError as exc:
        raise ApplicationsAPIError(
            f"Customer not found: {body.customer_id}",
            status_code=404,
            code="customer_not_found",
        ) from exc
    except CaseServiceError as exc:
        raise ValidationAPIError(str(exc)) from exc
    return APIResponse(
        success=True,
        message="Case created",
        data={"case": saved.to_dict()},
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{case_id}", response_model=APIResponse)
def get_case(
    request: Request,
    case_id: str,
    service: CaseService = Depends(get_case_service),
) -> APIResponse:
    """Get case by id."""
    try:
        case = service.get(case_id)
    except CaseNotFoundError as exc:
        raise _case_not_found(case_id) from exc
    return APIResponse(
        success=True,
        message="OK",
        data={"case": case.to_dict()},
        request_id=getattr(request.state, "request_id", None),
    )


@router.delete("/{case_id}", response_model=APIResponse)
def delete_case(
    request: Request,
    case_id: str,
    service: CaseService = Depends(get_case_service),
) -> APIResponse:
    """Delete a case."""
    deleted = service.delete(case_id)
    if not deleted:
        raise _case_not_found(case_id)
    return APIResponse(
        success=True,
        message="Case deleted",
        data={"case_id": case_id},
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{case_id}/export")
def export_case(
    case_id: str,
    format: str = Query("json", pattern="^(json|markdown|html)$"),
    service: CaseService = Depends(get_case_service),
) -> Response:
    """Export a case as JSON, Markdown, or HTML."""
    try:
        content = service.export(case_id, fmt=format)  # type: ignore[arg-type]
    except CaseNotFoundError as exc:
        raise _case_not_found(case_id) from exc

    media = {
        "json": "application/json",
        "markdown": "text/markdown; charset=utf-8",
        "html": "text/html; charset=utf-8",
    }[format]
    return Response(content=content, media_type=media)

"""Regression and approval workflow routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from applications.validation_console.api.schemas import (
    APIEnvelope,
    RegressionRequest,
    WorkflowRequest,
)
from applications.validation_console.api.services import (
    GoldenDatasetService,
    NotFoundError,
    ValidationConsoleError,
    ValidationError,
    WorkflowError,
)

router = APIRouter(tags=["Regression", "Workflow"])


def _service() -> GoldenDatasetService:
    return GoldenDatasetService()


def _envelope(request: Request, *, message: str, data: object) -> APIEnvelope:
    return APIEnvelope(
        success=True,
        message=message,
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )


def _http_error(exc: ValidationConsoleError) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(
            status_code=404,
            detail={"message": exc.message, **exc.details},
        )
    if isinstance(exc, ValidationError):
        return HTTPException(
            status_code=422,
            detail={
                "message": exc.message,
                "issues": [issue.to_dict() for issue in exc.issues],
                **exc.details,
            },
        )
    if isinstance(exc, WorkflowError):
        return HTTPException(
            status_code=409,
            detail={"message": exc.message, **exc.details},
        )
    return HTTPException(
        status_code=400,
        detail={"message": exc.message, **exc.details},
    )


@router.post("/datasets/{dataset_id}/regression")
def run_regression(
    request: Request,
    dataset_id: str,
    body: RegressionRequest | None = None,
) -> APIEnvelope:
    """Run regression test for a dataset."""
    actor = body.actor if body else "validator"
    try:
        data = _service().run_regression(dataset_id, actor=actor)
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Regression complete", data=data)


@router.get("/workflow/queue")
def approval_queue(request: Request) -> APIEnvelope:
    """List datasets in review."""
    data = _service().approval_queue()
    return _envelope(request, message="OK", data=data)


@router.post("/workflow/{dataset_id}")
def transition(
    request: Request,
    dataset_id: str,
    body: WorkflowRequest,
) -> APIEnvelope:
    """Submit / approve / reject / release a dataset."""
    try:
        data = _service().transition(
            dataset_id,
            action=body.action,
            actor=body.actor,
            message=body.message,
        )
    except ValidationConsoleError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Workflow updated", data=data)

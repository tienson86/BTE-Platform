"""Approval workflow routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from applications.knowledge_console.api.schemas import APIEnvelope, WorkflowRequest
from applications.knowledge_console.api.services import (
    KnowledgeEditorError,
    KnowledgeEditorService,
    NotFoundError,
    ValidationError,
    WorkflowError,
)

router = APIRouter(tags=["Workflow"])


def _service() -> KnowledgeEditorService:
    """Resolve editor service against the process store."""
    return KnowledgeEditorService()


def _envelope(request: Request, *, message: str, data: object) -> APIEnvelope:
    return APIEnvelope(
        success=True,
        message=message,
        data=data,
        request_id=getattr(request.state, "request_id", None),
    )


def _http_error(exc: KnowledgeEditorError) -> HTTPException:
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


@router.get("/workflow/queue")
def approval_queue(request: Request) -> APIEnvelope:
    """List assets in review."""
    data = _service().approval_queue()
    return _envelope(request, message="OK", data=data)


@router.post("/workflow/{asset_id}")
def transition(
    request: Request,
    asset_id: str,
    body: WorkflowRequest,
) -> APIEnvelope:
    """Submit / approve / reject / release an asset."""
    try:
        data = _service().transition(
            asset_id,
            action=body.action,
            actor=body.actor,
            message=body.message,
        )
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Workflow updated", data=data)

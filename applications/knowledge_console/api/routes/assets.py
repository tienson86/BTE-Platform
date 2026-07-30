"""Asset CRUD, validate, preview, diff, history, versions."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request

from applications.knowledge_console.api.schemas import (
    APIEnvelope,
    CreateAssetRequest,
    UpdateAssetRequest,
)
from applications.knowledge_console.api.services import (
    KnowledgeEditorError,
    KnowledgeEditorService,
    NotFoundError,
    ValidationError,
    WorkflowError,
)

router = APIRouter(tags=["Assets"])


def _service() -> KnowledgeEditorService:
    """Resolve editor service against the process store."""
    return KnowledgeEditorService()


def _envelope(
    request: Request,
    *,
    message: str,
    data: object,
) -> APIEnvelope:
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


@router.get("/assets")
def list_assets(
    request: Request,
    asset_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> APIEnvelope:
    """List knowledge assets."""
    try:
        data = _service().list_assets(asset_type=asset_type, status=status)
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.post("/assets")
def create_asset(request: Request, body: CreateAssetRequest) -> APIEnvelope:
    """Create a draft knowledge asset."""
    try:
        data = _service().create_asset(
            asset_type=body.asset_type,
            title=body.title,
            content=body.content,
            actor=body.actor,
            metadata=body.metadata,
        )
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Created", data=data)


@router.get("/assets/{asset_id}")
def get_asset(request: Request, asset_id: str) -> APIEnvelope:
    """Read one asset."""
    try:
        data = _service().get_asset(asset_id)
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.put("/assets/{asset_id}")
def update_asset(
    request: Request,
    asset_id: str,
    body: UpdateAssetRequest,
) -> APIEnvelope:
    """Update a draft/rejected asset."""
    try:
        data = _service().update_asset(
            asset_id,
            title=body.title,
            content=body.content,
            actor=body.actor,
            note=body.note,
        )
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Updated", data=data)


@router.post("/assets/{asset_id}/validate")
def validate_asset(request: Request, asset_id: str) -> APIEnvelope:
    """Validate asset content."""
    try:
        data = _service().validate(asset_id)
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="Validated", data=data)


@router.get("/assets/{asset_id}/preview")
def preview_asset(request: Request, asset_id: str) -> APIEnvelope:
    """Preview rendered asset text."""
    try:
        data = _service().preview(asset_id)
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.get("/assets/{asset_id}/history")
def asset_history(request: Request, asset_id: str) -> APIEnvelope:
    """Return asset history."""
    try:
        data = _service().history(asset_id)
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.get("/assets/{asset_id}/versions")
def asset_versions(request: Request, asset_id: str) -> APIEnvelope:
    """Return version snapshots."""
    try:
        data = _service().versions(asset_id)
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)


@router.get("/assets/{asset_id}/diff")
def asset_diff(
    request: Request,
    asset_id: str,
    from_version: str = Query(...),
    to_version: str | None = Query(default=None),
) -> APIEnvelope:
    """Diff two versions (or current draft)."""
    try:
        data = _service().diff(
            asset_id,
            from_version=from_version,
            to_version=to_version,
        )
    except KnowledgeEditorError as exc:
        raise _http_error(exc) from exc
    return _envelope(request, message="OK", data=data)

"""FastAPI routes for TV-01 Marriage Consulting public resources."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, Header, Query, Request, Response
from fastapi.responses import JSONResponse

from consulting.marriage.api.parse import parse_consultation_request
from consulting.marriage.api.serializers import (
    collect_warnings,
    public_version_bundle,
    serialize_consultation,
    serialize_envelope,
    serialize_error,
    serialize_history_row,
    serialize_report,
    serialize_runtime_error,
    serialize_summary,
)
from consulting.marriage.api.service import MarriageConsultationApi
from consulting.marriage.api.versions import API_VERSION
from consulting.marriage.exceptions import (
    MarriageConflictError,
    MarriageConsultingError,
    MarriageNotFoundError,
    MarriageValidationError,
)
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.runtime.container import MarriageContainer


def create_marriage_api_app(container: MarriageContainer | None = None):
    """Create an isolated FastAPI app that exposes TV-01 public routes."""
    from fastapi import FastAPI

    from consulting.marriage.runtime.api_wiring import wire_marriage_api_runtime

    bound = container or wire_marriage_api_runtime()
    app = FastAPI(title="TV-01 Marriage Consulting API", version=API_VERSION)
    app.include_router(build_marriage_router(bound), prefix="/api/v1")
    return app


def build_marriage_router(container: MarriageContainer) -> APIRouter:
    """Build `/consulting/marriage` routes bound to a TV-01 container."""
    api = container.api_contract
    if not isinstance(api, MarriageConsultationApi):
        raise TypeError("marriage_api_not_bound")
    router = APIRouter(prefix="/consulting/marriage", tags=["consulting-marriage"])

    @router.post("")
    def create_consultation(
        request: Request,
        response: Response,
        body: dict[str, Any] = Body(...),
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    ) -> JSONResponse:
        """POST /api/v1/consulting/marriage"""
        try:
            parsed = parse_consultation_request(body, idempotency_key=idempotency_key)
            created = api.create_consultation(parsed)
        except (MarriageValidationError, MarriageConflictError, MarriageConsultingError) as exc:
            return _error_response(exc, consultation_id=None)
        if created.status is not MarriageRuntimeStatus.SUCCESS:
            http_status = 400 if created.error and created.error.code == "VALIDATION_ERROR" else 500
            error = (
                serialize_runtime_error(created.error, created.consultation_id)
                if created.error
                else serialize_error(
                    code="INTERNAL_ERROR",
                    stage="runtime",
                    consultation_id=created.consultation_id,
                )
            )
            return JSONResponse(
                status_code=http_status,
                content=serialize_envelope(
                    status=MarriageRuntimeStatus.FAILED,
                    data=None,
                    errors=[error],
                    versions={"api_version": API_VERSION},
                ),
            )
        stored = api.get_stored(created.consultation_id or "")
        expert = _expert_requested(request, stored.request.options.expert_mode if stored.request.options else None)
        http_status = 200 if api.last_create_was_replay else 201
        response.status_code = http_status
        return JSONResponse(
            status_code=http_status,
            content=serialize_envelope(
                status=created.status,
                data=serialize_consultation(stored, expert=expert),
                warnings=collect_warnings(stored),
                versions=public_version_bundle(stored.result),
            ),
        )

    @router.get("/history")
    def list_history(
        cursor: str | None = Query(default=None),
        limit: int | None = Query(default=None),
        status: str | None = Query(default=None),
        language: str | None = Query(default=None),
        grade: str | None = Query(default=None),
    ) -> JSONResponse:
        """GET /api/v1/consulting/marriage/history"""
        try:
            rows, next_cursor = api.list_history_page(
                cursor=cursor,
                limit=limit,
                status=status,
                language=language,
                grade=grade,
            )
        except MarriageValidationError as exc:
            return _error_response(exc, consultation_id=None)
        return JSONResponse(
            content=serialize_envelope(
                status=MarriageRuntimeStatus.SUCCESS,
                data={
                    "items": [serialize_history_row(item) for item in rows],
                    "next_cursor": next_cursor,
                },
                versions={"api_version": API_VERSION},
            )
        )

    @router.get("/{consultation_id}")
    def get_consultation(request: Request, consultation_id: str) -> JSONResponse:
        """GET /api/v1/consulting/marriage/{consultation_id}"""
        try:
            stored = api.get_stored(consultation_id)
        except MarriageNotFoundError as exc:
            return _error_response(exc, consultation_id=consultation_id)
        expert = _expert_requested(request, stored.request.options.expert_mode if stored.request.options else None)
        return JSONResponse(
            content=serialize_envelope(
                status=stored.status,
                data=serialize_consultation(stored, expert=expert),
                warnings=collect_warnings(stored),
                versions=public_version_bundle(stored.result),
            )
        )

    @router.get("/{consultation_id}/summary")
    def get_summary(consultation_id: str) -> JSONResponse:
        """GET /api/v1/consulting/marriage/{consultation_id}/summary"""
        try:
            stored = api.get_stored(consultation_id)
        except MarriageNotFoundError as exc:
            return _error_response(exc, consultation_id=consultation_id)
        return JSONResponse(
            content=serialize_envelope(
                status=stored.status,
                data=serialize_summary(stored),
                warnings=collect_warnings(stored),
                versions=public_version_bundle(stored.result),
            )
        )

    @router.get("/{consultation_id}/report")
    def get_report(request: Request, consultation_id: str) -> JSONResponse:
        """GET /api/v1/consulting/marriage/{consultation_id}/report"""
        try:
            stored = api.get_stored(consultation_id)
        except MarriageNotFoundError as exc:
            return _error_response(exc, consultation_id=consultation_id)
        expert = _expert_requested(request, stored.request.options.expert_mode if stored.request.options else None)
        return JSONResponse(
            content=serialize_envelope(
                status=stored.status,
                data=serialize_report(stored, expert=expert),
                warnings=collect_warnings(stored),
                versions=public_version_bundle(stored.result),
            )
        )

    return router


def _expert_requested(request: Request, stored_flag: bool | None) -> bool:
    """Expert mode from query or stored option. Does not change Decision."""
    raw = request.query_params.get("expert")
    if raw is not None:
        return raw.strip().lower() in {"1", "true", "yes"}
    return bool(stored_flag)


def _error_response(exc: MarriageConsultingError, consultation_id: str | None) -> JSONResponse:
    """Map typed errors onto HTTP + business FAILED. No stack traces."""
    if isinstance(exc, MarriageValidationError):
        status_code = 400
        code = "VALIDATION_ERROR"
        stage = "request_validation"
    elif isinstance(exc, MarriageNotFoundError):
        status_code = 404
        code = "NOT_FOUND"
        stage = "api"
    elif isinstance(exc, MarriageConflictError):
        status_code = 409
        code = "CONFLICT"
        stage = "idempotency"
    else:
        status_code = 500
        code = "INTERNAL_ERROR"
        stage = "api"
    return JSONResponse(
        status_code=status_code,
        content=serialize_envelope(
            status=MarriageRuntimeStatus.FAILED,
            data=None,
            errors=[
                serialize_error(
                    code=code,
                    stage=stage,
                    consultation_id=consultation_id,
                    detail=str(exc) if code == "VALIDATION_ERROR" else None,
                )
            ],
            versions={"api_version": API_VERSION},
        ),
    )

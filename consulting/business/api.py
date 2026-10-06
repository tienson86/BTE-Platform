"""Archived business profiles hosted alongside the shared compatibility API."""

from dataclasses import asdict, replace
from typing import Literal

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask

from consulting.business.export import export_business_file
from consulting.business.presentation import resolve_business_profile, business_context
from consulting.marriage.api.serializers import collect_warnings, serialize_consultation, serialize_envelope, serialize_error, serialize_report
from consulting.marriage.api.service import MarriageConsultationApi
from consulting.marriage.dto.history import MarriageStoredResult
from consulting.marriage.exceptions import MarriageNotFoundError, MarriageValidationError
from consulting.marriage.models.enums import MarriageRuntimeStatus
from consulting.marriage.report.export import cleanup_marriage_export


def _profile_data(stored: MarriageStoredResult) -> dict:
    context = business_context(stored)
    return {
        "consultation_id": stored.history.consultation_id,
        "display_identity": f"{stored.result.person_a.display_name or 'Đối tác A'} / {stored.result.person_b.display_name or 'Đối tác B'}",
        "created_at": stored.history.created_at,
        "saved_at": stored.business_profile.saved_at if stored.business_profile else None,
        **(context or {}),
    }


def _error(code: str, consultation_id: str | None = None, stage: str = "archive") -> JSONResponse:
    return JSONResponse(status_code={"NOT_FOUND": 404, "VALIDATION_ERROR": 400}.get(code, 500), content=serialize_envelope(status=MarriageRuntimeStatus.FAILED, data=None, errors=[serialize_error(code=code, stage=stage, consultation_id=consultation_id)]))


def build_business_archive_router(api: MarriageConsultationApi) -> APIRouter:
    router = APIRouter(prefix="/business", tags=["consulting-business"])

    @router.get("/history")
    def history(cursor: str | None = None, limit: int = Query(default=100)):
        try:
            records, next_cursor = api.list_business_history_page(cursor=cursor, limit=limit)
        except MarriageValidationError:
            return _error("VALIDATION_ERROR")
        return serialize_envelope(status=MarriageRuntimeStatus.SUCCESS, data={"items": [_profile_data(stored) for stored in records], "next_cursor": next_cursor})

    @router.get("/{consultation_id}")
    def get_profile(consultation_id: str):
        try:
            stored = api.get_business_stored(consultation_id)
        except MarriageNotFoundError:
            return _error("NOT_FOUND", consultation_id)
        profile = resolve_business_profile(stored)
        payload = serialize_consultation(stored, expert=False)
        payload.update(assessment_cards=profile.assessment_cards, business_score=asdict(profile.business_score) if profile.business_score else None, business_context=_profile_data(stored), input={"person_a": asdict(stored.request.person_a), "person_b": asdict(stored.request.person_b)})
        payload["score"] = payload["grade"] = None
        return serialize_envelope(status=stored.status, data=payload, warnings=collect_warnings(stored))

    @router.get("/{consultation_id}/report")
    def report(consultation_id: str):
        try:
            stored = api.get_business_stored(consultation_id)
        except MarriageNotFoundError:
            return _error("NOT_FOUND", consultation_id)
        profile = resolve_business_profile(stored)
        payload = serialize_report(replace(stored, report_model=profile.report_model), expert=False)
        payload["metadata"]["consultation_kind"] = "business"
        payload["score"] = payload["grade"] = None
        payload["business_score"] = asdict(profile.business_score) if profile.business_score else None
        return serialize_envelope(status=stored.status, data=payload, warnings=collect_warnings(stored))

    @router.post("/{consultation_id}/save")
    def save(consultation_id: str):
        try:
            stored = api.save_business_profile(consultation_id)
        except MarriageNotFoundError:
            return _error("NOT_FOUND", consultation_id)
        except Exception:
            return _error("INTERNAL_ERROR", consultation_id)
        return serialize_envelope(status=stored.status, data=_profile_data(stored))

    @router.get("/{consultation_id}/export/{fmt}")
    def export(consultation_id: str, fmt: Literal["pdf", "docx"]):
        try:
            stored = api.get_business_stored(consultation_id)
            artifact = export_business_file(stored, fmt)
        except MarriageNotFoundError:
            return _error("NOT_FOUND", consultation_id)
        except Exception:
            return _error("INTERNAL_ERROR", consultation_id, "export")
        return FileResponse(str(artifact.path), media_type=artifact.media_type, filename=artifact.filename, background=BackgroundTask(cleanup_marriage_export, artifact.path), headers={"X-BTE-Consultation-Id": consultation_id, "X-Content-Type-Options": "nosniff"})

    return router

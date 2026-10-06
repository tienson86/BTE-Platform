"""FastAPI routes for childbirth consulting."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Literal, Mapping

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask

from consulting.childbirth.export import export_childbirth_file
from consulting.childbirth.repository import ChildbirthProfile, JsonChildbirthRepository
from consulting.marriage.report.export import cleanup_marriage_export

from consulting.childbirth.service import (
    CHILDBIRTH_MODULE_VERSION,
    DEFAULT_YEARS_AHEAD,
    analyze_childbirth_plan,
)
from consulting.marriage.dto.request import BirthPlaceInput, MarriagePersonInput
from consulting.marriage.models.enums import CanonicalGender
from consulting.marriage.models.enums import MarriageRuntimeStatus


def build_childbirth_router(repository: JsonChildbirthRepository | None = None) -> APIRouter:
    """Build `/consulting/childbirth` routes."""
    router = APIRouter(prefix="/consulting/childbirth", tags=["consulting-childbirth"])
    archive = repository if repository is not None else JsonChildbirthRepository.from_environment()

    @router.post("/analyze")
    def analyze(body: dict[str, Any] = Body(...)) -> JSONResponse:
        try:
            father = _person(body.get("father"), CanonicalGender.MALE, "father")
            mother = _person(body.get("mother"), CanonicalGender.FEMALE, "mother")
            options = body.get("options") if isinstance(body.get("options"), Mapping) else {}
            result = analyze_childbirth_plan(
                father=father,
                mother=mother,
                start_year=_optional_int(options.get("start_year")),
                years_ahead=_optional_int(options.get("years_ahead")) or DEFAULT_YEARS_AHEAD,
            )
            profile = archive.create(
                jsonable_encoder({"father": asdict(father), "mother": asdict(mother),
                                  "options": {"start_year": result["start_year"], "years_ahead": result["years_ahead"]}}),
                result,
            )
        except ValueError as exc:
            return _error_response(str(exc), 400)
        except Exception:
            return _error_response("childbirth_analysis_failed", 500)
        return _success(_profile_data(profile))

    @router.get("/history")
    def history() -> JSONResponse:
        try:
            profiles = archive.history()
            return _success({"items": [
                {"consultation_id": profile.consultation_id, "created_at": profile.created_at,
                 "saved_at": profile.saved_at,
                 "display_identity": f"{profile.input['father'].get('full_name') or 'Người bố'} / {profile.input['mother'].get('full_name') or 'Người mẹ'}",
                 "headline": profile.result["summary"]["headline"]}
                for profile in profiles
            ]})
        except Exception:
            return _error_response("childbirth_history_failed", 500)

    @router.get("/{consultation_id}")
    def get_profile(consultation_id: str) -> JSONResponse:
        try:
            return _success(_profile_data(archive.get(consultation_id)))
        except KeyError:
            return _error_response("childbirth_profile_not_found", 404)
        except Exception:
            return _error_response("childbirth_profile_failed", 500)

    @router.post("/{consultation_id}/save")
    def save(consultation_id: str) -> JSONResponse:
        try:
            profile = archive.save(consultation_id)
            return _success({"consultation_id": profile.consultation_id, "saved_at": profile.saved_at})
        except KeyError:
            return _error_response("childbirth_profile_not_found", 404)
        except Exception:
            return _error_response("childbirth_save_failed", 500)

    @router.get("/{consultation_id}/export/{fmt}")
    def export(consultation_id: str, fmt: Literal["pdf", "docx"]):
        try:
            profile = archive.get(consultation_id)
        except KeyError:
            return _error_response("childbirth_profile_not_found", 404)
        except Exception:
            return _error_response("childbirth_profile_failed", 500)
        try:
            artifact = export_childbirth_file(profile, fmt)
        except Exception:
            return _error_response("childbirth_export_failed", 500)
        return FileResponse(
            str(artifact.path), media_type=artifact.media_type, filename=artifact.filename,
            background=BackgroundTask(cleanup_marriage_export, artifact.path),
            headers={"X-BTE-Consultation-Id": consultation_id, "X-Content-Type-Options": "nosniff"},
        )

    return router


def _profile_data(profile: ChildbirthProfile) -> dict[str, Any]:
    return {**profile.result, "consultation_id": profile.consultation_id,
            "created_at": profile.created_at, "saved_at": profile.saved_at, "input": profile.input}


def _success(data: Any) -> JSONResponse:
    return JSONResponse(content={"status": "SUCCESS", "data": data, "warnings": [], "errors": [],
                                 "version_bundle": {"api_version": "v1", "module_version": CHILDBIRTH_MODULE_VERSION}})


def _person(raw: Any, gender: CanonicalGender, role: str) -> MarriagePersonInput:
    if not isinstance(raw, Mapping):
        raise ValueError(f"{role}_missing")
    raw_gender = str(raw.get("gender") or gender.value).strip().lower()
    if raw_gender != gender.value:
        raise ValueError(f"{role}_gender_mismatch")
    birth_date = str(raw.get("birth_date") or "").strip()
    if not birth_date:
        raise ValueError(f"{role}_birth_date_missing")
    return MarriagePersonInput(
        gender=gender,
        birth_date=birth_date,
        full_name=str(raw.get("full_name") or "").strip() or None,
        birth_time=str(raw.get("birth_time") or "").strip() or None,
        birth_place=_birth_place(raw.get("birth_place")),
        timezone=str(raw.get("timezone") or "").strip() or None,
    )


def _birth_place(raw: Any) -> BirthPlaceInput | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        text = raw.strip()
        return BirthPlaceInput(display_name=text) if text else None
    if not isinstance(raw, Mapping):
        return None
    return BirthPlaceInput(
        display_name=str(raw.get("display_name") or "").strip() or None,
        province=str(raw.get("province") or "").strip() or None,
        city=str(raw.get("city") or "").strip() or None,
        country=str(raw.get("country") or "").strip() or None,
        latitude=_optional_float(raw.get("latitude")),
        longitude=_optional_float(raw.get("longitude")),
    )


def _optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _error_response(code: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": MarriageRuntimeStatus.FAILED.value,
            "data": None,
            "warnings": [],
            "errors": [
                {
                    "code": {400: "VALIDATION_ERROR", 404: "NOT_FOUND"}.get(status_code, "INTERNAL_ERROR"),
                    "stage": "childbirth",
                    "message": "Không thể hoàn tất tư vấn sinh con lúc này.",
                    "detail": code if status_code == 400 else None,
                    "retryable": status_code >= 500,
                }
            ],
            "version_bundle": {
                "api_version": "v1",
                "module_version": CHILDBIRTH_MODULE_VERSION,
            },
        },
    )

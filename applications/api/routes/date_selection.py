"""Date Selection API routes — isolated from Bazi analysis."""

from __future__ import annotations

import logging
from datetime import date
from typing import Any, Literal
from urllib.parse import quote

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

from applications.api.exceptions import CustomerExportError, ValidationAPIError
from applications.api.schemas.common import APIResponse
from applications.api.services.date_selection_report_export import (
    EXPORT_FAILED_MESSAGE,
    cleanup_date_selection_export,
    export_displayed_search_result,
)
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.service import DateSelectionService

router = APIRouter(prefix="/date-selection", tags=["date-selection"])
_SERVICE = DateSelectionService()
logger = logging.getLogger(__name__)


class MonthQuery(BaseModel):
    """Gregorian month for the general calendar."""

    year: int = Field(..., ge=1, le=9999)
    month: int = Field(..., ge=1, le=12)


class DayQuery(MonthQuery):
    """Single civil date for day/hour/khắc inspection."""

    day: int = Field(..., ge=1, le=31)
    hour_branch: str | None = None
    gender: str | None = None


class SearchQuery(BaseModel):
    """Personalized date search payload."""

    full_name: str = Field(..., min_length=1)
    gender: str
    birth_year: int = Field(..., ge=1, le=9999)
    birth_month: int = Field(..., ge=1, le=12)
    birth_day: int = Field(..., ge=1, le=31)
    target_year: int | None = Field(None, ge=1, le=9999)
    target_month: int | None = Field(None, ge=1, le=12)


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def _ok(request: Request, message: str, data: dict) -> APIResponse:
    return APIResponse(
        success=True,
        message=message,
        data=data,
        request_id=_request_id(request),
    )


def _call(fn):
    try:
        return fn()
    except DateSelectionValidationError as exc:
        raise ValidationAPIError(str(exc)) from exc


@router.post("/month", response_model=APIResponse)
def month_endpoint(request: Request, body: MonthQuery) -> APIResponse:
    """Return a Gregorian month grid with six-state labels."""
    result = _call(lambda: _SERVICE.month_calendar(body.year, body.month))
    return _ok(request, "Date Selection month OK", result.to_dict())


@router.post("/day", response_model=APIResponse)
def day_endpoint(request: Request, body: DayQuery) -> APIResponse:
    """Return day classification plus twelve hours and six khắc."""
    result = _call(
        lambda: _SERVICE.inspect_day(
            body.year,
            body.month,
            body.day,
            hour_branch=body.hour_branch,
            gender=body.gender,
        )
    )
    payload = result.to_dict()
    if body.hour_branch:
        payload["selected_hour"] = next(
            (
                hour
                for hour in payload["hours"]
                if hour["window"]["branch"] == body.hour_branch
            ),
            None,
        )
    return _ok(request, "Date Selection day OK", payload)


@router.post("/search", response_model=APIResponse)
def search_endpoint(request: Request, body: SearchQuery) -> APIResponse:
    """Return personal verification plus up to five recommended dates."""
    today = date.today()
    target_year = body.target_year or today.year
    target_month = body.target_month or today.month
    result = _call(
        lambda: _SERVICE.search(
            full_name=body.full_name,
            gender=body.gender,
            birth_year=body.birth_year,
            birth_month=body.birth_month,
            birth_day=body.birth_day,
            target_year=target_year,
            target_month=target_month,
        )
    )
    return _ok(request, "Date Selection search OK", result.to_dict())


class ReportExportRequest(BaseModel):
    """Displayed SearchResult. Never a request to rerun Date Selection."""

    search_result: dict[str, Any] = Field(...)


def _content_disposition(filename: str) -> str:
    ascii_name = filename.encode("ascii", "ignore").decode("ascii") or "report.bin"
    encoded = quote(filename)
    return f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{encoded}"


def _report_file_response(
    body: ReportExportRequest,
    fmt: Literal["pdf", "docx"],
) -> FileResponse:
    try:
        path, download_name, media_type, result = export_displayed_search_result(
            body.search_result,
            fmt,
        )
    except CustomerExportError:
        raise
    except Exception:
        logger.exception("date_selection_report_export_unhandled format=%s", fmt)
        raise CustomerExportError(
            EXPORT_FAILED_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    return FileResponse(
        path=str(path),
        media_type=media_type,
        filename=download_name,
        background=BackgroundTask(cleanup_date_selection_export, path),
        headers={
            "Content-Disposition": _content_disposition(download_name),
            "X-BTE-Report-Id": result.case_id or "",
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.post("/report/pdf")
def export_date_selection_pdf(request: Request, body: ReportExportRequest) -> FileResponse:
    """PDF from the SearchResult currently displayed in the portal."""
    del request
    return _report_file_response(body, "pdf")


@router.post("/report/docx")
def export_date_selection_docx(request: Request, body: ReportExportRequest) -> FileResponse:
    """DOCX from the SearchResult currently displayed in the portal."""
    del request
    return _report_file_response(body, "docx")

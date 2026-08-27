"""Date Selection API routes — isolated from Bazi analysis."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from applications.api.exceptions import ValidationAPIError
from applications.api.schemas.common import APIResponse
from engines.date_selection.exceptions import DateSelectionValidationError
from engines.date_selection.service import DateSelectionService

router = APIRouter(prefix="/date-selection", tags=["date-selection"])
_SERVICE = DateSelectionService()


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

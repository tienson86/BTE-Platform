"""Read-only CASE catalog for Narrative Studio."""

from __future__ import annotations

from dataclasses import dataclass

from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.fixtures.case_0002_readiness import CASE_0002_REQUEST


@dataclass(frozen=True, slots=True)
class StudioCase:
    """Birth input for one review case. Not a Narrative."""

    case_id: str
    full_name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    gender: str
    timezone: str
    birth_place: str


def _from_request(request: object) -> StudioCase:
    return StudioCase(
        case_id=str(getattr(request, "case_id")),
        full_name=str(getattr(request, "full_name") or ""),
        year=int(getattr(request, "year")),
        month=int(getattr(request, "month")),
        day=int(getattr(request, "day")),
        hour=int(getattr(request, "hour")),
        minute=int(getattr(request, "minute")),
        gender=str(getattr(request, "gender") or ""),
        timezone=str(getattr(request, "timezone") or "Asia/Bangkok"),
        birth_place=str(getattr(request, "birth_place") or ""),
    )


CASES: dict[str, StudioCase] = {
    "CASE-0001": _from_request(CASE_0001_REQUEST),
    "CASE-0002": _from_request(CASE_0002_REQUEST),
}

DEFAULT_CASE_ID = "CASE-0001"


def list_cases() -> tuple[StudioCase, ...]:
    """Return catalog cases in stable id order."""
    return tuple(CASES[key] for key in sorted(CASES))


def get_case(case_id: str) -> StudioCase:
    """Return one catalog case or raise KeyError."""
    if case_id not in CASES:
        raise KeyError(case_id)
    return CASES[case_id]

"""Helpers for TV1-B06 public API tests."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.http import build_marriage_router
from consulting.marriage.api.service import MarriageConsultationApi
from consulting.marriage.runtime.api_wiring import wire_marriage_api_runtime
from consulting.marriage.runtime.container import MarriageContainer
from tests.consulting.runtime_fixtures import FakeCanonicalRunner


def valid_body(
    *,
    time_a: str | None = "04:30",
    time_b: str | None = "10:00",
    gender_a: str | None = "male",
    gender_b: str | None = "female",
    birth_date_a: str = "1987-01-21",
    birth_date_b: str = "1990-05-15",
) -> dict[str, Any]:
    """Public JSON body for a two-person consultation."""
    person_a: dict[str, Any] = {
        "birth_date": birth_date_a,
        "full_name": "An",
    }
    person_b: dict[str, Any] = {
        "birth_date": birth_date_b,
        "full_name": "Binh",
    }
    if gender_a is not None:
        person_a["gender"] = gender_a
    if gender_b is not None:
        person_b["gender"] = gender_b
    if time_a is not None:
        person_a["birth_time"] = time_a
    if time_b is not None:
        person_b["birth_time"] = time_b
    return {"person_a": person_a, "person_b": person_b}


def api_client(
    *,
    live: bool = False,
) -> tuple[TestClient, MarriageContainer]:
    """Build an isolated FastAPI app bound to the TV-01 API runtime."""
    adapter = None if live else CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner())
    container = wire_marriage_api_runtime(canonical_adapter=adapter)
    app = FastAPI()
    app.include_router(build_marriage_router(container), prefix="/api/v1")
    return TestClient(app), container


def api_service(container: MarriageContainer) -> MarriageConsultationApi:
    """Return the bound public API service."""
    api = container.api_contract
    assert isinstance(api, MarriageConsultationApi)
    return api

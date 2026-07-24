"""API integration smoke for WP11 customer/case endpoints."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.config import settings
from applications.api.dependencies import (
    clear_wp11_caches,
    get_auth_service,
    get_settings,
    get_user_store,
)


def _client(tmp_path: Path) -> TestClient:
    settings.data_dir = str(tmp_path / "data")
    get_settings.cache_clear()
    get_user_store.cache_clear()
    get_auth_service.cache_clear()
    clear_wp11_caches()
    return TestClient(create_app())


def test_customer_case_api_flow(tmp_path: Path) -> None:
    client = _client(tmp_path)

    created = client.post(
        "/api/v1/customers",
        json={
            "full_name": "API Customer",
            "gender": "male",
            "birth_datetime": "1990-05-15T10:30:00",
            "phone": "0909999888",
            "email": "api@example.com",
            "tags": ["demo"],
        },
    )
    assert created.status_code == 200
    customer_id = created.json()["data"]["customer"]["customer_id"]

    listed = client.get("/api/v1/customers", params={"name": "API"})
    assert listed.status_code == 200
    assert listed.json()["data"]["count"] >= 1

    case_resp = client.post(
        "/api/v1/cases",
        json={
            "customer_id": customer_id,
            "interpretation_result": {"summary": "manual"},
        },
    )
    assert case_resp.status_code == 200
    case_id = case_resp.json()["data"]["case"]["case_id"]

    got = client.get(f"/api/v1/cases/{case_id}")
    assert got.status_code == 200

    history = client.get(f"/api/v1/customers/{customer_id}/history")
    assert history.status_code == 200
    assert history.json()["data"]["count"] == 1

    export = client.get(
        f"/api/v1/cases/{case_id}/export",
        params={"format": "markdown"},
    )
    assert export.status_code == 200
    assert "Case" in export.text

    deleted = client.delete(f"/api/v1/cases/{case_id}")
    assert deleted.status_code == 200

    calendar = client.post(
        "/api/v1/calendar",
        json={"year": 1990, "month": 5, "day": 15},
    )
    assert calendar.status_code == 200

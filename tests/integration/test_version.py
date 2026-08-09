"""Integration tests for GET /version."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.contracts.version import (
    API_VERSION,
    MIN_ENGINE_VERSION,
    SCHEMA_VERSION,
)


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI test client."""
    return TestClient(create_app())


def test_version_contains_required_fields(client: TestClient) -> None:
    """GET /version returns frozen version fields."""
    response = client.get("/version")
    assert response.status_code == 200
    payload = response.json()
    assert payload["api_version"] == API_VERSION
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["minimum_engine_version"] == MIN_ENGINE_VERSION


def test_version_has_exactly_expected_keys(client: TestClient) -> None:
    """GET /version exposes only the public version keys."""
    response = client.get("/version")
    assert set(response.json()) == {
        "api_version",
        "schema_version",
        "minimum_engine_version",
    }

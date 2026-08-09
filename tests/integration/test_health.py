"""Integration tests for GET /health."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI test client."""
    return TestClient(create_app())


def test_health_returns_ok(client: TestClient) -> None:
    """GET /health returns HTTP 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

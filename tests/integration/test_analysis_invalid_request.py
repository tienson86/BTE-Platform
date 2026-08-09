"""Integration tests for invalid POST /analysis requests."""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app

INVALID_ANALYZE_REQUEST: dict[str, object] = {
    "request_id": "integration-invalid-001",
    "api_version": "1.0.0",
    "language": "vi",
    "chart": {},
    "report_template": "standard",
    "options": {},
}


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI test client."""
    return TestClient(create_app())


def test_invalid_analysis_returns_http_400(client: TestClient) -> None:
    """Invalid chart payload returns HTTP 400."""
    response = client.post("/analysis", json=INVALID_ANALYZE_REQUEST)
    assert response.status_code == 400


def test_invalid_analysis_returns_error_response(client: TestClient) -> None:
    """Invalid request returns ErrorResponse envelope."""
    response = client.post("/analysis", json=INVALID_ANALYZE_REQUEST)
    payload = response.json()
    assert payload["success"] is False
    assert "error" in payload
    error = payload["error"]
    assert error["code"] == "validation_error"
    assert error["request_id"] == "integration-invalid-001"
    assert error["message"]
    assert error["timestamp"]


def test_invalid_analysis_does_not_expose_stack_trace(client: TestClient) -> None:
    """ErrorResponse must not leak stack traces."""
    response = client.post("/analysis", json=INVALID_ANALYZE_REQUEST)
    body = json.dumps(response.json()).lower()
    assert "traceback" not in body
    assert "file \"" not in body
    assert ".py\", line" not in body

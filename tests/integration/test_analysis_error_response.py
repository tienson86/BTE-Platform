"""Integration tests for unexpected POST /analysis failures."""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.report_response import ReportResponse
from applications.api.dependencies.services import get_analysis_service

VALID_ANALYZE_REQUEST: dict[str, object] = {
    "request_id": "integration-error-001",
    "api_version": "1.0.0",
    "language": "vi",
    "chart": {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 10,
        "minute": 30,
        "gender": "male",
    },
    "report_template": "standard",
    "options": {},
}


class _FailingAnalysisService:
    """Service stub that raises an unexpected internal exception."""

    def execute(self, request: AnalyzeRequest) -> ReportResponse:
        """Raise an exception with sensitive implementation details."""
        raise RuntimeError(
            "secret failure in applications/api/adapters/analysis_adapter.py line 99"
        )


@pytest.fixture
def client() -> TestClient:
    """Return a client with a failing analysis service dependency."""
    app = create_app()
    app.dependency_overrides[get_analysis_service] = _FailingAnalysisService
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def test_unexpected_failure_returns_http_500(client: TestClient) -> None:
    """Unexpected service failure returns HTTP 500."""
    response = client.post("/analysis", json=VALID_ANALYZE_REQUEST)
    assert response.status_code == 500


def test_unexpected_failure_returns_error_response(client: TestClient) -> None:
    """Unexpected failure returns ErrorResponse without success."""
    response = client.post("/analysis", json=VALID_ANALYZE_REQUEST)
    payload = response.json()
    assert payload["success"] is False
    error = payload["error"]
    assert error["code"] == "internal_error"
    assert error["request_id"] == "integration-error-001"
    assert error["message"] == "Unexpected analysis failure."
    assert error["timestamp"]


def test_unexpected_failure_does_not_leak_internals(client: TestClient) -> None:
    """ErrorResponse must not leak internal implementation details."""
    response = client.post("/analysis", json=VALID_ANALYZE_REQUEST)
    body = json.dumps(response.json()).lower()
    assert "traceback" not in body
    assert "runtimeerror" not in body
    assert "analysis_adapter.py" not in body
    assert "secret failure" not in body
    assert "line 99" not in body

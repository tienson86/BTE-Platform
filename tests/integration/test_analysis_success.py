"""Integration tests for successful POST /analysis."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app

VALID_ANALYZE_REQUEST: dict[str, object] = {
    "request_id": "integration-success-001",
    "api_version": "1.0.0",
    "language": "vi",
    "chart": {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 10,
        "minute": 30,
        "gender": "male",
        "timezone": "Asia/Ho_Chi_Minh",
    },
    "report_template": "standard",
    "options": {},
}


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Return a FastAPI test client."""
    return TestClient(create_app())


@pytest.fixture(scope="module")
def analysis_response(client: TestClient) -> dict[str, object]:
    """Execute a valid analysis request once for this module."""
    response = client.post("/analysis", json=VALID_ANALYZE_REQUEST)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    return payload


def test_analysis_returns_http_200(analysis_response: dict[str, object]) -> None:
    """POST /analysis returns a successful ReportResponse payload."""
    assert analysis_response["success"] is True


def test_analysis_success_flag(analysis_response: dict[str, object]) -> None:
    """Successful analysis sets success to true."""
    assert analysis_response["success"] is True


def test_analysis_contains_metadata(analysis_response: dict[str, object]) -> None:
    """ReportResponse includes metadata."""
    assert "metadata" in analysis_response
    metadata = analysis_response["metadata"]
    assert isinstance(metadata, dict)
    assert metadata.get("request_id") == "integration-success-001"


def test_analysis_contains_chart(analysis_response: dict[str, object]) -> None:
    """ReportResponse includes chart."""
    assert "chart" in analysis_response
    assert isinstance(analysis_response["chart"], dict)


def test_analysis_contains_analysis(analysis_response: dict[str, object]) -> None:
    """ReportResponse includes analysis."""
    assert "analysis" in analysis_response
    assert isinstance(analysis_response["analysis"], dict)


def test_analysis_contains_interpretation(analysis_response: dict[str, object]) -> None:
    """ReportResponse includes interpretation."""
    assert "interpretation" in analysis_response
    assert isinstance(analysis_response["interpretation"], dict)


def test_analysis_contains_report(analysis_response: dict[str, object]) -> None:
    """ReportResponse includes report."""
    assert "report" in analysis_response
    assert isinstance(analysis_response["report"], dict)


def test_analysis_contains_diagnostics(analysis_response: dict[str, object]) -> None:
    """ReportResponse includes diagnostics."""
    assert "diagnostics" in analysis_response
    assert isinstance(analysis_response["diagnostics"], dict)

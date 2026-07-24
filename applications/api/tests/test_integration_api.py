"""Integration tests for Applications API V1 routes."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app

SAMPLE = {
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 10,
    "minute": 30,
    "gender": "male",
}


def _client() -> TestClient:
    return TestClient(create_app())


def test_health() -> None:
    client = _client()
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "X-Request-ID" in response.headers
    assert "X-Elapsed-Ms" in response.headers


def test_openapi_lists_all_endpoints() -> None:
    client = _client()
    schema = client.get("/openapi.json").json()
    paths = schema["paths"]
    expected = [
        "/api/v1/health",
        "/api/v1/calendar",
        "/api/v1/bazi",
        "/api/v1/pattern",
        "/api/v1/score",
        "/api/v1/interpretation",
        "/api/v1/report",
        "/api/v1/narrative",
        "/api/v1/analyze",
    ]
    for path in expected:
        assert path in paths, f"missing OpenAPI path: {path}"


def test_calendar_endpoint() -> None:
    client = _client()
    response = client.post("/api/v1/calendar", json=SAMPLE)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["pipeline"] == ["calendar"]
    assert "calendar" in body["data"]


def test_analyze_end_to_end() -> None:
    client = _client()
    response = client.post(
        "/api/v1/analyze",
        json=SAMPLE,
        headers={"X-Request-ID": "wp9-test-analyze"},
    )
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "wp9-test-analyze"
    assert "X-Elapsed-Ms" in response.headers

    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Analyze OK"
    assert body["request_id"] == "wp9-test-analyze"
    data = body["data"]
    assert data["pipeline"] == [
        "calendar",
        "bazi",
        "pattern",
        "score",
        "interpretation",
        "report",
        "narrative",
    ]
    for key in data["pipeline"]:
        assert key in data
    assert data.get("stage") == "analyze"


def test_report_stops_before_narrative() -> None:
    client = _client()
    response = client.post("/api/v1/report", json=SAMPLE)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["pipeline"] == [
        "calendar",
        "bazi",
        "pattern",
        "score",
        "interpretation",
        "report",
    ]
    assert "narrative" not in data


def test_invalid_body_returns_422() -> None:
    client = _client()
    response = client.post("/api/v1/analyze", json={"year": 1990})
    assert response.status_code == 422

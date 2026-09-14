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
    assert "bazi" in data
    assert "pattern" in data
    assert "result_meta" in data

    bazi_result = data["bazi_analysis_result"]
    assert bazi_result["contract"] == "bazi_analysis_result.v1"
    assert bazi_result["analysis_id"] == "wp9-test-analyze"
    assert bazi_result["technical_data"]["day_master"]["stem"]
    assert bazi_result["presentation_data"]["hero"]["title"] == "Kết quả luận giải Bát Tự"
    assert bazi_result["quality"]["customer_safe"] is True
    assert set(bazi_result["customer_narrative"]["technical_explanations"]) == {
        "day_master",
        "strength",
        "structure",
        "useful_god",
        "five_elements",
        "ten_gods",
        "shen_sha",
    }
    assert set(bazi_result["module_exports"]) == {
        "marriage_seed",
        "career_seed",
        "partnership_seed",
        "feng_shui_seed",
        "child_planning_seed",
    }
    assert [chapter["id"] for chapter in bazi_result["customer_narrative"]["report_chapters"]] == [
        "overview",
        "four_pillars",
        "day_master",
        "five_elements",
        "strength_structure_useful_god",
        "ten_gods",
        "shen_sha",
        "life_domains",
        "luck_cycles",
        "recommendations",
    ]
    report_document = bazi_result["customer_narrative"]["report_document"]
    assert report_document["format"] == "markdown"
    assert report_document["chapter_count"] == 10
    assert "# Bản luận giải lá số Bát Tự" in report_document["markdown"]
    assert "missing_module_exports" in bazi_result["quality"]
    assert bazi_result["quality"]["has_complete_report_chapters"] is True
    assert bazi_result["quality"]["has_report_document"] is True


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

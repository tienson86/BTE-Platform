"""API integration tests for Knowledge Expert Discussion (Epic 03 M10)."""

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


def test_openapi_includes_discussion_endpoint() -> None:
    client = _client()
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/discussion" in paths
    assert "/api/v1/analyze" in paths


def test_analyze_adds_knowledge_expert_without_pipeline_break() -> None:
    client = _client()
    response = client.post("/api/v1/analyze", json=SAMPLE)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["pipeline"] == [
        "calendar",
        "bazi",
        "pattern",
        "score",
        "interpretation",
        "report",
        "narrative",
    ]
    assert "narrative" in data
    assert "report" in data
    assert "knowledge_expert" in data
    assert data["knowledge_expert"]["alters_public_pipeline"] is False
    assert data["knowledge_expert"]["alters_narrative"] is False


def test_discussion_endpoint_returns_expert_payload() -> None:
    client = _client()
    response = client.post(
        "/api/v1/discussion",
        json={**SAMPLE, "question": "Why is this chart reading favored?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
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
    assert data["replaces_narrative"] is False
    assert "knowledge_expert" in data
    assert "summary" in data

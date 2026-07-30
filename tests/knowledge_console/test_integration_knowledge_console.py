"""Integration tests for Knowledge Console FastAPI."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_phrase(client: TestClient, text: str = "Xét tổng thể,") -> dict:
    response = client.post(
        "/api/v1/assets",
        json={
            "asset_type": "phrase",
            "title": "Opening phrase",
            "content": {
                "phrase_id": "OPEN_TEST",
                "text": text,
                "type": "opening",
            },
            "actor": "editor",
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["success"] is True
    return body["data"]


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_crud_validate_preview_workflow(client: TestClient) -> None:
    created = _create_phrase(client)
    asset_id = created["asset_id"]
    assert created["status"] == "draft"
    assert created["version"] == "0.1.0"

    listed = client.get("/api/v1/assets", params={"asset_type": "phrase"})
    assert listed.status_code == 200
    assert any(item["asset_id"] == asset_id for item in listed.json()["data"])

    updated = client.put(
        f"/api/v1/assets/{asset_id}",
        json={
            "content": {
                "phrase_id": "OPEN_TEST",
                "text": "Xét tổng thể mệnh cục,",
                "type": "opening",
            },
            "note": "Polish text",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["version"] == "0.1.1"

    validated = client.post(f"/api/v1/assets/{asset_id}/validate")
    assert validated.status_code == 200
    assert validated.json()["data"]["valid"] is True

    preview = client.get(f"/api/v1/assets/{asset_id}/preview")
    assert preview.status_code == 200
    assert "mệnh cục" in preview.json()["data"]["preview_text"]

    submitted = client.post(
        f"/api/v1/workflow/{asset_id}",
        json={"action": "submit", "actor": "editor"},
    )
    assert submitted.status_code == 200
    assert submitted.json()["data"]["status"] == "review"

    queue = client.get("/api/v1/workflow/queue")
    assert queue.status_code == 200
    assert any(item["asset_id"] == asset_id for item in queue.json()["data"])

    approved = client.post(
        f"/api/v1/workflow/{asset_id}",
        json={"action": "approve", "actor": "reviewer"},
    )
    assert approved.status_code == 200
    assert approved.json()["data"]["status"] == "approved"

    released = client.post(
        f"/api/v1/workflow/{asset_id}",
        json={"action": "release", "actor": "publisher"},
    )
    assert released.status_code == 200
    assert released.json()["data"]["status"] == "released"

    history = client.get(f"/api/v1/assets/{asset_id}/history")
    assert history.status_code == 200
    actions = [item["action"] for item in history.json()["data"]]
    assert "release" in actions
    assert "approve" in actions

    versions = client.get(f"/api/v1/assets/{asset_id}/versions")
    assert versions.status_code == 200
    version_ids = [item["version"] for item in versions.json()["data"]]
    assert "0.1.0" in version_ids

    diff = client.get(
        f"/api/v1/assets/{asset_id}/diff",
        params={"from_version": "0.1.0"},
    )
    assert diff.status_code == 200
    assert diff.json()["data"]["asset_id"] == asset_id


def test_reject_returns_to_editable(client: TestClient) -> None:
    created = _create_phrase(client, text="Draft phrase")
    asset_id = created["asset_id"]
    client.post(
        f"/api/v1/workflow/{asset_id}",
        json={"action": "submit", "actor": "editor"},
    )
    rejected = client.post(
        f"/api/v1/workflow/{asset_id}",
        json={"action": "reject", "actor": "reviewer", "message": "Needs polish"},
    )
    assert rejected.status_code == 200
    assert rejected.json()["data"]["status"] == "rejected"

    edited = client.put(
        f"/api/v1/assets/{asset_id}",
        json={
            "content": {
                "phrase_id": "OPEN_TEST",
                "text": "Improved phrase",
                "type": "opening",
            },
            "note": "Address review",
        },
    )
    assert edited.status_code == 200
    assert edited.json()["data"]["status"] == "draft"


def test_invalid_create_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/assets",
        json={
            "asset_type": "rule",
            "title": "Broken",
            "content": {"rule_id": "r1"},
        },
    )
    assert response.status_code == 422


def test_seeded_demo_assets(seeded_client: TestClient) -> None:
    response = seeded_client.get("/api/v1/assets")
    assert response.status_code == 200
    types = {item["asset_type"] for item in response.json()["data"]}
    assert {"rule", "sentence", "phrase", "terminology"} <= types

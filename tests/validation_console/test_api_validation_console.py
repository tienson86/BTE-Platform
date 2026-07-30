"""API-level unit/integration smoke tests for Validation Console."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_compare_regression_approve(client: TestClient) -> None:
    created = client.post(
        "/api/v1/datasets",
        json={
            "name": "API Pack",
            "module": "pattern",
            "cases": [
                {
                    "case_id": "case_a001",
                    "description": "pass case",
                    "input_fixture": {"a": 1},
                    "expected_output": {"pattern": "zheng_guan"},
                    "actual_output": {"pattern": "zheng_guan"},
                    "tags": ["canonical"],
                    "coverage_goal": "canonical",
                },
                {
                    "case_id": "case_a002",
                    "description": "fail case",
                    "input_fixture": {"a": 2},
                    "expected_output": {"pattern": "shang_guan"},
                    "actual_output": {"pattern": "other"},
                    "tags": ["boundary"],
                    "coverage_goal": "boundary",
                },
            ],
        },
    )
    assert created.status_code == 200, created.text
    dataset_id = created.json()["data"]["dataset_id"]

    compared = client.get(f"/api/v1/datasets/{dataset_id}/compare")
    assert compared.status_code == 200
    assert compared.json()["data"]["summary"]["passed"] == 1
    assert compared.json()["data"]["summary"]["failed"] == 1

    regression = client.post(
        f"/api/v1/datasets/{dataset_id}/regression",
        json={"actor": "ci"},
    )
    assert regression.status_code == 200
    assert regression.json()["data"]["failed"] == 1

    stats = client.get(f"/api/v1/datasets/{dataset_id}/statistics")
    assert stats.status_code == 200
    assert stats.json()["data"]["case_count"] == 2

    coverage = client.get(f"/api/v1/datasets/{dataset_id}/coverage")
    assert coverage.status_code == 200
    assert "canonical" in coverage.json()["data"]["covered_goals"]

    submit = client.post(
        f"/api/v1/workflow/{dataset_id}",
        json={"action": "submit", "actor": "editor"},
    )
    assert submit.status_code == 200
    assert submit.json()["data"]["status"] == "review"

    queue = client.get("/api/v1/workflow/queue")
    assert any(item["dataset_id"] == dataset_id for item in queue.json()["data"])

    approve = client.post(
        f"/api/v1/workflow/{dataset_id}",
        json={"action": "approve", "actor": "reviewer"},
    )
    assert approve.status_code == 200
    assert approve.json()["data"]["status"] == "approved"


def test_import_endpoint(client: TestClient) -> None:
    response = client.post(
        "/api/v1/datasets/import",
        json={
            "name": "Imported",
            "cases": [
                {
                    "case_id": "case_imp1",
                    "description": "imported case",
                    "input_fixture": {},
                    "expected_output": {"ok": True},
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["metadata"]["imported"] is True

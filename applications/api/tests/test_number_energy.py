"""Applications API smoke for Number Energy V1."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app


def test_number_energy_analyze_path_and_103() -> None:
    client = TestClient(create_app())
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/number-energy/analyze" in paths
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "103", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["sequence_state"] == "HIDDEN"
    assert data["occurrences"][0]["display_name"] == "Thiên Y"
    assert "score" not in data

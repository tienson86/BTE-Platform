"""Date Selection API smoke tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app


def test_month_endpoint() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/date-selection/month",
        json={"year": 2026, "month": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]["cells"]) == 28
    assert "Tiểu Lục Nhâm" not in response.text
    assert "%" not in "".join(cell["six_state"]["label"] for cell in body["data"]["cells"])


def test_day_endpoint_known_example() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/date-selection/day",
        json={"year": 2026, "month": 8, "day": 27, "hour_branch": "Thìn"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["six_state"]["label"] == "Tiểu Cát"
    assert data["calendar"]["year_ganzhi"] == "Bính Ngọ"
    selected = data["selected_hour"]
    assert selected["window"]["branch"] == "Thìn"
    assert selected["six_state"]["label"] == "Xích Khẩu"
    assert selected["ke_slots"][0]["six_state"]["label"] == "Tiểu Cát"


def test_search_requires_gender() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/date-selection/search",
        json={
            "full_name": "Nguyễn Văn A",
            "gender": "",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "target_year": 2026,
            "target_month": 8,
        },
    )
    assert response.status_code == 422


def test_search_returns_person_lunar_block() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/date-selection/search",
        json={
            "full_name": "Nguyễn Văn A",
            "gender": "male",
            "birth_year": 1990,
            "birth_month": 5,
            "birth_day": 15,
            "target_year": 2026,
            "target_month": 8,
        },
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["person"]["lunar_label"]
    assert data["person"]["trach"]["cung"]
    assert len(data["dates"]) <= 5
    assert "Tiểu Lục Nhâm" not in response.text

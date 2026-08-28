"""CP-01B live contract: HTTP JSON shape consumed by /good-date."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app as create_api_app
from engines.date_selection.identity import pillar_contract

ELEMENTS = {"Mộc", "Hỏa", "Thổ", "Kim", "Thủy"}


def _pillar_from_http(block: dict) -> dict[str, str]:
    """Same field names as static/js/date_selection.js tuTruPillar."""
    src = block or {}
    return {
        "canChi": (src.get("can_chi") or src.get("ganzhi") or "").strip(),
        "napAm": (src.get("nayin_element") or src.get("nayin") or "").strip(),
        "cungPhi": (src.get("cung_phi") or src.get("cung") or "").strip(),
    }


def _day_http() -> dict:
    client = TestClient(create_api_app())
    response = client.post(
        "/api/v1/date-selection/day",
        json={"year": 2026, "month": 8, "day": 28},
    )
    assert response.status_code == 200
    return response.json()["data"]


def test_live_http_json_has_four_pillar_contract() -> None:
    data = _day_http()
    for key in ("year", "month", "day"):
        pillar = data[key]
        assert pillar["can_chi"]
        assert pillar["nayin_element"] in ELEMENTS
        assert pillar["cung_phi"]
        assert "—" not in pillar["can_chi"] + pillar["nayin_element"] + pillar["cung_phi"]
    hour = next(item for item in data["hours"] if item["window"]["branch"] == "Tý")
    assert hour["can_chi"]
    assert hour["nayin_element"] in ELEMENTS
    assert hour["cung_phi"]


def test_good_date_mapper_preserves_http_pillars_without_dash() -> None:
    data = _day_http()
    hour = next(item for item in data["hours"] if item["window"]["branch"] == "Tý")
    mapped = {
        "year": _pillar_from_http(data["year"]),
        "month": _pillar_from_http(data["month"]),
        "day": _pillar_from_http(data["day"]),
        "hour": _pillar_from_http(hour),
    }
    for row in mapped.values():
        assert row["canChi"]
        assert row["napAm"] in ELEMENTS
        assert row["cungPhi"]
        assert "—" not in row["canChi"] + row["napAm"] + row["cungPhi"]


def test_binh_ngo_lookup_thuy_kham() -> None:
    pillar = pillar_contract("Bính Ngọ")
    assert pillar["nayin_element"] == "Thủy"
    assert pillar["cung_phi"] == "Khảm"
    data = _day_http()
    assert data["year"]["can_chi"] == "Bính Ngọ"
    assert data["year"]["nayin_element"] == "Thủy"
    assert data["year"]["cung_phi"] == "Khảm"

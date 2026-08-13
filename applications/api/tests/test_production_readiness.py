"""Production-readiness API assertions for portal-facing analyze payload."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app

SAMPLE = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 3,
    "minute": 30,
    "gender": "male",
    "metadata": {
        "debug": "should_not_echo",
        "bat_trach": {"cung_phi": "Khôn"},
    },
}


def _client() -> TestClient:
    return TestClient(create_app())


def test_analyze_hides_internal_metadata_and_debug_fields() -> None:
    client = _client()
    response = client.post("/api/v1/analyze", json=SAMPLE)
    assert response.status_code == 200
    data = response.json()["data"]

    customer = data["customer"]
    assert "metadata" not in customer

    interpretation = data["interpretation"]
    assert "summary" not in interpretation
    assert "matched_rule_count" not in interpretation
    assert "resolved_rule_count" not in interpretation
    assert interpretation["sections"]

    report = data["report"]
    assert report["title"] == "Bản luận Bát tự"
    assert "templates_used" not in report
    assert "Template Schema" not in report["markdown"]

    narrative = data["narrative"]
    assert narrative["title"] == "Bản luận Bát tự"
    assert "FPR" not in narrative["markdown"]
    assert "summary, warning, career" not in narrative["markdown"]


def test_calendar_and_bazi_are_portal_friendly() -> None:
    client = _client()
    response = client.post("/api/v1/analyze", json=SAMPLE)
    assert response.status_code == 200
    data = response.json()["data"]

    calendar = data["calendar"]
    assert calendar["solar_term"]["name"] == "Đại Hàn"
    assert calendar["lunar_date"] == "22/12/1986"
    assert calendar["year_can_chi"] == "Bính Dần"
    assert calendar["bazi_can_chi"]["year"] == "Bính Dần"
    assert calendar["bazi_can_chi"]["month"] == "Tân Sửu"
    assert calendar["bazi_can_chi"]["day"] == "Canh Ngọ"
    assert calendar["bazi_can_chi"]["hour"] == "Mậu Dần"
    assert calendar["cung_phi"] == "Khôn"
    assert calendar["menh_quai"] == "Khôn"

    bazi = data["bazi"]
    assert bazi["day_master"] == "Canh"
    assert bazi["year_pillar"]["nap_am"] == "Lư Trung Hỏa"
    assert bazi["day_pillar"]["nap_am"] == "Lộ Bàng Thổ"
    assert bazi["day_pillar"]["truong_sinh"] == "Mộc Dục"
    assert bazi["hour_pillar"]["ten_god"] == "Thiên Ấn"


def test_score_payload_does_not_expose_internal_details() -> None:
    client = _client()
    response = client.post("/api/v1/analyze", json=SAMPLE)
    assert response.status_code == 200
    score = response.json()["data"]["score"]

    assert "details" not in score
    assert "modules" not in score
    assert "execution_time" not in score
    assert "weighted_score" not in score

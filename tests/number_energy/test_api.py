"""API / integration tests for Number Energy V1."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.number_energy.constants import FORBIDDEN_CUSTOMER_PHRASES

ENDPOINT = "/api/v1/number-energy/analyze"


def _client() -> TestClient:
    return TestClient(create_app())


def _analyze(number: str, purpose_context: str = "generic_number"):
    return _client().post(
        ENDPOINT,
        json={"number": number, "purpose_context": purpose_context},
    )


def _payload_text(data: dict) -> str:
    return str(data).lower()


def test_openapi_lists_number_energy_analyze() -> None:
    schema = _client().get("/openapi.json").json()
    assert ENDPOINT in schema["paths"]
    assert "post" in schema["paths"][ENDPOINT]


def test_api_103_tian_yi_hidden() -> None:
    response = _analyze("103")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert set(data) == {
        "occurrences",
        "sequence_state",
        "patterns",
        "narrative",
        "warnings",
        "metadata",
        "reading",
    }
    item = data["occurrences"][0]
    assert item["energy_id"] == "tian_yi"
    assert item["display_name"] == "Thiên Y"
    assert item["strength_rank"] == 1
    assert item["state"] == "HIDDEN"
    assert item["pair_digits"] == "13"
    assert item["classification_label"] == "trường khí hỗ trợ"
    assert data["sequence_state"] == "HIDDEN"
    assert data["metadata"]["engine"] == "number_energy"
    assert data["narrative"]["health_disclaimer"]
    assert "score" not in data
    assert "grade" not in data
    assert "percent" not in data


def test_api_153_tian_yi_amplified() -> None:
    data = _analyze("153").json()["data"]
    item = data["occurrences"][0]
    assert item["display_name"] == "Thiên Y"
    assert item["strength_rank"] == 1
    assert item["state"] == "AMPLIFIED"


def test_api_108_wu_gui_hidden() -> None:
    data = _analyze("108").json()["data"]
    item = data["occurrences"][0]
    assert item["display_name"] == "Ngũ Quỷ"
    assert item["strength_rank"] == 1
    assert item["state"] == "HIDDEN"
    assert item["classification"] == "challenging"
    assert item["classification_label"] == "trường khí cần kiểm soát"


def test_api_1414_sheng_qi_repeated() -> None:
    data = _analyze("1414").json()["data"]
    assert [item["energy_id"] for item in data["occurrences"]] == [
        "sheng_qi",
        "sheng_qi",
        "sheng_qi",
    ]
    assert data["sequence_state"] == "REPEATED"


def test_api_141319_supportive_chain() -> None:
    data = _analyze("141319").json()["data"]
    first_seen: list[str] = []
    for item in data["occurrences"]:
        if item["energy_id"] not in first_seen:
            first_seen.append(item["energy_id"])
    assert first_seen == ["sheng_qi", "tian_yi", "yan_nian"]
    assert "approved_supportive_chain" in data["patterns"]
    assert data["metadata"]["summary"]["approved_supportive_chain"] is True
    assert data["metadata"]["pattern_labels"] == [
        "Chuỗi hỗ trợ đã khóa: Sinh Khí → Thiên Y → Diên Niên"
    ]


def test_api_219_not_neutralized() -> None:
    data = _analyze("219").json()["data"]
    assert [item["display_name"] for item in data["occurrences"]] == [
        "Tuyệt Mệnh",
        "Diên Niên",
    ]
    assert "NEUTRALIZED" not in data["metadata"]["sequence_states"]
    assert "CONTROLLED" not in data["metadata"]["sequence_states"]


def test_api_216_without_control() -> None:
    data = _analyze("216").json()["data"]
    assert [item["display_name"] for item in data["occurrences"]] == [
        "Tuyệt Mệnh",
        "Lục Sát",
    ]
    assert data["metadata"]["summary"]["controlled_energy_ids"] == []


def test_api_1003_unknown_or_not_defined() -> None:
    data = _analyze("1003").json()["data"]
    assert data["sequence_state"] == "UNKNOWN_OR_NOT_DEFINED"
    assert data["warnings"]
    assert data["warnings"][0]["code"] == "UNKNOWN_OR_NOT_DEFINED"
    assert "chưa được khóa" in data["warnings"][0]["customer_reason"]
    assert data["narrative"]["unknown_notice"]
    assert "UNKNOWN_OR_NOT_DEFINED" not in data["narrative"]["unknown_notice"]
    assert "không phải chẩn đoán y khoa" in data["narrative"]["health_disclaimer"]
    assert "UNKNOWN_OR_NOT_DEFINED" not in data["reading"]["summary"]


def test_api_phone_0328278786_strips_leading_zero() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    assert data["sequence_state"] != "UNKNOWN_OR_NOT_DEFINED"
    assert data["metadata"]["analyzed_input"] == "328278786"
    reading = data["reading"]
    assert reading["layout"] == "phone"
    assert [item["pair_digits"] for item in reading["pairs"]] == [
        "32",
        "28",
        "82",
        "27",
        "78",
        "87",
        "78",
        "86",
    ]
    assert reading["ending"]["pair_digits"] == "86"
    assert reading["ending"]["display_name"] == "Thiên Y"
    assert reading["dominant"]["display_name"] == "Diên Niên"
    assert reading["lifted"] is True
    assert "NEUTRALIZED" not in str(reading)


def test_api_phone_interior_zero_warning() -> None:
    data = _analyze("103", "phone_number").json()["data"]
    assert "Số 0 chỉ nên xuất hiện ở đầu" in (data["reading"]["interior_zero_note"] or "")
    assert data["occurrences"][0]["display_name"] == "Thiên Y"


@pytest.mark.parametrize(
    "payload",
    [
        {"number": "12a", "purpose_context": "generic_number"},
        {"number": "12-13", "purpose_context": "generic_number"},
        {"number": "103", "purpose_context": "lottery_number"},
        {"number": "", "purpose_context": "generic_number"},
        {"number": "１２３", "purpose_context": "generic_number"},
        {"number": "1" * 129, "purpose_context": "generic_number"},
        {"number": 103, "purpose_context": "generic_number"},
        {"purpose_context": "generic_number"},
    ],
)
def test_api_invalid_input_returns_422(payload: dict) -> None:
    response = _client().post(ENDPOINT, json=payload)
    assert response.status_code == 422


def test_api_strips_surrounding_space() -> None:
    response = _analyze(" 103 ")
    assert response.status_code == 200
    assert response.json()["data"]["metadata"]["input_raw"] == "103"


def test_api_narrative_is_not_medical_diagnosis() -> None:
    data = _analyze("1414", purpose_context="phone_number").json()["data"]
    blob = _payload_text(data)
    for phrase in FORBIDDEN_CUSTOMER_PHRASES:
        assert phrase.lower() not in blob
    assert "chẩn đoán bệnh" not in blob
    narrative = data["narrative"]
    assert "Bát Cực Linh Số" in narrative["system_name"]
    assert narrative["health_disclaimer"]
    assert "không phải chẩn đoán y khoa" in narrative["health_disclaimer"]
    assert narrative["strengths"]
    assert narrative["watchouts"]

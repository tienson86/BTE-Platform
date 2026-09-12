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
        "pair_occurrences",
        "pair_summary",
        "energy_distribution",
        "triple_occurrences",
        "chain",
        "wealth_nodes",
        "wealth_flow",
        "later_outcome",
        "wealth_story",
        "domain_insights",
        "strengths",
        "cautions",
        "evidence",
        "assessment",
        "recommendation",
        "score",
        "grade",
        "verified_by_runtime",
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
    assert data["score"] is None
    assert data["grade"] is None
    assert data["verified_by_runtime"] is False
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


def test_api_rb05_a_golden_phone_pair_structure() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    pairs = data["pair_occurrences"]
    assert len(pairs) == 8
    assert [item["pair_digits"] for item in pairs] == [
        "32",
        "28",
        "82",
        "27",
        "78",
        "87",
        "78",
        "86",
    ]
    first = pairs[0]
    last = pairs[-1]
    assert first["display_name"] == "Họa Hại"
    assert first["category"] == "HUNG"
    assert first["strength_label"] == "Nhẹ"
    assert last["display_name"] == "Thiên Y"
    assert last["category"] == "CAT"
    assert last["strength_label"] == "Mạnh"
    forbidden = {
        "occurrence_id",
        "source_span",
        "energy_id",
        "strength_rank",
        "state",
        "classification",
    }
    for item in pairs:
        assert forbidden.isdisjoint(item.keys())
    summary = data["pair_summary"]
    assert summary["supportive_pair_count"] == 7
    assert summary["challenging_pair_count"] == 1
    rows = data["energy_distribution"]
    assert len(rows) == 8
    assert rows[3] == {"energy_label": "Phục Vị", "count": 0}
    assert rows[0]["energy_label"] == "Sinh Khí"
    assert rows[0]["count"] == 2
    assert rows[2]["count"] == 3
    assert rows[4] == {"energy_label": "Họa Hại", "count": 1}


def test_api_rb05_b_golden_phone_triples_and_chain() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    triples = data["triple_occurrences"]
    assert len(triples) == 7
    assert [item["digits"] for item in triples] == [
        "328",
        "282",
        "827",
        "278",
        "787",
        "878",
        "786",
    ]
    titles = {item["digits"]: item["customer_title"] for item in triples}
    assert titles["328"] == "Khẩu tài tốt"
    assert titles["282"] == "Quý nhân và cơ hội được tăng cường"
    assert titles["827"] == "Quý nhân mang đến Tài vận"
    assert titles["278"] == "Tài đi vào sự nghiệp"
    assert titles["787"] == "Năng lực nghề nghiệp được tăng cường"
    assert titles["878"] == "Năng lực nghề nghiệp được tăng cường"
    assert titles["786"] == "Năng lực nghề nghiệp tạo Tài"
    by_digits = {item["digits"]: item for item in triples}
    assert by_digits["827"]["priority"] == "FEATURED"
    assert by_digits["278"]["priority"] == "FEATURED"
    assert by_digits["786"]["priority"] == "FEATURED"
    assert by_digits["787"]["priority"] == "COMPACT"
    assert by_digits["878"]["priority"] == "COMPACT"
    forbidden = {
        "occurrence_id",
        "source_span",
        "energy_id",
        "strength_rank",
        "state",
        "classification",
    }
    for item in triples:
        assert forbidden.isdisjoint(item.keys())
    chain = data["chain"]
    assert chain["primary_energy_label"] == "Diên Niên"
    assert chain["terminal_pair_digits"] == "86"
    assert chain["terminal_energy_label"] == "Thiên Y"
    assert chain["terminal_triple_digits"] == "786"
    assert chain["terminal_interaction_label"] == "Diên Niên → Thiên Y"
    assert "energy_id" not in chain


def test_api_rb05_c_golden_phone_wealth_flow() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    stages = data["wealth_flow"]["stages"]
    assert len(stages) == 4
    assert [item["label"] for item in stages] == [
        "TÀI VẬN",
        "TÀI TỪ ĐÂU?",
        "TÀI ĐI ĐÂU?",
        "HẬU VẬN",
    ]
    assert stages[0]["headline"] == "Có Thiên Y"
    assert stages[0]["evidence"] == "27 · 86"
    assert stages[1]["headline"] == "Quý nhân & cơ hội"
    assert stages[1]["evidence"] == "827"
    assert stages[1]["interaction"] == "Sinh Khí → Thiên Y"
    assert stages[2]["headline"] == "Sự nghiệp & lập nghiệp"
    assert stages[2]["evidence"] == "278"
    assert stages[2]["interaction"] == "Thiên Y → Diên Niên"
    assert stages[3]["headline"] == "Thiên Y"
    assert stages[3]["evidence"] == "786"
    assert stages[3]["interaction"] == "Diên Niên → Thiên Y"
    later = data["later_outcome"]
    assert later["terminal_pair_digits"] == "86"
    assert later["terminal_energy_label"] == "Thiên Y"
    assert later["terminal_triple_digits"] == "786"
    assert later["terminal_interaction_label"] == "Diên Niên → Thiên Y"
    story = data["wealth_story"]
    assert "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài" in story["display"]
    blob = str(
        {
            "nodes": data["wealth_nodes"],
            "flow": data["wealth_flow"],
            "later": later,
            "story": story,
        }
    ).lower()
    assert "chắc chắn phát tài" not in blob
    assert "source_span" not in blob
    forbidden = {
        "occurrence_id",
        "source_span",
        "energy_id",
        "strength_rank",
        "state",
        "classification",
        "rank",
    }
    for item in data["wealth_nodes"]:
        assert forbidden.isdisjoint(item.keys())
    for item in stages:
        assert forbidden.isdisjoint(item.keys())
    assert forbidden.isdisjoint(later.keys())
    assert forbidden.isdisjoint(story.keys())


def test_api_rb05_d_golden_phone_domain_findings() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    domains = data["domain_insights"]
    assert [
        (item["domain"], item["conclusion"]) for item in domains
    ] == [
        ("Tài vận", "Có đường Tài tương đối rõ"),
        ("Công việc & sự nghiệp", "Đây là một trong những điểm mạnh nhất của dãy"),
        ("Tình cảm & quan hệ", "Quan hệ xã hội có yếu tố hỗ trợ"),
        ("Tính cách & năng lực", "Trách nhiệm và năng lực làm việc khá rõ"),
        ("Cân bằng trường khí", "Cát tinh giữ vai trò chủ đạo"),
    ]
    assert [item["title"] for item in data["strengths"]] == [
        "Quý nhân có thể mở đường cho Tài",
        "Năng lực nghề nghiệp nổi bật",
        "Công việc có khả năng tạo thành quả",
        "Khẩu tài có thể phát huy tích cực",
    ]
    assert [item["title"] for item in data["cautions"]] == [
        "Cần chú ý cách sử dụng lời nói",
        "Không nên chỉ nhìn số lượng Cát tinh",
    ]
    blob = str(
        {
            "domains": domains,
            "strengths": data["strengths"],
            "cautions": data["cautions"],
            "evidence": data["evidence"],
        }
    ).lower()
    assert "chắc chắn phát tài" not in blob
    assert "source_span" not in blob
    assert "energy_id" not in blob
    assert "82 / 100" not in blob
    forbidden = {
        "occurrence_id",
        "source_span",
        "energy_id",
        "strength_rank",
        "state",
        "classification",
        "rank",
    }
    for item in (*domains, *data["strengths"], *data["cautions"]):
        assert forbidden.isdisjoint(item.keys())
        assert item["evidence_refs"]
        for ref in item["evidence_refs"]:
            assert ref["source"] in {
                "pair_occurrences",
                "pair_summary",
                "energy_distribution",
                "triple_occurrences",
                "chain",
                "wealth_flow",
                "later_outcome",
            }
            assert forbidden.isdisjoint(ref.keys())
    for group in data["evidence"]:
        assert group["source"] != "score"
        assert forbidden.isdisjoint(group.keys())
        for item in group["items"]:
            assert forbidden.isdisjoint(item.keys())


def test_api_rb05_f_golden_phone_assessment_and_recommendation() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    assessment = data["assessment"]
    assert assessment["title"] == "Đánh giá tổng thể"
    assert assessment["summary"] == (
        "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y. "
        "Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp "
        "tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy."
    )
    assert assessment["story_line"] == "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI"
    recommendation = data["recommendation"]
    assert recommendation["label"] == "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
    assert recommendation["state"] == "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
    assert recommendation["summary"] == (
        "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài."
    )
    blob = str({"assessment": assessment, "recommendation": recommendation}).lower()
    assert "chắc chắn phát tài" not in blob
    assert "đổi số ngay" not in blob
    assert "mua số" not in blob
    assert "source_span" not in blob
    assert "energy_id" not in blob
    assert "verified_by_runtime" not in blob
    assert "82 / 100" not in blob
    assert "score" not in assessment
    assert "grade" not in assessment
    assert "score" not in recommendation
    assert "grade" not in recommendation


def test_api_rb05_e_golden_phone_score_and_verified() -> None:
    data = _analyze("0328278786", "phone_number").json()["data"]
    assert data["grade"] == "TỐT"
    assert data["verified_by_runtime"] is True
    score = data["score"]
    assert score["total"] == 82
    assert score["max"] == 100
    assert score["display"] == "82 / 100"
    assert score["grade"] == "TỐT"
    assert score["verified_by_runtime"] is True
    assert "%" not in score["display"]
    breakdown = score["breakdown"]
    assert [
        (item["label"], item["earned"], item["max"]) for item in breakdown
    ] == [
        ("Cấu trúc năng lượng", 21, 25),
        ("Dòng tài vận", 22, 25),
        ("Công việc & trợ lực", 17, 20),
        ("Ổn định & rủi ro", 10, 15),
        ("Năng lượng kết", 12, 15),
    ]
    assert sum(item["earned"] for item in breakdown) == 82
    assert [item["title"] for item in score["reasons"]] == [
        "Cấu trúc Cát giữ vai trò chủ đạo",
        "Dòng Tài có nguồn rõ",
        "Công việc là trục mạnh",
        "Họa Hại cần được sử dụng đúng cách",
    ]
    assert data["recommendation"]["label"] == "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
    assert data["assessment"]["story_line"] == "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI"
    blob = str(score).lower()
    assert "chắc chắn phát tài" not in blob
    assert "source_span" not in blob
    assert "energy_id" not in blob
    assert "strength_rank" not in blob
    forbidden = {
        "occurrence_id",
        "source_span",
        "energy_id",
        "strength_rank",
        "state",
        "classification",
        "rank",
    }
    assert forbidden.isdisjoint(score.keys())
    for item in (*breakdown, *score["reasons"]):
        assert forbidden.isdisjoint(item.keys())


def test_api_non_phone_does_not_reuse_phone_score() -> None:
    data = _analyze("0328278786", "car_plate").json()["data"]
    assert data["score"] is None
    assert data["grade"] is None
    assert data["verified_by_runtime"] is False


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
    assert data["score"] is not None
    assert data["verified_by_runtime"] is True
    assert data["score"]["total"] != 82
    assert "pair_occurrences" in data
    assert "pair_summary" in data
    assert "energy_distribution" in data


def test_number_energy_golden_phone_pair_structure() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "0328278786", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["pair_occurrences"]) == 8
    assert data["pair_summary"]["supportive_pair_count"] == 7
    assert data["pair_summary"]["challenging_pair_count"] == 1
    assert len(data["energy_distribution"]) == 8
    assert data["pair_occurrences"][0]["category"] == "HUNG"
    assert data["pair_occurrences"][-1]["category"] == "CAT"


def test_number_energy_golden_phone_triples_and_chain() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "0328278786", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert [item["digits"] for item in data["triple_occurrences"]] == [
        "328",
        "282",
        "827",
        "278",
        "787",
        "878",
        "786",
    ]
    assert data["chain"]["primary_energy_label"] == "Diên Niên"
    assert data["chain"]["terminal_triple_digits"] == "786"
    assert data["chain"]["terminal_interaction_label"] == "Diên Niên → Thiên Y"


def test_number_energy_golden_phone_wealth_flow() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "0328278786", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    stages = data["wealth_flow"]["stages"]
    assert len(stages) == 4
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
    assert "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài" in data["wealth_story"]["display"]


def test_number_energy_golden_phone_domain_findings() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "0328278786", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert [
        (item["domain"], item["conclusion"]) for item in data["domain_insights"]
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
    assert data["evidence"]


def test_number_energy_golden_phone_assessment_and_recommendation() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "0328278786", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["assessment"]["title"] == "Đánh giá tổng thể"
    assert data["assessment"]["story_line"] == "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI"
    assert "Diên Niên" in data["assessment"]["summary"]
    assert "Quý nhân và cơ hội" in data["assessment"]["summary"]
    assert data["recommendation"]["label"] == "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
    assert data["recommendation"]["summary"] == (
        "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài."
    )


def test_number_energy_golden_phone_score() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "0328278786", "purpose_context": "phone_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["grade"] == "TỐT"
    assert data["verified_by_runtime"] is True
    score = data["score"]
    assert score["total"] == 82
    assert score["max"] == 100
    assert score["display"] == "82 / 100"
    assert [
        (item["label"], item["earned"], item["max"]) for item in score["breakdown"]
    ] == [
        ("Cấu trúc năng lượng", 21, 25),
        ("Dòng tài vận", 22, 25),
        ("Công việc & trợ lực", 17, 20),
        ("Ổn định & rủi ro", 10, 15),
        ("Năng lượng kết", 12, 15),
    ]
    assert [item["title"] for item in score["reasons"]] == [
        "Cấu trúc Cát giữ vai trò chủ đạo",
        "Dòng Tài có nguồn rõ",
        "Công việc là trục mạnh",
        "Họa Hại cần được sử dụng đúng cách",
    ]
    assert data["recommendation"]["label"] == "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"


def test_number_energy_vehicle_plate_letters_are_supported() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "30F-058.11", "purpose_context": "car_plate"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["metadata"]["input_raw"] == "30F-058.11"
    assert data["metadata"]["analyzed_input"] == "30605811"
    assert data["pair_occurrences"]
    assert data["score"] is not None
    assert data["verified_by_runtime"] is True


def test_number_energy_id_number_passport_letters_are_supported() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/number-energy/analyze",
        json={"number": "B1234567", "purpose_context": "id_number"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["metadata"]["input_raw"] == "B1234567"
    assert data["metadata"]["analyzed_input"] == "21234567"
    assert data["metadata"]["purpose_context"] == "id_number"
    assert data["score"] is not None
    assert data["verified_by_runtime"] is True

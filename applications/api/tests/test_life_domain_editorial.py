from applications.api.services.life_domain_editorial import run_life_domain_editorial


def _phuong_payload() -> dict:
    return {
        "bazi": {"day_master": "Giáp Mộc"},
        "strength": {
            "strength_level": "balanced",
            "strength_score": 0.51,
            "root_score": 0.22,
            "drain_score": -0.23,
            "control_score": -0.08,
        },
        "useful_god": {"useful_display": "Thủy · Nhâm · Thiên Ấn"},
        "five_elements": {"counts": {"wood": 3, "fire": 5, "earth": 7, "metal": 2, "water": 2}},
        "ten_gods": {
            "visible": [
                {"ten_god": "Thương Quan"},
                {"ten_god": "Thực Thần"},
                {"ten_god": "Chính Quan"},
            ],
            "hidden": [
                {"ten_god": "Chính Tài"},
                {"ten_god": "Thiên Tài"},
                {"ten_god": "Chính Ấn"},
            ],
        },
    }


def test_cross_domain_editorial_connects_value_money_career_and_health() -> None:
    result = run_life_domain_editorial(_phuong_payload())

    assert result["status"] == "ready"
    assert result["validation"]["passed"] is True
    assert [step["id"] for step in result["reasoning"]][:2] == ["value-to-money", "career-chain"]
    assert "năng lực cá nhân tạo ra sản phẩm" in " ".join(result["sections"]["career"])
    assert "doanh thu tăng nhưng tài sản ròng" in " ".join(result["sections"]["wealth"])
    assert "tăng giá trị trên mỗi đơn vị công sức" in " ".join(result["sections"]["health"])
    assert result["evidence"]["strength_nuance"] == "Thân trung hòa nhưng chịu tiết/khắc đáng kể và vẫn có căn"


def test_cross_domain_editorial_does_not_invent_a_chain() -> None:
    payload = _phuong_payload()
    payload["ten_gods"] = {"visible": [{"ten_god": "Chính Quan"}], "hidden": []}

    result = run_life_domain_editorial(payload)

    assert result["status"] == "ready"
    assert all(step["id"] != "career-chain" for step in result["reasoning"])
    assert "chưa tạo thành một chuỗi" in " ".join(result["sections"]["career"])

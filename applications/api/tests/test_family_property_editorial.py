from applications.api.services.family_property_editorial import run_family_property_editorial


def _phuong_payload() -> dict:
    return {
        "bazi": {
            "day_master": "Giáp Mộc",
            "day_pillar": {"can_chi": "Giáp Thìn"},
            "hour_pillar": {"can_chi": "Tân Mùi"},
        },
        "strength": {"strength_level": "balanced"},
        "useful_god": {"useful_display": "Thủy · Nhâm · Thiên Ấn"},
        "five_elements": {"counts": {"earth": 7}},
        "ten_gods": {
            "visible": [
                {"pillar": "year", "ten_god": "Thương Quan"},
                {"pillar": "month", "ten_god": "Thực Thần"},
                {"pillar": "hour", "ten_god": "Chính Quan"},
            ],
            "hidden": [
                {"pillar": "year", "ten_god": "Chính Ấn"},
                {"pillar": "day", "ten_god": "Chính Ấn"},
                {"pillar": "day", "ten_god": "Thiên Tài"},
                {"pillar": "hour", "ten_god": "Chính Tài"},
                {"pillar": "hour", "ten_god": "Thương Quan"},
                {"pillar": "hour", "ten_god": "Kiếp Tài"},
            ],
        },
    }


def test_family_property_editorial_connects_three_generations() -> None:
    result = run_family_property_editorial(_phuong_payload())

    assert result["status"] == "ready"
    assert result["validation"]["passed"] is True
    assert [step["id"] for step in result["reasoning"]] == ["parents", "children", "property", "generation-chain"]
    assert "hiếu nhưng có ranh giới" in " ".join(result["sections"]["parents"])
    assert "không cho phép chốt chính xác có bao nhiêu con" in " ".join(result["sections"]["children"])
    assert "Hợp không luôn tốt, Xung không luôn xấu" in " ".join(result["sections"]["property"])
    assert "không để trách nhiệm với cha mẹ, con cái và nhà cửa" in " ".join(result["sections"]["property"])


def test_family_property_editorial_does_not_invent_children_signal() -> None:
    payload = _phuong_payload()
    payload["ten_gods"]["visible"] = [{"pillar": "hour", "ten_god": "Chính Quan"}]
    payload["ten_gods"]["hidden"] = [{"pillar": "day", "ten_god": "Chính Ấn"}]

    result = run_family_property_editorial(payload)

    assert result["status"] == "ready"
    assert all(step["id"] != "children" for step in result["reasoning"])
    assert result["sections"]["children"] == []

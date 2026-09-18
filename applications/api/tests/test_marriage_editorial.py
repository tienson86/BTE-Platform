from __future__ import annotations

from applications.api.services.marriage_editorial import (
    build_marriage_evidence,
    build_marriage_reasoning,
    compose_marriage_narrative,
    run_marriage_editorial,
    validate_marriage_narrative,
)


def _thu_phuong_payload() -> dict:
    return {
        "customer": {"full_name": "Hoàng Thị Thu Phương", "gender": "female", "gender_label": "Nữ"},
        "identity": {"person": {"gender": "female", "gender_label": "Nữ"}},
        "bazi": {
            "day_master": "Giáp",
            "year_pillar": {"can_chi": "Đinh Sửu"},
            "month_pillar": {"can_chi": "Bính Ngọ"},
            "day_pillar": {"can_chi": "Giáp Thìn", "ten_god": "Nhật chủ"},
            "hour_pillar": {"can_chi": "Tân Mùi", "ten_god": "Chính Quan"},
        },
        "strength": {"strength_level": "Thân nhược có căn"},
        "pattern": {"than_vuong_nhuoc": "Thân nhược có căn"},
        "useful_god": {"useful_display": "Thủy · Nhâm · Thiên Ấn"},
        "ten_gods": {
            "visible": [{"pillar": "hour", "stem": "Tân", "ten_god": "Chính Quan"}],
            "hidden": [
                {"pillar": "day", "hidden_stem": "Mậu", "ten_god": "Thiên Tài"},
                {"pillar": "day", "hidden_stem": "Ất", "ten_god": "Kiếp Tài"},
                {"pillar": "day", "hidden_stem": "Quý", "ten_god": "Chính Ấn"},
            ],
        },
    }


def test_five_stage_marriage_editorial_pipeline() -> None:
    payload = _thu_phuong_payload()
    evidence = build_marriage_evidence(payload)
    reasoning = build_marriage_reasoning(evidence)
    paragraphs = compose_marriage_narrative(evidence, reasoning)
    validation = validate_marriage_narrative("\n\n".join(paragraphs), evidence)
    result = run_marriage_editorial(payload)

    assert evidence.spouse_role == "Phu tinh"
    assert evidence.spouse_stars == ("Chính Quan", "Thất Sát")
    assert evidence.spouse_palace == "Thìn"
    assert evidence.palace_hidden_gods == ("Thiên Tài", "Kiếp Tài", "Chính Ấn")
    assert any(item.god == "Chính Quan" and item.pillar == "hour" and item.visibility == "lộ" for item in evidence.occurrences)
    assert [step.id for step in reasoning] == ["spouse-star", "spouse-palace", "strength", "useful-god"]
    assert "Điểm đáng chú ý nhất" in paragraphs[0]
    assert "Duyên chính thức thường rõ hơn" in paragraphs[0]
    assert "Cung phối ngẫu đặt tại Thìn" in " ".join(paragraphs)
    assert "Kết luận thực tế:" in paragraphs[-1]
    assert validation["passed"] is True
    assert result["status"] == "ready"
    assert result["provider"] == "grounded_editorial_v1"


def test_validator_rejects_unsupported_absolute_marriage_claim() -> None:
    evidence = build_marriage_evidence(_thu_phuong_payload())
    report = validate_marriage_narrative(
        "Chính Quan lộ tại trụ giờ, cung phối ngẫu Thìn. Chắc chắn ly hôn.",
        evidence,
    )

    assert report["passed"] is False
    assert "unsupported_absolute_claim" in report["errors"]

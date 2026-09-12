"""RB05-E phone score result and verified_by_runtime."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine

GOLDEN_BREAKDOWN = [
    ("Cấu trúc năng lượng", 21, 25),
    ("Dòng tài vận", 22, 25),
    ("Công việc & trợ lực", 17, 20),
    ("Ổn định & rủi ro", 10, 15),
    ("Năng lượng kết", 12, 15),
]
GOLDEN_REASONS = [
    "Cấu trúc Cát giữ vai trò chủ đạo",
    "Dòng Tài có nguồn rõ",
    "Công việc là trục mạnh",
    "Họa Hại cần được sử dụng đúng cách",
]
FORBIDDEN_KEYS = {
    "occurrence_id",
    "source_span",
    "energy_id",
    "strength_rank",
    "state",
    "classification",
    "rank",
}


def _phone(number: str = "0328278786", purpose_context: str = "phone_number"):
    return NumberEnergyEngine().analyze(number, purpose_context=purpose_context)


def test_golden_phone_score_grade_and_verified() -> None:
    result = _phone()
    assert result.score is not None
    payload = result.score.to_dict()
    assert payload["total"] == 82
    assert payload["max"] == 100
    assert payload["display"] == "82 / 100"
    assert payload["grade"] == "TỐT"
    assert payload["verified_by_runtime"] is True
    assert result.verified_by_runtime is True
    assert "%" not in payload["display"]
    rows = payload["breakdown"]
    assert [(item["label"], item["earned"], item["max"]) for item in rows] == GOLDEN_BREAKDOWN
    assert sum(item["earned"] for item in rows) == 82
    assert [item["title"] for item in payload["reasons"]] == GOLDEN_REASONS
    assert FORBIDDEN_KEYS.isdisjoint(payload.keys())
    blob = str(payload).lower()
    assert "chắc chắn phát tài" not in blob
    assert "source_span" not in blob
    assert "energy_id" not in blob


def test_golden_score_does_not_change_recommendation() -> None:
    result = _phone()
    assert result.recommendation is not None
    assert result.recommendation.label == "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
    assert result.assessment is not None
    assert result.assessment.story_line == "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI"


def test_non_phone_does_not_receive_phone_score() -> None:
    result = _phone(purpose_context="car_plate")
    assert result.score is None
    assert result.verified_by_runtime is False
    generic = _phone("103", purpose_context="generic_number")
    assert generic.score is None
    assert generic.verified_by_runtime is False


def test_phone_without_golden_pattern_is_not_fixture_82() -> None:
    result = _phone("103")
    assert result.score is not None
    assert result.verified_by_runtime is True
    assert result.score.total != 82
    payload = result.score.to_dict()
    assert payload["display"] == f"{result.score.total} / 100"
    assert "%" not in payload["display"]

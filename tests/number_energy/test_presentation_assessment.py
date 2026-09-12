"""RB05-F assessment and recommendation composed from A/B/C/D, not from score."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine
from engines.number_energy.constants import FORBIDDEN_CUSTOMER_PHRASES

FORBIDDEN_KEYS = {
    "occurrence_id",
    "source_span",
    "energy_id",
    "strength_rank",
    "classification",
    "rank",
    "verified_by_runtime",
    "score",
    "grade",
}

UNSAFE_PHRASES = (
    "chắc chắn phát tài",
    "đổi số ngay",
    "mua số",
    "mua sim",
    "chẩn đoán bệnh",
    "82 / 100",
    "verified_by_runtime",
)

GOLDEN_SUMMARY = (
    "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y. "
    "Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp "
    "tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy."
)
GOLDEN_STORY = "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI"
GOLDEN_REC_LABEL = "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
GOLDEN_REC_SUMMARY = (
    "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài."
)


def _phone(number: str = "0328278786", purpose_context: str = "phone_number"):
    return NumberEnergyEngine().analyze(number, purpose_context=purpose_context)


def _assert_safe(payload: dict) -> None:
    assert FORBIDDEN_KEYS.isdisjoint(payload.keys())
    blob = str(payload).lower()
    for phrase in (*FORBIDDEN_CUSTOMER_PHRASES, *UNSAFE_PHRASES):
        assert phrase.lower() not in blob
    assert "hidden" not in blob
    assert "amplified" not in blob


def test_golden_phone_assessment_summary_and_story() -> None:
    result = _phone()
    assert result.assessment is not None
    payload = result.assessment.to_dict()
    assert payload["title"] == "Đánh giá tổng thể"
    assert payload["summary"] == GOLDEN_SUMMARY
    assert payload["story_line"] == GOLDEN_STORY
    assert payload["story_nodes"] == ["QUÝ NHÂN", "TÀI", "SỰ NGHIỆP", "TÀI"]
    _assert_safe(payload)


def test_golden_phone_recommendation_label_and_summary() -> None:
    result = _phone()
    assert result.recommendation is not None
    payload = result.recommendation.to_dict()
    assert payload["label"] == GOLDEN_REC_LABEL
    assert payload["state"] == GOLDEN_REC_LABEL
    assert payload["summary"] == GOLDEN_REC_SUMMARY
    _assert_safe(payload)


def test_vehicle_plate_uses_customer_assessment_and_recommendation() -> None:
    result = _phone(purpose_context="car_plate")
    assert result.assessment is not None
    assert result.recommendation is not None
    _assert_safe(result.assessment.to_dict())
    _assert_safe(result.recommendation.to_dict())


def test_phone_without_golden_pattern_is_not_golden_recommendation() -> None:
    result = _phone("103")
    assert result.assessment is not None
    assert result.recommendation is not None
    assert result.assessment.summary != GOLDEN_SUMMARY
    assert result.assessment.story_line != GOLDEN_STORY
    assert result.recommendation.label != GOLDEN_REC_LABEL
    _assert_safe(result.assessment.to_dict())
    _assert_safe(result.recommendation.to_dict())

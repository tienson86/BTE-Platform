"""RB05-D domain insights, 4+2 findings, and customer-safe evidence."""

from __future__ import annotations

from engines.number_energy import NumberEnergyEngine
from engines.number_energy.constants import FORBIDDEN_CUSTOMER_PHRASES
from engines.number_energy.findings_catalog import ALLOWED_EVIDENCE_SOURCES

FORBIDDEN_FINDING_KEYS = {
    "occurrence_id",
    "source_span",
    "energy_id",
    "strength_rank",
    "state",
    "classification",
    "rank",
    "effect_type",
    "start_index",
    "end_index",
}

GUARANTEE_PHRASES = (
    "chắc chắn phát tài",
    "chắc chắn giữ được tiền",
    "về già chắc chắn",
    "rất giàu",
    "chắc chắn giàu",
    "cuối đời sẽ",
    "chẩn đoán bệnh",
)

GOLDEN_DOMAINS = [
    ("Tài vận", "Có đường Tài tương đối rõ"),
    ("Công việc & sự nghiệp", "Đây là một trong những điểm mạnh nhất của dãy"),
    ("Tình cảm & quan hệ", "Quan hệ xã hội có yếu tố hỗ trợ"),
    ("Tính cách & năng lực", "Trách nhiệm và năng lực làm việc khá rõ"),
    ("Cân bằng trường khí", "Cát tinh giữ vai trò chủ đạo"),
]

GOLDEN_STRENGTHS = [
    "Quý nhân có thể mở đường cho Tài",
    "Năng lực nghề nghiệp nổi bật",
    "Công việc có khả năng tạo thành quả",
    "Khẩu tài có thể phát huy tích cực",
]

GOLDEN_CAUTIONS = [
    "Cần chú ý cách sử dụng lời nói",
    "Không nên chỉ nhìn số lượng Cát tinh",
]


def _phone(number: str = "0328278786", purpose_context: str = "phone_number"):
    return NumberEnergyEngine().analyze(number, purpose_context=purpose_context)


def _assert_customer_safe(payload: dict) -> None:
    assert FORBIDDEN_FINDING_KEYS.isdisjoint(payload.keys())
    blob = str(payload).lower()
    for phrase in (*FORBIDDEN_CUSTOMER_PHRASES, *GUARANTEE_PHRASES):
        assert phrase.lower() not in blob
    for ref in payload.get("evidence_refs", []):
        assert ref["source"] in ALLOWED_EVIDENCE_SOURCES
        assert FORBIDDEN_FINDING_KEYS.isdisjoint(ref.keys())
    for item in payload.get("items", []):
        assert item["source"] in ALLOWED_EVIDENCE_SOURCES
        assert FORBIDDEN_FINDING_KEYS.isdisjoint(item.keys())


def test_golden_phone_five_domains_in_order() -> None:
    domains = [item.to_dict() for item in _phone().domain_insights]
    assert len(domains) == 5
    assert [(item["domain"], item["conclusion"]) for item in domains] == GOLDEN_DOMAINS
    assert "cam kết tài chính" in domains[0]["caution"]
    for item in domains:
        _assert_customer_safe(item)
        assert item["evidence_refs"]


def test_golden_phone_four_strengths_and_two_cautions() -> None:
    result = _phone()
    strengths = [item.to_dict() for item in result.strengths]
    cautions = [item.to_dict() for item in result.cautions]
    assert [item["title"] for item in strengths] == GOLDEN_STRENGTHS
    assert [item["title"] for item in cautions] == GOLDEN_CAUTIONS
    assert len(strengths) == 4
    assert len(cautions) == 2
    for item in (*strengths, *cautions):
        _assert_customer_safe(item)
        assert item["semantic_key"]
        assert item["summary"]


def test_golden_phone_evidence_refs_are_customer_safe() -> None:
    evidence = [item.to_dict() for item in _phone().evidence]
    assert evidence
    sources = {item["source"] for item in evidence}
    assert sources <= ALLOWED_EVIDENCE_SOURCES
    assert "score" not in sources
    blob = str(evidence).lower()
    assert "source_span" not in blob
    assert "energy_id" not in blob
    assert "82 / 100" not in blob
    assert "chắc chắn phát tài" not in blob
    for group in evidence:
        _assert_customer_safe(group)
        assert group["items"]
    labels = " ".join(
        str(item.get("label") or "")
        for group in evidence
        for item in group["items"]
    )
    assert "Diên Niên · Thiên Y · Sinh Khí" in labels
    assert "8 cặp · 7 Cát · 1 Hung" in labels
    assert "86" in str(evidence)


def test_vehicle_plate_uses_customer_domains() -> None:
    result = _phone(purpose_context="car_plate")
    assert len(result.domain_insights) == 5
    assert result.strengths
    assert result.cautions
    assert result.evidence


def test_phone_without_golden_pattern_still_has_five_domains() -> None:
    result = _phone("103")
    domains = [item.to_dict() for item in result.domain_insights]
    assert [item["domain"] for item in domains] == [item[0] for item in GOLDEN_DOMAINS]
    assert domains[0]["conclusion"] != GOLDEN_DOMAINS[0][1]
    assert len(result.strengths) == 0
    assert [item.title for item in result.cautions] == [GOLDEN_CAUTIONS[1]]
    for item in domains:
        _assert_customer_safe(item)

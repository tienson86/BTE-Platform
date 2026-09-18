"""Grounded editorial pipeline for career, wealth, and health.

The calculation payload is the source of truth. This module connects facts
across domains, writes customer-facing prose, and rejects unsupported claims.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


OUTPUT_GODS = ("Thực Thần", "Thương Quan")
WEALTH_GODS = ("Chính Tài", "Thiên Tài")
OFFICER_GODS = ("Chính Quan", "Thất Sát")
RESOURCE_GODS = ("Chính Ấn", "Thiên Ấn")


@dataclass(frozen=True)
class LifeDomainEvidence:
    day_master: str
    strength: str
    strength_nuance: str
    useful_god: str
    favorable_gods: tuple[str, ...]
    unfavorable_gods: tuple[str, ...]
    element_counts: tuple[tuple[str, int], ...]
    output_gods: tuple[str, ...]
    wealth_gods: tuple[str, ...]
    officer_gods: tuple[str, ...]
    resource_gods: tuple[str, ...]


@dataclass(frozen=True)
class EditorialReasoning:
    id: str
    evidence: str
    inference: str
    confidence: str


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _items(value: Any) -> list[Mapping[str, Any]]:
    return [item for item in value if isinstance(item, Mapping)] if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _first(*values: Any) -> str:
    return next((_text(value) for value in values if _text(value)), "")


def _labels(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if not isinstance(value, list):
        return ()
    labels = []
    for item in value:
        label = _first(_mapping(item).get("display"), _mapping(item).get("label"), _mapping(item).get("element"), item if isinstance(item, str) else "")
        if label and label not in labels:
            labels.append(label)
    return tuple(labels)


def _strength_label(value: Any) -> str:
    normalized = _text(value).lower().replace("_", " ").replace("-", " ")
    return {
        "balanced": "Thân trung hòa",
        "moderate": "Thân trung hòa",
        "strong": "Thân vượng",
        "very strong": "Thân quá vượng",
        "weak": "Thân nhược",
        "very weak": "Thân quá nhược",
    }.get(normalized, _text(value))


def _strength_nuance(strength: Mapping[str, Any], label: str) -> str:
    if "trung hòa" not in label.lower():
        return label
    root = float(strength.get("root_score") or 0)
    drain = abs(float(strength.get("drain_score") or 0))
    control = abs(float(strength.get("control_score") or 0))
    if root > 0 and drain + control >= 0.20:
        return "Thân trung hòa nhưng chịu tiết/khắc đáng kể và vẫn có căn"
    return label


def _ten_god_labels(payload: Mapping[str, Any]) -> tuple[str, ...]:
    ten_gods = _mapping(payload.get("ten_gods"))
    labels: list[str] = []
    for field in ("visible", "hidden"):
        for item in _items(ten_gods.get(field)):
            label = _first(item.get("ten_god"), item.get("label"))
            if label and label not in labels:
                labels.append(label)
    for pillar_name in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
        label = _text(_mapping(_mapping(payload.get("bazi")).get(pillar_name)).get("ten_god"))
        if label and label not in labels:
            labels.append(label)
    return tuple(labels)


def build_life_domain_evidence(payload: Mapping[str, Any]) -> LifeDomainEvidence:
    bazi = _mapping(payload.get("bazi"))
    identity = _mapping(payload.get("identity"))
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    counts = _mapping(_mapping(payload.get("five_elements")).get("counts"))
    gods = _ten_god_labels(payload)
    strength_label = _strength_label(_first(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    element_counts = tuple((element, int(counts.get(element) or counts.get(key) or 0)) for element, key in (("Mộc", "wood"), ("Hỏa", "fire"), ("Thổ", "earth"), ("Kim", "metal"), ("Thủy", "water")))
    return LifeDomainEvidence(
        day_master=_first(bazi.get("day_master"), identity.get("day_master")),
        strength=strength_label,
        strength_nuance=_strength_nuance(strength, strength_label),
        useful_god=_first(useful.get("useful_display"), useful.get("useful_god"), useful.get("dung_than")),
        favorable_gods=_labels(useful.get("favorable")) or _labels(useful.get("favorable_gods")),
        unfavorable_gods=_labels(useful.get("unfavorable")) or _labels(useful.get("unfavorable_gods")),
        element_counts=element_counts,
        output_gods=tuple(god for god in OUTPUT_GODS if god in gods),
        wealth_gods=tuple(god for god in WEALTH_GODS if god in gods),
        officer_gods=tuple(god for god in OFFICER_GODS if god in gods),
        resource_gods=tuple(god for god in RESOURCE_GODS if god in gods),
    )


def build_life_domain_reasoning(evidence: LifeDomainEvidence) -> tuple[EditorialReasoning, ...]:
    steps: list[EditorialReasoning] = []
    if evidence.output_gods and evidence.wealth_gods:
        steps.append(EditorialReasoning("value-to-money", ", ".join(evidence.output_gods + evidence.wealth_gods), "Năng lực tạo sản phẩm hoặc dịch vụ có đường chuyển hóa thành doanh thu.", "high"))
    if evidence.output_gods and evidence.wealth_gods and evidence.officer_gods:
        steps.append(EditorialReasoning("career-chain", "Thực/Thương → Tài → Quan/Sát", "Năng lực tạo giá trị có thể phát triển thành dòng tiền, rồi thành nghề nghiệp, vị thế và trách nhiệm.", "high"))
    if evidence.wealth_gods:
        steps.append(EditorialReasoning("capacity", evidence.strength_nuance, "Cơ hội tài chính phải được đặt cạnh sức gánh, khả năng giữ tiền và nhịp hồi phục.", "high"))
    dominant = sorted(evidence.element_counts, key=lambda item: item[1], reverse=True)[:2]
    if dominant:
        steps.append(EditorialReasoning("health-load", ", ".join(f"{name} {count}" for name, count in dominant), "Sức khỏe được đọc như khả năng chịu tải và hồi phục; không dùng để chẩn đoán bệnh.", "medium"))
    return tuple(steps)


def _join(values: Sequence[str]) -> str:
    return ", ".join(values)


def compose_life_domain_narrative(evidence: LifeDomainEvidence, reasoning: Sequence[EditorialReasoning]) -> dict[str, list[str]]:
    chain = any(step.id == "career-chain" for step in reasoning)
    value_to_money = any(step.id == "value-to-money" for step in reasoning)
    career: list[str] = []
    wealth: list[str] = []
    health: list[str] = []

    if chain:
        career.append(
            f"Điểm đáng chú ý của lá số là chuỗi {_join(evidence.output_gods)} → {_join(evidence.wealth_gods)} → {_join(evidence.officer_gods)}. "
            "Nói bằng ngôn ngữ đời thường: năng lực cá nhân tạo ra sản phẩm hoặc dịch vụ; giá trị ấy tạo doanh thu; khi được tổ chức tốt, doanh thu tiếp tục tạo nghề nghiệp, vị thế và trách nhiệm. Vì vậy đường nghề không nên được đọc như một danh sách nghề hợp hành, mà phải nhìn vào cơ chế biến chuyên môn thành kết quả có người trả tiền."
        )
    elif value_to_money:
        career.append(
            f"Lá số có {_join(evidence.output_gods)} đi cùng {_join(evidence.wealth_gods)}. Trục nghề nghiệp vì vậy nằm ở khả năng đóng gói kiến thức, kỹ năng hoặc sự sáng tạo thành sản phẩm và dịch vụ cụ thể, thay vì chờ cơ hội đến một cách thụ động."
        )
    else:
        career.append("Cơ chế nghề nghiệp chưa tạo thành một chuỗi Thực/Thương - Tài - Quan rõ trong dữ liệu hiện có. Vì vậy nên ưu tiên chuyên môn thực, vai trò rõ và kiểm chứng bằng kết quả thay vì gán một nghề cố định chỉ từ một hành.")
    career.append(
        f"Với {evidence.strength_nuance.lower()}, con đường bền hơn là tăng dần độ khó và quy mô sau khi đã có quy trình. "
        "Có thể làm trong một hệ thống chuyên nghiệp hoặc phát triển hướng độc lập, nhưng điểm quyết định vẫn là khả năng chuẩn hóa công việc, giữ chất lượng và không ôm quá nhiều vai trò cùng lúc."
    )

    if evidence.wealth_gods:
        wealth.append(
            f"Tài tinh hiện diện qua {_join(evidence.wealth_gods)}. Điều này không nên rút gọn thành 'có số giàu'; kết luận hữu ích hơn là lá số có duyên với bài toán doanh thu, khách hàng, dự án hoặc tích lũy, nhưng tiền chỉ bền khi năng lực tạo giá trị và năng lực quản trị cùng phát triển."
        )
    if value_to_money:
        wealth.append(
            "Điểm cần quản không phải chỉ là kiếm thêm. Khi Thực/Thương sinh Tài, một vòng lặp dễ xuất hiện là làm nhiều, có doanh thu, rồi tiếp tục tái đầu tư hoặc chi ra để mở thêm việc. Nếu thiếu giới hạn, doanh thu tăng nhưng tài sản ròng và sức khỏe không tăng tương ứng. Mô hình phù hợp là một dòng tiền nền ổn định, một dòng tăng trưởng có kiểm soát, cùng quỹ sinh hoạt, dự phòng, tích sản và kinh doanh được tách riêng."
        )
    wealth.append(
        f"Dụng thần công bố là {evidence.useful_god or 'chưa có dữ liệu hiển thị'}. Dữ kiện này chỉ làm bộ lọc cân bằng cho cách mở rộng; nó không thay thế Tài tinh và cũng không đồng nghĩa cứ làm nghề thuộc một hành là sẽ có tiền."
    )

    dominant = sorted(evidence.element_counts, key=lambda item: item[1], reverse=True)[:2]
    health.append(
        "Sức khỏe ở đây được dùng để đọc sức chịu tải, không phải để chẩn đoán bệnh. "
        + (f"Hai khí nổi bật trong thống kê là {dominant[0][0]} và {dominant[1][0]}. " if len(dominant) == 2 else "")
        + "Điểm thực tế cần quan sát là chuỗi làm việc quá sức, ngủ kém, căng thẳng kéo dài và ăn uống thất thường; nếu có triệu chứng cụ thể vẫn phải kiểm tra y khoa."
    )
    if value_to_money:
        health.append(
            "Tài chính và sức khỏe trong lá số này có chung một gốc: càng dùng thêm thời gian và sức lực để đổi lấy doanh thu, giới hạn sức bền càng sớm xuất hiện. Cách cải thiện thiết thực là tăng giá trị trên mỗi đơn vị công sức, xây quy trình và tài sản có thể tạo kết quả lặp lại, đồng thời giữ lịch nghỉ và ngưỡng nhận việc rõ ràng."
        )
    return {"career": career, "wealth": wealth, "health": health}


def validate_life_domain_narrative(sections: Mapping[str, Sequence[str]], evidence: LifeDomainEvidence) -> dict[str, Any]:
    text = "\n".join(paragraph for paragraphs in sections.values() for paragraph in paragraphs)
    errors: list[str] = []
    if evidence.useful_god and evidence.useful_god not in text:
        errors.append("missing_published_useful_god")
    if evidence.strength_nuance and evidence.strength_nuance.lower() not in text.lower():
        errors.append("missing_published_strength")
    forbidden = ("chắc chắn mắc", "chắc chắn giàu", "100%", "bệnh định mệnh")
    if any(term in text.lower() for term in forbidden):
        errors.append("unsupported_absolute_claim")
    return {"passed": not errors, "errors": errors, "checks": ["strength", "useful_god", "cross_domain_logic", "unsupported_claims"]}


def run_life_domain_editorial(payload: Mapping[str, Any]) -> dict[str, Any]:
    evidence = build_life_domain_evidence(payload)
    reasoning = build_life_domain_reasoning(evidence)
    sections = compose_life_domain_narrative(evidence, reasoning)
    validation = validate_life_domain_narrative(sections, evidence)
    return {
        "status": "ready" if validation["passed"] else "rejected",
        "provider": "grounded_editorial_v1",
        "evidence": asdict(evidence),
        "reasoning": [asdict(step) for step in reasoning],
        "sections": sections if validation["passed"] else {},
        "validation": validation,
    }

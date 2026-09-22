"""Grounded editorial pipeline for parents, children, and property."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


RESOURCE_GODS = ("Chính Ấn", "Thiên Ấn")
WEALTH_GODS = ("Chính Tài", "Thiên Tài")
OUTPUT_GODS = ("Thực Thần", "Thương Quan")


@dataclass(frozen=True)
class FamilyPropertyEvidence:
    day_master: str
    strength: str
    useful_god: str
    resource_gods: tuple[str, ...]
    wealth_gods: tuple[str, ...]
    output_gods: tuple[str, ...]
    visible_gods: tuple[str, ...]
    hidden_gods: tuple[str, ...]
    hour_branch: str
    hour_hidden_gods: tuple[str, ...]
    day_branch: str
    earth_count: int


@dataclass(frozen=True)
class FamilyReasoning:
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


def _unique(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def _branch(pillar: Mapping[str, Any]) -> str:
    direct = _text(pillar.get("branch"))
    if direct:
        return direct
    parts = _first(pillar.get("can_chi"), pillar.get("ganzhi"), pillar.get("name")).split()
    return parts[-1] if len(parts) >= 2 else ""


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


def build_family_property_evidence(payload: Mapping[str, Any]) -> FamilyPropertyEvidence:
    bazi = _mapping(payload.get("bazi"))
    ten_gods = _mapping(payload.get("ten_gods"))
    visible_items = _items(ten_gods.get("visible"))
    hidden_items = _items(ten_gods.get("hidden"))
    visible = _unique([_first(item.get("ten_god"), item.get("label")) for item in visible_items])
    hidden = _unique([_first(item.get("ten_god"), item.get("label")) for item in hidden_items])
    all_gods = set(visible + hidden)
    hour_hidden = _unique([
        _first(item.get("ten_god"), item.get("label"))
        for item in hidden_items
        if _text(item.get("pillar")) == "hour"
    ])
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    counts = _mapping(_mapping(payload.get("five_elements")).get("counts"))
    return FamilyPropertyEvidence(
        day_master=_first(bazi.get("day_master"), _mapping(payload.get("identity")).get("day_master")),
        strength=_strength_label(_first(strength.get("strength_level"), pattern.get("than_vuong_nhuoc"))),
        useful_god=_first(useful.get("useful_display"), useful.get("useful_god"), useful.get("dung_than")),
        resource_gods=tuple(god for god in RESOURCE_GODS if god in all_gods),
        wealth_gods=tuple(god for god in WEALTH_GODS if god in all_gods),
        output_gods=tuple(god for god in OUTPUT_GODS if god in all_gods),
        visible_gods=visible,
        hidden_gods=hidden,
        hour_branch=_branch(_mapping(bazi.get("hour_pillar"))),
        hour_hidden_gods=hour_hidden,
        day_branch=_branch(_mapping(bazi.get("day_pillar"))),
        earth_count=int(counts.get("earth") or counts.get("Thổ") or 0),
    )


def build_family_property_reasoning(evidence: FamilyPropertyEvidence) -> tuple[FamilyReasoning, ...]:
    steps: list[FamilyReasoning] = []
    if evidence.resource_gods or evidence.wealth_gods:
        resource_state = "ẩn" if evidence.resource_gods and all(god in evidence.hidden_gods for god in evidence.resource_gods) else "hiện"
        steps.append(FamilyReasoning(
            "parents",
            f"Ấn {resource_state}: {', '.join(evidence.resource_gods) or 'không rõ'}; Tài: {', '.join(evidence.wealth_gods) or 'không rõ'}",
            "Cha mẹ phải được đọc bằng cung vị cùng Tài và Ấn; không quy một sao thành một sự kiện gia đình.",
            "high",
        ))
    if evidence.output_gods:
        steps.append(FamilyReasoning(
            "children",
            f"Tử tinh: {', '.join(evidence.output_gods)}; cung giờ {evidence.hour_branch or 'chưa rõ'} chứa {', '.join(evidence.hour_hidden_gods) or 'chưa rõ'}",
            "Duyên con và cách nuôi dạy được đọc từ Thực/Thương kết hợp trụ giờ, không dùng để định số con.",
            "high",
        ))
    if evidence.earth_count or evidence.wealth_gods:
        steps.append(FamilyReasoning(
            "property",
            f"Thổ {evidence.earth_count}; Tài tinh {', '.join(evidence.wealth_gods) or 'chưa rõ'}; Nhật chi {evidence.day_branch or 'chưa rõ'}",
            "Điền sản được đọc từ khả năng tụ tài, tài sản hữu hình và vận kích hoạt; Bát Tự không có một cung Điền Trạch cố định như Tử Vi.",
            "high",
        ))
    if evidence.resource_gods and evidence.output_gods and evidence.wealth_gods:
        steps.append(FamilyReasoning(
            "generation-chain",
            "Ấn → Nhật chủ → Thực/Thương → Tài",
            "Nguồn lực từ gia đình gốc đi qua năng lực bản thân, chuyển sang thế hệ sau và nền tảng vật chất.",
            "high",
        ))
    return tuple(steps)


def compose_family_property_narrative(evidence: FamilyPropertyEvidence, reasoning: Sequence[FamilyReasoning]) -> dict[str, list[str]]:
    parents: list[str] = []
    children: list[str] = []
    property_lines: list[str] = []
    resource_hidden = evidence.resource_gods and all(god in evidence.hidden_gods for god in evidence.resource_gods)

    if evidence.resource_gods or evidence.wealth_gods:
        parents.append(
            f"Phần cha mẹ được đọc đồng thời qua Ấn tinh ({', '.join(evidence.resource_gods) or 'chưa lộ rõ'}), Tài tinh ({', '.join(evidence.wealth_gods) or 'chưa lộ rõ'}) và cung phụ mẫu. "
            "Tài nghiêng về cách gia đình lo việc thực tế, kinh tế và trách nhiệm; Ấn nghiêng về nuôi dưỡng, che chở và nền học hỏi. Hai nhóm này không được dùng máy móc để gán một sao cho một người rồi kết luận sự kiện cụ thể."
        )
        if resource_hidden:
            parents.append(
                "Ấn tinh có mặt nhưng nằm ở tầng tàng can. Cách diễn đạt phù hợp là sự chăm sóc và nâng đỡ vẫn có, song thường đi phía sau, thể hiện bằng lo toan hoặc hành động nhiều hơn lời nói. Khi Tài tinh đồng thời rõ, tình thương trong gia đình dễ đi kèm các tiêu chuẩn thực tế về nghề nghiệp, thu nhập, hôn nhân và chỗ ở."
            )
        parents.append(
            f"Với {evidence.strength.lower() or 'thế Thân hiện tại'}, quan hệ với cha mẹ thường cân bằng hơn khi chủ mệnh có nghề nghiệp, tài chính và ranh giới riêng. Kết luận nên dùng là hiếu nhưng có ranh giới; lá số không đủ căn cứ để phán cha mẹ ly tán, mất sớm hay một biến cố gia đình cụ thể."
        )

    if evidence.output_gods:
        children.append(
            f"Tử tinh được nhận diện qua {', '.join(evidence.output_gods)}. Khi nhóm Thực/Thương hiện rõ, duyên dành năng lượng cho con cái và thế hệ sau không phải chủ đề mờ; tuy nhiên điều này chỉ nói về cấu trúc quan hệ, không cho phép chốt chính xác có bao nhiêu con hoặc thay thế đánh giá y khoa về sinh sản."
        )
    if evidence.hour_branch and (evidence.output_gods or evidence.hour_hidden_gods):
        detail = f", bên trong có {', '.join(evidence.hour_hidden_gods)}" if evidence.hour_hidden_gods else ""
        children.append(
            f"Cung giờ đặt tại {evidence.hour_branch}{detail}. Đây là lớp dữ liệu để hiểu cách tương tác với con và hậu vận. Nếu Thương Quan hoặc Kiếp Tài nằm trong cung giờ, trẻ dễ có cá tính và nhu cầu tự chủ; cách nuôi phù hợp là nguyên tắc rõ nhưng vẫn cho quyền lựa chọn trong giới hạn, thay vì kiểm soát mọi chi tiết."
        )
    if evidence.output_gods:
        children.append(
            "Mặt cần giữ là xu hướng sinh xuất quá nhiều: thời gian, tiền bạc và sự quan tâm có thể dồn mạnh cho con. Bài toán không phải 'con khắc mẹ/cha', mà là người lớn cần giữ phần đời, sức khỏe và kế hoạch tài chính của mình để việc chăm con không trở thành kiệt sức kéo dài."
        )

    property_lines.append(
        f"Bát Tự không có một cung Điền Trạch cố định giống Tử Vi. Phần nhà đất phải tổng hợp Tài tinh, Thổ, Nhật chi và khả năng tụ tài theo vận. Trong dữ liệu hiện tại, Thổ có mức {evidence.earth_count} và Tài tinh gồm {', '.join(evidence.wealth_gods) or 'chưa lộ rõ'}; đây là tín hiệu để nghiên cứu khả năng chuyển thu nhập thành tài sản hữu hình, không phải lời bảo đảm rằng mua bất động sản lúc nào cũng có lợi."
    )
    if evidence.output_gods and evidence.wealth_gods:
        property_lines.append(
            "Mạch Thực/Thương sinh Tài cho thấy kiểu tạo điền sản hợp lý hơn là dùng năng lực và nghề nghiệp tạo dòng tiền, rồi từng bước chuyển dòng tiền thành tài sản. Hỗ trợ gia đình có thể là bệ đỡ, nhưng hệ thống không được tự suy thành chắc chắn thừa kế nhà đất."
        )
    property_lines.append(
        "Khi xét năm mua, bán hoặc chuyển nhà, Hợp chỉ cho biết có sự kết nối/kích hoạt và Xung chỉ cho biết có chuyển động; Hợp không luôn tốt, Xung không luôn xấu. Quyết định thực tế vẫn phải kiểm tra dòng tiền chịu được, mức vay, pháp lý, thanh khoản và mục tiêu nắm giữ."
    )

    if any(step.id == "generation-chain" for step in reasoning):
        bridge = (
            "Ba phần nối thành một mạch: nguồn lực và kỳ vọng từ gia đình gốc đi qua năng lực tự lập của chủ mệnh; phần sinh xuất tiếp tục dành cho con cái; thành quả tài chính có xu hướng được chuyển thành nền tảng vật chất. Bài học chung là không để trách nhiệm với cha mẹ, con cái và nhà cửa cùng lúc tiêu hao hết sức lực và dòng tiền của bản thân."
        )
        parents.append(bridge)
        children.append(bridge)
        property_lines.append(bridge)
    return {"parents": parents, "children": children, "property": property_lines}


def validate_family_property_narrative(sections: Mapping[str, Sequence[str]], evidence: FamilyPropertyEvidence) -> dict[str, Any]:
    text = "\n".join(paragraph for paragraphs in sections.values() for paragraph in paragraphs)
    errors: list[str] = []
    if evidence.output_gods and not any(god in text for god in evidence.output_gods):
        errors.append("missing_child_star")
    if evidence.resource_gods and not any(god in text for god in evidence.resource_gods):
        errors.append("missing_resource_star")
    forbidden = (
        "chắc chắn có 1 con",
        "chắc chắn có 2 con",
        "cha mẹ sẽ ly hôn",
        "cha sẽ mất sớm",
        "mẹ sẽ mất sớm",
        "chắc chắn được thừa kế",
    )
    if any(term in text.lower() for term in forbidden):
        errors.append("unsupported_family_claim")
    return {"passed": not errors, "errors": errors, "checks": ["parents", "children", "property", "unsupported_claims"]}


def run_family_property_editorial(payload: Mapping[str, Any]) -> dict[str, Any]:
    evidence = build_family_property_evidence(payload)
    reasoning = build_family_property_reasoning(evidence)
    sections = compose_family_property_narrative(evidence, reasoning)
    validation = validate_family_property_narrative(sections, evidence)
    return {
        "status": "ready" if validation["passed"] else "rejected",
        "provider": "grounded_editorial_v1",
        "evidence": asdict(evidence),
        "reasoning": [asdict(step) for step in reasoning],
        "sections": sections if validation["passed"] else {},
        "validation": validation,
    }

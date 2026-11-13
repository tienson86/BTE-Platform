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
        resource_state = "ẩn" if evidence.resource_gods and all(god in evidence.hidden_gods and god not in evidence.visible_gods for god in evidence.resource_gods) else "hiện"
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
    resource_hidden = bool(evidence.resource_gods) and all(
        god in evidence.hidden_gods and god not in evidence.visible_gods
        for god in evidence.resource_gods
    )

    if evidence.resource_gods or evidence.wealth_gods:
        facts = []
        if evidence.resource_gods:
            facts.append(f"Ấn tinh gồm {', '.join(evidence.resource_gods)}")
        if evidence.wealth_gods:
            facts.append(f"Tài tinh gồm {', '.join(evidence.wealth_gods)}")
        parents.append(
            "; ".join(facts) + ". Trong cách luận truyền thống về gia đình, Ấn gắn với sự nuôi dưỡng "
            "và học hỏi, còn Tài gợi phần chăm lo vật chất và trách nhiệm thực tế. Khi hai mặt ấy "
            "được đặt cạnh nhau, điều cần quan tâm là cách bạn vừa đón nhận sự hỗ trợ, vừa hình "
            "thành lựa chọn riêng. Những dấu hiệu này không xác nhận tính cách hay biến cố của cha mẹ."
        )
        if resource_hidden:
            parents.append(
                "Ấn tinh nằm trong Tàng Can, không lộ trên Thiên Can. Theo hướng biểu tượng này, "
                "sự nâng đỡ có thể kín đáo, được cảm nhận qua những việc nhỏ hơn là lời bày tỏ trực tiếp. "
                "Bạn nên đối chiếu với điều gia đình thực sự đã làm cho mình, thay vì mặc định sự "
                "im lặng đồng nghĩa với thiếu quan tâm hoặc chắc chắn có hy sinh phía sau."
            )
        parents.append(
            "Điều đáng vun đắp là hiếu nhưng có ranh giới: nói rõ khả năng và phần trách nhiệm bạn "
            "có thể nhận, đồng thời lắng nghe điều bố mẹ thật sự cần. Nếu hoàn cảnh hoặc mong muốn "
            "khác nhau, một thỏa thuận cụ thể thường giúp hai bên hiểu nhau hơn việc cố làm vừa lòng "
            "tất cả rồi âm thầm mệt mỏi."
        )

    if evidence.output_gods:
        children.append(
            f"Lá số có {', '.join(evidence.output_gods)}, nhóm thường được liên hệ với sự sinh xuất, "
            "diễn đạt và truyền lại điều mình có. Khi bàn con cái, nét này gợi cách bạn dành tâm sức "
            "để hướng dẫn, chăm sóc và đồng hành. Nó không cho phép chốt chính xác có bao nhiêu con "
            "hoặc thay thế đánh giá y khoa về sinh sản."
        )
    if evidence.hour_branch and (evidence.output_gods or evidence.hour_hidden_gods):
        detail = f", Tàng Can có {', '.join(evidence.hour_hidden_gods)}" if evidence.hour_hidden_gods else ""
        children.append(
            f"Trụ giờ mang chi {evidence.hour_branch}{detail}. Đây là phần được xem cùng Thực/Thương "
            "khi bàn cách bạn trao kinh nghiệm và chăm lo cho thế hệ sau. Sự gắn bó không chỉ nằm "
            "ở việc làm thay, mà còn ở khả năng để người khác tự thử và trưởng thành."
        )
        if any(god in evidence.hour_hidden_gods for god in ("Thương Quan", "Kiếp Tài")):
            children.append(
                "Thương Quan hoặc Kiếp Tài trong trụ giờ làm nổi bật chủ đề tự chủ trong cách "
                "diễn giải quan hệ này. Điều cần chú ý là mong muốn hướng dẫn của bạn có để lại "
                "không gian lựa chọn cho người đi sau hay không. Nếu đang nuôi dạy con, có thể "
                "thống nhất giới hạn an toàn rồi để con chọn cách thực hiện; không suy từ dấu này "
                "rằng con nhất định có một tính cách cụ thể."
            )
    if evidence.output_gods:
        children.append(
            "Nếu bạn đang dành nhiều thời gian và công sức cho con, hãy giữ cả thời gian hồi phục "
            "và những kế hoạch riêng. Sự chăm sóc bền vững cần người lớn còn đủ sức lắng nghe, "
            "không phải hy sinh mọi nhu cầu rồi mong con bù đắp lại. Nếu chưa có con, phần ý nghĩa "
            "về truyền đạt và dìu dắt vẫn có thể đối chiếu với người bạn đang hướng dẫn."
        )

    facts = []
    if evidence.wealth_gods:
        facts.append(f"Tài tinh gồm {', '.join(evidence.wealth_gods)}")
    if evidence.day_branch:
        facts.append(f"Nhật chi là {evidence.day_branch}")
    if facts:
        property_lines.append(
            "; ".join(facts) + ". Khi bàn điền trạch, cần nối khả năng tạo thu nhập với việc "
            "tích lũy và nhu cầu về nơi ở. Số lần xuất hiện của Thổ trong bảng ngũ hành không "
            "đồng nghĩa với số lượng nhà đất hay khả năng được thừa kế. Một nơi ở phù hợp trước "
            "hết cần đáp ứng sinh hoạt và khả năng chi trả thực tế của bạn."
        )
    else:
        property_lines.append(
            "Chưa đủ dữ kiện riêng để luận xu hướng điền trạch. Không nên suy quyền sở hữu nhà đất "
            "chỉ từ một hành nổi bật hoặc một tên sao. Khi lựa chọn nơi ở, hãy ưu tiên nhu cầu "
            "sinh hoạt, khả năng chi trả và thông tin pháp lý đã được kiểm tra."
        )
    if evidence.output_gods and evidence.wealth_gods:
        property_lines.append(
            f"Sự hiện diện của {', '.join(evidence.output_gods)} cùng {', '.join(evidence.wealth_gods)} "
            "gợi chủ đề dùng năng lực để tạo nguồn thu rồi tích lũy từng bước. Đây là mối liên hệ "
            "cần đọc cùng sức mạnh của các hành và hoàn cảnh thực tế, không tự bảo đảm một khoản "
            "thu sẽ chuyển thành tài sản. Khi có kế hoạch lớn, nên phân biệt phần tiền có sẵn "
            "với phần chỉ đang kỳ vọng."
        )
    property_lines.append(
        "Hợp không luôn tốt, Xung không luôn xấu: một thay đổi về nhà ở có thể phù hợp hoặc "
        "không tùy hoàn cảnh. Vì vậy, năm có tương tác Can Chi không tự trở thành thời điểm nên "
        "mua bán. Quyết định thực tế cần cân nhắc nhu cầu, dòng tiền, khoản vay và pháp lý."
    )
    if any(step.id == "generation-chain" for step in reasoning):
        # One synthesis only, instead of the same paragraph repeated in three chapters.
        property_lines.append(
            "Trong kế hoạch dài hạn, điều quan trọng là không để trách nhiệm với cha mẹ, con cái "
            "và nhà cửa cùng lúc tiêu hao hết sức lực và nguồn dự phòng của bạn. Hãy phân biệt "
            "việc cần lo ngay, việc có thể cùng người thân chia sẻ và việc nên chờ đến khi đủ điều kiện."
        )
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

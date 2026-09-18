"""Grounded marriage editorial pipeline.

The calculator remains the only source of Bazi facts.  This module turns those
facts into a reasoning plan and customer prose, then verifies that the prose did
not change the published chart.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


PILLAR_LABELS = {"year": "năm", "month": "tháng", "day": "ngày", "hour": "giờ"}
PILLAR_CONTEXT = {
    "year": "Duyên thường mở qua môi trường xã hội rộng, nền gia đình hoặc các mối quan hệ từ giai đoạn sớm.",
    "month": "Hình tượng phối ngẫu dễ gắn với công việc, môi trường nghề nghiệp và nhịp sống trưởng thành.",
    "day": "Chủ đề bạn đời đi sát đời sống riêng và thường được cảm nhận trực tiếp hơn.",
    "hour": "Duyên chính thức thường rõ hơn khi chủ mệnh đã trưởng thành về nghề nghiệp, tài chính và cách tổ chức cuộc sống.",
}


@dataclass(frozen=True)
class SpouseOccurrence:
    god: str
    pillar: str
    visibility: str


@dataclass(frozen=True)
class MarriageEvidencePack:
    gender: str
    day_master: str
    strength: str
    useful_god: str
    spouse_role: str
    spouse_stars: tuple[str, ...]
    occurrences: tuple[SpouseOccurrence, ...]
    spouse_palace: str
    palace_hidden_stems: tuple[str, ...]
    palace_hidden_gods: tuple[str, ...]


@dataclass(frozen=True)
class ReasoningStep:
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


def _pillar_branch(pillar: Mapping[str, Any]) -> str:
    direct = _text(pillar.get("branch"))
    if direct:
        return direct
    parts = _first(pillar.get("can_chi"), pillar.get("ganzhi"), pillar.get("name")).split()
    return parts[-1] if len(parts) >= 2 else ""


def _gender(payload: Mapping[str, Any]) -> str:
    customer = _mapping(payload.get("customer"))
    person = _mapping(_mapping(payload.get("identity")).get("person"))
    return _first(customer.get("gender_label"), customer.get("gender"), person.get("gender_label"), person.get("gender")).lower()


def _spouse_definition(gender: str) -> tuple[str, tuple[str, ...]]:
    if gender in {"female", "nữ", "nu", "f"}:
        return "Phu tinh", ("Chính Quan", "Thất Sát")
    if gender in {"male", "nam", "m"}:
        return "Thê tinh", ("Chính Tài", "Thiên Tài")
    return "Sao phối ngẫu", ()


def _strength_label(value: Any) -> str:
    text = _text(value)
    normalized = text.lower().replace("_", " ").replace("-", " ")
    labels = {
        "balanced": "Thân trung hòa",
        "moderate": "Thân trung hòa",
        "strong": "Thân vượng",
        "very strong": "Thân quá vượng",
        "weak": "Thân nhược",
        "very weak": "Thân quá nhược",
    }
    return labels.get(normalized, text)


def build_marriage_evidence(payload: Mapping[str, Any]) -> MarriageEvidencePack:
    gender = _gender(payload)
    spouse_role, spouse_stars = _spouse_definition(gender)
    bazi = _mapping(payload.get("bazi"))
    ten_gods = _mapping(payload.get("ten_gods"))
    occurrences: list[SpouseOccurrence] = []
    seen: set[tuple[str, str, str]] = set()
    for field, visibility in (("visible", "lộ"), ("hidden", "ẩn")):
        for item in _items(ten_gods.get(field)):
            god = _first(item.get("ten_god"), item.get("label"))
            pillar = _text(item.get("pillar"))
            key = (god, pillar, visibility)
            if god in spouse_stars and key not in seen:
                seen.add(key)
                occurrences.append(SpouseOccurrence(god, pillar, visibility))

    # Some providers publish the visible stem's Ten God on the pillar itself.
    for pillar_key in PILLAR_LABELS:
        pillar = _mapping(bazi.get(f"{pillar_key}_pillar"))
        god = _text(pillar.get("ten_god"))
        key = (god, pillar_key, "lộ")
        if god in spouse_stars and key not in seen:
            seen.add(key)
            occurrences.append(SpouseOccurrence(god, pillar_key, "lộ"))

    day_hidden = [item for item in _items(ten_gods.get("hidden")) if _text(item.get("pillar")) == "day"]
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    return MarriageEvidencePack(
        gender=gender,
        day_master=_first(bazi.get("day_master"), _mapping(payload.get("identity")).get("day_master")),
        strength=_strength_label(_first(strength.get("strength_level"), pattern.get("than_vuong_nhuoc"))),
        useful_god=_first(useful.get("useful_display"), useful.get("useful_god"), useful.get("dung_than")),
        spouse_role=spouse_role,
        spouse_stars=spouse_stars,
        occurrences=tuple(occurrences),
        spouse_palace=_pillar_branch(_mapping(bazi.get("day_pillar"))),
        palace_hidden_stems=tuple(dict.fromkeys(_first(item.get("hidden_stem"), item.get("stem")) for item in day_hidden if _first(item.get("hidden_stem"), item.get("stem")))),
        palace_hidden_gods=tuple(dict.fromkeys(_first(item.get("ten_god"), item.get("label")) for item in day_hidden if _first(item.get("ten_god"), item.get("label")))),
    )


def build_marriage_reasoning(evidence: MarriageEvidencePack) -> tuple[ReasoningStep, ...]:
    steps: list[ReasoningStep] = []
    visible = [item for item in evidence.occurrences if item.visibility == "lộ"]
    hidden = [item for item in evidence.occurrences if item.visibility == "ẩn"]
    if visible:
        labels = ", ".join(f"{item.god} lộ ở trụ {PILLAR_LABELS.get(item.pillar, item.pillar)}" for item in visible)
        steps.append(ReasoningStep("spouse-star", labels, "Hình tượng phối ngẫu và thái độ với cam kết biểu hiện tương đối rõ.", "high"))
    elif hidden:
        labels = ", ".join(f"{item.god} ẩn ở trụ {PILLAR_LABELS.get(item.pillar, item.pillar)}" for item in hidden)
        steps.append(ReasoningStep("spouse-star", labels, "Duyên có nền nhưng thường cần đúng môi trường hoặc đúng vận mới hiện rõ.", "medium"))
    else:
        steps.append(ReasoningStep("spouse-star", "Chưa thấy sao phối ngẫu trong dữ liệu nguyên cục.", "Không được dựng chân dung quá cụ thể; phải dựa thêm vào cung phối ngẫu và vận.", "limited"))

    if evidence.spouse_palace:
        palace = f"Cung phối ngẫu {evidence.spouse_palace}"
        if evidence.palace_hidden_gods:
            palace += " chứa " + ", ".join(evidence.palace_hidden_gods)
        contains_spouse = any(god in evidence.spouse_stars for god in evidence.palace_hidden_gods)
        inference = (
            "Sao phối ngẫu nằm trong cung, nên chủ đề bạn đời đi trực tiếp vào đời sống riêng."
            if contains_spouse
            else "Sao phối ngẫu không nằm trực tiếp trong cung; hôn nhân còn phải giải các bài toán thực tế được chứa trong cung này."
        )
        steps.append(ReasoningStep("spouse-palace", palace, inference, "high"))

    if evidence.strength:
        if "nhược" in evidence.strength.lower():
            inference = "Quan hệ bền hơn khi tạo an toàn và nâng đỡ, nhưng chủ mệnh vẫn phải giữ tiếng nói riêng."
        elif "vượng" in evidence.strength.lower():
            inference = "Quan hệ cần ranh giới và khả năng nhường nhịp để lập trường mạnh không biến thành hơn thua."
        else:
            inference = "Quan hệ phù hợp cần cân bằng giữa độc lập và nương tựa."
        steps.append(ReasoningStep("strength", evidence.strength, inference, "medium"))
    if evidence.useful_god:
        steps.append(ReasoningStep("useful-god", evidence.useful_god, "Dụng thần chỉ làm bộ lọc cân bằng; không thay thế Phu/Thê tinh và cung phối ngẫu.", "high"))
    return tuple(steps)


def _dominant_portrait(evidence: MarriageEvidencePack) -> tuple[str, str]:
    gods = {item.god for item in evidence.occurrences}
    if "Chính Quan" in gods and "Thất Sát" not in gods:
        return (
            "một người chồng chững chạc, có nghề nghiệp và nguyên tắc rõ, coi trọng trách nhiệm và danh dự",
            "người sống tùy hứng, nóng nảy, thiếu trách nhiệm hoặc dùng nguyên tắc để kiểm soát người khác",
        )
    if "Thất Sát" in gods and "Chính Quan" not in gods:
        return (
            "một người chồng quyết đoán, chịu áp lực tốt nhưng biết tôn trọng ranh giới",
            "người mạnh nhưng độc đoán, đẩy rủi ro và áp lực sang bạn đời",
        )
    if "Chính Quan" in gods and "Thất Sát" in gods:
        return (
            "người vừa có bản lĩnh vừa có ý thức cam kết; sức mạnh phải đi cùng sự ổn định",
            "người tạo cảm xúc mạnh nhưng thiếu cấu trúc để sống lâu dài",
        )
    if "Chính Tài" in gods:
        return (
            "người vợ biết vun vén, giữ lời và có khả năng cùng xây kế hoạch dài hạn",
            "người thiếu minh bạch trong trách nhiệm và tài chính",
        )
    if "Thiên Tài" in gods:
        return (
            "người vợ linh hoạt, giao tiếp tốt nhưng sẵn sàng đưa cảm xúc vào một cam kết rõ ràng",
            "mối quan hệ nhiều cơ hội nhưng không có nhịp sống chung ổn định",
        )
    return ("người có trách nhiệm và cùng giải được bài toán đời sống thực tế", "người hấp dẫn ban đầu nhưng thiếu ổn định và cam kết")


def compose_marriage_narrative(evidence: MarriageEvidencePack, reasoning: Sequence[ReasoningStep]) -> tuple[str, ...]:
    visible = [item for item in evidence.occurrences if item.visibility == "lộ"]
    hidden = [item for item in evidence.occurrences if item.visibility == "ẩn"]
    paragraphs: list[str] = []
    if visible:
        lead = visible[0]
        placement = "; ".join(
            f"{item.god} lộ tại trụ {PILLAR_LABELS.get(item.pillar, item.pillar)}"
            for item in visible
        )
        paragraphs.append(
            f"Với {'nữ' if evidence.spouse_role == 'Phu tinh' else 'nam'} mệnh, {evidence.spouse_role} được đọc qua {', '.join(evidence.spouse_stars)}. "
            f"Điểm đáng chú ý nhất trong đường hôn nhân là {placement}. "
            f"Điều này làm hình tượng người phối ngẫu hiện khá rõ trong nguyên cục. {PILLAR_CONTEXT.get(lead.pillar, '')}"
        )
    elif hidden:
        lead = hidden[0]
        paragraphs.append(
            f"{evidence.spouse_role} có mặt nhưng đang ẩn ở trụ {PILLAR_LABELS.get(lead.pillar, lead.pillar)}. "
            "Vì vậy không nên kết luận là thiếu duyên; đúng hơn là duyên cần đúng môi trường hoặc đúng vận mới trở thành một quan hệ rõ ràng."
        )
    else:
        paragraphs.append(
            f"Nguyên cục chưa cho thấy {evidence.spouse_role.lower()} lộ rõ. Vì vậy phần hôn nhân phải đặt trọng tâm ở cung phối ngẫu và vận kích hoạt, không được dựng một chân dung người bạn đời quá cụ thể."
        )

    portrait, warning = _dominant_portrait(evidence)
    paragraphs.append(
        f"Từ cấu trúc sao phối ngẫu, hình tượng phù hợp là {portrait}. Điều quan trọng không nằm ở vẻ ngoài hay một nghề cố định, mà ở cách người đó giữ lời, gánh trách nhiệm và tổ chức cuộc sống chung."
    )

    palace_detail = ", ".join(evidence.palace_hidden_gods)
    if evidence.spouse_palace:
        text = f"Cung phối ngẫu đặt tại {evidence.spouse_palace}"
        if palace_detail:
            text += f", bên trong có {palace_detail}"
        text += ". Đây là phần mô tả đời sống sau khi sức hút ban đầu đã qua."
        if not any(god in evidence.spouse_stars for god in evidence.palace_hidden_gods):
            text += " Vì Phu/Thê tinh không nằm trực tiếp trong cung này, người đi đến hôn nhân không chỉ cần hợp cảm xúc mà còn phải cùng chủ mệnh giải được chuyện công việc, tiền bạc, gia đình và sự nâng đỡ tinh thần."
        paragraphs.append(text)

    strength_step = next((step for step in reasoning if step.id == "strength"), None)
    if strength_step:
        paragraphs.append(f"Xét thế Thân, lá số được xác định là {evidence.strength}. {strength_step.inference}")
    if evidence.useful_god:
        paragraphs.append(
            f"Dụng thần {evidence.useful_god} được dùng như bộ lọc cân bằng, không phải công thức chọn chồng hoặc vợ theo một hành duy nhất. Một người phù hợp phải làm đời sống chung sáng rõ và ổn định hơn, chứ không chỉ tạo cảm giác bị thu hút lúc đầu."
        )
    paragraphs.append(
        f"Kết luận thực tế: nên ưu tiên người có các phẩm chất ổn định vừa nêu; cần thận trọng với {warning}. Lá số không đủ độ phân giải để chốt chính xác nghề nghiệp, ngoại hình, tuổi của người phối ngẫu hay số lần đổ vỡ, nên những nội dung đó chỉ được nêu khi có thêm căn cứ từ vận và dữ liệu thực tế."
    )
    return tuple(paragraphs)


def validate_marriage_narrative(text: str, evidence: MarriageEvidencePack) -> dict[str, Any]:
    errors: list[str] = []
    for occurrence in evidence.occurrences:
        if occurrence.visibility == "lộ" and occurrence.god not in text:
            errors.append(f"missing_visible_spouse_star:{occurrence.god}")
    if evidence.spouse_palace and evidence.spouse_palace not in text:
        errors.append("missing_spouse_palace")
    role_text = text.replace("Phu/Thê tinh", "")
    opposite_role = "Thê tinh" if evidence.spouse_role == "Phu tinh" else "Phu tinh"
    if opposite_role in role_text and evidence.spouse_role not in role_text:
        errors.append("gender_role_mismatch")
    absolute_terms = ("chắc chắn cưới", "chắc chắn ly hôn", "phải hai đời", "100%")
    if any(term in text.lower() for term in absolute_terms):
        errors.append("unsupported_absolute_claim")
    return {"passed": not errors, "errors": errors, "checks": ["gender", "spouse_star", "spouse_palace", "unsupported_claims"]}


def run_marriage_editorial(payload: Mapping[str, Any]) -> dict[str, Any]:
    evidence = build_marriage_evidence(payload)
    reasoning = build_marriage_reasoning(evidence)
    paragraphs = compose_marriage_narrative(evidence, reasoning)
    validation = validate_marriage_narrative("\n\n".join(paragraphs), evidence)
    return {
        "status": "ready" if validation["passed"] else "rejected",
        "provider": "grounded_editorial_v1",
        "evidence": asdict(evidence),
        "reasoning": [asdict(step) for step in reasoning],
        "paragraphs": list(paragraphs) if validation["passed"] else [],
        "validation": validation,
    }

"""Render TV-01 comparison facts into customer Vietnamese. Decision stays structured."""

from __future__ import annotations

from consulting.marriage.models.comparison import MarriageComparisonFact
from consulting.marriage.models.enums import RelationshipSubject

_ELEMENT = {
    "wood": "Mộc",
    "fire": "Hỏa",
    "earth": "Thổ",
    "metal": "Kim",
    "water": "Thủy",
}
_SLOT = {
    "year": "niên trụ",
    "month": "nguyệt trụ",
    "day": "nhật trụ",
    "hour": "thời trụ",
}
_RELATION = {
    "stem_combination": "hợp can",
    "stem_control": "khắc can",
    "branch_combination": "hợp chi",
    "branch_clash": "xung chi",
    "branch_harm": "hại chi",
    "branch_punishment": "hình chi",
    "branch_break": "phá chi",
    "branch_meeting": "hội chi",
}
_THEME = {
    "support": "bổ trợ",
    "control": "kiểm soát / trách nhiệm",
    "finance": "tài chính / nguồn lực",
    "expression": "thể hiện / giao tiếp",
    "competition": "cạnh tranh vai trò",
    "resource": "nguồn lực nền tảng",
    "earning_role_complement": "bổ sung vai trò tạo nguồn",
    "resource_competition": "cạnh tranh nguồn lực",
    "financial_control_pressure": "áp lực kiểm soát tiền bạc",
    "shared_financial_support": "hỗ trợ tài chính dùng chung",
}
_Q2 = {
    "mutual_material_support": "Hai người có bổ trợ vật chất hai chiều, không chỉ một phía.",
    "limited_or_one_way": "Bổ trợ có thật nhưng nghiêng một phía hơn là đều hai chiều.",
    "support_not_established": "Chưa đủ tín hiệu bổ trợ cụ thể để kết luận hai chiều.",
}
_Q3 = {
    "a_supports_more": "Người A bổ trợ Người B rõ hơn chiều ngược lại.",
    "b_supports_more": "Người B bổ trợ Người A rõ hơn chiều ngược lại.",
    "balanced_support": "Mức bổ trợ hai chiều tương đối cân, không lệch hẳn một phía.",
    "support_not_directional": "Chưa tách được chiều bổ trợ A→B và B→A một cách rõ.",
}
_Q5 = {
    "major_conflict_mitigated": "Xung đột lớn có yếu tố giảm, nhưng phần dư vẫn cần quản lý.",
    "rescue_present": "Có yếu tố cứu giải đi kèm các điểm căng.",
    "conflict_unmitigated": "Điểm xung lớn chưa thấy yếu tố giảm đi kèm.",
    "rescue_not_established": "Chưa đủ cơ sở để nói các xung đột đã được giảm.",
}
_Q6 = {
    "structure_supports_long_term": "Nền tảng có khả năng duy trì tốt nếu hai người giữ quy ước đang hiệu quả.",
    "maintainable_if_managed": "Khả năng hòa hợp khá nhưng cần quản lý đúng điểm căng.",
    "needs_active_management": "Cấu trúc có áp lực rõ; sống chung ổn định được nếu quản lý đúng điểm lệch.",
    "insufficient": "Chưa đủ dữ liệu cấu trúc để nói về khả năng đi lâu dài.",
}


def render_fact(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Turn one structured fact into a customer sentence. No internal ids."""
    renderer = _RENDERERS.get(fact.template_key, _fallback)
    return renderer(fact, person_a, person_b)


def render_question(key: str, fallback: str) -> str:
    """Render one overall-question key. Unknown keys stay conservative."""
    catalog = {**_Q2, **_Q3, **_Q5, **_Q6}
    return catalog.get(key, fallback)


def _people(fact: MarriageComparisonFact, person_a: str, person_b: str) -> tuple[str, str]:
    """Return (offer, need) labels for a directional fact."""
    if fact.subject is RelationshipSubject.A_TO_B:
        return person_a, person_b
    if fact.subject is RelationshipSubject.B_TO_A:
        return person_b, person_a
    return person_a, person_b


def _element(value: str) -> str:
    """Map an element code onto Vietnamese."""
    return _ELEMENT.get(value, value)


def _slot(value: str) -> str:
    """Map a pillar slot onto Vietnamese."""
    return _SLOT.get(value, value)


def _useful_god_support(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """B hỗ trợ Dụng thần of A, or the reverse."""
    offer, need = _people(fact, person_a, person_b)
    element = _element(fact.slots.get("element") or "")
    return f"{offer} hỗ trợ Dụng thần {element} của {need}"


def _favorable_support(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Favorable-element support, distinct from useful-god support."""
    offer, need = _people(fact, person_a, person_b)
    element = _element(fact.slots.get("element") or "")
    return f"{offer} bổ trợ hành {element} vốn thuận với {need}"


def _unfavorable_activation(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Offering chart activates an unfavorable factor in the other."""
    offer, need = _people(fact, person_a, person_b)
    element = _element(fact.slots.get("element") or "")
    return f"{offer} kích hoạt yếu tố bất lợi {element} trong cấu trúc của {need}"


def _useful_need(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Published useful-god need. Not missing-element logic."""
    need_side = fact.slots.get("need_side") or ""
    need = person_a if need_side == "A" else person_b
    element = _element(fact.slots.get("element") or "")
    return f"{need} cần Dụng thần {element}"


def _stem_branch(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Specific Can Chi interaction with pillar context."""
    relation = _RELATION.get(fact.template_key, fact.template_key)
    slot_a = _slot(fact.slots.get("slot_a") or "")
    slot_b = _slot(fact.slots.get("slot_b") or "")
    can_a = fact.slots.get("can_chi_a") or ""
    can_b = fact.slots.get("can_chi_b") or ""
    if slot_a and slot_b:
        place = f"{slot_a} của {person_a} và {slot_b} của {person_b}"
    else:
        place = "cấu trúc Can Chi của hai người"
    detail = f" ({can_a} / {can_b})" if can_a and can_b else ""
    if fact.template_key == "stem_control":
        offer, need = _people(fact, person_a, person_b)
        return f"{offer} có quan hệ {relation} hướng tới {need} ở {place}{detail}"
    return f"{place} có quan hệ {relation}{detail}"


def _rescued_interaction(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Rescue reduces residual clash. It does not erase the original atom."""
    _ = (person_a, person_b)
    relation = _RELATION.get(fact.slots.get("relation_type") or "", "xung")
    return f"Quan hệ {relation} này có yếu tố hợp hỗ trợ làm giảm, nhưng phần dư vẫn cần lưu ý"


def _role_support(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Named role complement. Explains which role is being supported."""
    offer, need = _people(fact, person_a, person_b)
    role = fact.slots.get("role") or "vai trò"
    theme_key = fact.slots.get("theme") or ""
    theme = _THEME.get(theme_key, "bổ trợ")
    if theme_key == "competition":
        return f"Hệ vai trò cho thấy {offer} mang vai trò {role}, cùng nhóm cạnh tranh nguồn lực với {need}"
    return f"Hệ vai trò cho thấy {offer} bổ sung phần {theme} ({role}) cho {need}"


def _role_pressure(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Named role pressure. Explains which role is being pressured."""
    offer, need = _people(fact, person_a, person_b)
    role = fact.slots.get("role") or "vai trò"
    theme = _THEME.get(fact.slots.get("theme") or "", "áp lực vai trò")
    return f"Hệ vai trò cho thấy {offer} tạo áp lực ở phần {theme} ({role}) của {need}"


def _wealth(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Finance meaning without predicting wealth."""
    offer, need = _people(fact, person_a, person_b)
    role = fact.slots.get("role") or "vai trò tài"
    theme = _THEME.get(fact.slots.get("theme") or "", "")
    if fact.template_key == "wealth_support":
        return (
            f"{offer} bổ sung vai trò tạo nguồn ({role}) cho việc phối hợp tài chính với {need}"
            if theme
            else f"{offer} có vai trò tài ({role}) có thể phối hợp với {need}"
        )
    return f"{offer} và {need} có tín hiệu cạnh tranh nguồn lực từ vai trò {role}"


def _luck(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Timing activation. No calendar years."""
    person_key = fact.slots.get("person") or ""
    person = person_a if person_key == "A" else person_b if person_key == "B" else "một người"
    element = _element(fact.slots.get("element") or "")
    if fact.template_key == "luck_alignment":
        return f"Nhịp thời điểm của {person} đang kích hoạt hướng hỗ trợ {element}, không viết lại nền tảng"
    return f"Nhịp thời điểm của {person} đang kích hoạt hướng nhạy {element}, không viết lại nền tảng"


def _derived(template: str, text: str):
    """Bind a derived-interaction sentence."""

    def _render(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
        _ = (fact, person_a, person_b, template)
        return text

    return _render


def _fallback(fact: MarriageComparisonFact, person_a: str, person_b: str) -> str:
    """Conservative fallback. Still names the comparison class."""
    _ = (person_a, person_b)
    return f"Có tín hiệu so sánh cụ thể ở lớp {fact.domain.value} ({fact.template_key})"


_RENDERERS = {
    "useful_god_support": _useful_god_support,
    "favorable_support": _favorable_support,
    "unfavorable_activation": _unfavorable_activation,
    "useful_need": _useful_need,
    "stem_combination": _stem_branch,
    "stem_control": _stem_branch,
    "branch_combination": _stem_branch,
    "branch_clash": _stem_branch,
    "branch_harm": _stem_branch,
    "branch_punishment": _stem_branch,
    "branch_break": _stem_branch,
    "branch_meeting": _stem_branch,
    "rescued_interaction": _rescued_interaction,
    "role_support": _role_support,
    "role_pressure": _role_pressure,
    "wealth_support": _wealth,
    "wealth_pressure": _wealth,
    "luck_alignment": _luck,
    "luck_misalignment": _luck,
    "communication_support": _derived(
        "communication_support",
        "Xu hướng giao tiếp được nâng đỡ từ các mối hợp Can Chi đã thấy ở nền tảng",
    ),
    "communication_friction": _derived(
        "communication_friction",
        "Ma sát giao tiếp bám theo các mối xung/hại Can Chi, không phải suy diễn tính cách",
    ),
    "decision_style_tension": _derived(
        "decision_style_tension",
        "Cách quyết định dễ lệch nhịp vì hệ vai trò có điểm áp lực",
    ),
    "control_tension": _derived(
        "control_tension",
        "Có căng về kiểm soát xuất phát từ khắc can hoặc áp lực vai trò đã ghi nhận",
    ),
    "adaptive_interaction": _derived(
        "adaptive_interaction",
        "Hai người vừa bổ trợ vừa cần điều chỉnh ở ngũ hành, nên tương tác cần linh hoạt có quy ước",
    ),
    "conflict_resolution_capacity": _derived(
        "conflict_resolution_capacity",
        "Khả năng giảm xung được nâng bởi các mối hợp/hội đi kèm điểm căng",
    ),
    "responsibility_alignment": _derived(
        "responsibility_alignment",
        "Phần trách nhiệm gia đình được nâng từ hệ vai trò bổ trợ đã có",
    ),
    "authority_tension": _derived(
        "authority_tension",
        "Có căng quyền quyết trong đời sống chung, bám theo áp lực vai trò đã thấy",
    ),
    "household_cooperation": _derived(
        "household_cooperation",
        "Việc chung trong nhà được nâng bởi các mối hợp Can Chi đã ghi nhận",
    ),
}

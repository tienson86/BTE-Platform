"""Build a customer-safe, auditable compatibility matrix for TV-01."""

from __future__ import annotations

from consulting.canon.du_nien import FAVORABLE_IDS, lookup
from consulting.marriage.models.comparison import (
    DirectionalAssessment,
    MarriageDomainComparison,
)
from consulting.marriage.models.enums import (
    ComparisonFactKind,
    DirectionalAssessmentState,
    FiveElement,
    MarriageDomain,
    RelationshipSubject,
    YinYang,
)
from consulting.marriage.models.matrix import (
    MarriageCompatibilityMatrix,
    MarriageMatrixRow,
    MarriageMatrixSection,
)
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot, PillarValue

MATRIX_VERSION = "marriage.compatibility_matrix.v1@1.0.0"

_ELEMENT_LABEL = {
    FiveElement.WOOD: "Mộc",
    FiveElement.FIRE: "Hỏa",
    FiveElement.EARTH: "Thổ",
    FiveElement.METAL: "Kim",
    FiveElement.WATER: "Thủy",
}
_ELEMENT_BY_VALUE = {item.value: item for item in FiveElement}
_YIN_YANG_LABEL = {YinYang.YIN: "Âm", YinYang.YANG: "Dương"}
_GENERATES = {
    FiveElement.WOOD: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WATER,
    FiveElement.WATER: FiveElement.WOOD,
}
_CONTROLS = {
    FiveElement.WOOD: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.WATER,
    FiveElement.WATER: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WOOD,
}
_CUNG_EFFECT = {
    "sinh_khi": 2.0,
    "thien_y": 1.5,
    "dien_nien": 2.0,
    "phuc_vi": 1.0,
    "hoa_hai": -1.0,
    "luc_sat": -1.5,
    "ngu_quy": -2.0,
    "tuyet_menh": -2.0,
}
_RELATION_LABEL = {
    "stem_combination": "Thiên Can hợp",
    "stem_control": "Thiên Can khắc",
    "branch_combination": "Địa Chi lục hợp",
    "branch_meeting": "Địa Chi hội hợp",
    "branch_clash": "Địa Chi xung",
    "branch_harm": "Địa Chi hại",
    "branch_punishment": "Địa Chi hình",
    "branch_break": "Địa Chi phá",
}
_PILLAR_LABEL = {"year": "Năm", "month": "Tháng", "day": "Ngày", "hour": "Giờ"}


def project_compatibility_matrix(result: MarriageDecisionResult) -> MarriageCompatibilityMatrix:
    """Project existing Canonical and comparison facts into transparent rows."""
    return MarriageCompatibilityMatrix(
        version=MATRIX_VERSION,
        sections=[
            _useful_god_section(result),
            _cung_phi_section(result),
            _structure_section(result),
            _life_section(result),
        ],
    )


def _useful_god_section(result: MarriageDecisionResult) -> MarriageMatrixSection:
    comparison = result.comparison.five_elements if result.comparison else None
    rows: list[MarriageMatrixRow] = []
    if comparison is None:
        rows.append(_unavailable("useful_god", "Bổ trợ Dụng/Hỷ thần"))
    else:
        rows.extend(
            (
                _directional_element_row(
                    "a_to_b",
                    "Người Nữ bổ trợ Người Nam",
                    comparison.a_to_b,
                    result.canonical_a,
                    result.canonical_b,
                    comparison.confidence,
                ),
                _directional_element_row(
                    "b_to_a",
                    "Người Nam bổ trợ Người Nữ",
                    comparison.b_to_a,
                    result.canonical_b,
                    result.canonical_a,
                    comparison.confidence,
                ),
            )
        )
    return MarriageMatrixSection(
        key="useful_god",
        title="Ngũ Hành và Dụng/Hỷ thần",
        description="Đối chiếu nhu cầu của từng lá số với lượng Ngũ Hành thực có ở người còn lại.",
        rows=tuple(rows),
    )


def _directional_element_row(
    key: str,
    label: str,
    assessment: DirectionalAssessment,
    provider: MarriageCanonicalSnapshot,
    receiver: MarriageCanonicalSnapshot,
    confidence: float,
) -> MarriageMatrixRow:
    provider_text = _provider_elements(provider, assessment)
    receiver_text = _useful_god_text(receiver)
    if assessment.subject is RelationshipSubject.A_TO_B:
        value_a, value_b = provider_text, receiver_text
    else:
        value_a, value_b = receiver_text, provider_text
    provided = _named_values(assessment.provided)
    activated = _named_values(assessment.activated_unfavorable)
    if assessment.state is DirectionalAssessmentState.SUPPORT:
        relationship = f"Bổ đúng nhu cầu: {provided or 'có yếu tố hỗ trợ'}."
        status = "supportive"
    elif assessment.state is DirectionalAssessmentState.PRESSURE:
        relationship = f"Kích hoạt hành bất lợi: {activated or 'có yếu tố gây áp lực'}."
        status = "pressured"
    elif assessment.state is DirectionalAssessmentState.MIXED:
        relationship = f"Có bổ trợ ({provided or 'có'}) nhưng đồng thời kích hoạt bất lợi ({activated or 'có'})."
        status = "mixed"
    elif assessment.state is DirectionalAssessmentState.NEUTRAL:
        relationship = "Chưa thấy phần bù trừ nổi trội theo dữ liệu hiện có."
        status = "balanced"
    else:
        relationship = "Chưa đủ dữ liệu để đối chiếu theo chiều này."
        status = "unavailable"
    return MarriageMatrixRow(
        key=key,
        label=label,
        value_a=value_a,
        value_b=value_b,
        relationship=relationship,
        status=status,
        confidence=confidence,
        basis="Dụng thần, Hỷ thần và Kỵ thần đã xuất bản được đối chiếu với phân bố Ngũ Hành của người còn lại.",
        available=assessment.state is not DirectionalAssessmentState.INSUFFICIENT,
    )


def _provider_elements(snapshot: MarriageCanonicalSnapshot, assessment: DirectionalAssessment) -> str:
    relevant = tuple(dict.fromkeys((*assessment.provided, *assessment.activated_unfavorable)))
    if not relevant:
        return "Chưa có hành đối ứng nổi trội"
    parts: list[str] = []
    for value in relevant:
        element = _ELEMENT_BY_VALUE.get(value)
        if element is None:
            parts.append(value)
            continue
        amount = snapshot.five_elements.distribution.get(element, 0.0)
        parts.append(f"{_ELEMENT_LABEL[element]} {amount:g}")
    return "Có: " + ", ".join(parts)


def _useful_god_text(snapshot: MarriageCanonicalSnapshot) -> str:
    useful = _refs_text(snapshot.useful_god.useful)
    favorable = _refs_text(snapshot.useful_god.favorable)
    unfavorable = _refs_text(snapshot.useful_god.unfavorable)
    parts = [f"Dụng: {useful or 'chưa rõ'}", f"Hỷ: {favorable or 'chưa rõ'}"]
    if unfavorable:
        parts.append(f"Kỵ: {unfavorable}")
    return "; ".join(parts)


def _refs_text(items: list | None) -> str:
    values: list[str] = []
    for item in items or []:
        if item.element is not None:
            values.append(_ELEMENT_LABEL[item.element])
        elif item.stem:
            values.append(item.stem)
    return ", ".join(dict.fromkeys(values))


def _named_values(values: tuple[str, ...]) -> str:
    return ", ".join(
        _ELEMENT_LABEL.get(_ELEMENT_BY_VALUE.get(value), value) for value in values
    )


def _cung_phi_section(result: MarriageDecisionResult) -> MarriageMatrixSection:
    rows: list[MarriageMatrixRow] = []
    feng_a = result.canonical_a.feng_shui
    feng_b = result.canonical_b.feng_shui
    rows.append(
        _cung_row(
            "personal",
            "Cung Phi bản mệnh",
            feng_a.cung_phi if feng_a else None,
            feng_b.cung_phi if feng_b else None,
            result.confidence.overall,
            "Mệnh quái cá nhân theo năm sinh và giới tính; tra ma trận Du Niên 8×8.",
        )
    )
    for slot in ("year", "month", "day", "hour"):
        pillar_a = getattr(result.canonical_a.pillars, slot)
        pillar_b = getattr(result.canonical_b.pillars, slot)
        rows.append(
            _cung_row(
                slot,
                f"Cung Phi trụ {_PILLAR_LABEL[slot].lower()}",
                pillar_a.cung_phi if pillar_a else None,
                pillar_b.cung_phi if pillar_b else None,
                result.confidence.overall,
                f"Cung Phi của Can Chi trụ {_PILLAR_LABEL[slot].lower()}; tra ma trận Du Niên 8×8.",
            )
        )
    return MarriageMatrixSection(
        key="cung_phi",
        title="Cung Phi hai lá số",
        description="Ghép từng cặp cung theo cùng trụ. Kết quả là chỉ báo phụ và được giới hạn ảnh hưởng lên điểm tổng.",
        rows=tuple(rows),
    )


def _cung_row(
    key: str,
    label: str,
    value_a: str | None,
    value_b: str | None,
    confidence: float,
    basis: str,
) -> MarriageMatrixRow:
    if not value_a or not value_b:
        return MarriageMatrixRow(
            key=key,
            label=label,
            value_a=value_a or "Không có dữ liệu",
            value_b=value_b or "Không có dữ liệu",
            relationship="Không tính hàng này vì thiếu dữ liệu.",
            status="unavailable",
            confidence=0.0,
            basis=basis,
            available=False,
        )
    relation = lookup(value_a, value_b)
    if relation is None:
        return MarriageMatrixRow(
            key=key,
            label=label,
            value_a=value_a,
            value_b=value_b,
            relationship="Cặp cung chưa có trong bảng chuẩn.",
            status="unavailable",
            confidence=0.0,
            basis=basis,
            available=False,
        )
    return MarriageMatrixRow(
        key=key,
        label=label,
        value_a=value_a,
        value_b=value_b,
        relationship=f"{relation.relationship_label}: {relation.customer_summary}",
        status="supportive" if relation.relationship_id in FAVORABLE_IDS else "pressured",
        confidence=confidence,
        basis=basis,
        score_effect=_CUNG_EFFECT.get(relation.relationship_id),
    )


def _structure_section(result: MarriageDecisionResult) -> MarriageMatrixSection:
    rows = [_day_master_row(result)]
    rows.extend(_stem_branch_rows(result))
    rows.extend(_ten_god_rows(result))
    rows.append(_pattern_row(result))
    rows.append(_shen_sha_row(result))
    return MarriageMatrixSection(
        key="structure",
        title="Nhật Chủ và cấu trúc Bát Tự",
        description="Tách riêng quan hệ Nhật Chủ, Thiên Can–Địa Chi, Thập Thần, Mệnh Cục và Thần Sát để thấy yếu tố nào thực sự tạo hỗ trợ hay áp lực.",
        rows=tuple(rows),
    )


def _day_master_row(result: MarriageDecisionResult) -> MarriageMatrixRow:
    a = result.canonical_a.day_master
    b = result.canonical_b.day_master
    opposite = a.yin_yang is not b.yin_yang
    if a.element is b.element:
        relationship = "Đồng hành Ngũ Hành; khác âm dương tạo độ bổ sung." if opposite else "Đồng hành Ngũ Hành, dễ tương đồng cách phản ứng."
        status, effect = "supportive", 2.0 if opposite else 1.0
    elif _GENERATES[a.element] is b.element or _GENERATES[b.element] is a.element:
        relationship = "Hai Nhật Chủ nằm trong quan hệ tương sinh."
        status, effect = "supportive", 4.0 if opposite else 3.0
    elif _CONTROLS[a.element] is b.element or _CONTROLS[b.element] is a.element:
        relationship = "Hai Nhật Chủ nằm trong quan hệ tương khắc, cần xem thêm yếu tố cứu giải."
        status, effect = "pressured", -3.0 if opposite else -4.0
    else:
        relationship = "Quan hệ Nhật Chủ trung tính."
        status, effect = "balanced", 0.0
    return MarriageMatrixRow(
        key="day_master",
        label="Nhật Chủ",
        value_a=f"{a.stem} · {_YIN_YANG_LABEL[a.yin_yang]} {_ELEMENT_LABEL[a.element]}",
        value_b=f"{b.stem} · {_YIN_YANG_LABEL[b.yin_yang]} {_ELEMENT_LABEL[b.element]}",
        relationship=relationship,
        status=status,
        confidence=result.comparison.stem_branch.confidence if result.comparison else result.confidence.overall,
        basis="So sánh Ngũ Hành sinh–khắc và âm dương của hai Nhật Chủ.",
        score_effect=effect,
    )


def _stem_branch_rows(result: MarriageDecisionResult) -> list[MarriageMatrixRow]:
    if result.comparison is None:
        return [_unavailable("stem_branch", "Thiên Can – Địa Chi")]
    facts = [item for item in result.comparison.facts if item.domain is MarriageDomain.STEM_BRANCH]
    rows: list[MarriageMatrixRow] = []
    for index, fact in enumerate(facts):
        relation_type = fact.slots.get("relation_type", "")
        relation_label = _RELATION_LABEL.get(relation_type, "Quan hệ Can Chi")
        slot_a = _PILLAR_LABEL.get(fact.slots.get("slot_a", ""), "")
        slot_b = _PILLAR_LABEL.get(fact.slots.get("slot_b", ""), "")
        if fact.kind is ComparisonFactKind.SUPPORT:
            status, conclusion = "supportive", "Tạo liên kết hoặc điểm đồng thuận."
        elif fact.kind is ComparisonFactKind.RESCUE:
            status, conclusion = "balanced", "Có yếu tố cứu giải làm giảm áp lực."
        else:
            status, conclusion = "pressured", "Tạo ma sát; cần đọc cùng yếu tố cứu giải."
        rows.append(
            MarriageMatrixRow(
                key=f"stem_branch_{index + 1}",
                label=f"{relation_label} · {slot_a}–{slot_b}".rstrip(" ·–"),
                value_a=fact.slots.get("can_chi_a", "") or "Theo trụ đã nêu",
                value_b=fact.slots.get("can_chi_b", "") or "Theo trụ đã nêu",
                relationship=conclusion,
                status=status,
                confidence=fact.confidence,
                basis="Quan hệ Can Chi liên lá số đã được bộ máy bằng chứng xác định.",
            )
        )
    return rows or [_unavailable("stem_branch", "Thiên Can – Địa Chi")]


def _ten_god_rows(result: MarriageDecisionResult) -> list[MarriageMatrixRow]:
    comparison = result.comparison.ten_gods if result.comparison else None
    if comparison is None:
        return [_unavailable("ten_gods", "Thập Thần bổ trợ")]
    return [
        _directional_role_row("ten_gods_a_to_b", "Vai trò Nữ → Nam", comparison.a_to_b, comparison.confidence),
        _directional_role_row("ten_gods_b_to_a", "Vai trò Nam → Nữ", comparison.b_to_a, comparison.confidence),
    ]


def _directional_role_row(
    key: str,
    label: str,
    assessment: DirectionalAssessment,
    confidence: float,
) -> MarriageMatrixRow:
    needed = ", ".join(assessment.needed) or "Chưa có nhu cầu vai trò nổi trội"
    provided = ", ".join(assessment.provided) or "Chưa thấy vai trò bù trừ"
    pressure = ", ".join(assessment.activated_unfavorable)
    if assessment.subject is RelationshipSubject.A_TO_B:
        value_a, value_b = f"Có: {provided}", f"Cần: {needed}"
    else:
        value_a, value_b = f"Cần: {needed}", f"Có: {provided}"
    status = {
        DirectionalAssessmentState.SUPPORT: "supportive",
        DirectionalAssessmentState.PRESSURE: "pressured",
        DirectionalAssessmentState.MIXED: "mixed",
        DirectionalAssessmentState.NEUTRAL: "balanced",
        DirectionalAssessmentState.INSUFFICIENT: "unavailable",
    }[assessment.state]
    relationship = "Vai trò có khả năng bổ trợ cho nhau."
    if pressure:
        relationship = f"Có áp lực vai trò: {pressure}." if not assessment.provided else f"Vừa bổ trợ vừa có áp lực vai trò: {pressure}."
    elif assessment.state in {DirectionalAssessmentState.NEUTRAL, DirectionalAssessmentState.INSUFFICIENT}:
        relationship = "Chưa có tín hiệu vai trò đủ mạnh để kết luận."
    return MarriageMatrixRow(
        key=key,
        label=label,
        value_a=value_a,
        value_b=value_b,
        relationship=relationship,
        status=status,
        confidence=confidence,
        basis="Đối chiếu các vai trò Thập Thần cần thiết với vai trò hiện diện ở người còn lại.",
        available=assessment.state is not DirectionalAssessmentState.INSUFFICIENT,
    )


def _pattern_row(result: MarriageDecisionResult) -> MarriageMatrixRow:
    a = result.canonical_a.pattern
    b = result.canonical_b.pattern
    return MarriageMatrixRow(
        key="pattern",
        label="Mệnh Cục",
        value_a=a.pattern_name or a.pattern_id or "Chưa xác định",
        value_b=b.pattern_name or b.pattern_id or "Chưa xác định",
        relationship="Dùng để hiểu bối cảnh vận hành của mỗi người; giống hay khác không tự động đồng nghĩa hợp hay khắc.",
        status="reference",
        confidence=min(value for value in (a.confidence, b.confidence, 1.0) if value is not None),
        basis="Mệnh Cục là lớp bối cảnh, không được tự quy đổi thành điểm tốt/xấu.",
        available=bool(a.pattern_name or a.pattern_id) and bool(b.pattern_name or b.pattern_id),
    )


def _shen_sha_row(result: MarriageDecisionResult) -> MarriageMatrixRow:
    names_a = ", ".join(item.name for item in (result.canonical_a.shen_sha.items if result.canonical_a.shen_sha else []))
    names_b = ", ".join(item.name for item in (result.canonical_b.shen_sha.items if result.canonical_b.shen_sha else []))
    available = bool(names_a or names_b)
    return MarriageMatrixRow(
        key="shen_sha",
        label="Thần Sát",
        value_a=names_a or "Không có dữ liệu",
        value_b=names_b or "Không có dữ liệu",
        relationship="Chỉ dùng làm tín hiệu phụ để bổ sung ngữ cảnh, không quyết định độ hợp.",
        status="reference" if available else "unavailable",
        confidence=0.4 if available else 0.0,
        basis="Danh sách Thần Sát từ hai lá số; không cộng điểm lõi độc lập.",
        available=available,
    )


def _life_section(result: MarriageDecisionResult) -> MarriageMatrixSection:
    comparison = result.comparison
    if comparison is None:
        rows = (_unavailable("life", "Đời sống sau kết hôn"),)
    else:
        rows = (
            _life_row(
                "interaction",
                "Tính cách và giao tiếp",
                comparison.interaction,
                _roles_text(result.canonical_a),
                _roles_text(result.canonical_b),
                "Suy ra từ các quan hệ Can Chi và vai trò Thập Thần đã có bằng chứng.",
            ),
            _life_row(
                "family",
                "Phối hợp gia đình",
                comparison.family,
                _pattern_strength_text(result.canonical_a),
                _pattern_strength_text(result.canonical_b),
                "Đối chiếu Mệnh Cục, độ mạnh thân và các tín hiệu trách nhiệm/gia đạo.",
            ),
            _life_row(
                "finance",
                "Tài vận sau kết hôn",
                comparison.finance,
                _roles_text(result.canonical_a),
                _roles_text(result.canonical_b),
                "Đánh giá khả năng phối hợp vai trò tài chính; không dự đoán số tiền hoặc mức giàu nghèo.",
            ),
            _life_row(
                "children",
                "Phối hợp nuôi dạy con",
                comparison.children,
                "Dữ liệu vai trò cha/mẹ chưa đủ",
                "Dữ liệu vai trò cha/mẹ chưa đủ",
                "Chỉ kết luận khi có bằng chứng cấu trúc chuyên biệt; thiếu dữ liệu không được coi là bất lợi sinh sản.",
            ),
            _life_row(
                "luck",
                "Nhịp thời vận chung",
                comparison.luck,
                _luck_text(result.canonical_a),
                _luck_text(result.canonical_b),
                "So sánh đại vận hiện tại; thời vận chỉ điều chỉnh, không đảo ngược nền tảng lá số.",
            ),
        )
    return MarriageMatrixSection(
        key="married_life",
        title="Đời sống sau kết hôn",
        description="Tổng hợp các miền ứng dụng từ bằng chứng cấu trúc; không biến chúng thành lời tiên đoán sự kiện chắc chắn.",
        rows=rows,
    )


def _life_row(
    key: str,
    label: str,
    comparison: MarriageDomainComparison,
    value_a: str,
    value_b: str,
    basis: str,
) -> MarriageMatrixRow:
    state = comparison.mutual_state
    if not comparison.available or state == "INSUFFICIENT":
        status = "unavailable"
        relationship = "Chưa đủ căn cứ chuyên biệt để kết luận; hàng này không tạo điểm phạt."
    elif state in {"MUTUAL_SUPPORT", "A_SUPPORTS_B", "B_SUPPORTS_A"}:
        status = "supportive"
        relationship = "Các tín hiệu hiện có nghiêng về khả năng phối hợp và nâng đỡ."
    elif state in {"MUTUAL_PRESSURE"}:
        status = "pressured"
        relationship = "Có áp lực hai chiều cần được quản lý bằng thỏa thuận rõ ràng."
    elif state in {"MIXED_SUPPORT_PRESSURE", "ASYMMETRIC_SUPPORT"}:
        status = "mixed"
        relationship = "Có cả phần hỗ trợ và phần lệch vai trò cần điều chỉnh."
    else:
        status = "balanced"
        relationship = "Tín hiệu hiện tại ở mức cân bằng, chưa có xu hướng trội."
    return MarriageMatrixRow(
        key=key,
        label=label,
        value_a=value_a,
        value_b=value_b,
        relationship=relationship,
        status=status,
        confidence=comparison.confidence,
        basis=basis,
        available=comparison.available,
    )


def _roles_text(snapshot: MarriageCanonicalSnapshot) -> str:
    values = [*(snapshot.ten_gods.dominant_roles or [])]
    values.extend(item.name for item in (snapshot.ten_gods.visible or []))
    unique = list(dict.fromkeys(value for value in values if value))
    return "Vai trò nổi: " + ", ".join(unique[:4]) if unique else "Chưa có vai trò nổi trội"


def _pattern_strength_text(snapshot: MarriageCanonicalSnapshot) -> str:
    pattern = snapshot.pattern.pattern_name or snapshot.pattern.pattern_id or "chưa rõ"
    return f"Mệnh Cục: {pattern}; thân: {snapshot.strength.classification}"


def _luck_text(snapshot: MarriageCanonicalSnapshot) -> str:
    cycle = snapshot.luck.current_cycle if snapshot.luck else None
    if cycle is None:
        return "Chưa có đại vận hiện tại"
    return f"{cycle.can_chi} ({cycle.start_year}–{cycle.end_year})"


def _unavailable(key: str, label: str) -> MarriageMatrixRow:
    return MarriageMatrixRow(
        key=key,
        label=label,
        value_a="Không có dữ liệu",
        value_b="Không có dữ liệu",
        relationship="Chưa đủ dữ liệu để đối chiếu.",
        status="unavailable",
        confidence=0.0,
        basis="Hàng này không được đưa vào kết luận khi thiếu dữ liệu.",
        available=False,
    )

"""Customer presentation mapping for Ten Gods. No new analytical conclusions."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import (
    EvaluationStatus,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodStructuralRole,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.constants import (
    CONDITION_UNRESOLVED_DEPENDENCY,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.helpers import ACTIVE_STATES
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    TenGodCombinationCollection,
    TenGodCombinationResult,
)
from engines.detailed_interpretation_engine.ten_gods.constants import GOD_ID_TO_LABEL
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import (
    EcosystemRoleAssignment,
    TenGodEcosystemResult,
)
from engines.detailed_interpretation_engine.ten_gods.models import (
    TenGodInterpretationCollection,
    TenGodInterpretationResult,
)

UNRESOLVED_COPY = "Chưa đủ dữ liệu để kết luận chi tiết"

STATUS_LABELS: dict[str, str] = {
    TenGodPresenceState.ABSENT.value: "Không hiện rõ",
    TenGodPresenceState.HIDDEN_ONLY.value: "Ẩn",
    TenGodPresenceState.UNRESOLVED.value: UNRESOLVED_COPY,
}

STRENGTH_STATUS: dict[str, str] = {
    TenGodEffectiveStrength.VERY_WEAK.value: "Yếu",
    TenGodEffectiveStrength.WEAK.value: "Yếu",
    TenGodEffectiveStrength.MODERATE.value: "Vừa",
    TenGodEffectiveStrength.STRONG.value: "Mạnh",
    TenGodEffectiveStrength.VERY_STRONG.value: "Mạnh",
}

ROLE_LABELS: dict[str, str] = {
    TenGodStructuralRole.PRIMARY_PATTERN.value: "Primary",
    TenGodStructuralRole.SECONDARY_PATTERN.value: "Support",
    TenGodStructuralRole.PATTERN_SUPPORT.value: "Support",
    TenGodStructuralRole.CAPACITY_SUPPORT.value: "Support",
    TenGodStructuralRole.PATTERN_GENERATOR.value: "Support",
    TenGodStructuralRole.RESCUE_SOURCE.value: "Support",
    TenGodStructuralRole.CAPACITY_PRESSURE.value: "Pressure",
    TenGodStructuralRole.PATTERN_CONTROLLER.value: "Pressure",
    TenGodStructuralRole.DAMAGE_SOURCE.value: "Pressure",
    TenGodStructuralRole.NEUTRAL.value: "Neutral",
}

EXPRESSION_LABELS: dict[str, str] = {
    "self_reliance": "Tự lực",
    "persistence": "Bền bỉ",
    "independence": "Độc lập",
    "peer_equality": "Quan hệ ngang vai",
    "execution_capacity": "Năng lực thực thi",
    "carrying_capacity_support": "Nâng sức Nhật Chủ",
    "competitiveness": "Cạnh tranh",
    "boldness": "Quyết đoán mở cửa",
    "initiative": "Chủ động",
    "peer_mobilization": "Huy động đồng vai",
    "risk_tolerance": "Chịu rủi ngắn",
    "entrepreneurial_drive": "Động lực mở nguồn",
    "production": "Sản xuất",
    "stable_expression": "Biểu đạt ổn",
    "skill": "Tay nghề",
    "creativity": "Sáng tạo có khung",
    "product_creation": "Tạo sản phẩm",
    "innovation": "Đổi cách làm",
    "critical_thinking": "Phản biện",
    "expression": "Biểu đạt",
    "commercial_creativity": "Sáng tạo thương mại",
    "public_visibility": "Lộ diện công việc",
    "opportunity_recognition": "Nhìn cửa lệch",
    "flexible_resource_use": "Dùng nguồn linh hoạt",
    "commercial_activity": "Hoạt động thương mại",
    "expansion": "Mở rộng",
    "entrepreneurship": "Mở nguồn riêng",
    "disciplined_resource_management": "Giữ sổ có hạn",
    "stable_income_orientation": "Nguồn có phép",
    "accumulation": "Tích lũy",
    "financial_responsibility": "Trách nhiệm nguồn",
    "operational_management": "Vận hành",
    "pressure_tolerance": "Chịu sức ép",
    "decisiveness": "Quyết nhanh",
    "command": "Chỉ huy tình huống",
    "leadership": "Cầm việc",
    "high_responsibility_execution": "Gánh việc nặng",
    "responsibility": "Trách nhiệm",
    "organizational_discipline": "Kỷ luật tổ chức",
    "formal_structure": "Khung phép",
    "management": "Quản trị",
    "institutional_fit": "Hợp môi trường có chuẩn",
    "specialized_learning": "Học chuyên biệt",
    "unconventional_knowledge": "Tri thức lệch khung",
    "research": "Nghiên cứu",
    "technical_specialization": "Chuyên môn kỹ thuật",
    "independent_cognition": "Tự xử lý tri thức",
    "structured_knowledge": "Tri thức có khung",
    "learning": "Học có hệ",
    "support": "Nâng đỡ",
    "protection": "Bảo vệ cấu trúc",
    "mediation": "Trung hòa xung đột",
    "excessive_self_focus": "Tự giữ phần quá mức",
    "competition": "So phần",
    "resistance_to_control": "Khó nhận khung",
    "resource_division": "Chia nguồn",
    "financial_competition": "Tranh nguồn",
    "resource_leakage": "Rò nguồn",
    "impulsive_expansion": "Mở cửa gấp",
    "excessive_rivalry": "Cạnh tranh quá mức",
    "excessive_drain": "Rút sức Nhật Chủ",
    "over_comfort": "Dễ thỏa",
    "weakened_discipline": "Lỏng kỷ luật",
    "authority_conflict": "Căng với khung phép",
    "excessive_criticism": "Phản biện quá mức",
    "instability": "Mất ổn",
    "over_expression": "Lộ quá mức",
    "volatility": "Nguồn dao động",
    "opportunism_without_retention": "Cửa lệch khó giữ",
    "overextension": "Ôm quá nền",
    "material_pressure": "Áp lực nguồn",
    "excessive_material_responsibility": "Nghĩa vụ nguồn quá nền",
    "rigidity": "Cứng khung",
    "excessive_pressure": "Sức ép quá mức",
    "conflict": "Xung đột",
    "control_burden": "Gánh kiểm",
    "overconstraint": "Khung siết",
    "pressure": "Áp lực vai",
    "over_isolation": "Thu mình",
    "excessive_internalization": "Ngầm quá mức",
    "output_suppression": "Kìm đầu ra",
    "over_support": "Nâng đỡ quá mức",
    "reduced_output": "Giảm đầu ra",
    "dependence": "Dựa khung",
    "mc01_reference_not_bound": "Chưa gắn Mệnh Cục",
    "hour_pillar_incomplete": "Giờ sinh chưa đủ",
    "pattern_context_unresolved": "Cách cục chưa đủ để chốt vai",
    "useful_god_unresolved": "Dụng Thần chưa đủ để chốt",
    "convert_skill_to_value": "Kỹ năng có đường chuyển thành giá trị.",
    "stable_value_creation": "Đường tạo giá trị tương đối ổn.",
    "innovation_monetization": "Sáng tạo có đường ra giá trị.",
    "entrepreneurship": "Có đường mở nguồn riêng.",
    "resources_support_responsibility": "Nguồn đang đỡ trách nhiệm.",
    "commercial_results_support_authority": "Kết quả thương mại đang đỡ khung phép.",
    "responsibility_creates_support": "Trách nhiệm đang sinh chỗ dựa tri thức.",
    "formal_structure_becomes_sustainable": "Khung phép có đường bền.",
    "institutional_continuity": "Dòng Tài → Quan → Ấn đang nối.",
    "structured_career_flow": "Có dòng nghề có khung.",
    "pressure_transformed_into_capability": "Áp lực có đường chuyển thành năng lực.",
    "disciplined_learning": "Học dưới sức ép có khung.",
    "financial_opportunity": "Cửa nguồn đang hiện.",
    "high_responsibility_environment": "Môi trường trách nhiệm nặng.",
    "capacity_can_carry_wealth": "Nền Nhật Chủ đủ để gánh Tài.",
    "discipline_organizes_self_force": "Khung phép đang tổ chức lực tự thân.",
    "output_releases_self_force": "Đầu ra đang xả lực tự thân.",
    "resource_restores_capacity": "Ấn đang đỡ nền Nhật Chủ.",
    "peer_increases_carrying_capacity": "Tỷ Kiếp đang nâng sức gánh.",
    "learning": "Học có bề dày.",
    "technical_depth": "Chuyên môn có độ sâu.",
    "output_drains_weak_day_master": "Đầu ra có thể rút nền Nhật Chủ.",
    "retention_weaker_than_creation": "Giữ nguồn yếu hơn đường tạo.",
    "authority_conflict_elsewhere": "Căng với khung phép có thể nằm chỗ khác.",
    "wealth_and_officer_pressure_weak_day_master": "Tài và Quan cùng đè nền yếu.",
    "resource_may_block_output": "Ấn dày có thể kìm đầu ra.",
    "intermediate_link_limits_flow": "Mắt xích giữa đang hạn chế dòng.",
    "pressure_before_transformation": "Áp lực có thể tới trước khi chuyển hóa.",
    "friction_with_formal_authority": "Ma sát với khung phép.",
    "expression_versus_rules": "Biểu đạt căng với luật.",
    "over_analysis": "Phân tích quá mức.",
    "resource_competition": "Tranh nguồn.",
    "difficult_retention": "Khó giữ nguồn.",
    "mixed_authority_style": "Hai kiểu quyền hạn cùng hiện.",
    "carrying_capacity_strained": "Nền gánh đang căng.",
    "pressure_exceeds_capacity": "Sức ép vượt nền.",
    "unfavorable_if_wealth_is_avoided": "Khó dùng nếu Tài đang là kỵ.",
    "authority_unusable_if_damaged": "Khó dùng Quan nếu Quan đã tổn.",
    "under_discipline_if_officer_weak": "Dễ lỏng kỷ nếu Quan yếu.",
    "help_blocked_if_resource_is_avoided": "Khó đỡ nếu Ấn đang là kỵ.",
    "capacity_support_with_wealth_competition": "Đỡ nền nhưng có thể tranh nguồn.",
    "unresolved_dependency": "Chưa đủ dữ liệu để chốt",
    "residual_co_presence": "Chỉ cùng hiện phần tàng, chưa thành quan hệ.",
    "mediated_reach": "Có trung gian, không tính xung trực tiếp.",
    "day_master_band_mismatch": "Không khớp nền Nhật Chủ cho quan hệ này.",
    "no_active_chain": "Chưa có chuỗi đang hoạt động.",
    "driver_unresolved_without_pattern": "Chưa đủ Cách cục để chốt động lực.",
}


def _status_label(item: TenGodInterpretationResult) -> str:
    if item.state is EvaluationStatus.UNRESOLVED:
        return UNRESOLVED_COPY
    if item.presence_state is TenGodPresenceState.ABSENT:
        return STATUS_LABELS[TenGodPresenceState.ABSENT.value]
    if item.presence_state is TenGodPresenceState.HIDDEN_ONLY:
        return STATUS_LABELS[TenGodPresenceState.HIDDEN_ONLY.value]
    return STRENGTH_STATUS.get(item.effective_strength.value, STATUS_LABELS.get(item.presence_state.value, UNRESOLVED_COPY))


def _role_label(item: TenGodInterpretationResult) -> str:
    if item.structural_role is TenGodStructuralRole.UNRESOLVED:
        return ""
    return ROLE_LABELS.get(item.structural_role.value, "")


def _map_codes(codes: tuple[str, ...]) -> list[str]:
    labels: list[str] = []
    for code in codes:
        label = EXPRESSION_LABELS.get(code, "")
        if label and label not in labels:
            labels.append(label)
    return labels


def present_ten_god(item: TenGodInterpretationResult) -> dict[str, Any]:
    """Customer-safe card fields. No IDs, traces, or JSON dumps."""
    unresolved = item.state is EvaluationStatus.UNRESOLVED or (
        item.presence_state is TenGodPresenceState.UNRESOLVED
    )
    return {
        "name": GOD_ID_TO_LABEL.get(item.ten_god_id, ""),
        "status_label": _status_label(item),
        "role_label": "" if unresolved else _role_label(item),
        "positives": [] if unresolved else _map_codes(item.positive_expressions)[:3],
        "risks": [] if unresolved else _map_codes(item.risk_expressions)[:2],
        "conditions": [] if unresolved else _map_codes(item.conditions),
        "unresolved": unresolved,
        "fallback": UNRESOLVED_COPY if unresolved else "",
    }


def present_ten_gods_customer(collection: TenGodInterpretationCollection) -> dict[str, Any]:
    """Customer projection of the natal Ten God collection."""
    return {
        "state": collection.state.value,
        "items": [present_ten_god(item) for item in collection.items],
    }


COMBINATION_NAMES: dict[str, str] = {
    "shi_shen_generates_wealth": "Thực Thần → Tài",
    "shang_guan_generates_wealth": "Thương Quan → Tài",
    "wealth_generates_officer": "Tài → Quan",
    "officer_generates_resource": "Quan → Ấn",
    "wealth_officer_resource_chain": "Tài → Quan → Ấn",
    "killer_resource_day_master_chain": "Sát → Ấn → Thân",
    "hurting_officer_meets_officer": "Thương Quan kiến Quan",
    "owl_robs_food_combination": "Kiêu Thần đoạt Thực",
    "peer_competes_wealth": "Tỷ Kiếp đoạt Tài",
    "officer_killer_mixed": "Quan Sát hỗn tạp",
    "wealth_exceeds_day_master": "Tài nhiều Thân nhược",
    "killer_exceeds_day_master": "Sát mạnh Thân nhược",
    "resource_strong_day_master_strong": "Ấn vượng Thân cường",
    "strong_day_master_uses_wealth": "Thân vượng dụng Tài",
    "strong_day_master_uses_officer": "Thân vượng dụng Quan",
    "strong_day_master_uses_output": "Thân vượng dụng Thực/Thương",
    "weak_day_master_uses_resource": "Thân nhược dụng Ấn",
    "weak_day_master_uses_peer": "Thân nhược dụng Tỷ/Kiếp",
}

COMBINATION_STATE_LABELS: dict[str, str] = {
    "confirmed": "Đang hoạt động",
    "conditional": "Có điều kiện",
    "weak": "Yếu",
    "broken": "Chưa hoàn chỉnh",
    "unresolved": "Chưa đủ dữ liệu để chốt",
}

SUBJECT_LABELS: dict[str, str] = {
    **GOD_ID_TO_LABEL,
    "day_master": "Nhật Chủ",
    "resource": "Ấn",
    "peer": "Tỷ Kiếp",
    "output": "Thực Thương",
    "wealth": "Tài",
    "authority": "Quan Sát",
    "officer": "Quan Sát",
    "companion": "Tỷ Kiếp",
}

ROLE_CUSTOMER_LABELS: dict[str, str] = {
    "driver": "Động lực chính",
    "supporting": "Hỗ trợ",
    "bottleneck": "Điểm nghẽn",
    "blocked": "Lực bị chặn",
    "suppressed": "Lực bị kìm",
    "excessive": "Lực dư",
    "deficient": "Lực thiếu",
    "missing": "Không hiện chức năng",
    "balancer": "Lực cân",
    "neutral": "Trung tính",
}

FALLBACK_INSUFFICIENT = "Chưa đủ dữ liệu để chốt"


def _customer_subject(subject: str) -> str:
    return SUBJECT_LABELS.get(subject, "")


def _meaningful_combination(item: TenGodCombinationResult) -> bool:
    if item.source_combination_id:
        return False
    if item.state in ACTIVE_STATES:
        return True
    if item.state.value in {"broken", "unresolved"} and item.participants:
        return True
    return False


def present_combination(item: TenGodCombinationResult) -> dict[str, Any]:
    """Customer-safe combination row. No IDs or traces."""
    unresolved = item.state.value == "unresolved" or CONDITION_UNRESOLVED_DEPENDENCY in item.conditions
    mechanism = ""
    if item.positive_expressions:
        mechanism = EXPRESSION_LABELS.get(item.positive_expressions[0], "")
    elif item.state.value == "broken":
        mechanism = "Chuỗi hiện chưa hoàn chỉnh."
    elif unresolved:
        mechanism = FALLBACK_INSUFFICIENT
    condition = ""
    if item.conditions:
        condition = EXPRESSION_LABELS.get(item.conditions[0], "")
    return {
        "name": COMBINATION_NAMES.get(item.combination_id, ""),
        "state_label": COMBINATION_STATE_LABELS.get(item.state.value, FALLBACK_INSUFFICIENT),
        "mechanism": mechanism,
        "condition": condition,
        "unresolved": unresolved,
        "fallback": FALLBACK_INSUFFICIENT if unresolved else "",
    }


def present_combinations_customer(collection: TenGodCombinationCollection) -> dict[str, Any]:
    """Customer projection of active or meaningful conditional combinations."""
    items = [present_combination(item) for item in collection.items if _meaningful_combination(item)]
    return {
        "state": collection.state.value,
        "items": items,
    }


def _present_role(assignment: EcosystemRoleAssignment) -> dict[str, Any]:
    unresolved = assignment.state.value in {"unresolved", "not_evaluated"}
    missing = assignment.state.value == "not_applicable" or not assignment.subject
    if unresolved:
        label = FALLBACK_INSUFFICIENT
    elif missing:
        label = "Không áp dụng"
    else:
        label = _customer_subject(assignment.subject) or FALLBACK_INSUFFICIENT
    return {
        "label": label,
        "unresolved": unresolved,
    }


def present_ecosystem_customer(result: TenGodEcosystemResult) -> dict[str, Any]:
    """Customer projection of the Ten Gods ecosystem. No IDs or traces."""
    flow_nodes = []
    if result.flow:
        flow_nodes = [_customer_subject(node) for node in result.flow[0].nodes if _customer_subject(node)]
    flow_quality = {
        "broken": "Gãy",
        "restricted": "Bị hạn",
        "conditional": "Có điều kiện",
        "functional": "Vận hành được",
        "strong": "Mạnh",
        "excellent": "Mạnh",
        "unresolved": FALLBACK_INSUFFICIENT,
    }.get(result.flow_quality.value, FALLBACK_INSUFFICIENT)
    unresolved = result.state.value in {"unresolved", "not_evaluated"}
    return {
        "state": result.state.value,
        "unresolved": unresolved,
        "fallback": FALLBACK_INSUFFICIENT if unresolved and not result.driver.subject else "",
        "driver": _present_role(result.driver),
        "support": _present_role(result.support),
        "bottleneck": _present_role(result.bottleneck),
        "blocked": _present_role(result.blocked),
        "suppressed": _present_role(result.suppressed),
        "excessive": _present_role(result.excessive),
        "deficient": _present_role(result.deficient),
        "missing": _present_role(result.missing),
        "flow": " → ".join(flow_nodes) if flow_nodes else FALLBACK_INSUFFICIENT,
        "flow_quality": flow_quality,
        "role_labels": ROLE_CUSTOMER_LABELS,
    }

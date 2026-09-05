"""Deterministic Vietnamese catalog for Narrative Composer. No inference."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domain_interpretation.labels import (
    DIMENSION_LABELS,
    DOMAIN_TITLES,
    STATE_LABELS,
)
from engines.detailed_interpretation_engine.evidence_priority.labels import (
    ACHIEVEMENT_LABELS,
    CONDITION_LABELS,
    DAMAGE_LABELS,
    INTEGRITY_LABELS,
    WEALTH_LABELS,
)
from engines.detailed_interpretation_engine.life_optimization.labels import ACTION_LABELS, REASON_LABELS
from engines.detailed_interpretation_engine.luck_activation.labels import STATE_LABELS as LUCK_STATE_LABELS
from engines.detailed_interpretation_engine.luck_interaction.labels import SITUATION_LABELS, TYPE_LABELS

SECTION_TITLES: dict[str, str] = {
    "executive_summary": "Tóm tắt",
    "strength": "Điểm mạnh",
    "risk": "Rủi ro",
    "opportunity": "Cơ hội",
    "domain_section": "Sáu trụ cột",
    "temporal": "Vận hiện tại",
    "optimization_section": "Việc ưu tiên",
    "closing_summary": "Kết luận",
}

WHO_TEMPLATE: str = "Lá số này thuộc mệnh cục {pattern}, hạng {grade}."
WHO_UNRESOLVED: str = "Cấu trúc mệnh cục chưa đủ dữ liệu để kết luận kiểu."
INTEGRITY_TEMPLATE: str = "Tính toàn vẹn cấu trúc hiện {integrity}."
MATTERS_TEMPLATE: str = "Trọng tâm hiện tại là {label}."
PRIORITY_TEMPLATE: str = "Ưu tiên hành động: {action}."
QUALIFIED: str = "Cần đọc kèm điều kiện."
ALREADY_NOTED: str = "Đã nêu ở phần trước."
LUCK_WINDOW: str = "Đại vận hiện tại: {window}."
ANNUAL_WINDOW: str = "Năm {year} điều chỉnh biểu đạt trong khung đại vận, không đổi nền natal."
OVERLOAD_TEMPLATE: str = "{domain} đang {state}."
INTERACTION_TEMPLATE: str = "{source} {relation} {target}."
NO_EVENT: str = "Đây là biểu đạt vận, không phải dự báo sự kiện."
CLOSING_LEAD: str = "Giữ thứ tự: xử lý nút thắt trước, rồi mới mở rộng."
UNCERTAIN: str = "Phần này chưa đủ dữ liệu để kết luận."

DOMAIN_FIELD: dict[str, str] = {
    "state": "Hiện trạng",
    "driver": "Động lực",
    "bottleneck": "Điểm nghẽn",
    "opportunity": "Cơ hội",
    "caution": "Lưu ý",
    "condition": "Điều kiện",
}


def leakage_label(value: str) -> str:
    """Consumed domain leakage label. Empty when the code is unknown."""
    return DIMENSION_LABELS.get(value, "")


def domain_title(domain_id: str) -> str:
    """Consumed domain title."""
    return DOMAIN_TITLES.get(domain_id, domain_id)


def state_label(value: str) -> str:
    """Consumed domain state label."""
    return STATE_LABELS.get(value, value)


def luck_state_label(value: str) -> str:
    """Consumed luck activation label."""
    return LUCK_STATE_LABELS.get(value, value)


def integrity_label(value: str) -> str:
    """Consumed MC-01 integrity label."""
    return INTEGRITY_LABELS.get(value, value) or value


def damage_label(value: str) -> str:
    """Consumed damage label."""
    return DAMAGE_LABELS.get(value, value)


def wealth_label(value: str) -> str:
    """Consumed wealth dimension label."""
    return WEALTH_LABELS.get(value, value)


def achievement_label(value: str) -> str:
    """Consumed achievement label."""
    return ACHIEVEMENT_LABELS.get(value, value)


def condition_label(value: str) -> str:
    """Consumed condition label."""
    return CONDITION_LABELS.get(value, "")


def action_label(key: str) -> str:
    """Consumed Life Optimization action label."""
    return ACTION_LABELS.get(key, "")


def reason_label(key: str) -> str:
    """Consumed Life Optimization reason label."""
    return REASON_LABELS.get(key, "")


def situation_label(value: str) -> str:
    """Consumed luck situation label."""
    return SITUATION_LABELS.get(value, "")


def interaction_label(value: str) -> str:
    """Consumed luck interaction type label."""
    return TYPE_LABELS.get(value, "")

"""Customer labels for Luck Activation. Not DI-19 Composer."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domain_interpretation.labels import DOMAIN_TITLES
from engines.detailed_interpretation_engine.enums import ActivationState

TITLE: str = "Kích hoạt vận hiện tại"

STATE_LABELS: dict[str, str] = {
    ActivationState.DORMANT.value: "Ngủ",
    ActivationState.WEAK.value: "Yếu",
    ActivationState.MODERATE.value: "Vừa",
    ActivationState.STRONG.value: "Mạnh",
    ActivationState.PEAK.value: "Đỉnh",
    ActivationState.OVERLOADED.value: "Quá tải",
    ActivationState.BLOCKED.value: "Chưa tính được",
    ActivationState.SUPPRESSED.value: "Bị kìm",
    ActivationState.CONDITIONAL.value: "Có điều kiện",
    ActivationState.UNRESOLVED.value: "Chưa đủ dữ liệu",
}

DRIVER_LABELS: dict[str, str] = {
    "temporal_officer": "Quan vận kỳ này",
    "temporal_killer": "Sát vận kỳ này",
    "temporal_wealth": "Tài vận kỳ này",
    "temporal_output": "Thực Thương kỳ này",
    "temporal_resource": "Ấn vận kỳ này",
    "temporal_peer": "Tỷ Kiếp kỳ này",
    "temporal_useful_god": "Dụng Thần kỳ này",
    "temporal_element_support": "Ngũ hành nâng đỡ",
    "temporal_element_drain": "Ngũ hành tiết khí",
    "temporal_element_control": "Ngũ hành chế hóa",
    "not_applicable": "",
    "unresolved": "",
}

LEVEL_MARKERS: dict[str, str] = {
    "none": "",
    "low": "Nhẹ",
    "moderate": "Vừa",
    "high": "Mạnh",
    "excessive": "Quá mức",
}

BOTTLENECK_LABELS: dict[str, str] = {
    "peer_luck_pressure": "Tỷ Kiếp vận tăng áp lực",
    "officer_luck_pressure": "Quan/Sát vận tăng áp lực",
    "output_vs_officer": "Thực Thương kìm Quan",
    "resource_overload_window": "Ấn vận dễ quá tải",
    "carrying_capacity": "Sức chứa natal hạn chế biểu đạt",
    "none": "",
    "not_applicable": "",
}

DOMAIN_TITLES_ACTIVATION: dict[str, str] = {
    **DOMAIN_TITLES,
    "wealth": "Tài chính",
    "vitality": "Sức bền",
}

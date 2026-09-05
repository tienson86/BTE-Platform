"""Customer labels for Temporal Activation. Not DI-19 Composer."""

from __future__ import annotations

from engines.detailed_interpretation_engine.luck_activation.labels import (
    DOMAIN_TITLES_ACTIVATION,
    STATE_LABELS as LUCK_STATE_LABELS,
)
from engines.detailed_interpretation_engine.domain_interpretation.labels import STATE_LABELS as NATAL_STATE_LABELS

TITLE: str = "Biểu hiện lưu niên"

EXPRESSION_LABELS: dict[str, str] = {
    **LUCK_STATE_LABELS,
    "active": "Đang hiện",
    "recovering": "Được giảm áp",
    "transition": "Ổn định",
}

MODIFIER_LABELS: dict[str, str] = {
    "activate": "Kích hoạt",
    "strengthen": "Tăng lực",
    "weaken": "Giảm lực",
    "suppress": "Kìm",
    "stress": "Tăng áp",
    "recover": "Phục hồi",
    "accelerate": "Đẩy nhanh",
    "delay": "Làm chậm",
    "stabilize": "Ổn định",
    "destabilize": "Mất ổn",
    "open_condition": "Mở điều kiện",
    "block_condition": "Khóa điều kiện",
}

DRIVER_LABELS: dict[str, str] = {
    "annual_officer": "Quan lưu niên",
    "annual_killer": "Sát lưu niên",
    "annual_wealth": "Tài lưu niên",
    "annual_output": "Thực Thương lưu niên",
    "annual_resource": "Ấn lưu niên",
    "annual_peer": "Tỷ Kiếp lưu niên",
    "annual_useful_god": "Dụng Thần lưu niên",
    "annual_element_support": "Ngũ hành nâng đỡ năm này",
    "annual_element_drain": "Ngũ hành tiết khí năm này",
    "annual_element_control": "Ngũ hành chế hóa năm này",
    "annual_clash_pressure": "Xung năm này cần đọc điều kiện",
    "not_applicable": "",
    "unresolved": "",
}

BOTTLENECK_LABELS: dict[str, str] = {
    "annual_carrying_capacity": "Sức chứa năm này hạn chế biểu đạt",
    "annual_parent_overload": "Đại vận quá tải, lưu niên không gỡ hết",
    "annual_officer_pressure": "Quan/Sát năm này tăng áp lực",
    "annual_peer_pressure": "Tỷ Kiếp năm này tăng áp lực",
    "annual_output_vs_officer": "Thực Thương năm này kìm Quan",
    "none": "",
    "not_applicable": "",
}

LEVEL_MARKERS: dict[str, str] = {
    "none": "",
    "low": "Nhẹ",
    "moderate": "Vừa",
    "high": "Mạnh",
    "excessive": "Quá mức",
}

DOMAIN_TITLES: dict[str, str] = dict(DOMAIN_TITLES_ACTIVATION)
NATAL_LABELS: dict[str, str] = dict(NATAL_STATE_LABELS)

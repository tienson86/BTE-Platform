"""Canonical Vietnamese display labels for Report V1.

Internal engine codes stay in ReportInputV1. Renderers must use this table.
"""

from __future__ import annotations

GENDER_LABELS: dict[str, str] = {
    "male": "Nam",
    "female": "Nữ",
    "m": "Nam",
    "f": "Nữ",
    "nam": "Nam",
    "nu": "Nữ",
    "nữ": "Nữ",
}

STRENGTH_LABELS: dict[str, str] = {
    "strong": "Thân vượng",
    "very_strong": "Thân vượng",
    "weak": "Thân nhược",
    "very_weak": "Thân nhược",
    "balanced": "Trung hòa",
    "neutral": "Trung hòa",
}

PATTERN_STATUS_LABELS: dict[str, str] = {
    "success": "Đắc cách",
    "true": "Đắc cách",
    "failed": "Thất cách",
    "fail": "Thất cách",
    "false": "Thất cách",
    "unknown": "Chưa xác định",
}

TEMPERATURE_LABELS: dict[str, str] = {
    "hot": "Nhiệt",
    "warm": "Ôn",
    "cold": "Hàn",
    "cool": "Lương",
    "dry": "Táo",
    "humid": "Thấp",
    "damp": "Thấp",
}

SEASON_LABELS: dict[str, str] = {
    "spring": "Xuân",
    "summer": "Hạ",
    "autumn": "Thu",
    "fall": "Thu",
    "winter": "Đông",
    "xuan": "Xuân",
    "ha": "Hạ",
    "thu": "Thu",
    "dong": "Đông",
}

LUCK_DIRECTION_LABELS: dict[str, str] = {
    "forward": "Thuận",
    "reverse": "Nghịch",
    "backward": "Nghịch",
}

CONFIDENCE_LEVEL_LABELS: dict[str, str] = {
    "very_high": "Rất cao",
    "high": "Cao",
    "medium": "Trung bình",
    "moderate": "Trung bình",
    "low": "Thấp",
    "very_low": "Rất thấp",
}

BALANCING_NEED_LABELS: dict[str, str] = {
    "warming": "Cần ôn ấm",
    "cooling": "Cần làm mát",
    "balance": "Cần cân Hỏa Thủy",
}

CATEGORY_LABELS: dict[str, str] = {
    "shensha": "Thần sát",
    "shen_sha": "Thần sát",
    "god_sha": "Thần sát",
}

DOMAIN_TABLES: dict[str, dict[str, str]] = {
    "gender": GENDER_LABELS,
    "strength": STRENGTH_LABELS,
    "pattern_status": PATTERN_STATUS_LABELS,
    "temperature": TEMPERATURE_LABELS,
    "season": SEASON_LABELS,
    "luck_direction": LUCK_DIRECTION_LABELS,
    "confidence_level": CONFIDENCE_LEVEL_LABELS,
    "balancing_need": BALANCING_NEED_LABELS,
    "category": CATEGORY_LABELS,
}

GENERIC_LABELS: dict[str, str] = {}
for _table in DOMAIN_TABLES.values():
    GENERIC_LABELS.update(_table)

RUNTIME_GAP_MESSAGE = "DATA NOT PROVIDED BY RUNTIME"
EXECUTIVE_SUMMARY_MISSING = "Chưa có dữ liệu tổng hợp."
FULL_LUCK_CYCLES_GAP_NOTE = (
    "Toàn bộ đại vận (full luck cycles): DATA NOT PROVIDED BY RUNTIME"
)

"""Customer labels for Luck Interaction. Not DI-19 Composer."""

from __future__ import annotations

from engines.detailed_interpretation_engine.luck_activation.labels import DOMAIN_TITLES_ACTIVATION

TITLE: str = "Tương tác vận hiện tại"

SITUATION_LABELS: dict[str, str] = {
    "career_expansion": "Mở rộng sự nghiệp",
    "creative_expansion": "Mở rộng sáng tạo",
    "authority_consolidation": "Củng cố quyền hạn",
    "learning_phase": "Giai đoạn học",
    "resource_pressure": "Áp lực tăng trưởng",
    "relationship_stress": "Áp lực quan hệ",
    "recovery_phase": "Pha phục hồi",
    "transition_phase": "Giai đoạn chuyển",
    "balanced_growth": "Tăng trưởng cân",
    "blocked_growth": "Tăng trưởng bị kìm",
    "unresolved": "Chưa đủ dữ liệu",
    "not_applicable": "",
}

TYPE_LABELS: dict[str, str] = {
    "support": "Hỗ trợ",
    "conflict": "Xung đột",
    "trade_off": "Đánh đổi",
    "reinforcement": "Gia cố",
    "competition": "Cạnh tranh",
    "resource_shift": "Dồn nguồn lực",
    "stress_transfer": "Chuyển áp lực",
    "conditional_dependency": "Phụ thuộc điều kiện",
    "blocked_expression": "Biểu đạt bị kìm",
    "unresolved": "Chưa kết luận",
}

DOMAIN_TITLES: dict[str, str] = dict(DOMAIN_TITLES_ACTIVATION)

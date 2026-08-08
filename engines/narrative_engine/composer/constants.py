"""Sprint D2 composer constants (writing-system approved copy only)."""

from __future__ import annotations

# Approved insufficient-evidence narrative (Stabilization / Sprint B–C).
INSUFFICIENT_EVIDENCE_NARRATIVE = "Chưa đủ dữ liệu để đưa ra kết luận."

COMPONENT_TITLES: dict[str, str] = {
    "executive_summary": "Tóm tắt điều hành",
    "observation": "Quan sát",
    "reasoning": "Lý giải",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "warning": "Lưu ý",
    "conclusion": "Kết luận",
}

COMPONENT_TONES: dict[str, str] = {
    "executive_summary": "briefing",
    "observation": "neutral_factual",
    "reasoning": "explanatory",
    "impact": "empathic_concrete",
    "recommendation": "directive_supportive",
    "warning": "cautionary_calm",
    "conclusion": "settling",
}

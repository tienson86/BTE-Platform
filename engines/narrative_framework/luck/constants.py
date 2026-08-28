"""INT-02E Luck Narrative constants. Templates bind published facts only."""

from __future__ import annotations

from typing import Final, Mapping

TOPIC_ID: Final[str] = "luck"
SOURCE_PATH: Final[str] = "analysis.luck"
UNIT_SCHEMA: Final[str] = "1.0.0"

LUCK_BLOCKS: Final[tuple[str, ...]] = (
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "summary",
)

LUCK_BLOCK_TITLES: Final[Mapping[str, str]] = {
    "observation": "Quan sát",
    "reasoning": "Lý do",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "summary": "Tóm tắt",
}

IMPACT_COPY: Final[str] = (
    "Với giai đoạn vận đã công bố {stage}, nhịp hiện tại được đọc theo trục này."
)

SUPPORT_GROUP_LABEL: Final[str] = "Yếu tố hỗ trợ vận đã công bố"
RESTRAIN_GROUP_LABEL: Final[str] = "Yếu tố xung khắc vận đã công bố"
PUBLISHED_CLASS_PREFIX: Final[str] = "Giai đoạn vận đã công bố vẫn là"

EVIDENCE_FIELDS: Final[tuple[str, ...]] = (
    "current_cycle",
    "current_liunian",
    "cycle_index",
    "age",
    "reference_year",
    "timeline",
    "reasoning",
    "confidence",
    "recommendations",
)

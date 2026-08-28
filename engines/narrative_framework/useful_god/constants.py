"""INT-02C Useful God Narrative constants. Templates bind published facts only."""

from __future__ import annotations

from typing import Final, Mapping

TOPIC_ID: Final[str] = "useful_god"
SOURCE_PATH: Final[str] = "analysis.useful_god"
UNIT_SCHEMA: Final[str] = "1.0.0"

USEFUL_GOD_BLOCKS: Final[tuple[str, ...]] = (
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "summary",
)

USEFUL_GOD_BLOCK_TITLES: Final[Mapping[str, str]] = {
    "observation": "Quan sát",
    "reasoning": "Lý do",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "summary": "Tóm tắt",
}

IMPACT_COPY: Final[str] = (
    "Với Dụng thần đã công bố {useful_display}, nhịp điều chỉnh lấy hướng này làm trục."
)

SUPPORT_GROUP_LABEL: Final[str] = "Yếu tố hỗ trợ Dụng thần"
RESTRAIN_GROUP_LABEL: Final[str] = "Yếu tố kỵ với Dụng thần"
PUBLISHED_CLASS_PREFIX: Final[str] = "Dụng thần đã công bố vẫn là"

EVIDENCE_FIELDS: Final[tuple[str, ...]] = (
    "useful_god",
    "useful_display",
    "favorable_gods",
    "unfavorable_gods",
    "winning_rule_id",
    "confidence",
    "reasoning",
)

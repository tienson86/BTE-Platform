"""INT-02D Pattern Narrative constants. Templates bind published facts only."""

from __future__ import annotations

from typing import Final, Mapping

TOPIC_ID: Final[str] = "pattern"
SOURCE_PATH: Final[str] = "analysis.pattern"
UNIT_SCHEMA: Final[str] = "1.0.0"

PATTERN_BLOCKS: Final[tuple[str, ...]] = (
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "summary",
)

PATTERN_BLOCK_TITLES: Final[Mapping[str, str]] = {
    "observation": "Quan sát",
    "reasoning": "Lý do",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "summary": "Tóm tắt",
}

IMPACT_COPY: Final[str] = (
    "Với cách cục đã công bố {pattern_name}, nhịp vận hành được đọc theo trục này."
)

SUPPORT_GROUP_LABEL: Final[str] = "Yếu tố hỗ trợ cách cục"
RESTRAIN_GROUP_LABEL: Final[str] = "Yếu tố bất lợi cho cách cục"
PUBLISHED_CLASS_PREFIX: Final[str] = "Cách cục đã công bố vẫn là"

EVIDENCE_FIELDS: Final[tuple[str, ...]] = (
    "pattern_name",
    "pattern_class",
    "dieu_hau",
    "special_pattern",
    "winning_rule",
    "matched_rules",
    "reasoning",
    "confidence",
)

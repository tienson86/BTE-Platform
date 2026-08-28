"""INT-02B Strength Narrative constants. Templates bind published facts only."""

from __future__ import annotations

from typing import Final, Mapping

TOPIC_ID: Final[str] = "strength"
SOURCE_PATH: Final[str] = "analysis.strength"
UNIT_SCHEMA: Final[str] = "1.0.0"

STRENGTH_BLOCKS: Final[tuple[str, ...]] = (
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "summary",
)

STRENGTH_BLOCK_TITLES: Final[Mapping[str, str]] = {
    "observation": "Quan sát",
    "reasoning": "Lý do",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "summary": "Tóm tắt",
}

IMPACT_BY_LEVEL: Final[Mapping[str, str]] = {
    "strong": (
        "Với thế Thân vượng đã công bố, nhịp vận hành nghiêng về chủ động và chịu tải."
    ),
    "weak": (
        "Với thế Thân nhược đã công bố, nhịp vận hành nghiêng về cần điểm tựa."
    ),
    "balanced": (
        "Với thế Thân cân bằng đã công bố, nhịp vận hành ít bị kéo lệch một phía."
    ),
}

EVIDENCE_FIELDS: Final[tuple[str, ...]] = (
    "season_strength",
    "root_strength",
    "support_strength",
    "control_strength",
    "drain_strength",
    "temperature_state",
    "special_rules",
    "confidence",
    "strength_level",
    "score",
)

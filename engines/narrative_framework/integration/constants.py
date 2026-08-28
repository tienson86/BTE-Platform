"""INT-02F integrated narrative constants."""

from __future__ import annotations

from typing import Final, Mapping

TOPIC_ID: Final[str] = "integrated"
SOURCE_PATH: Final[str] = "analysis.narrative"
UNIT_SCHEMA: Final[str] = "1.0.0"

TOPIC_ORDER: Final[tuple[str, ...]] = (
    "strength",
    "useful_god",
    "pattern",
    "luck",
)

INTEGRATED_BLOCKS: Final[tuple[str, ...]] = (
    "executive_summary",
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "summary",
)

INTEGRATED_BLOCK_TITLES: Final[Mapping[str, str]] = {
    "executive_summary": "Tổng quan",
    "observation": "Quan sát",
    "reasoning": "Lý do",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "summary": "Tóm tắt",
}

SPEECH_SLOTS: Final[tuple[str, ...]] = (
    "observation",
    "reasoning",
    "impact",
    "recommendation",
)

RESTATEMENT_MARKERS: Final[tuple[str, ...]] = (
    "được đọc là",
    "đã công bố là",
    "đã công bố vẫn là",
    "đã công bố:",
)

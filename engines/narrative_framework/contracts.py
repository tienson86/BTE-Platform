"""INT-02A frozen Narrative Framework constants.

Architecture only. Does not calculate analytical results.
"""

from __future__ import annotations

from typing import Any, Final, Mapping

CONTRACT_ID: Final[str] = "bte.narrative.framework.v1"
FRAMEWORK_VERSION: Final[str] = "1.0.0"
INSUFFICIENT_COPY: Final[str] = "Chưa có dữ liệu"

NARRATIVE_BLOCKS: Final[tuple[str, ...]] = (
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "conclusion",
)

BLOCK_IDS: Final[Mapping[str, str]] = {
    "observation": "sec-observation",
    "reasoning": "sec-reasoning",
    "impact": "sec-impact",
    "recommendation": "sec-recommendation",
    "conclusion": "sec-conclusion",
}

BLOCK_TITLES_VI: Final[Mapping[str, str]] = {
    "observation": "Quan sát",
    "reasoning": "Lý do",
    "impact": "Tác động",
    "recommendation": "Khuyến nghị",
    "conclusion": "Kết luận",
}

WORKSPACE_BLOCK_ALIASES: Final[Mapping[str, str]] = {
    "observe": "observation",
    "reason": "reasoning",
    "impact": "impact",
    "advice": "recommendation",
}

ANALYTICAL_TOPICS: Final[tuple[str, ...]] = (
    "strength",
    "pattern",
    "useful_god",
    "five_elements",
    "ten_gods",
    "shensha",
    "temperature",
    "luck",
)

TEMPLATE_HIERARCHY: Final[tuple[str, ...]] = (
    "topic_template",
    "block_template",
    "sentence_template",
    "slot",
)

SENTENCE_OWNERS: Final[Mapping[str, str]] = {
    "fact": "engine_result",
    "template": "sentence_library",
    "composition": "narrative_framework",
    "selection": "interpretation_engine",
    "delivery": "report_or_portal",
}

COMPOSITION_STAGES: Final[tuple[str, ...]] = (
    "engine_result",
    "topic_evidence_pack",
    "block_fill",
    "topic_narrative_unit",
)

FORBIDDEN_EMPTY_TOKENS: Final[tuple[str, ...]] = (
    "N/A",
    "null",
    "undefined",
    "Không",
    "Chờ dữ liệu",
)


def narrative_framework_contract() -> dict[str, Any]:
    """Return the frozen INT-02A public contract surface."""
    return {
        "contract_id": CONTRACT_ID,
        "framework_version": FRAMEWORK_VERSION,
        "runtime": False,
        "recalculates": False,
        "llm": False,
        "frontend": False,
        "blocks": list(NARRATIVE_BLOCKS),
        "block_ids": dict(BLOCK_IDS),
        "block_titles_vi": dict(BLOCK_TITLES_VI),
        "topics": list(ANALYTICAL_TOPICS),
        "template_hierarchy": list(TEMPLATE_HIERARCHY),
        "sentence_owners": dict(SENTENCE_OWNERS),
        "composition_stages": list(COMPOSITION_STAGES),
        "insufficient_copy": INSUFFICIENT_COPY,
        "workspace_aliases": dict(WORKSPACE_BLOCK_ALIASES),
    }

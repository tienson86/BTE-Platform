"""INT-03A frozen Commercial Composer constants.

Composition only. Does not calculate analytical results.
"""

from __future__ import annotations

from typing import Any, Final, Mapping

CONTRACT_ID: Final[str] = "bte.commercial.composer.v1"
FRAMEWORK_VERSION: Final[str] = "1.0.0"
INSUFFICIENT_COPY: Final[str] = "Chưa có dữ liệu"
SOURCE_PATH: Final[str] = "integrated_narrative"
UNIT_SCHEMA: Final[str] = "1.0.0"

COMMERCIAL_SECTIONS: Final[tuple[str, ...]] = (
    "executive_summary",
    "overall_reading",
    "current_situation",
    "strengths",
    "risks",
    "key_recommendation",
    "conclusion",
)

SECTION_IDS: Final[Mapping[str, str]] = {
    "executive_summary": "sec-commercial-executive",
    "overall_reading": "sec-commercial-reading",
    "current_situation": "sec-commercial-situation",
    "strengths": "sec-commercial-strengths",
    "risks": "sec-commercial-risks",
    "key_recommendation": "sec-commercial-recommendation",
    "conclusion": "sec-commercial-conclusion",
}

SECTION_TITLES_VI: Final[Mapping[str, str]] = {
    "executive_summary": "Tổng quan",
    "overall_reading": "Luận giải tổng thể",
    "current_situation": "Hiện trạng",
    "strengths": "Điểm mạnh",
    "risks": "Rủi ro chính",
    "key_recommendation": "Khuyến nghị trọng tâm",
    "conclusion": "Kết luận",
}

INTEGRATED_SLOTS: Final[tuple[str, ...]] = (
    "executive_summary",
    "observation",
    "reasoning",
    "impact",
    "recommendation",
    "summary",
)

SECTION_SOURCES: Final[Mapping[str, tuple[str, ...]]] = {
    "executive_summary": ("executive_summary",),
    "overall_reading": ("summary",),
    "current_situation": ("observation",),
    "strengths": ("impact",),
    "risks": ("reasoning", "recommendation"),
    "key_recommendation": ("recommendation",),
    "conclusion": ("summary", "recommendation"),
}

RISK_PATH_MARKERS: Final[tuple[str, ...]] = (
    "negative",
    "unfavorable",
)

ALLOWED_OPERATIONS: Final[tuple[str, ...]] = (
    "merge",
    "rewrite",
    "simplify",
    "reorder",
    "summarize",
)

FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "predict",
    "calculate",
    "infer",
    "invent",
    "expand",
)

COMPOSITION_STAGES: Final[tuple[str, ...]] = (
    "integrated_narrative",
    "drop_machine_only",
    "map_sections",
    "commercial_narrative_unit",
)

FORBIDDEN_EMPTY_TOKENS: Final[tuple[str, ...]] = (
    "N/A",
    "null",
    "undefined",
    "Không",
    "Chờ dữ liệu",
)


def commercial_composer_contract() -> dict[str, Any]:
    """Return the frozen INT-03A public contract surface."""
    return {
        "contract_id": CONTRACT_ID,
        "framework_version": FRAMEWORK_VERSION,
        "runtime": True,
        "recalculates": False,
        "llm": False,
        "engine": False,
        "frontend": False,
        "input": "IntegratedNarrativeUnit",
        "output": "CommercialNarrativeUnit",
        "sections": list(COMMERCIAL_SECTIONS),
        "section_ids": dict(SECTION_IDS),
        "section_titles_vi": dict(SECTION_TITLES_VI),
        "section_sources": {key: list(value) for key, value in SECTION_SOURCES.items()},
        "allowed_operations": list(ALLOWED_OPERATIONS),
        "forbidden_operations": list(FORBIDDEN_OPERATIONS),
        "composition_stages": list(COMPOSITION_STAGES),
        "insufficient_copy": INSUFFICIENT_COPY,
        "source_path": SOURCE_PATH,
        "consulting_compose": "compose_commercial_consulting",
    }

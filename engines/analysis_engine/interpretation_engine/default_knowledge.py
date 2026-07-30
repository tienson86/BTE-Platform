"""Deterministic default Interpretation Knowledge pack."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_CONFIDENCE,
    ASSET_PRIORITY,
    ASSET_SECTIONS,
    ASSET_SENTENCES,
    ASSET_TEMPLATES,
    MODULE_ID,
    REQUIRED_ASSETS,
    AssetView,
    InMemoryKnowledgeSession,
    ModuleView,
)

KNOWLEDGE_VERSION = "1.0.0"

_SECTION_TITLES: dict[str, str] = {
    "overview": "Tổng quan",
    "strength": "Vượng suy",
    "temperature": "Hàn nhiệt",
    "pattern": "Cách cục",
    "useful_god": "Dụng thần",
    "ten_gods": "Thập thần",
    "combination": "Hợp xung",
    "shensha": "Thần sát",
    "luck": "Vận hạn",
    "recommendations": "Khuyến nghị",
}


def _freeze(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(data))


def build_default_interpretation_knowledge() -> dict[str, AssetView]:
    """Build the default frozen asset set for interpretation_knowledge."""
    sentences = [
        {
            "sentence_id": "overview_intro",
            "section_id": "overview",
            "source_stage": "summary",
            "template_id": "tpl_overview_intro",
            "priority": 100,
            "match": {},
            "placeholders": ["day_master"],
            "required_placeholders": ["day_master"],
        },
        {
            "sentence_id": "strength_strong",
            "section_id": "strength",
            "source_stage": "strength",
            "template_id": "tpl_strength_strong",
            "priority": 90,
            "match": {"classification": "strong"},
            "placeholders": ["day_master", "classification"],
            "required_placeholders": ["day_master", "classification"],
        },
        {
            "sentence_id": "strength_weak",
            "section_id": "strength",
            "source_stage": "strength",
            "template_id": "tpl_strength_weak",
            "priority": 90,
            "match": {"classification": "weak"},
            "placeholders": ["day_master", "classification"],
            "required_placeholders": ["day_master", "classification"],
        },
        {
            "sentence_id": "temperature_balanced",
            "section_id": "temperature",
            "source_stage": "temperature",
            "template_id": "tpl_temperature_balanced",
            "priority": 85,
            "match": {"classification": "balanced"},
            "placeholders": ["classification"],
            "required_placeholders": ["classification"],
        },
        {
            "sentence_id": "pattern_named",
            "section_id": "pattern",
            "source_stage": "pattern",
            "template_id": "tpl_pattern_named",
            "priority": 88,
            "match": {},
            "placeholders": ["pattern_id"],
            "required_placeholders": ["pattern_id"],
        },
        {
            "sentence_id": "useful_god_list",
            "section_id": "useful_god",
            "source_stage": "useful_god",
            "template_id": "tpl_useful_god_list",
            "priority": 80,
            "match": {},
            "placeholders": ["useful_gods"],
            "required_placeholders": ["useful_gods"],
        },
        {
            "sentence_id": "ten_gods_presence",
            "section_id": "ten_gods",
            "source_stage": "ten_gods",
            "template_id": "tpl_ten_gods_presence",
            "priority": 75,
            "match": {},
            "placeholders": ["presence_count"],
            "required_placeholders": [],
        },
        {
            "sentence_id": "combination_summary",
            "section_id": "combination",
            "source_stage": "combination",
            "template_id": "tpl_combination_summary",
            "priority": 70,
            "match": {},
            "placeholders": [],
            "required_placeholders": [],
        },
        {
            "sentence_id": "shensha_presence",
            "section_id": "shensha",
            "source_stage": "shensha",
            "template_id": "tpl_shensha_presence",
            "priority": 72,
            "match": {},
            "placeholders": ["presence_count"],
            "required_placeholders": [],
        },
        {
            "sentence_id": "luck_active",
            "section_id": "luck",
            "source_stage": "luck",
            "template_id": "tpl_luck_active",
            "priority": 78,
            "match": {},
            "placeholders": ["active_count", "current_da_yun_index"],
            "required_placeholders": [],
        },
        {
            "sentence_id": "recommendations_close",
            "section_id": "recommendations",
            "source_stage": "summary",
            "template_id": "tpl_recommendations_close",
            "priority": 60,
            "match": {},
            "placeholders": ["day_master"],
            "required_placeholders": ["day_master"],
        },
    ]

    templates = {
        "tpl_overview_intro": (
            "Bản luận giải cho Nhật Chủ {day_master} được tổng hợp từ toàn bộ "
            "kết quả phân tích."
        ),
        "tpl_strength_strong": (
            "Nhật Chủ {day_master} thuộc loại {classification}, lực lượng vững."
        ),
        "tpl_strength_weak": (
            "Nhật Chủ {day_master} thuộc loại {classification}, cần bồi bổ."
        ),
        "tpl_temperature_balanced": (
            "Khí hậu cục diện ở trạng thái {classification}."
        ),
        "tpl_pattern_named": "Cách cục chủ đạo là {pattern_id}.",
        "tpl_useful_god_list": "Dụng thần ưu tiên gồm: {useful_gods}.",
        "tpl_ten_gods_presence": (
            "Thập thần hiện diện với {presence_count} mục chính."
        ),
        "tpl_combination_summary": (
            "Các quan hệ hợp xung đã được đánh giá theo Rule Database."
        ),
        "tpl_shensha_presence": (
            "Thần sát ghi nhận {presence_count} dấu hiệu liên quan."
        ),
        "tpl_luck_active": (
            "Lớp vận hạn đang hoạt động: {active_count}, "
            "Đại vận hiện tại index {current_da_yun_index}."
        ),
        "tpl_recommendations_close": (
            "Nên theo dõi biến động vận hạn gắn với Nhật Chủ {day_master}."
        ),
    }

    section_order = list(_SECTION_TITLES.keys())

    return {
        ASSET_SENTENCES: AssetView(
            asset_id=ASSET_SENTENCES,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"rows": sentences}),
        ),
        ASSET_TEMPLATES: AssetView(
            asset_id=ASSET_TEMPLATES,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"templates": templates}),
        ),
        ASSET_SECTIONS: AssetView(
            asset_id=ASSET_SECTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "order": section_order,
                    "titles": dict(_SECTION_TITLES),
                    "max_sentences_per_section": 3,
                }
            ),
        ),
        ASSET_PRIORITY: AssetView(
            asset_id=ASSET_PRIORITY,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"tie_break": ["priority_desc", "sentence_id_asc"]}),
        ),
        ASSET_CONFIDENCE: AssetView(
            asset_id=ASSET_CONFIDENCE,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "base_score": 0.75,
                    "level": "high",
                    "per_section_bonus": 0.02,
                    "max_score": 0.95,
                }
            ),
        ),
    }


def create_default_knowledge_session() -> InMemoryKnowledgeSession:
    """Create a default KnowledgeSession for Interpretation Engine."""
    assets = build_default_interpretation_knowledge()
    module = ModuleView(
        module_id=MODULE_ID,
        version=KNOWLEDGE_VERSION,
        assets=REQUIRED_ASSETS,
        metadata={"name": "Interpretation Knowledge"},
    )
    return InMemoryKnowledgeSession(
        modules={MODULE_ID: module},
        assets=assets,
    )

"""Deterministic default Combination Knowledge pack served via Knowledge SDK."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.combination_engine.knowledge_access import (
    ASSET_BRANCH_COMBINATIONS,
    ASSET_CLASH,
    ASSET_CONFIDENCE,
    ASSET_DESTRUCTION,
    ASSET_HARM,
    ASSET_HIDDEN_COMBINATION,
    ASSET_PRIORITY,
    ASSET_PUNISHMENT,
    ASSET_STEM_COMBINATIONS,
    ASSET_TRANSFORMATION,
    ASSET_UPSTREAM_QUALIFIERS,
    MODULE_ID,
    REQUIRED_ASSETS,
    AssetView,
    InMemoryKnowledgeSession,
    ModuleView,
)

KNOWLEDGE_VERSION = "1.0.0"


def _freeze(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(data))


def build_default_combination_knowledge() -> dict[str, AssetView]:
    """Build the default frozen asset set for combination_knowledge."""
    # Heavenly stem six combinations (Giáp-Kỷ → Thổ, etc.)
    stem_pairs = [
        {"a": "Giáp", "b": "Kỷ", "result_element": "Thổ", "relation_id": "stem_jia_ji"},
        {"a": "Ất", "b": "Canh", "result_element": "Kim", "relation_id": "stem_yi_geng"},
        {"a": "Bính", "b": "Tân", "result_element": "Thủy", "relation_id": "stem_bing_xin"},
        {"a": "Đinh", "b": "Nhâm", "result_element": "Mộc", "relation_id": "stem_ding_ren"},
        {"a": "Mậu", "b": "Quý", "result_element": "Hỏa", "relation_id": "stem_wu_gui"},
        # Pinyin aliases
        {"a": "Jia", "b": "Ji", "result_element": "Thổ", "relation_id": "stem_jia_ji"},
        {"a": "Yi", "b": "Geng", "result_element": "Kim", "relation_id": "stem_yi_geng"},
        {"a": "Bing", "b": "Xin", "result_element": "Thủy", "relation_id": "stem_bing_xin"},
        {"a": "Ding", "b": "Ren", "result_element": "Mộc", "relation_id": "stem_ding_ren"},
        {"a": "Wu", "b": "Gui", "result_element": "Hỏa", "relation_id": "stem_wu_gui"},
    ]

    branch_six = [
        {"a": "Tý", "b": "Sửu", "result_element": "Thổ", "relation_id": "branch_zi_chou"},
        {"a": "Dần", "b": "Hợi", "result_element": "Mộc", "relation_id": "branch_yin_hai"},
        {"a": "Mão", "b": "Tuất", "result_element": "Hỏa", "relation_id": "branch_mao_xu"},
        {"a": "Thìn", "b": "Dậu", "result_element": "Kim", "relation_id": "branch_chen_you"},
        {"a": "Tỵ", "b": "Thân", "result_element": "Thủy", "relation_id": "branch_si_shen"},
        {"a": "Ngọ", "b": "Mùi", "result_element": "Thổ", "relation_id": "branch_wu_wei"},
        # Pinyin
        {"a": "Zi", "b": "Chou", "result_element": "Thổ", "relation_id": "branch_zi_chou"},
        {"a": "Yin", "b": "Hai", "result_element": "Mộc", "relation_id": "branch_yin_hai"},
        {"a": "Mao", "b": "Xu", "result_element": "Hỏa", "relation_id": "branch_mao_xu"},
        {"a": "Chen", "b": "You", "result_element": "Kim", "relation_id": "branch_chen_you"},
        {"a": "Si", "b": "Shen", "result_element": "Thủy", "relation_id": "branch_si_shen"},
        {"a": "Wu", "b": "Wei", "result_element": "Thổ", "relation_id": "branch_wu_wei"},
    ]

    branch_triads = [
        {
            "members": ["Thân", "Tý", "Thìn"],
            "result_element": "Thủy",
            "relation_id": "triad_water",
        },
        {
            "members": ["Dần", "Ngọ", "Tuất"],
            "result_element": "Hỏa",
            "relation_id": "triad_fire",
        },
        {
            "members": ["Tỵ", "Dậu", "Sửu"],
            "result_element": "Kim",
            "relation_id": "triad_metal",
        },
        {
            "members": ["Hợi", "Mão", "Mùi"],
            "result_element": "Mộc",
            "relation_id": "triad_wood",
        },
        {
            "members": ["Shen", "Zi", "Chen"],
            "result_element": "Thủy",
            "relation_id": "triad_water",
        },
        {
            "members": ["Yin", "Wu", "Xu"],
            "result_element": "Hỏa",
            "relation_id": "triad_fire",
        },
        {
            "members": ["Si", "You", "Chou"],
            "result_element": "Kim",
            "relation_id": "triad_metal",
        },
        {
            "members": ["Hai", "Mao", "Wei"],
            "result_element": "Mộc",
            "relation_id": "triad_wood",
        },
    ]

    clashes = [
        {"a": "Tý", "b": "Ngọ", "relation_id": "clash_zi_wu"},
        {"a": "Sửu", "b": "Mùi", "relation_id": "clash_chou_wei"},
        {"a": "Dần", "b": "Thân", "relation_id": "clash_yin_shen"},
        {"a": "Mão", "b": "Dậu", "relation_id": "clash_mao_you"},
        {"a": "Thìn", "b": "Tuất", "relation_id": "clash_chen_xu"},
        {"a": "Tỵ", "b": "Hợi", "relation_id": "clash_si_hai"},
        {"a": "Zi", "b": "Wu", "relation_id": "clash_zi_wu"},
        {"a": "Chou", "b": "Wei", "relation_id": "clash_chou_wei"},
        {"a": "Yin", "b": "Shen", "relation_id": "clash_yin_shen"},
        {"a": "Mao", "b": "You", "relation_id": "clash_mao_you"},
        {"a": "Chen", "b": "Xu", "relation_id": "clash_chen_xu"},
        {"a": "Si", "b": "Hai", "relation_id": "clash_si_hai"},
    ]

    harms = [
        {"a": "Tý", "b": "Mùi", "relation_id": "harm_zi_wei"},
        {"a": "Sửu", "b": "Ngọ", "relation_id": "harm_chou_wu"},
        {"a": "Dần", "b": "Tỵ", "relation_id": "harm_yin_si"},
        {"a": "Mão", "b": "Thìn", "relation_id": "harm_mao_chen"},
        {"a": "Thân", "b": "Hợi", "relation_id": "harm_shen_hai"},
        {"a": "Dậu", "b": "Tuất", "relation_id": "harm_you_xu"},
        {"a": "Zi", "b": "Wei", "relation_id": "harm_zi_wei"},
        {"a": "Chou", "b": "Wu", "relation_id": "harm_chou_wu"},
        {"a": "Yin", "b": "Si", "relation_id": "harm_yin_si"},
        {"a": "Mao", "b": "Chen", "relation_id": "harm_mao_chen"},
        {"a": "Shen", "b": "Hai", "relation_id": "harm_shen_hai"},
        {"a": "You", "b": "Xu", "relation_id": "harm_you_xu"},
    ]

    punishments = [
        {
            "members": ["Dần", "Tỵ", "Thân"],
            "relation_id": "punish_yin_si_shen",
            "mode": "triad",
        },
        {
            "members": ["Sửu", "Tuất", "Mùi"],
            "relation_id": "punish_chou_xu_wei",
            "mode": "triad",
        },
        {"a": "Tý", "b": "Mão", "relation_id": "punish_zi_mao", "mode": "pair"},
        {"a": "Thìn", "b": "Thìn", "relation_id": "punish_chen_self", "mode": "self"},
        {"a": "Ngọ", "b": "Ngọ", "relation_id": "punish_wu_self", "mode": "self"},
        {"a": "Dậu", "b": "Dậu", "relation_id": "punish_you_self", "mode": "self"},
        {"a": "Hợi", "b": "Hợi", "relation_id": "punish_hai_self", "mode": "self"},
        {
            "members": ["Yin", "Si", "Shen"],
            "relation_id": "punish_yin_si_shen",
            "mode": "triad",
        },
        {
            "members": ["Chou", "Xu", "Wei"],
            "relation_id": "punish_chou_xu_wei",
            "mode": "triad",
        },
        {"a": "Zi", "b": "Mao", "relation_id": "punish_zi_mao", "mode": "pair"},
    ]

    destructions = [
        {"a": "Tý", "b": "Dậu", "relation_id": "destroy_zi_you"},
        {"a": "Sửu", "b": "Thìn", "relation_id": "destroy_chou_chen"},
        {"a": "Dần", "b": "Hợi", "relation_id": "destroy_yin_hai"},
        {"a": "Mão", "b": "Ngọ", "relation_id": "destroy_mao_wu"},
        {"a": "Tỵ", "b": "Thân", "relation_id": "destroy_si_shen"},
        {"a": "Ngọ", "b": "Dậu", "relation_id": "destroy_wu_you"},
        {"a": "Zi", "b": "You", "relation_id": "destroy_zi_you"},
        {"a": "Chou", "b": "Chen", "relation_id": "destroy_chou_chen"},
        {"a": "Yin", "b": "Hai", "relation_id": "destroy_yin_hai"},
        {"a": "Mao", "b": "Wu", "relation_id": "destroy_mao_wu"},
        {"a": "Si", "b": "Shen", "relation_id": "destroy_si_shen"},
        {"a": "Wu", "b": "You", "relation_id": "destroy_wu_you"},
    ]

    hidden_stems = {
        "Tý": ["Quý"],
        "Sửu": ["Kỷ", "Quý", "Tân"],
        "Dần": ["Giáp", "Bính", "Mậu"],
        "Mão": ["Ất"],
        "Thìn": ["Mậu", "Ất", "Quý"],
        "Tỵ": ["Bính", "Mậu", "Canh"],
        "Ngọ": ["Đinh", "Kỷ"],
        "Mùi": ["Kỷ", "Đinh", "Ất"],
        "Thân": ["Canh", "Nhâm", "Mậu"],
        "Dậu": ["Tân"],
        "Tuất": ["Mậu", "Tân", "Đinh"],
        "Hợi": ["Nhâm", "Giáp"],
        "Zi": ["Gui"],
        "Chou": ["Ji", "Gui", "Xin"],
        "Yin": ["Jia", "Bing", "Wu"],
        "Mao": ["Yi"],
        "Chen": ["Wu", "Yi", "Gui"],
        "Si": ["Bing", "Wu", "Geng"],
        "Wu": ["Ding", "Ji"],
        "Wei": ["Ji", "Ding", "Yi"],
        "Shen": ["Geng", "Ren", "Wu"],
        "You": ["Xin"],
        "Xu": ["Wu", "Xin", "Ding"],
        "Hai": ["Ren", "Jia"],
    }

    return {
        ASSET_STEM_COMBINATIONS: AssetView(
            asset_id=ASSET_STEM_COMBINATIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"pairs": stem_pairs, "priority": 80}),
        ),
        ASSET_BRANCH_COMBINATIONS: AssetView(
            asset_id=ASSET_BRANCH_COMBINATIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "six_combinations": branch_six,
                    "triads": branch_triads,
                    "priority": 85,
                }
            ),
        ),
        ASSET_CLASH: AssetView(
            asset_id=ASSET_CLASH,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"pairs": clashes, "priority": 95}),
        ),
        ASSET_HARM: AssetView(
            asset_id=ASSET_HARM,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"pairs": harms, "priority": 70}),
        ),
        ASSET_PUNISHMENT: AssetView(
            asset_id=ASSET_PUNISHMENT,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"rules": punishments, "priority": 75}),
        ),
        ASSET_DESTRUCTION: AssetView(
            asset_id=ASSET_DESTRUCTION,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"pairs": destructions, "priority": 65}),
        ),
        ASSET_HIDDEN_COMBINATION: AssetView(
            asset_id=ASSET_HIDDEN_COMBINATION,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "hidden_stems": hidden_stems,
                    "stem_pairs": stem_pairs,
                    "priority": 60,
                }
            ),
        ),
        ASSET_TRANSFORMATION: AssetView(
            asset_id=ASSET_TRANSFORMATION,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "success_requires": {
                        "no_clash_on_members": True,
                        "min_support_from_useful_god": False,
                    },
                    "clash_blocks_transform": True,
                    "priority": 90,
                }
            ),
        ),
        ASSET_UPSTREAM_QUALIFIERS: AssetView(
            asset_id=ASSET_UPSTREAM_QUALIFIERS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "dimension": "strength",
                            "classification": "strong",
                            "effect": "stabilize_transform",
                            "priority": 40,
                        },
                        {
                            "dimension": "strength",
                            "classification": "weak",
                            "effect": "weaken_transform",
                            "priority": 40,
                        },
                        {
                            "dimension": "ten_gods",
                            "has_presence": True,
                            "effect": "structure_context",
                            "priority": 20,
                        },
                    ]
                }
            ),
        ),
        ASSET_PRIORITY: AssetView(
            asset_id=ASSET_PRIORITY,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "type_priority": {
                        "clash": 100,
                        "punishment": 90,
                        "harm": 80,
                        "destruction": 70,
                        "stem_combination": 60,
                        "branch_combination": 65,
                        "hidden_combination": 50,
                    },
                    "status_priority": {
                        "active": 0,
                        "blocked": 1,
                        "qualified": 2,
                    },
                }
            ),
        ),
        ASSET_CONFIDENCE: AssetView(
            asset_id=ASSET_CONFIDENCE,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "weights": {
                        "detection": 0.45,
                        "transformation": 0.25,
                        "resolution": 0.20,
                        "upstream": 0.10,
                    },
                    "levels": [
                        {"min": 0.85, "level": "high"},
                        {"min": 0.60, "level": "medium"},
                        {"min": 0.0, "level": "low"},
                    ],
                }
            ),
        ),
    }


def create_default_knowledge_session() -> InMemoryKnowledgeSession:
    """Create a frozen KnowledgeSession exposing default Combination knowledge."""
    assets = build_default_combination_knowledge()
    module = ModuleView(
        module_id=MODULE_ID,
        version=KNOWLEDGE_VERSION,
        assets=REQUIRED_ASSETS,
        metadata={"domain": "combination"},
    )
    return InMemoryKnowledgeSession(
        modules={MODULE_ID: module},
        assets=assets,
    )

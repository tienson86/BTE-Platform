"""Deterministic default Ten Gods Knowledge pack served via Knowledge SDK session."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.ten_gods_engine.knowledge_access import (
    ASSET_CONFIDENCE,
    ASSET_FAVORABILITY,
    ASSET_IDENTITIES,
    ASSET_LIFE_AREAS,
    ASSET_PATTERN_INTERACTIONS,
    ASSET_PRIORITY,
    ASSET_RELATIONSHIPS,
    ASSET_STEM_RELATIONS,
    ASSET_STRENGTH_INTERACTIONS,
    ASSET_TEMPERATURE_INTERACTIONS,
    ASSET_USEFUL_GOD_INTERACTIONS,
    MODULE_ID,
    REQUIRED_ASSETS,
    AssetView,
    InMemoryKnowledgeSession,
    ModuleView,
)

KNOWLEDGE_VERSION = "1.0.0"

# Stem metadata used by stem_relations resolution (knowledge data, not engine rules).
_STEM_META: dict[str, tuple[str, str]] = {
    "Giáp": ("Mộc", "Dương"),
    "Ất": ("Mộc", "Âm"),
    "Bính": ("Hỏa", "Dương"),
    "Đinh": ("Hỏa", "Âm"),
    "Mậu": ("Thổ", "Dương"),
    "Kỷ": ("Thổ", "Âm"),
    "Canh": ("Kim", "Dương"),
    "Tân": ("Kim", "Âm"),
    "Nhâm": ("Thủy", "Dương"),
    "Quý": ("Thủy", "Âm"),
    # Pinyin aliases for deterministic chart fixtures
    "Jia": ("Mộc", "Dương"),
    "Yi": ("Mộc", "Âm"),
    "Bing": ("Hỏa", "Dương"),
    "Ding": ("Hỏa", "Âm"),
    "Wu": ("Thổ", "Dương"),
    "Ji": ("Thổ", "Âm"),
    "Geng": ("Kim", "Dương"),
    "Xin": ("Kim", "Âm"),
    "Ren": ("Thủy", "Dương"),
    "Gui": ("Thủy", "Âm"),
}

_GENERATES: dict[str, str] = {
    "Mộc": "Hỏa",
    "Hỏa": "Thổ",
    "Thổ": "Kim",
    "Kim": "Thủy",
    "Thủy": "Mộc",
}

_CONTROLS: dict[str, str] = {
    "Mộc": "Thổ",
    "Hỏa": "Kim",
    "Thổ": "Thủy",
    "Kim": "Mộc",
    "Thủy": "Hỏa",
}

# relation_key = same_element|generates_dm|generated_by_dm|controls|controlled
_RELATION_TO_GOD: dict[str, dict[str, str]] = {
    "same_element": {"same_polarity": "bi_jian", "diff_polarity": "jie_cai"},
    "generated_by_other": {"same_polarity": "pian_yin", "diff_polarity": "zheng_yin"},
    "generates_other": {"same_polarity": "shi_shen", "diff_polarity": "shang_guan"},
    "controls_other": {"same_polarity": "pian_cai", "diff_polarity": "zheng_cai"},
    "controlled_by_other": {"same_polarity": "qi_sha", "diff_polarity": "zheng_guan"},
}


def _freeze(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(data))


def build_default_ten_gods_knowledge() -> dict[str, AssetView]:
    """Build the default frozen asset set for ten_gods_knowledge."""
    identities = {
        "bi_jian": {"label": "Bi Jian", "polarity_class": "peer", "vi": "Tỷ Kiên"},
        "jie_cai": {"label": "Jie Cai", "polarity_class": "peer", "vi": "Kiếp Tài"},
        "shi_shen": {"label": "Shi Shen", "polarity_class": "output", "vi": "Thực Thần"},
        "shang_guan": {
            "label": "Shang Guan",
            "polarity_class": "output",
            "vi": "Thương Quan",
        },
        "pian_cai": {
            "label": "Pian Cai",
            "polarity_class": "wealth",
            "vi": "Thiên Tài",
        },
        "zheng_cai": {
            "label": "Zheng Cai",
            "polarity_class": "wealth",
            "vi": "Chính Tài",
        },
        "qi_sha": {"label": "Qi Sha", "polarity_class": "officer", "vi": "Thất Sát"},
        "zheng_guan": {
            "label": "Zheng Guan",
            "polarity_class": "officer",
            "vi": "Chính Quan",
        },
        "pian_yin": {
            "label": "Pian Yin",
            "polarity_class": "resource",
            "vi": "Thiên Ấn",
        },
        "zheng_yin": {
            "label": "Zheng Yin",
            "polarity_class": "resource",
            "vi": "Chính Ấn",
        },
    }

    assets: dict[str, AssetView] = {
        ASSET_IDENTITIES: AssetView(
            asset_id=ASSET_IDENTITIES,
            version=KNOWLEDGE_VERSION,
            data=_freeze({"identities": identities}),
        ),
        ASSET_STEM_RELATIONS: AssetView(
            asset_id=ASSET_STEM_RELATIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "stem_meta": _STEM_META,
                    "generates": _GENERATES,
                    "controls": _CONTROLS,
                    "relation_to_god": _RELATION_TO_GOD,
                }
            ),
        ),
        ASSET_RELATIONSHIPS: AssetView(
            asset_id=ASSET_RELATIONSHIPS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "pairs": [
                        {
                            "left": "zheng_guan",
                            "right": "zheng_yin",
                            "relation": "mutual_support",
                            "priority": 90,
                        },
                        {
                            "left": "qi_sha",
                            "right": "shi_shen",
                            "relation": "control_transform",
                            "priority": 85,
                        },
                        {
                            "left": "shang_guan",
                            "right": "zheng_guan",
                            "relation": "conflict",
                            "priority": 80,
                        },
                        {
                            "left": "zheng_cai",
                            "right": "jie_cai",
                            "relation": "wealth_contest",
                            "priority": 70,
                        },
                    ]
                }
            ),
        ),
        ASSET_STRENGTH_INTERACTIONS: AssetView(
            asset_id=ASSET_STRENGTH_INTERACTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "strength_class": "strong",
                            "god_id": "zheng_guan",
                            "effect": "favor_boost",
                            "priority": 80,
                        },
                        {
                            "strength_class": "strong",
                            "god_id": "shi_shen",
                            "effect": "favor_boost",
                            "priority": 70,
                        },
                        {
                            "strength_class": "weak",
                            "god_id": "zheng_yin",
                            "effect": "favor_boost",
                            "priority": 80,
                        },
                        {
                            "strength_class": "weak",
                            "god_id": "qi_sha",
                            "effect": "favor_penalty",
                            "priority": 75,
                        },
                        {
                            "strength_class": "balanced",
                            "god_id": "*",
                            "effect": "neutral",
                            "priority": 10,
                        },
                    ]
                }
            ),
        ),
        ASSET_TEMPERATURE_INTERACTIONS: AssetView(
            asset_id=ASSET_TEMPERATURE_INTERACTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "temperature_class": "cold",
                            "god_id": "shi_shen",
                            "effect": "warm_support",
                            "priority": 60,
                        },
                        {
                            "temperature_class": "hot",
                            "god_id": "zheng_yin",
                            "effect": "cool_support",
                            "priority": 60,
                        },
                        {
                            "temperature_class": "balanced",
                            "god_id": "*",
                            "effect": "neutral",
                            "priority": 10,
                        },
                    ]
                }
            ),
        ),
        ASSET_PATTERN_INTERACTIONS: AssetView(
            asset_id=ASSET_PATTERN_INTERACTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "pattern_id": "zheng_guan_ge",
                            "god_id": "zheng_guan",
                            "effect": "structure_core",
                            "priority": 95,
                        },
                        {
                            "pattern_id": "shi_shen_ge",
                            "god_id": "shi_shen",
                            "effect": "structure_core",
                            "priority": 95,
                        },
                        {
                            "pattern_id": "*",
                            "god_id": "*",
                            "effect": "structure_secondary",
                            "priority": 5,
                        },
                    ]
                }
            ),
        ),
        ASSET_USEFUL_GOD_INTERACTIONS: AssetView(
            asset_id=ASSET_USEFUL_GOD_INTERACTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "role": "useful",
                            "god_id": "*",
                            "effect": "favor_reinforce",
                            "priority": 90,
                        },
                        {
                            "role": "unfavorable",
                            "god_id": "*",
                            "effect": "favor_oppose",
                            "priority": 90,
                        },
                    ]
                }
            ),
        ),
        ASSET_FAVORABILITY: AssetView(
            asset_id=ASSET_FAVORABILITY,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "base": {
                        "bi_jian": "neutral",
                        "jie_cai": "conditional",
                        "shi_shen": "favorable",
                        "shang_guan": "conditional",
                        "pian_cai": "favorable",
                        "zheng_cai": "favorable",
                        "qi_sha": "conditional",
                        "zheng_guan": "favorable",
                        "pian_yin": "favorable",
                        "zheng_yin": "favorable",
                    },
                    "effect_map": {
                        "favor_boost": "favorable",
                        "favor_reinforce": "favorable",
                        "favor_penalty": "unfavorable",
                        "favor_oppose": "unfavorable",
                        "structure_core": "favorable",
                        "warm_support": "favorable",
                        "cool_support": "favorable",
                        "neutral": "neutral",
                        "structure_secondary": "neutral",
                    },
                    "priority_order": [
                        "unfavorable",
                        "favorable",
                        "conditional",
                        "neutral",
                    ],
                }
            ),
        ),
        ASSET_LIFE_AREAS: AssetView(
            asset_id=ASSET_LIFE_AREAS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "area": "personality",
                            "god_id": "shi_shen",
                            "concept_id": "expressive",
                            "tag": "personality.expressive",
                        },
                        {
                            "area": "career",
                            "god_id": "zheng_guan",
                            "concept_id": "authority",
                            "tag": "career.authority",
                        },
                        {
                            "area": "wealth",
                            "god_id": "zheng_cai",
                            "concept_id": "stable_wealth",
                            "tag": "wealth.stable",
                        },
                        {
                            "area": "marriage",
                            "god_id": "zheng_cai",
                            "concept_id": "partner_link",
                            "tag": "marriage.partner_link",
                        },
                        {
                            "area": "health",
                            "god_id": "zheng_yin",
                            "concept_id": "resource_support",
                            "tag": "health.resource_support",
                        },
                        {
                            "area": "career",
                            "god_id": "qi_sha",
                            "concept_id": "pressure_drive",
                            "tag": "career.pressure_drive",
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
                    "god_priority": {
                        "zheng_guan": 100,
                        "qi_sha": 95,
                        "zheng_yin": 90,
                        "pian_yin": 85,
                        "zheng_cai": 80,
                        "pian_cai": 75,
                        "shi_shen": 70,
                        "shang_guan": 65,
                        "bi_jian": 60,
                        "jie_cai": 55,
                    }
                }
            ),
        ),
        ASSET_CONFIDENCE: AssetView(
            asset_id=ASSET_CONFIDENCE,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "weights": {
                        "presence": 0.30,
                        "relationship": 0.15,
                        "interaction": 0.25,
                        "favorability": 0.20,
                        "life_area": 0.10,
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
    return assets


def create_default_knowledge_session() -> InMemoryKnowledgeSession:
    """Create a frozen KnowledgeSession exposing default Ten Gods knowledge."""
    assets = build_default_ten_gods_knowledge()
    module = ModuleView(
        module_id=MODULE_ID,
        version=KNOWLEDGE_VERSION,
        assets=REQUIRED_ASSETS,
        metadata={"domain": "ten_gods"},
    )
    return InMemoryKnowledgeSession(
        modules={MODULE_ID: module},
        assets=assets,
    )

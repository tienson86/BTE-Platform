"""Deterministic default Luck Knowledge pack served via Knowledge SDK."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.luck_engine.knowledge_access import (
    ASSET_ACTIVATION,
    ASSET_CONFIDENCE,
    ASSET_DA_YUN,
    ASSET_FAVORABILITY,
    ASSET_INTERACTION,
    ASSET_LIU_NIAN,
    ASSET_LIU_RI,
    ASSET_LIU_SHI,
    ASSET_LIU_YUE,
    ASSET_PRIORITY,
    ASSET_TIMING,
    MODULE_ID,
    REQUIRED_ASSETS,
    AssetView,
    InMemoryKnowledgeSession,
    ModuleView,
)

KNOWLEDGE_VERSION = "1.0.0"

_STEM_ELEMENT: dict[str, str] = {
    "Giáp": "Mộc",
    "Ất": "Mộc",
    "Bính": "Hỏa",
    "Đinh": "Hỏa",
    "Mậu": "Thổ",
    "Kỷ": "Thổ",
    "Canh": "Kim",
    "Tân": "Kim",
    "Nhâm": "Thủy",
    "Quý": "Thủy",
}

_BRANCH_ELEMENT: dict[str, str] = {
    "Tý": "Thủy",
    "Sửu": "Thổ",
    "Dần": "Mộc",
    "Mão": "Mộc",
    "Thìn": "Thổ",
    "Tỵ": "Hỏa",
    "Ngọ": "Hỏa",
    "Mùi": "Thổ",
    "Thân": "Kim",
    "Dậu": "Kim",
    "Tuất": "Thổ",
    "Hợi": "Thủy",
}


def _freeze(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(data))


def _layer_asset(
    asset_id: str,
    *,
    layer: str,
    priority: int,
) -> AssetView:
    return AssetView(
        asset_id=asset_id,
        version=KNOWLEDGE_VERSION,
        data=_freeze(
            {
                "layer": layer,
                "priority": priority,
                "requires_parent_active": layer != "da_yun",
                "parent_layer": {
                    "liu_nian": "da_yun",
                    "liu_yue": "liu_nian",
                    "liu_ri": "liu_yue",
                    "liu_shi": "liu_ri",
                }.get(layer),
            }
        ),
    )


def build_default_luck_knowledge() -> dict[str, AssetView]:
    """Build the default frozen asset set for luck_knowledge."""
    return {
        ASSET_DA_YUN: _layer_asset(ASSET_DA_YUN, layer="da_yun", priority=100),
        ASSET_LIU_NIAN: _layer_asset(ASSET_LIU_NIAN, layer="liu_nian", priority=90),
        ASSET_LIU_YUE: _layer_asset(ASSET_LIU_YUE, layer="liu_yue", priority=80),
        ASSET_LIU_RI: _layer_asset(ASSET_LIU_RI, layer="liu_ri", priority=70),
        ASSET_LIU_SHI: _layer_asset(ASSET_LIU_SHI, layer="liu_shi", priority=60),
        ASSET_INTERACTION: AssetView(
            asset_id=ASSET_INTERACTION,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "dimension": "strength",
                            "classification": "strong",
                            "effect": "stabilize_luck",
                            "priority": 50,
                        },
                        {
                            "dimension": "strength",
                            "classification": "weak",
                            "effect": "weaken_luck",
                            "priority": 50,
                        },
                        {
                            "dimension": "useful_god",
                            "overlap": True,
                            "effect": "favor_boost",
                            "priority": 80,
                        },
                        {
                            "dimension": "shensha",
                            "has_inauspicious": True,
                            "effect": "stress_luck",
                            "priority": 40,
                        },
                        {
                            "dimension": "combination",
                            "has_clash": True,
                            "effect": "disrupt_luck",
                            "priority": 45,
                        },
                    ]
                }
            ),
        ),
        ASSET_TIMING: AssetView(
            asset_id=ASSET_TIMING,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "phases": {
                        "early": {"min_ratio": 0.0, "max_ratio": 0.33},
                        "peak": {"min_ratio": 0.33, "max_ratio": 0.67},
                        "late": {"min_ratio": 0.67, "max_ratio": 1.01},
                    },
                    "default_phase": "peak",
                }
            ),
        ),
        ASSET_ACTIVATION: AssetView(
            asset_id=ASSET_ACTIVATION,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rules": [
                        {
                            "layer": "da_yun",
                            "require_current_age_in_range": True,
                        },
                        {
                            "layer": "liu_nian",
                            "require_parent_active": True,
                        },
                        {
                            "layer": "liu_yue",
                            "require_parent_active": True,
                        },
                        {
                            "layer": "liu_ri",
                            "require_parent_active": True,
                        },
                        {
                            "layer": "liu_shi",
                            "require_parent_active": True,
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
                    "stem_element": _STEM_ELEMENT,
                    "branch_element": _BRANCH_ELEMENT,
                    "useful_god_elements": {
                        # Vietnamese ten-god labels / ids mapped to supportive elements are
                        # resolved via useful_god payload values when present.
                    },
                    "effect_map": {
                        "favor_boost": "favorable",
                        "stabilize_luck": "favorable",
                        "weaken_luck": "conditional",
                        "stress_luck": "unfavorable",
                        "disrupt_luck": "unfavorable",
                    },
                    "base_by_element_vs_day_master": {
                        "same": "neutral",
                        "generates_dm": "favorable",
                        "generated_by_dm": "conditional",
                        "controls_dm": "unfavorable",
                        "controlled_by_dm": "favorable",
                    },
                    "generates": {
                        "Mộc": "Hỏa",
                        "Hỏa": "Thổ",
                        "Thổ": "Kim",
                        "Kim": "Thủy",
                        "Thủy": "Mộc",
                    },
                    "controls": {
                        "Mộc": "Thổ",
                        "Hỏa": "Kim",
                        "Thổ": "Thủy",
                        "Kim": "Mộc",
                        "Thủy": "Hỏa",
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
        ASSET_PRIORITY: AssetView(
            asset_id=ASSET_PRIORITY,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "layer_priority": {
                        "da_yun": 100,
                        "liu_nian": 90,
                        "liu_yue": 80,
                        "liu_ri": 70,
                        "liu_shi": 60,
                    },
                    "status_priority": {
                        "active": 0,
                        "inactive": 1,
                        "blocked": 2,
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
                        "layers": 0.40,
                        "activation": 0.20,
                        "interaction": 0.20,
                        "favorability": 0.20,
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
    """Create a frozen KnowledgeSession exposing default Luck knowledge."""
    assets = build_default_luck_knowledge()
    module = ModuleView(
        module_id=MODULE_ID,
        version=KNOWLEDGE_VERSION,
        assets=REQUIRED_ASSETS,
        metadata={"domain": "luck"},
    )
    return InMemoryKnowledgeSession(
        modules={MODULE_ID: module},
        assets=assets,
    )

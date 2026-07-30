"""Deterministic default ShenSha Knowledge pack served via Knowledge SDK."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.shensha_engine.knowledge_access import (
    ASSET_CALCULATION_REFERENCES,
    ASSET_COMPATIBILITY,
    ASSET_CONFIDENCE,
    ASSET_EXCEPTIONS,
    ASSET_IDENTITIES,
    ASSET_INTERACTIONS,
    ASSET_LOOKUP_TABLES,
    ASSET_MAPPING_TABLES,
    ASSET_PRIORITY,
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


def build_default_shensha_knowledge() -> dict[str, AssetView]:
    """Build the default frozen asset set for shensha_knowledge."""
    # Tian Yi Gui Ren by day stem -> noble branches
    tianyi = {
        "Giáp": ["Sửu", "Mùi"],
        "Ất": ["Tý", "Thân"],
        "Bính": ["Hợi", "Dậu"],
        "Đinh": ["Hợi", "Dậu"],
        "Mậu": ["Sửu", "Mùi"],
        "Kỷ": ["Tý", "Thân"],
        "Canh": ["Ngọ", "Dần"],
        "Tân": ["Ngọ", "Dần"],
        "Nhâm": ["Tỵ", "Mão"],
        "Quý": ["Tỵ", "Mão"],
        "Jia": ["Chou", "Wei"],
        "Yi": ["Zi", "Shen"],
        "Bing": ["Hai", "You"],
        "Ding": ["Hai", "You"],
        "Wu": ["Chou", "Wei"],
        "Ji": ["Zi", "Shen"],
        "Geng": ["Wu", "Yin"],
        "Xin": ["Wu", "Yin"],
        "Ren": ["Si", "Mao"],
        "Gui": ["Si", "Mao"],
    }

    # Yang Ren (Blade) by day stem
    yangren = {
        "Giáp": "Mão",
        "Bính": "Ngọ",
        "Mậu": "Ngọ",
        "Canh": "Dậu",
        "Nhâm": "Tý",
        "Jia": "Mao",
        "Bing": "Wu",
        "Wu": "Wu",
        "Geng": "You",
        "Ren": "Zi",
    }

    # Tao Hua by year branch triad group (Vietnamese branch names).
    taohua = {
        "Thân": "Dậu",
        "Tý": "Dậu",
        "Thìn": "Dậu",
        "Dần": "Mão",
        "Ngọ": "Mão",
        "Tuất": "Mão",
        "Tỵ": "Ngọ",
        "Dậu": "Ngọ",
        "Sửu": "Ngọ",
        "Hợi": "Tý",
        "Mão": "Tý",
        "Mùi": "Tý",
    }

    # Yi Ma by year branch triad group (Vietnamese branch names).
    yima = {
        "Thân": "Dần",
        "Tý": "Dần",
        "Thìn": "Dần",
        "Dần": "Thân",
        "Ngọ": "Thân",
        "Tuất": "Thân",
        "Tỵ": "Hợi",
        "Dậu": "Hợi",
        "Sửu": "Hợi",
        "Hợi": "Tỵ",
        "Mão": "Tỵ",
        "Mùi": "Tỵ",
    }

    return {
        ASSET_CALCULATION_REFERENCES: AssetView(
            asset_id=ASSET_CALCULATION_REFERENCES,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "anchors": [
                        {
                            "anchor_id": "day_stem",
                            "source": "stems.day",
                            "fallback": "day_master",
                        },
                        {
                            "anchor_id": "year_branch",
                            "source": "branches.year",
                        },
                        {
                            "anchor_id": "day_branch",
                            "source": "branches.day",
                        },
                    ]
                }
            ),
        ),
        ASSET_LOOKUP_TABLES: AssetView(
            asset_id=ASSET_LOOKUP_TABLES,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "tables": [
                        {
                            "table_id": "tianyi_guiren",
                            "anchor_id": "day_stem",
                            "match_mode": "branch_in_list",
                            "lookup": tianyi,
                        },
                        {
                            "table_id": "yangren",
                            "anchor_id": "day_stem",
                            "match_mode": "branch_equals",
                            "lookup": yangren,
                        },
                        {
                            "table_id": "taohua",
                            "anchor_id": "year_branch",
                            "match_mode": "branch_equals",
                            "lookup": taohua,
                        },
                        {
                            "table_id": "yima",
                            "anchor_id": "year_branch",
                            "match_mode": "branch_equals",
                            "lookup": yima,
                        },
                    ]
                }
            ),
        ),
        ASSET_MAPPING_TABLES: AssetView(
            asset_id=ASSET_MAPPING_TABLES,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "mappings": {
                        "tianyi_guiren": {
                            "shensha_id": "tianyi_guiren",
                            "polarity": "auspicious",
                        },
                        "yangren": {
                            "shensha_id": "yangren",
                            "polarity": "inauspicious",
                        },
                        "taohua": {
                            "shensha_id": "taohua",
                            "polarity": "conditional",
                        },
                        "yima": {
                            "shensha_id": "yima",
                            "polarity": "auspicious",
                        },
                    }
                }
            ),
        ),
        ASSET_IDENTITIES: AssetView(
            asset_id=ASSET_IDENTITIES,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "identities": {
                        "tianyi_guiren": {
                            "label": "Tian Yi Gui Ren",
                            "vi": "Thiên Ất Quý Nhân",
                            "default_polarity": "auspicious",
                        },
                        "yangren": {
                            "label": "Yang Ren",
                            "vi": "Dương Nhẫn",
                            "default_polarity": "inauspicious",
                        },
                        "taohua": {
                            "label": "Tao Hua",
                            "vi": "Đào Hoa",
                            "default_polarity": "conditional",
                        },
                        "yima": {
                            "label": "Yi Ma",
                            "vi": "Dịch Mã",
                            "default_polarity": "auspicious",
                        },
                    }
                }
            ),
        ),
        ASSET_INTERACTIONS: AssetView(
            asset_id=ASSET_INTERACTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "pairs": [
                        {
                            "left": "tianyi_guiren",
                            "right": "yangren",
                            "relation": "mitigation",
                            "effect": "soften_inauspicious",
                            "priority": 80,
                        },
                        {
                            "left": "taohua",
                            "right": "yima",
                            "relation": "amplify",
                            "effect": "mobility_romance",
                            "priority": 60,
                        },
                    ]
                }
            ),
        ),
        ASSET_COMPATIBILITY: AssetView(
            asset_id=ASSET_COMPATIBILITY,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rows": [
                        {
                            "shensha_id": "tianyi_guiren",
                            "compatibility": "supportive",
                        },
                        {
                            "shensha_id": "yangren",
                            "compatibility": "volatile",
                        },
                        {
                            "shensha_id": "taohua",
                            "compatibility": "contextual",
                        },
                        {
                            "shensha_id": "yima",
                            "compatibility": "supportive",
                        },
                    ]
                }
            ),
        ),
        ASSET_EXCEPTIONS: AssetView(
            asset_id=ASSET_EXCEPTIONS,
            version=KNOWLEDGE_VERSION,
            data=_freeze(
                {
                    "rules": [
                        {
                            "shensha_id": "yangren",
                            "when_strength": "weak",
                            "action": "suppress",
                            "reason_code": "weak_day_master_suppress_blade",
                            "priority": 90,
                        },
                        {
                            "shensha_id": "taohua",
                            "when_combination_has_clash": True,
                            "action": "qualify",
                            "reason_code": "clash_qualifies_peach_blossom",
                            "priority": 70,
                        },
                    ]
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
                            "effect": "amplify_auspicious",
                            "priority": 40,
                        },
                        {
                            "dimension": "combination",
                            "has_clash": True,
                            "effect": "stress_context",
                            "priority": 35,
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
                    "shensha_priority": {
                        "tianyi_guiren": 100,
                        "yangren": 90,
                        "yima": 80,
                        "taohua": 70,
                    },
                    "status_priority": {
                        "active": 0,
                        "qualified": 1,
                        "suppressed": 2,
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
                        "presence": 0.40,
                        "interaction": 0.20,
                        "compatibility": 0.15,
                        "exception": 0.15,
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
    """Create a frozen KnowledgeSession exposing default ShenSha knowledge."""
    assets = build_default_shensha_knowledge()
    module = ModuleView(
        module_id=MODULE_ID,
        version=KNOWLEDGE_VERSION,
        assets=REQUIRED_ASSETS,
        metadata={"domain": "shensha"},
    )
    return InMemoryKnowledgeSession(
        modules={MODULE_ID: module},
        assets=assets,
    )

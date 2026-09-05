"""DI-18 Life Optimization constants. No scoring weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import (
    LIFE_OPTIMIZATION_RULESET_VERSION,
    PUBLISHED_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.domain_interpretation.constants import MAIN_DOMAIN_IDS
from engines.detailed_interpretation_engine.enums import PriorityTier

MAIN_OPTIMIZATION_IDS: tuple[str, ...] = MAIN_DOMAIN_IDS
KNOWN_OPTIMIZATION_IDS: frozenset[str] = frozenset(PUBLISHED_DOMAIN_IDS)

ACTION_TYPES: frozenset[str] = frozenset(
    {
        "strengthen",
        "reduce",
        "protect",
        "stabilize",
        "release",
        "support",
        "convert",
        "retain",
        "recover",
        "develop",
        "avoid",
        "monitor",
    }
)

ACTION_STATES: frozenset[str] = frozenset(
    {
        "strongly_recommended",
        "recommended",
        "conditional",
        "optional",
        "avoid",
        "monitor",
        "unresolved",
    }
)

TIME_SCOPES: frozenset[str] = frozenset(
    {
        "natal_long_term",
        "current_luck_cycle",
        "current_annual",
    }
)

PRIORITY_VALUES: frozenset[str] = frozenset(item.value for item in PriorityTier)

SATURATION_STATES: frozenset[str] = frozenset({"overloaded", "peak"})

LEAKAGE_DOMAINS: frozenset[str] = frozenset(
    {"wealth", "relationship", "legacy", "vitality"}
)

CONVERSION_BRIDGES: dict[str, tuple[str, str]] = {
    "career": ("skill", "role"),
    "wealth": ("production", "economic_value"),
    "relationship": ("compatibility", "stability"),
    "legacy": ("creation", "transmission"),
    "vitality": ("capacity", "sustainable_function"),
}

ELEMENT_FUNCTIONS: dict[str, tuple[str, ...]] = {
    "Mộc": ("growth", "planning", "development", "learning", "flexibility"),
    "Hỏa": ("activation", "warmth", "visibility", "communication", "leadership_expression"),
    "Thổ": ("stability", "systems", "retention", "continuity", "discipline"),
    "Kim": ("precision", "rules", "execution", "quality_control"),
    "Thủy": ("adaptation", "recovery", "information", "flow", "reflection"),
}

ELEMENT_TOKENS: tuple[str, ...] = ("Kim", "Mộc", "Thủy", "Hỏa", "Thổ")

# Evaluation order inside an evidence floor. Does not rerank DI-07.
CATEGORY_RANK: dict[str, int] = {
    "saturation": 0,
    "critical_risk": 1,
    "leakage": 2,
    "bottleneck": 3,
    "useful_god": 4,
    "domain_bottleneck": 5,
    "opportunity": 6,
    "element_support": 7,
    "shen_sha": 8,
}

OVERLOAD_AVOID_KEYS: frozenset[str] = frozenset(
    {
        "opt.career.strengthen_workload",
        "opt.career.increase_output",
        "opt.career.expand_responsibility",
        "opt.authority.increase_exposure",
        "opt.authority.strengthen_command",
        "opt.wealth.aggressive_investment",
        "opt.wealth.expand_aggressively",
    }
)

FORBIDDEN_ACTION_KEYS: frozenset[str] = frozenset(
    {
        "wear_red",
        "live_near_water",
        "buy_plants",
        "medical_treatment",
        "medication",
        "diagnosis",
        "buy_securities",
        "sell_securities",
        "leverage",
        "borrow_amount",
        "legal_evasion",
        "political_tactics",
    }
)

FORBIDDEN_CUSTOMER_TOKENS: tuple[str, ...] = (
    "mặc đỏ",
    "wear red",
    "sống gần nước",
    "mua cây",
    "chẩn đoán",
    "điều trị",
    "uống thuốc",
    "mua cổ phiếu",
    "bán khống",
    "đòn bẩy",
    "vay đúng",
    "chắc chắn giàu",
    "chắc chắn thăng chức",
)

__all__ = ["LIFE_OPTIMIZATION_RULESET_VERSION"]

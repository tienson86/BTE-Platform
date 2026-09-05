"""DI-11 Temporal Activation constants. No scoring weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import (
    PUBLISHED_DOMAIN_IDS,
    TEMPORAL_ACTIVATION_RULESET_VERSION,
    TEMPORAL_LAYER_PARENT,
)
from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    KNOWN_DOMAIN_IDS,
    MAIN_DOMAIN_IDS,
    SUPPORT_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.luck_activation.constants import (
    ACTIVATION_DRIVER_IDS,
    GOD_TO_FAMILY,
)

__all__ = ["TEMPORAL_ACTIVATION_RULESET_VERSION"]

ANNUAL_SOURCE_PATH: str = "engines.luck_engine.providers.liunian.DefaultLiunianProvider"

REQUESTED_RUNTIME_LAYERS: tuple[str, ...] = ("luck_cycle", "annual")
CONTRACT_SHELL_LAYERS: tuple[str, ...] = ("monthly", "daily", "hourly")
KNOWN_LAYER_IDS: frozenset[str] = frozenset(TEMPORAL_LAYER_PARENT)
PARENT_OF: dict[str, str] = dict(TEMPORAL_LAYER_PARENT)

MAIN_TEMPORAL_IDS: tuple[str, ...] = MAIN_DOMAIN_IDS
SUPPORT_TEMPORAL_IDS: tuple[str, ...] = SUPPORT_DOMAIN_IDS
KNOWN_TEMPORAL_IDS: frozenset[str] = KNOWN_DOMAIN_IDS
PUBLISHED_TEMPORAL_IDS: tuple[str, ...] = PUBLISHED_DOMAIN_IDS

MODIFIER_EFFECTS: frozenset[str] = frozenset(
    {
        "activate",
        "strengthen",
        "weaken",
        "suppress",
        "stress",
        "recover",
        "accelerate",
        "delay",
        "stabilize",
        "destabilize",
        "open_condition",
        "block_condition",
    }
)

EXPRESSION_STATES: frozenset[str] = frozenset(
    {
        "dormant",
        "suppressed",
        "weak",
        "moderate",
        "active",
        "strong",
        "peak",
        "overloaded",
        "blocked",
        "recovering",
        "transition",
        "conditional",
        "unresolved",
    }
)

TEMPORAL_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "annual_officer",
        "annual_killer",
        "annual_wealth",
        "annual_output",
        "annual_resource",
        "annual_peer",
        "annual_useful_god",
        "annual_element_support",
        "annual_element_drain",
        "annual_element_control",
        "annual_clash_pressure",
        "not_applicable",
        "unresolved",
    }
)

TEMPORAL_BOTTLENECK_IDS: frozenset[str] = frozenset(
    {
        "annual_carrying_capacity",
        "annual_parent_overload",
        "annual_officer_pressure",
        "annual_peer_pressure",
        "annual_output_vs_officer",
        "none",
        "not_applicable",
    }
)

GOD_TO_ANNUAL_DRIVER: dict[str, str] = {
    "zheng_guan": "annual_officer",
    "qi_sha": "annual_killer",
    "zheng_cai": "annual_wealth",
    "pian_cai": "annual_wealth",
    "shi_shen": "annual_output",
    "shang_guan": "annual_output",
    "zheng_yin": "annual_resource",
    "pian_yin": "annual_resource",
    "bi_jian": "annual_peer",
    "jie_cai": "annual_peer",
}

FORBIDDEN_DRIVER_IDS: frozenset[str] = ACTIVATION_DRIVER_IDS | frozenset(
    {
        "hybrid",
        "mixed",
        "communication",
        "resilience",
        "career",
        "authority",
        "wealth",
        "relationship",
        "legacy",
        "vitality",
        "creative",
        "academic",
        "leadership",
        "management",
        "learning",
        "personal_growth",
    }
)

RELATION_KINDS: frozenset[str] = frozenset(
    {
        "generation",
        "control",
        "combination",
        "clash",
        "punishment",
        "harm",
        "break",
    }
)

ELEMENT_GENERATES: dict[str, str] = {
    "Mộc": "Hỏa",
    "Hỏa": "Thổ",
    "Thổ": "Kim",
    "Kim": "Thủy",
    "Thủy": "Mộc",
}

ELEMENT_CONTROLS: dict[str, str] = {
    "Mộc": "Thổ",
    "Thổ": "Thủy",
    "Thủy": "Hỏa",
    "Hỏa": "Kim",
    "Kim": "Mộc",
}

EXPRESSION_RANK: dict[str, int] = {
    "dormant": 0,
    "blocked": 0,
    "unresolved": 0,
    "suppressed": 1,
    "weak": 1,
    "recovering": 2,
    "transition": 2,
    "conditional": 2,
    "moderate": 3,
    "active": 3,
    "strong": 4,
    "overloaded": 4,
    "peak": 5,
}

GOD_FAMILIES: dict[str, str] = GOD_TO_FAMILY

LEVELS: tuple[str, ...] = ("none", "low", "moderate", "high", "excessive")

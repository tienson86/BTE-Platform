"""DI-09 Luck Activation constants. No scoring weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import (
    LUCK_ACTIVATION_RULESET_VERSION,
    PUBLISHED_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    KNOWN_DOMAIN_IDS,
    MAIN_DOMAIN_IDS,
    SUPPORT_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.enums import ActivationState

__all__ = ["LUCK_ACTIVATION_RULESET_VERSION"]

ACTIVATION_CYCLE_KIND: str = "dai_van"

MAIN_ACTIVATION_IDS: tuple[str, ...] = MAIN_DOMAIN_IDS
SUPPORT_ACTIVATION_IDS: tuple[str, ...] = SUPPORT_DOMAIN_IDS
KNOWN_ACTIVATION_IDS: frozenset[str] = KNOWN_DOMAIN_IDS
PUBLISHED_ACTIVATION_IDS: tuple[str, ...] = PUBLISHED_DOMAIN_IDS

ACTIVATION_TYPES: frozenset[str] = frozenset(
    {
        "activation",
        "suppression",
        "acceleration",
        "delay",
        "support",
        "stress",
        "recovery",
        "opportunity",
        "restriction",
        "damage_activation",
        "rescue_activation",
    }
)

ACTIVATION_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "temporal_officer",
        "temporal_killer",
        "temporal_wealth",
        "temporal_output",
        "temporal_resource",
        "temporal_peer",
        "temporal_useful_god",
        "temporal_element_support",
        "temporal_element_drain",
        "temporal_element_control",
        "not_applicable",
        "unresolved",
    }
)

GOD_TO_FAMILY: dict[str, str] = {
    "zheng_guan": "officer",
    "qi_sha": "officer",
    "zheng_cai": "wealth",
    "pian_cai": "wealth",
    "shi_shen": "output",
    "shang_guan": "output",
    "zheng_yin": "resource",
    "pian_yin": "resource",
    "bi_jian": "peer",
    "jie_cai": "peer",
}

GOD_TO_DRIVER: dict[str, str] = {
    "zheng_guan": "temporal_officer",
    "qi_sha": "temporal_killer",
    "zheng_cai": "temporal_wealth",
    "pian_cai": "temporal_wealth",
    "shi_shen": "temporal_output",
    "shang_guan": "temporal_output",
    "zheng_yin": "temporal_resource",
    "pian_yin": "temporal_resource",
    "bi_jian": "temporal_peer",
    "jie_cai": "temporal_peer",
}

DOMAIN_SUPPORT_FAMILIES: dict[str, frozenset[str]] = {
    "authority": frozenset({"officer", "resource", "wealth"}),
    "career": frozenset({"officer", "output", "resource", "wealth"}),
    "wealth": frozenset({"wealth", "output"}),
    "relationship": frozenset({"output", "resource"}),
    "legacy": frozenset({"resource", "output", "wealth"}),
    "vitality": frozenset({"resource"}),
    "creative": frozenset({"output"}),
    "academic": frozenset({"resource"}),
    "leadership": frozenset({"officer"}),
    "management": frozenset({"officer", "resource"}),
    "learning": frozenset({"resource"}),
    "personal_growth": frozenset({"resource", "output"}),
}

DOMAIN_STRESS_FAMILIES: dict[str, frozenset[str]] = {
    "authority": frozenset({"output"}),
    "career": frozenset({"peer"}),
    "wealth": frozenset({"peer"}),
    "relationship": frozenset({"peer", "officer"}),
    "legacy": frozenset({"peer"}),
    "vitality": frozenset({"officer", "peer", "output"}),
    "creative": frozenset({"resource"}),
    "academic": frozenset({"output"}),
    "leadership": frozenset({"output"}),
    "management": frozenset({"peer"}),
    "learning": frozenset({"output"}),
    "personal_growth": frozenset({"peer"}),
}

OVERLOAD_DOMAINS: frozenset[str] = frozenset({"authority", "career", "vitality"})

LEVEL_RANK: dict[str, int] = {
    "none": 0,
    "low": 1,
    "moderate": 2,
    "high": 3,
    "excessive": 4,
}

STATE_RANK: dict[ActivationState, int] = {
    ActivationState.DORMANT: 0,
    ActivationState.WEAK: 1,
    ActivationState.MODERATE: 2,
    ActivationState.CONDITIONAL: 2,
    ActivationState.STRONG: 3,
    ActivationState.PEAK: 4,
    ActivationState.OVERLOADED: 3,
    ActivationState.SUPPRESSED: 1,
    ActivationState.BLOCKED: 0,
    ActivationState.UNRESOLVED: 0,
}

NATAL_STRONG: frozenset[str] = frozenset({"very_strong", "strong"})
NATAL_LIMITED: frozenset[str] = frozenset({"conditional", "fragmented", "weak"})
NATAL_MISSING: frozenset[str] = frozenset({"unresolved", "blocked", "not_evaluated"})

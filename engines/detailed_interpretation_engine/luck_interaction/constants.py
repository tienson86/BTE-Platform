"""DI-10 Luck Interaction constants. No scoring weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import LUCK_INTERACTION_RULESET_VERSION
from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    KNOWN_DOMAIN_IDS,
    MAIN_DOMAIN_IDS,
    SUPPORT_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.enums import ActivationState

__all__ = ["LUCK_INTERACTION_RULESET_VERSION"]

INTERACTION_CYCLE_KIND: str = "dai_van"

MAIN_INTERACTION_IDS: tuple[str, ...] = MAIN_DOMAIN_IDS
SUPPORT_INTERACTION_IDS: tuple[str, ...] = SUPPORT_DOMAIN_IDS
KNOWN_INTERACTION_IDS: frozenset[str] = KNOWN_DOMAIN_IDS

INTERACTION_TYPES: frozenset[str] = frozenset(
    {
        "support",
        "conflict",
        "trade_off",
        "reinforcement",
        "competition",
        "resource_shift",
        "stress_transfer",
        "conditional_dependency",
        "blocked_expression",
        "unresolved",
    }
)

GRAPH_RELATIONS: frozenset[str] = frozenset(
    {
        "supports",
        "conflicts",
        "competes",
        "reinforces",
        "depends_on",
        "stresses",
        "recovers",
    }
)

TYPE_TO_RELATION: dict[str, str] = {
    "support": "supports",
    "conflict": "conflicts",
    "trade_off": "competes",
    "reinforcement": "reinforces",
    "competition": "competes",
    "resource_shift": "depends_on",
    "stress_transfer": "stresses",
    "conditional_dependency": "depends_on",
    "blocked_expression": "depends_on",
}

STRENGTH_RANK: dict[str, int] = {
    "none": 0,
    "low": 1,
    "moderate": 2,
    "high": 3,
    "dominant": 4,
}

SITUATION_IDS: frozenset[str] = frozenset(
    {
        "career_expansion",
        "creative_expansion",
        "authority_consolidation",
        "learning_phase",
        "resource_pressure",
        "relationship_stress",
        "recovery_phase",
        "transition_phase",
        "balanced_growth",
        "blocked_growth",
        "unresolved",
        "not_applicable",
    }
)

ENGAGED_STATES: frozenset[ActivationState] = frozenset(
    {
        ActivationState.WEAK,
        ActivationState.MODERATE,
        ActivationState.STRONG,
        ActivationState.PEAK,
        ActivationState.OVERLOADED,
        ActivationState.SUPPRESSED,
        ActivationState.CONDITIONAL,
    }
)

LOUD_STATES: frozenset[ActivationState] = frozenset(
    {
        ActivationState.STRONG,
        ActivationState.PEAK,
        ActivationState.OVERLOADED,
        ActivationState.CONDITIONAL,
    }
)

QUIET_STATES: frozenset[ActivationState] = frozenset(
    {
        ActivationState.DORMANT,
        ActivationState.WEAK,
        ActivationState.SUPPRESSED,
    }
)

STRESSED_STATES: frozenset[ActivationState] = frozenset({ActivationState.OVERLOADED})
DRIVER_SENTINELS: frozenset[str] = frozenset({"", "not_applicable", "none", "unresolved"})

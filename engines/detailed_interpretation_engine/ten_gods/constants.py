"""Canonical Ten God IDs and structured expression catalogs.

IDs are consumed from the Ten Gods identity engine. Expressions are codes, not prose.
"""

from __future__ import annotations

from engines.ten_gods_engine.constants import (
    GOD_ID_TO_FAMILY,
    GOD_ID_TO_LABEL,
    LABEL_TO_GOD_ID,
    TEN_GOD_IDS,
)

CANONICAL_TEN_GOD_IDS: tuple[str, ...] = TEN_GOD_IDS
FORBIDDEN_ALIAS_IDS: frozenset[str] = frozenset({"thien_quan", "thienquan"})

PILLAR_STEM_LAYER: dict[str, str] = {
    "year": "year_stem",
    "month": "month_stem",
    "day": "day_context",
    "hour": "hour_stem",
}

HIDDEN_LAYER_BY_POSITION: dict[str, str] = {
    "primary": "main_qi",
    "1": "main_qi",
    "secondary": "middle_qi",
    "2": "middle_qi",
    "tertiary": "residual_qi",
    "3": "residual_qi",
}

DAY_MASTER_LABELS: frozenset[str] = frozenset({"Nhật Chủ", "Nhat Chu", "day_master"})

WEAK_STRENGTH_LEVELS: frozenset[str] = frozenset(
    {"extremely_weak", "very_weak", "weak", "than_nhuoc", "nhược", "nhuoc"}
)
STRONG_STRENGTH_LEVELS: frozenset[str] = frozenset(
    {"strong", "very_strong", "extremely_strong", "than_vuong", "vượng", "vuong"}
)
MODERATE_STRENGTH_LEVELS: frozenset[str] = frozenset(
    {"balanced", "moderate", "trung_hoa", "trung"}
)

POSITIVE_CODES: dict[str, tuple[str, ...]] = {
    "bi_jian": (
        "self_reliance",
        "persistence",
        "independence",
        "peer_equality",
        "execution_capacity",
        "carrying_capacity_support",
    ),
    "jie_cai": (
        "competitiveness",
        "boldness",
        "initiative",
        "peer_mobilization",
        "risk_tolerance",
        "entrepreneurial_drive",
    ),
    "shi_shen": (
        "production",
        "stable_expression",
        "skill",
        "creativity",
        "product_creation",
    ),
    "shang_guan": (
        "innovation",
        "critical_thinking",
        "expression",
        "commercial_creativity",
        "public_visibility",
    ),
    "pian_cai": (
        "opportunity_recognition",
        "flexible_resource_use",
        "commercial_activity",
        "expansion",
        "entrepreneurship",
    ),
    "zheng_cai": (
        "disciplined_resource_management",
        "stable_income_orientation",
        "accumulation",
        "financial_responsibility",
        "operational_management",
    ),
    "qi_sha": (
        "pressure_tolerance",
        "decisiveness",
        "command",
        "leadership",
        "high_responsibility_execution",
    ),
    "zheng_guan": (
        "responsibility",
        "organizational_discipline",
        "formal_structure",
        "management",
        "institutional_fit",
    ),
    "pian_yin": (
        "specialized_learning",
        "unconventional_knowledge",
        "research",
        "technical_specialization",
        "independent_cognition",
    ),
    "zheng_yin": (
        "structured_knowledge",
        "learning",
        "support",
        "protection",
        "mediation",
    ),
}

RISK_CODES: dict[str, tuple[str, ...]] = {
    "bi_jian": ("excessive_self_focus", "competition", "resistance_to_control", "resource_division"),
    "jie_cai": ("financial_competition", "resource_leakage", "impulsive_expansion", "excessive_rivalry"),
    "shi_shen": ("excessive_drain", "over_comfort", "weakened_discipline"),
    "shang_guan": ("authority_conflict", "excessive_criticism", "instability", "over_expression"),
    "pian_cai": ("volatility", "opportunism_without_retention", "overextension"),
    "zheng_cai": ("material_pressure", "excessive_material_responsibility", "rigidity"),
    "qi_sha": ("excessive_pressure", "conflict", "control_burden"),
    "zheng_guan": ("overconstraint", "pressure", "authority_conflict"),
    "pian_yin": ("over_isolation", "excessive_internalization", "output_suppression"),
    "zheng_yin": ("over_support", "reduced_output", "dependence"),
}

CONDITION_MC01_NOT_BOUND: str = "mc01_reference_not_bound"
CONDITION_HOUR_INCOMPLETE: str = "hour_pillar_incomplete"
CONDITION_PATTERN_UNRESOLVED: str = "pattern_context_unresolved"
CONDITION_USEFUL_GOD_UNRESOLVED: str = "useful_god_unresolved"

__all__ = [
    "CANONICAL_TEN_GOD_IDS",
    "CONDITION_HOUR_INCOMPLETE",
    "CONDITION_MC01_NOT_BOUND",
    "CONDITION_PATTERN_UNRESOLVED",
    "CONDITION_USEFUL_GOD_UNRESOLVED",
    "DAY_MASTER_LABELS",
    "FORBIDDEN_ALIAS_IDS",
    "GOD_ID_TO_FAMILY",
    "GOD_ID_TO_LABEL",
    "HIDDEN_LAYER_BY_POSITION",
    "LABEL_TO_GOD_ID",
    "MODERATE_STRENGTH_LEVELS",
    "PILLAR_STEM_LAYER",
    "POSITIVE_CODES",
    "RISK_CODES",
    "STRONG_STRENGTH_LEVELS",
    "WEAK_STRENGTH_LEVELS",
]

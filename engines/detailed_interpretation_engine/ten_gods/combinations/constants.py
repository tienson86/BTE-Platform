"""DI-02 V1 combination IDs and evaluation specs. Codes only."""

from __future__ import annotations

from dataclasses import dataclass

from engines.detailed_interpretation_engine.ten_gods.constants import GOD_ID_TO_FAMILY

CONDITION_UNRESOLVED_DEPENDENCY: str = "unresolved_dependency"
CONDITION_MC01_NOT_BOUND: str = "mc01_reference_not_bound"
CONDITION_RESIDUAL_ONLY: str = "residual_co_presence"
CONDITION_MEDIATED_REACH: str = "mediated_reach"
CONDITION_DAY_MASTER_MISMATCH: str = "day_master_band_mismatch"

FAMILY_MEMBERS: dict[str, tuple[str, ...]] = {
    "companion": ("bi_jian", "jie_cai"),
    "output": ("shi_shen", "shang_guan"),
    "wealth": ("pian_cai", "zheng_cai"),
    "officer": ("qi_sha", "zheng_guan"),
    "resource": ("pian_yin", "zheng_yin"),
}

ECOSYSTEM_FAMILY: dict[str, str] = {
    "companion": "peer",
    "output": "output",
    "wealth": "wealth",
    "officer": "authority",
    "resource": "resource",
}

V1_COMBINATION_IDS: tuple[str, ...] = (
    "shi_shen_generates_wealth",
    "shang_guan_generates_wealth",
    "wealth_generates_officer",
    "officer_generates_resource",
    "wealth_officer_resource_chain",
    "killer_resource_day_master_chain",
    "hurting_officer_meets_officer",
    "owl_robs_food_combination",
    "peer_competes_wealth",
    "officer_killer_mixed",
    "wealth_exceeds_day_master",
    "killer_exceeds_day_master",
    "resource_strong_day_master_strong",
    "strong_day_master_uses_wealth",
    "strong_day_master_uses_officer",
    "strong_day_master_uses_output",
    "weak_day_master_uses_resource",
    "weak_day_master_uses_peer",
)

TICKET_ALIASES: dict[str, str] = {
    "officer_generates_seal": "officer_generates_resource",
    "wealth_officer_seal_chain": "wealth_officer_resource_chain",
    "sha_yin_mutual_generation": "killer_resource_day_master_chain",
    "hurting_officer_attacks_officer": "hurting_officer_meets_officer",
    "owl_robs_food": "owl_robs_food_combination",
    "peer_robs_wealth": "peer_competes_wealth",
    "mixed_officer_killer": "officer_killer_mixed",
    "wealth_overloads_weak_day_master": "wealth_exceeds_day_master",
    "killer_overloads_weak_day_master": "killer_exceeds_day_master",
    "seal_excess_strong_day_master": "resource_strong_day_master_strong",
    "weak_day_master_uses_seal": "weak_day_master_uses_resource",
}

POSITIVE_CODES: dict[str, tuple[str, ...]] = {
    "shi_shen_generates_wealth": ("convert_skill_to_value", "stable_value_creation"),
    "shang_guan_generates_wealth": ("innovation_monetization", "entrepreneurship"),
    "wealth_generates_officer": ("resources_support_responsibility", "commercial_results_support_authority"),
    "officer_generates_resource": ("responsibility_creates_support", "formal_structure_becomes_sustainable"),
    "wealth_officer_resource_chain": ("institutional_continuity", "structured_career_flow"),
    "killer_resource_day_master_chain": ("pressure_transformed_into_capability", "disciplined_learning"),
    "hurting_officer_meets_officer": ("innovation", "entrepreneurship"),
    "owl_robs_food_combination": ("specialized_learning",),
    "peer_competes_wealth": ("carrying_capacity_support",),
    "officer_killer_mixed": ("command_with_formality",),
    "wealth_exceeds_day_master": ("financial_opportunity",),
    "killer_exceeds_day_master": ("high_responsibility_environment",),
    "resource_strong_day_master_strong": ("learning", "technical_depth"),
    "strong_day_master_uses_wealth": ("capacity_can_carry_wealth",),
    "strong_day_master_uses_officer": ("discipline_organizes_self_force",),
    "strong_day_master_uses_output": ("output_releases_self_force",),
    "weak_day_master_uses_resource": ("resource_restores_capacity",),
    "weak_day_master_uses_peer": ("peer_increases_carrying_capacity",),
}

RISK_CODES: dict[str, tuple[str, ...]] = {
    "shi_shen_generates_wealth": ("output_drains_weak_day_master", "retention_weaker_than_creation"),
    "shang_guan_generates_wealth": ("volatility", "authority_conflict_elsewhere"),
    "wealth_generates_officer": ("wealth_and_officer_pressure_weak_day_master",),
    "officer_generates_resource": ("resource_may_block_output",),
    "wealth_officer_resource_chain": ("intermediate_link_limits_flow",),
    "killer_resource_day_master_chain": ("pressure_before_transformation",),
    "hurting_officer_meets_officer": ("friction_with_formal_authority", "expression_versus_rules"),
    "owl_robs_food_combination": ("output_suppression", "over_analysis"),
    "peer_competes_wealth": ("resource_competition", "difficult_retention"),
    "officer_killer_mixed": ("mixed_authority_style",),
    "wealth_exceeds_day_master": ("carrying_capacity_strained",),
    "killer_exceeds_day_master": ("pressure_exceeds_capacity",),
    "resource_strong_day_master_strong": ("reduced_output", "over_support"),
    "strong_day_master_uses_wealth": ("unfavorable_if_wealth_is_avoided",),
    "strong_day_master_uses_officer": ("authority_unusable_if_damaged",),
    "strong_day_master_uses_output": ("under_discipline_if_officer_weak",),
    "weak_day_master_uses_resource": ("help_blocked_if_resource_is_avoided",),
    "weak_day_master_uses_peer": ("capacity_support_with_wealth_competition",),
}


@dataclass(frozen=True, slots=True)
class CombinationSpec:
    """One V1 combination framework. Not a dictionary meaning."""

    combination_id: str
    types: tuple[str, ...]
    kind: str
    causal_group: str
    source_god: str = ""
    source_family: str = ""
    target_god: str = ""
    target_family: str = ""
    mediator_family: str = ""
    chain_families: tuple[str, ...] = ()
    requires_mc01: str = ""
    dm_required: str = ""
    min_strength: str = ""
    mediation_family: str = ""


V1_SPECS: tuple[CombinationSpec, ...] = (
    CombinationSpec(
        "shi_shen_generates_wealth",
        ("generation_chain",),
        "generation",
        "output_generates_wealth",
        source_god="shi_shen",
        target_family="wealth",
    ),
    CombinationSpec(
        "shang_guan_generates_wealth",
        ("generation_chain",),
        "generation",
        "output_generates_wealth",
        source_god="shang_guan",
        target_family="wealth",
    ),
    CombinationSpec(
        "wealth_generates_officer",
        ("generation_chain",),
        "generation",
        "wealth_officer_resource",
        source_family="wealth",
        target_family="officer",
    ),
    CombinationSpec(
        "officer_generates_resource",
        ("generation_chain",),
        "generation",
        "wealth_officer_resource",
        source_family="officer",
        target_family="resource",
    ),
    CombinationSpec(
        "wealth_officer_resource_chain",
        ("generation_chain",),
        "chain",
        "wealth_officer_resource",
        chain_families=("wealth", "officer", "resource"),
    ),
    CombinationSpec(
        "killer_resource_day_master_chain",
        ("transformation_of_function", "rescue_chain"),
        "transform",
        "seal_transforms_killer",
        source_god="qi_sha",
        mediator_family="resource",
        requires_mc01="rescue",
    ),
    CombinationSpec(
        "hurting_officer_meets_officer",
        ("control_chain", "damage_chain"),
        "control",
        "hurting_officer_attacks_officer",
        source_god="shang_guan",
        target_god="zheng_guan",
        requires_mc01="damage",
        mediation_family="wealth",
    ),
    CombinationSpec(
        "owl_robs_food_combination",
        ("control_chain", "damage_chain", "blocked_chain"),
        "control",
        "owl_robs_food",
        source_god="pian_yin",
        target_god="shi_shen",
        requires_mc01="damage",
    ),
    CombinationSpec(
        "peer_competes_wealth",
        ("competition", "damage_chain"),
        "control",
        "peer_robs_wealth",
        source_family="companion",
        target_family="wealth",
        requires_mc01="damage",
    ),
    CombinationSpec(
        "officer_killer_mixed",
        ("mixed_structure",),
        "mixed",
        "mixed_officer_killer",
        source_god="zheng_guan",
        target_god="qi_sha",
        requires_mc01="purity",
    ),
    CombinationSpec(
        "wealth_exceeds_day_master",
        ("capacity_mismatch", "damage_chain"),
        "capacity",
        "wealth_overloads_weak_day_master",
        source_family="wealth",
        dm_required="weak",
        min_strength="strong",
        requires_mc01="damage",
    ),
    CombinationSpec(
        "killer_exceeds_day_master",
        ("capacity_mismatch", "damage_chain"),
        "capacity",
        "killer_overloads_weak_day_master",
        source_god="qi_sha",
        dm_required="weak",
        min_strength="strong",
        requires_mc01="damage",
    ),
    CombinationSpec(
        "resource_strong_day_master_strong",
        ("capacity_mismatch", "support_chain"),
        "capacity",
        "resource_overload",
        source_family="resource",
        dm_required="strong",
        min_strength="strong",
        requires_mc01="optional",
    ),
    CombinationSpec(
        "strong_day_master_uses_wealth",
        ("support_chain", "generation_chain"),
        "use",
        "strong_dm_uses_wealth",
        target_family="wealth",
        dm_required="strong",
    ),
    CombinationSpec(
        "strong_day_master_uses_officer",
        ("support_chain",),
        "use",
        "strong_dm_uses_officer",
        target_family="officer",
        dm_required="strong",
    ),
    CombinationSpec(
        "strong_day_master_uses_output",
        ("support_chain", "drain_chain"),
        "use",
        "strong_dm_uses_output",
        target_family="output",
        dm_required="strong",
    ),
    CombinationSpec(
        "weak_day_master_uses_resource",
        ("support_chain", "rescue_chain"),
        "use",
        "weak_dm_uses_resource",
        target_family="resource",
        dm_required="weak",
    ),
    CombinationSpec(
        "weak_day_master_uses_peer",
        ("support_chain", "competition"),
        "use",
        "weak_dm_uses_peer",
        target_family="companion",
        dm_required="weak",
    ),
)

assert tuple(spec.combination_id for spec in V1_SPECS) == V1_COMBINATION_IDS
assert GOD_ID_TO_FAMILY["shi_shen"] == "output"

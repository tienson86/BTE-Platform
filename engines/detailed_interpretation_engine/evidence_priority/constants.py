"""DI-07 categorical ranking constants. No numeric cross-tier weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import PriorityTier

EVIDENCE_PRIORITY_RULESET_VERSION: str = (
    "bte.detailed_interpretation.evidence_priority.rules.v1"
)

TIER_ORDER: tuple[PriorityTier, ...] = (
    PriorityTier.P0,
    PriorityTier.P1,
    PriorityTier.P2,
    PriorityTier.P3,
    PriorityTier.P4,
    PriorityTier.P5,
)

TIER_INDEX: dict[str, int] = {item.value: index for index, item in enumerate(TIER_ORDER)}

IMPORTANCE_BY_TIER: dict[str, str] = {
    PriorityTier.P0.value: "critical",
    PriorityTier.P1.value: "major",
    PriorityTier.P2.value: "important",
    PriorityTier.P3.value: "supporting",
    PriorityTier.P4.value: "context",
    PriorityTier.P5.value: "optional",
}

DOMAIN_ORDER: tuple[str, ...] = (
    "pattern",
    "integrity",
    "grade",
    "capacity",
    "authority",
    "wealth",
    "career",
    "academic",
    "creative",
    "protection",
    "risk",
    "relationship",
    "children",
    "health",
)

DOMAIN_INDEX: dict[str, int] = {item: index for index, item in enumerate(DOMAIN_ORDER)}

CATEGORY_ORDER: tuple[str, ...] = (
    "structural",
    "driver",
    "bottleneck",
    "risk",
    "opportunity",
    "condition",
    "warning",
    "combination",
    "balance",
    "cluster",
    "supporting",
)

CATEGORY_INDEX: dict[str, int] = {item: index for index, item in enumerate(CATEGORY_ORDER)}

SHEN_SHA_SOURCE_KINDS: frozenset[str] = frozenset(
    {"shen_sha", "shen_sha_cluster", "shen_sha_ecosystem"}
)

SHEN_SHA_TIER_CEILING: PriorityTier = PriorityTier.P2

CRITICAL_DAMAGE_SEVERITIES: frozenset[str] = frozenset({"critical"})
MAJOR_DAMAGE_SEVERITIES: frozenset[str] = frozenset({"major", "critical"})

MAJOR_COMBINATION_IDS: frozenset[str] = frozenset(
    {
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
    }
)

GOD_FAMILY_DOMAIN: dict[str, str] = {
    "zheng_yin": "academic",
    "pian_yin": "academic",
    "zheng_guan": "authority",
    "qi_sha": "authority",
    "zheng_cai": "wealth",
    "pian_cai": "wealth",
    "shi_shen": "creative",
    "shang_guan": "creative",
    "bi_jian": "capacity",
    "jie_cai": "capacity",
}

PATTERN_FAMILY_DOMAIN: dict[str, str] = {
    "Chính Ấn": "academic",
    "Thiên Ấn": "academic",
    "Chính Quan": "authority",
    "Thất Sát": "authority",
    "Chính Tài": "wealth",
    "Thiên Tài": "wealth",
    "Thực Thần": "creative",
    "Thương Quan": "creative",
    "Tỷ Kiên": "capacity",
    "Kiếp Tài": "capacity",
}

SOURCE_KIND_ORDER: tuple[str, ...] = (
    "pattern",
    "integrity",
    "grade",
    "damage",
    "rescue",
    "ten_gods_ecosystem",
    "achievement",
    "wealth",
    "career",
    "condition",
    "warning",
    "combination",
    "ten_god",
    "shen_sha_cluster",
    "shen_sha",
    "purity",
)

SOURCE_KIND_INDEX: dict[str, int] = {item: index for index, item in enumerate(SOURCE_KIND_ORDER)}

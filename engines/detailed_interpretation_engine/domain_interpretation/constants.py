"""DI-08 Domain Interpretation constants. No scoring weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import PUBLISHED_DOMAIN_IDS
from engines.detailed_interpretation_engine.enums import DomainState, PriorityTier
from engines.detailed_interpretation_engine.evidence_priority.constants import TIER_INDEX

DOMAIN_INTERPRETATION_RULESET_VERSION: str = (
    "bte.detailed_interpretation.domain.rules.v1"
)

MAIN_DOMAIN_IDS: tuple[str, ...] = PUBLISHED_DOMAIN_IDS

SUPPORT_DOMAIN_IDS: tuple[str, ...] = (
    "creative",
    "academic",
    "leadership",
    "management",
    "learning",
    "personal_growth",
)

KNOWN_DOMAIN_IDS: frozenset[str] = frozenset(MAIN_DOMAIN_IDS + SUPPORT_DOMAIN_IDS)

GRAPH_RELATIONS: frozenset[str] = frozenset(
    {"supports", "depends_on", "conflicts", "reinforces"}
)

HIGH_BANDS: frozenset[str] = frozenset({"very_high", "high", "above_average"})
LOW_BANDS: frozenset[str] = frozenset({"below_average", "low", "very_low"})
SPLIT_PAIRS: tuple[tuple[str, str], ...] = (
    ("wealth_creation", "wealth_retention"),
    ("wealth_creation", "wealth_accumulation"),
)

BAND_TO_STATE: dict[str, DomainState] = {
    "very_high": DomainState.VERY_STRONG,
    "high": DomainState.STRONG,
    "above_average": DomainState.STRONG,
    "moderate": DomainState.MODERATE,
    "average": DomainState.MODERATE,
    "below_average": DomainState.WEAK,
    "low": DomainState.WEAK,
    "very_low": DomainState.WEAK,
}

MAJOR_DAMAGE_TYPES: frozenset[str] = frozenset(
    {
        "resource_overload",
        "peer_robs_wealth",
        "hurting_officer_attacks_officer",
        "owl_robs_food",
        "wealth_overloads_weak_day_master",
        "killer_overloads_weak_day_master",
        "mixed_officer_killer",
    }
)

AUTHORITY_SCOPE: frozenset[str] = frozenset({"authority"})
CAREER_SCOPE: frozenset[str] = frozenset(
    {"career", "academic", "creative", "authority"}
)
WEALTH_SCOPE: frozenset[str] = frozenset({"wealth", "creative"})
RELATIONSHIP_SCOPE: frozenset[str] = frozenset({"relationship"})
LEGACY_SCOPE: frozenset[str] = frozenset({"academic", "creative", "children", "legacy"})
VITALITY_SCOPE: frozenset[str] = frozenset({"health", "capacity", "vitality"})

DOMAIN_SCOPES: dict[str, frozenset[str]] = {
    "authority": AUTHORITY_SCOPE,
    "career": CAREER_SCOPE,
    "wealth": WEALTH_SCOPE,
    "relationship": RELATIONSHIP_SCOPE,
    "legacy": LEGACY_SCOPE,
    "vitality": VITALITY_SCOPE,
    "creative": frozenset({"creative"}),
    "academic": frozenset({"academic"}),
    "leadership": frozenset({"authority", "career"}),
    "management": frozenset({"career"}),
    "learning": frozenset({"academic"}),
    "personal_growth": frozenset({"capacity", "academic"}),
}

OUTPUT_WEALTH_COMBINATIONS: frozenset[str] = frozenset(
    {
        "shi_shen_generates_wealth",
        "shang_guan_generates_wealth",
    }
)

PEER_WEALTH_COMBINATIONS: frozenset[str] = frozenset({"peer_competes_wealth"})

SHEN_SHA_SOURCE_KINDS: frozenset[str] = frozenset(
    {"shen_sha", "shen_sha_cluster", "shen_sha_ecosystem"}
)

HONG_LOAN_KEYS: frozenset[str] = frozenset(
    {"hong_luan", "hong_loan", "thien_hy", "thiên hỷ", "hồng loan"}
)

TIER_RANK: dict[str, int] = TIER_INDEX

DEFAULT_PRIORITY: str = PriorityTier.P3.value

SHARED_DRIVER_IDS: frozenset[str] = frozenset({"not_applicable", "unresolved"})

AUTHORITY_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "zheng_guan_primary",
        "qi_sha_yin_chain",
        "cai_sheng_guan",
        "guan_yin_chain",
        "management_structure",
        "professional_authority",
        "mixed",
    }
    | SHARED_DRIVER_IDS
)

CAREER_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "authority_management",
        "entrepreneurship",
        "technical_specialization",
        "academic_depth",
        "creative_output",
        "commercial_chain",
        "public_visibility",
        "hybrid",
    }
    | SHARED_DRIVER_IDS
)

WEALTH_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "output",
        "commercial",
        "authority",
        "technical",
        "creative",
        "management",
        "entrepreneurship",
        "hybrid",
    }
    | SHARED_DRIVER_IDS
)

RELATIONSHIP_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "compatibility",
        "trust",
        "communication",
        "commitment",
        "shared_growth",
        "mutual_support",
        "hybrid",
    }
    | SHARED_DRIVER_IDS
)

LEGACY_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "teaching",
        "knowledge",
        "creative",
        "business",
        "family",
        "community",
        "hybrid",
    }
    | SHARED_DRIVER_IDS
)

VITALITY_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "capacity",
        "recovery",
        "resilience",
        "energy",
        "hybrid",
    }
    | SHARED_DRIVER_IDS
)

DOMAIN_DRIVER_IDS: dict[str, frozenset[str]] = {
    "authority": AUTHORITY_DRIVER_IDS,
    "career": CAREER_DRIVER_IDS,
    "wealth": WEALTH_DRIVER_IDS,
    "relationship": RELATIONSHIP_DRIVER_IDS,
    "legacy": LEGACY_DRIVER_IDS,
    "vitality": VITALITY_DRIVER_IDS,
}

FORBIDDEN_AUTHORITY_DRIVER_IDS: frozenset[str] = frozenset(
    {"authority", "quyen_han", "quyền hạn", "quyenhan"}
)

FORBIDDEN_WEALTH_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "retention",
        "accumulation",
        "expansion",
        "volatility",
        "creation",
        "wealth_retention",
        "wealth_creation",
        "wealth_accumulation",
        "financial_volatility",
        "giu_tai",
        "tao_tai",
    }
)

FORBIDDEN_VITALITY_DRIVER_IDS: frozenset[str] = frozenset(
    {
        "stress",
        "stress_overload",
        "fatigue",
        "burnout",
        "career_overload",
        "career_pressure",
        "relationship_pressure",
        "resource_overload",
        "damage",
    }
    | MAJOR_DAMAGE_TYPES
)

CAI_SHENG_GUAN_COMBINATIONS: frozenset[str] = frozenset(
    {"wealth_generates_officer", "wealth_officer_resource_chain"}
)
QI_SHA_YIN_COMBINATIONS: frozenset[str] = frozenset(
    {"killer_resource_day_master_chain"}
)
GUAN_YIN_COMBINATIONS: frozenset[str] = frozenset(
    {"officer_generates_resource", "wealth_officer_resource_chain"}
)
DAMAGE_SOURCE_KINDS: frozenset[str] = frozenset({"damage", "warning"})
RISK_CATEGORIES: frozenset[str] = frozenset({"risk", "warning", "bottleneck"})

"""DI-04 ecosystem constants. Roles are structural, not dictionary labels."""

from __future__ import annotations

from engines.detailed_interpretation_engine.ten_gods.combinations.constants import ECOSYSTEM_FAMILY

CONDITION_NO_ACTIVE_CHAIN: str = "no_active_chain"
CONDITION_PATTERN_UNRESOLVED: str = "pattern_context_unresolved"
CONDITION_MC01_NOT_BOUND: str = "mc01_reference_not_bound"
CONDITION_UNRESOLVED_DRIVER: str = "driver_unresolved_without_pattern"
UNRESOLVED_COPY_KEY: str = "insufficient_data"

FAMILY_ORDER: tuple[str, ...] = ("resource", "peer", "output", "wealth", "authority")

FAMILY_GODS: dict[str, tuple[str, ...]] = {
    "resource": ("zheng_yin", "pian_yin"),
    "peer": ("bi_jian", "jie_cai"),
    "output": ("shi_shen", "shang_guan"),
    "wealth": ("zheng_cai", "pian_cai"),
    "authority": ("zheng_guan", "qi_sha"),
}

ENGINE_TO_ECOSYSTEM_FAMILY = ECOSYSTEM_FAMILY

GENERATION_FLOW_IDS: tuple[str, ...] = (
    "shi_shen_generates_wealth",
    "shang_guan_generates_wealth",
    "wealth_generates_officer",
    "officer_generates_resource",
    "wealth_officer_resource_chain",
)

USE_CHAIN_IDS: tuple[str, ...] = (
    "strong_day_master_uses_wealth",
    "strong_day_master_uses_officer",
    "strong_day_master_uses_output",
    "weak_day_master_uses_resource",
    "weak_day_master_uses_peer",
)

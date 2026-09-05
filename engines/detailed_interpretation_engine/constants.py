"""Pack 07 foundation version and identity constants.

These are design-freeze targets. They are not scoring weights.
"""

from __future__ import annotations

PACK07_DESIGN_FREEZE_VERSION: str = "1.0"
PACK07_ENGINE_VERSION: str = "1.0.0"
ENGINE_REGISTRY_NAME: str = "detailed_interpretation"

SCHEMA_CONTEXT: str = "bte.detailed_interpretation.context.v1"
SCHEMA_RESULT: str = "bte.detailed_interpretation.result.v1"
SCHEMA_RULES: str = "bte.detailed_interpretation.rules.v1"
SCHEMA_COMPOSER: str = "bte.detailed_interpretation.composer.v1"
SCHEMA_RUNTIME_CONTRACT: str = "bte.detailed_interpretation.runtime_contract.v1"
SCHEMA_EVIDENCE_PRIORITY: str = "bte.detailed_interpretation.evidence_priority.v1"
SCHEMA_DOMAIN: str = "bte.detailed_interpretation.domain.v1"
SCHEMA_LUCK_ACTIVATION: str = "bte.detailed_interpretation.luck_activation.v1"
SCHEMA_LUCK_INTERACTION: str = "bte.detailed_interpretation.luck_interaction.v1"
SCHEMA_TEMPORAL: str = "bte.detailed_interpretation.temporal_activation.v1"
SCHEMA_AUTHORITY: str = "bte.detailed_interpretation.authority.v1"
SCHEMA_CAREER: str = "bte.detailed_interpretation.career.v1"
SCHEMA_WEALTH: str = "bte.detailed_interpretation.wealth.v1"
SCHEMA_RELATIONSHIP: str = "bte.detailed_interpretation.relationship.v1"
SCHEMA_LEGACY: str = "bte.detailed_interpretation.legacy.v1"
SCHEMA_VITALITY: str = "bte.detailed_interpretation.vitality.v1"
SCHEMA_LIFE_OPTIMIZATION: str = "bte.detailed_interpretation.life_optimization.v1"
SCHEMA_CONSISTENCY: str = "bte.detailed_interpretation.system_consistency.v1"
SCHEMA_VERIFICATION: str = "bte.detailed_interpretation.verification.v1"
SCHEMA_MESSAGES: str = "bte.detailed_interpretation.messages.vi.v1"
SCHEMA_MINGJU_DECISION: str = "bte.mingju.decision.v1"
MC01_RULESET_VERSION: str = "pattern_rule_context_v1+score_rule_context_v1"
MC01_BIND_REJECT_KEY: str = "_mc01_reject"
SCHEMA_TEN_GODS: str = "bte.detailed_interpretation.ten_gods.v1"
TEN_GODS_RULESET_VERSION: str = "bte.detailed_interpretation.ten_gods.rules.v1"
SCHEMA_TEN_GOD_COMBINATIONS: str = "bte.detailed_interpretation.ten_god_combinations.v1"
TEN_GOD_COMBINATIONS_RULESET_VERSION: str = "bte.detailed_interpretation.ten_god_combinations.rules.v1"
SCHEMA_TEN_GODS_BALANCE: str = "bte.detailed_interpretation.ten_gods_balance.v1"
TEN_GODS_BALANCE_RULESET_VERSION: str = "bte.detailed_interpretation.ten_gods_balance.rules.v1"
SCHEMA_SHEN_SHA: str = "bte.detailed_interpretation.shen_sha.v1"
SHEN_SHA_RULESET_VERSION: str = "bte.detailed_interpretation.shen_sha.rules.v1"
SCHEMA_SHEN_SHA_ECOSYSTEM: str = "bte.detailed_interpretation.shen_sha_ecosystem.v1"
SHEN_SHA_ECOSYSTEM_RULESET_VERSION: str = "bte.detailed_interpretation.shen_sha_ecosystem.rules.v1"
EVIDENCE_PRIORITY_RULESET_VERSION: str = "bte.detailed_interpretation.evidence_priority.rules.v1"
DOMAIN_INTERPRETATION_RULESET_VERSION: str = "bte.detailed_interpretation.domain.rules.v1"
LUCK_ACTIVATION_RULESET_VERSION: str = "bte.detailed_interpretation.luck_activation.rules.v1"
LUCK_INTERACTION_RULESET_VERSION: str = "bte.detailed_interpretation.luck_interaction.rules.v1"
TEMPORAL_ACTIVATION_RULESET_VERSION: str = "bte.detailed_interpretation.temporal_activation.rules.v1"
LIFE_OPTIMIZATION_RULESET_VERSION: str = "bte.detailed_interpretation.life_optimization.rules.v1"
NARRATIVE_COMPOSER_RULESET_VERSION: str = "bte.detailed_interpretation.composer.rules.v1"

PACK07_VALIDATOR_VERSION: str = "1.0.0"

TEMPORAL_LAYER_PARENT: dict[str, str] = {
    "luck_cycle": "natal",
    "annual": "luck_cycle",
    "monthly": "annual",
    "daily": "monthly",
    "hourly": "daily",
}

FORBIDDEN_OWNED_TRUTH_KEYS: frozenset[str] = frozenset(
    {
        "pattern",
        "grade",
        "integrity",
        "achievement",
        "wealth_profile",
        "career_profile",
        "mingju_decision",
    }
)

MC01_NOT_BOUND_CODE: str = "P7V-CTX-MC01-NOT-BOUND"
MC01_NOT_BOUND_MESSAGE: str = "MC-01 reference not yet bound"
MC01_HASH_MISMATCH_CODE: str = "P7V-CTX-MC01-HASH-MISMATCH"
MC01_LINEAGE_MISMATCH_CODE: str = "P7V-CTX-MC01-LINEAGE-MISMATCH"
MC01_STALE_CODE: str = "P7V-CTX-MC01-STALE"
MC01_HASH_MISSING_CODE: str = "P7V-CTX-MC01-HASH-MISSING"
MC01_PATTERN_MISSING_CODE: str = "P7V-CTX-MC01-PATTERN-MISSING"
MC01_GRADE_MISSING_CODE: str = "P7V-CTX-MC01-GRADE-MISSING"
MC01_SNAPSHOT_HASH_CODE: str = "P7V-CTX-MC01-SNAPSHOT-HASH"
MC01_OWNERSHIP_DAMAGE_CODE: str = "P7V-OWNERSHIP-DAMAGE"
MC01_OWNERSHIP_RESCUE_CODE: str = "P7V-OWNERSHIP-RESCUE"

DEFAULT_LOCALE: str = "vi"

CANONICAL_DOMAIN_IDS: tuple[str, ...] = (
    "authority",
    "wealth",
    "career",
    "relationship",
    "children",
    "health",
    "creative",
    "academic",
    "leadership",
    "management",
    "learning",
    "personal_growth",
)

PUBLISHED_DOMAIN_IDS: tuple[str, ...] = (
    "authority",
    "career",
    "wealth",
    "relationship",
    "legacy",
    "vitality",
)

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

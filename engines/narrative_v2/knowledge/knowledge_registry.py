"""Documented semantic scopes and domain aliases.

Matching strategy only. Does not invent knowledge content.
"""

from __future__ import annotations

from dataclasses import dataclass

DOMAIN_ALIASES: dict[str, str] = {
    "pattern": "pattern",
    "Pattern": "pattern",
    "strength": "strength",
    "Strength": "strength",
    "useful_god": "useful_god",
    "UsefulGod": "useful_god",
    "ten_gods": "ten_gods",
    "TenGods": "ten_gods",
    "shensha": "shensha",
    "ShenSha": "shensha",
    "temperature": "temperature",
    "luck": "luck",
    "concept": "concept",
}

SEMANTIC_ALIASES: dict[str, str] = {}

TARGET_SEMANTIC_KEYS: frozenset[str] = frozenset(
    {
        "core.pattern_context",
        "core.useful_god_context",
        "core.temperature_balancing_context",
        "core.pattern_ten_gods_relation",
        "core.luck_temporal_context",
        "boundary.approved_rule_unavailable",
    }
)


@dataclass(frozen=True, slots=True)
class EntityLookup:
    """Exact entity lookup from published evidence values."""

    domain: str
    evidence_ids: tuple[str, ...]
    required_source: str


SEMANTIC_LOOKUPS: dict[str, tuple[EntityLookup, ...]] = {
    "core.pattern_context": (
        EntityLookup(
            domain="pattern",
            evidence_ids=("evidence.pattern.primary", "evidence.pattern.cach_cuc"),
            required_source="knowledge/interpretation/domains/pattern/",
        ),
        EntityLookup(
            domain="strength",
            evidence_ids=("evidence.strength.level",),
            required_source="knowledge/interpretation/domains/strength/",
        ),
    ),
    "core.useful_god_context": (
        EntityLookup(
            domain="useful_god",
            evidence_ids=("evidence.useful_god.primary", "evidence.useful_god.ten_god"),
            required_source="knowledge/interpretation/domains/useful_god/",
        ),
        EntityLookup(
            domain="strength",
            evidence_ids=("evidence.strength.level",),
            required_source="knowledge/interpretation/domains/strength/",
        ),
    ),
    "core.temperature_balancing_context": (
        EntityLookup(
            domain="temperature",
            evidence_ids=(
                "evidence.temperature.balancing_need",
                "evidence.temperature.climate_state",
            ),
            required_source="knowledge/interpretation/domains/temperature/",
        ),
    ),
    "core.pattern_ten_gods_relation": (
        EntityLookup(
            domain="pattern",
            evidence_ids=("evidence.pattern.primary",),
            required_source="knowledge/interpretation/domains/pattern/",
        ),
        EntityLookup(
            domain="ten_gods",
            evidence_ids=("evidence.ten_gods.visible_labels",),
            required_source="knowledge/interpretation/domains/ten_gods/",
        ),
    ),
    "core.luck_temporal_context": (
        EntityLookup(
            domain="luck",
            evidence_ids=("evidence.luck.current_cycle",),
            required_source="knowledge/interpretation/domains/luck/",
        ),
    ),
    "boundary.approved_rule_unavailable": (
        EntityLookup(
            domain="shensha",
            evidence_ids=("evidence.shensha.names",),
            required_source="knowledge/interpretation/domains/shensha/",
        ),
    ),
}


def normalize_domain(domain: str) -> str:
    """Return the canonical index domain or the original token."""
    return DOMAIN_ALIASES.get(domain, domain.lower())


class KnowledgeRegistry:
    """Semantic-scope registry. Does not load file content."""

    def target_keys(self) -> frozenset[str]:
        """Return semantic keys this sprint may resolve."""
        return TARGET_SEMANTIC_KEYS

    def lookups(self, semantic_key: str) -> tuple[EntityLookup, ...]:
        """Return documented entity lookups for a semantic key."""
        aliased = SEMANTIC_ALIASES.get(semantic_key, semantic_key)
        return SEMANTIC_LOOKUPS.get(aliased, ())

    def alias_of(self, semantic_key: str) -> str:
        """Return the documented semantic alias, or the key itself."""
        return SEMANTIC_ALIASES.get(semantic_key, semantic_key)

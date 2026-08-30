"""ReasoningEdge — deterministic graph relationship."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.reasoning.reasoning_reference import ReasoningReference

RELATION_SUPPORTS = "supports"
RELATION_CONSTRAINS = "constrains"
RELATION_QUALIFIES = "qualifies"
RELATION_BALANCES = "balances"
RELATION_AMPLIFIES = "amplifies"
RELATION_REDUCES = "reduces"
RELATION_CONTEXTUALIZES = "contextualizes"

ALLOWED_RELATION_TYPES: frozenset[str] = frozenset(
    {
        RELATION_SUPPORTS,
        RELATION_CONSTRAINS,
        RELATION_QUALIFIES,
        RELATION_BALANCES,
        RELATION_AMPLIFIES,
        RELATION_REDUCES,
        RELATION_CONTEXTUALIZES,
    }
)

STATUS_ACTIVE = "active"
STATUS_CONFLICT = "conflict"
STATUS_QUALIFIED = "qualified"

ALLOWED_EDGE_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_ACTIVE,
        STATUS_CONFLICT,
        STATUS_QUALIFIED,
    }
)

DEFAULT_EDGE_WEIGHT = 1.0


@dataclass(frozen=True, slots=True)
class ReasoningEdge:
    """Directed relation between reasoning nodes. Weight is not a score."""

    edge_id: str
    source_ids: tuple[str, ...]
    target_id: str
    relation_type: str
    weight: float
    status: str
    references: tuple[ReasoningReference, ...]
    metadata: tuple[tuple[str, str], ...] = ()

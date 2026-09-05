"""Pack 07 schema registry.

Registers frozen schema IDs to model types. Does not evaluate rules.
"""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.constants import (
    SCHEMA_AUTHORITY,
    SCHEMA_CAREER,
    SCHEMA_COMPOSER,
    SCHEMA_CONTEXT,
    SCHEMA_DOMAIN,
    SCHEMA_EVIDENCE_PRIORITY,
    SCHEMA_LEGACY,
    SCHEMA_LIFE_OPTIMIZATION,
    SCHEMA_LUCK_ACTIVATION,
    SCHEMA_LUCK_INTERACTION,
    SCHEMA_RELATIONSHIP,
    SCHEMA_RESULT,
    SCHEMA_RUNTIME_CONTRACT,
    SCHEMA_TEMPORAL,
    SCHEMA_TEN_GODS,
    SCHEMA_TEN_GOD_COMBINATIONS,
    SCHEMA_TEN_GODS_BALANCE,
    SCHEMA_SHEN_SHA,
    SCHEMA_SHEN_SHA_ECOSYSTEM,
    SCHEMA_VITALITY,
    SCHEMA_WEALTH,
)
from engines.detailed_interpretation_engine.context import InterpretationContext
from engines.detailed_interpretation_engine.domains import (
    AuthorityResult,
    CareerResult,
    DomainInterpretationResult,
    LegacyResult,
    RelationshipResult,
    VitalityResult,
    WealthResult,
)
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.narrative import NarrativeGraph, NarrativeResult
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult
from engines.detailed_interpretation_engine.runtime import CanonicalRuntimeResult
from engines.detailed_interpretation_engine.temporal import (
    LuckActivationResult,
    LuckInteractionResult,
    TemporalActivationResult,
)
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaEcosystemResult,
    ShenShaInterpretationCollection,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.models import TenGodCombinationCollection
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import TenGodEcosystemResult
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationCollection

PACK07_SCHEMA_REGISTRY: dict[str, type[Any]] = {
    SCHEMA_CONTEXT: InterpretationContext,
    SCHEMA_RESULT: CanonicalRuntimeResult,
    SCHEMA_RUNTIME_CONTRACT: CanonicalRuntimeResult,
    SCHEMA_EVIDENCE_PRIORITY: EvidencePriorityResult,
    SCHEMA_DOMAIN: DomainInterpretationResult,
    SCHEMA_LUCK_ACTIVATION: LuckActivationResult,
    SCHEMA_LUCK_INTERACTION: LuckInteractionResult,
    SCHEMA_TEMPORAL: TemporalActivationResult,
    SCHEMA_AUTHORITY: AuthorityResult,
    SCHEMA_CAREER: CareerResult,
    SCHEMA_WEALTH: WealthResult,
    SCHEMA_RELATIONSHIP: RelationshipResult,
    SCHEMA_LEGACY: LegacyResult,
    SCHEMA_VITALITY: VitalityResult,
    SCHEMA_LIFE_OPTIMIZATION: LifeOptimizationResult,
    SCHEMA_COMPOSER: NarrativeResult,
    SCHEMA_TEN_GODS: TenGodInterpretationCollection,
    SCHEMA_TEN_GOD_COMBINATIONS: TenGodCombinationCollection,
    SCHEMA_TEN_GODS_BALANCE: TenGodEcosystemResult,
    SCHEMA_SHEN_SHA: ShenShaInterpretationCollection,
    SCHEMA_SHEN_SHA_ECOSYSTEM: ShenShaEcosystemResult,
}


def registered_schema_ids() -> tuple[str, ...]:
    """Return frozen Pack 07 schema identifiers."""
    return tuple(sorted(PACK07_SCHEMA_REGISTRY))


def model_for_schema(schema_id: str) -> type[Any] | None:
    """Return the model type registered for a schema id."""
    return PACK07_SCHEMA_REGISTRY.get(schema_id)


def register_pack07_schemas(registry: dict[str, type[Any]] | None = None) -> dict[str, type[Any]]:
    """Merge Pack 07 schema ids into an existing registry mapping."""
    target = registry if registry is not None else {}
    target.update(PACK07_SCHEMA_REGISTRY)
    target.setdefault("bte.detailed_interpretation.narrative_graph.v1", NarrativeGraph)
    return target

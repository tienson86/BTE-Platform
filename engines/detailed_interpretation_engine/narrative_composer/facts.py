"""Read immutable Pack 07 findings for composition. Does not recalculate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult
from engines.detailed_interpretation_engine.enums import DomainState, EvaluationStatus
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.mc01 import Mc01StructuralSnapshot, snapshot_from_live_payload
from engines.detailed_interpretation_engine.narrative_composer.constants import MAIN_NARRATIVE_DOMAINS
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult
from engines.detailed_interpretation_engine.temporal import (
    LuckActivationResult,
    LuckInteractionResult,
    TemporalActivationResult,
)


@dataclass(frozen=True, slots=True)
class NarrativeComposerFacts:
    """Inputs Composer may read. Upstream objects are referenced, not mutated."""

    analysis_id: str
    snapshot: Mc01StructuralSnapshot | None
    evidence_priority: EvidencePriorityResult
    natal: dict[str, DomainInterpretationResult]
    luck: LuckActivationResult
    interaction: LuckInteractionResult
    temporal: TemporalActivationResult
    optimization: LifeOptimizationResult
    domain_order: tuple[str, ...]


def collect_narrative_facts(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> NarrativeComposerFacts:
    """Snapshot Pack 07 truth for composition. No new analysis."""
    data = payload if isinstance(payload, Mapping) else {}
    domains = context.runtime.domains
    natal = {
        "authority": domains.authority.natal,
        "career": domains.career.natal,
        "wealth": domains.wealth.natal,
        "relationship": domains.relationship.natal,
        "legacy": domains.legacy.natal,
        "vitality": domains.vitality.natal,
    }
    ranked = [
        item for item in context.runtime.interpretation.evidence_priority.ranked_domains if item in natal
    ]
    order = list(ranked)
    for item in MAIN_NARRATIVE_DOMAINS:
        if item not in order:
            order.append(item)
    return NarrativeComposerFacts(
        analysis_id=context.analysis_id,
        snapshot=snapshot_from_live_payload(data),
        evidence_priority=context.runtime.interpretation.evidence_priority,
        natal=natal,
        luck=context.runtime.temporal.luck_activation,
        interaction=context.runtime.temporal.luck_interaction,
        temporal=context.runtime.temporal.temporal_activation,
        optimization=context.runtime.optimization,
        domain_order=tuple(order) or MAIN_NARRATIVE_DOMAINS,
    )


def narrative_ready(facts: NarrativeComposerFacts) -> bool:
    """True when at least one published natal domain has been interpreted."""
    if facts.evidence_priority.status is EvaluationStatus.NOT_EVALUATED:
        return False
    return any(item.state is not DomainState.NOT_EVALUATED for item in facts.natal.values())

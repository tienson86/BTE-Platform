"""Read natal graph and Luck Activation. Does not recalculate activation."""

from __future__ import annotations

from dataclasses import dataclass

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domains import DomainSection
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.temporal import LuckActivationResult


@dataclass(frozen=True, slots=True)
class LuckInteractionFacts:
    """Inputs Luck Interaction may explain. Upstream objects are read-only."""

    analysis_id: str
    activation: LuckActivationResult
    domains: DomainSection
    evidence_priority: EvidencePriorityResult


def collect_luck_interaction_facts(context: CanonicalAnalysisContext) -> LuckInteractionFacts:
    """Copy activation and natal graph snapshots. Does not rebuild Đại Vận."""
    return LuckInteractionFacts(
        analysis_id=context.analysis_id,
        activation=context.runtime.temporal.luck_activation,
        domains=context.runtime.domains,
        evidence_priority=context.runtime.interpretation.evidence_priority,
    )

"""Shen Sha cluster and ecosystem evaluation. Not raw star counting."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import (
    EvaluationStatus,
    ShenShaClusterState,
    ShenShaClusterStrength,
    ShenShaConfidenceModifier,
    ShenShaDependencyState,
)
from engines.detailed_interpretation_engine.shen_sha.constants import (
    APPLIED_MODIFIERS,
    BLOCKED_MODIFIERS,
    CANONICAL_CLUSTER_IDS,
    CLUSTER_CANDIDATES,
    CLUSTER_REQUIRED_DOMAINS,
    CLUSTER_RISK,
    CONDITION_MC01_NOT_BOUND,
    DOMAIN_RANK,
    STRENGTH_RANK,
    SUPPORTED_BANDS,
    USABLE_MODIFIERS,
    WARNING_NO_STRUCTURAL_PROMOTION,
)
from engines.detailed_interpretation_engine.shen_sha.evaluate import resolve_dependency_gate
from engines.detailed_interpretation_engine.shen_sha.facts import UpstreamShenShaFacts
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaClusterMember,
    ShenShaClusterResult,
    ShenShaEcosystemResult,
    ShenShaInterpretationCollection,
    ShenShaInterpretationResult,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def _item_map(
    collection: ShenShaInterpretationCollection,
) -> dict[str, ShenShaInterpretationResult]:
    return {item.shen_sha_id: item for item in collection.items if item.shen_sha_id}


def _contribution(item: ShenShaInterpretationResult) -> str:
    modifier = item.modifier_state.value
    if modifier in APPLIED_MODIFIERS:
        return "primary"
    if modifier in USABLE_MODIFIERS:
        return "secondary"
    return "ignored"


def _cluster_strength(
    applied_count: int,
    usable_count: int,
    gate: ShenShaDependencyState,
    best_band: str,
) -> ShenShaClusterStrength:
    if gate is ShenShaDependencyState.UNRESOLVED:
        return ShenShaClusterStrength.UNRESOLVED
    if gate is ShenShaDependencyState.BLOCKED:
        return ShenShaClusterStrength.NONE
    if applied_count <= 0:
        return ShenShaClusterStrength.NONE if usable_count <= 0 else ShenShaClusterStrength.WEAK
    domain_high = best_band in {"high", "very_strong", "strong"}
    if domain_high and applied_count >= 2 and usable_count >= 2:
        return ShenShaClusterStrength.STRONG
    if domain_high and applied_count >= 1:
        return ShenShaClusterStrength.MODERATE
    if best_band in SUPPORTED_BANDS and applied_count >= 1:
        return ShenShaClusterStrength.MODERATE if applied_count >= 2 else ShenShaClusterStrength.WEAK
    return ShenShaClusterStrength.WEAK


def evaluate_cluster(
    cluster_id: str,
    collection: ShenShaInterpretationCollection,
    facts: UpstreamShenShaFacts,
) -> ShenShaClusterResult:
    """Build one cluster from DI-05 members. Blocked stars cannot activate it."""
    candidates = CLUSTER_CANDIDATES.get(cluster_id, ())
    required = CLUSTER_REQUIRED_DOMAINS.get(cluster_id, ())
    lookup = _item_map(collection)
    members: list[ShenShaClusterMember] = []
    applied: list[str] = []
    blocked: list[str] = []
    usable: list[str] = []
    evidence: list[str] = []
    traces: list[str] = []
    for star_id in candidates:
        item = lookup.get(star_id)
        if item is None or not item.detected:
            continue
        contribution = _contribution(item)
        members.append(
            ShenShaClusterMember(
                shen_sha_id=star_id,
                di05_state=item.modifier_state.value,
                contribution=contribution,
            )
        )
        if item.modifier_state.value in APPLIED_MODIFIERS:
            applied.append(star_id)
        if item.modifier_state.value in USABLE_MODIFIERS:
            usable.append(star_id)
        if item.modifier_state.value in BLOCKED_MODIFIERS:
            blocked.append(star_id)
        evidence.extend(item.evidence_ids)
        traces.extend(item.trace_ids)
    gate = resolve_dependency_gate(required, facts)
    conditions = [f"cluster:{cluster_id}", f"dependency:{gate.state.value}"]
    warnings = [WARNING_NO_STRUCTURAL_PROMOTION]
    if not facts.mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    if not members:
        state = ShenShaClusterState.INACTIVE
        strength = ShenShaClusterStrength.NONE
        modifier = ShenShaConfidenceModifier.NO_EFFECT
        supported: tuple[str, ...] = ()
        dependency = ShenShaDependencyState.NOT_AVAILABLE if not required else gate.state
    elif not applied and all(member.contribution == "ignored" for member in members):
        if gate.state is ShenShaDependencyState.UNRESOLVED:
            state = ShenShaClusterState.UNRESOLVED
            strength = ShenShaClusterStrength.UNRESOLVED
            modifier = ShenShaConfidenceModifier.NO_EFFECT
        elif gate.state is ShenShaDependencyState.BLOCKED:
            state = ShenShaClusterState.BLOCKED
            strength = ShenShaClusterStrength.NONE
            modifier = ShenShaConfidenceModifier.BLOCKED
        else:
            state = ShenShaClusterState.INACTIVE
            strength = ShenShaClusterStrength.NONE
            modifier = ShenShaConfidenceModifier.NO_EFFECT
        supported = ()
        dependency = gate.state
        warnings.append("warning:blocked_members_cannot_activate")
    elif gate.state is ShenShaDependencyState.UNRESOLVED:
        state = ShenShaClusterState.UNRESOLVED
        strength = ShenShaClusterStrength.UNRESOLVED
        modifier = ShenShaConfidenceModifier.NO_EFFECT
        supported = ()
        dependency = gate.state
    elif gate.state is ShenShaDependencyState.BLOCKED:
        state = ShenShaClusterState.BLOCKED
        strength = ShenShaClusterStrength.NONE
        modifier = ShenShaConfidenceModifier.BLOCKED
        supported = ()
        dependency = gate.state
    else:
        strength = _cluster_strength(len(applied), len(usable), gate.state, gate.best_band)
        supported = gate.supported_domains
        dependency = gate.state
        if cluster_id == CLUSTER_RISK:
            state = ShenShaClusterState.CONDITIONAL
            modifier = ShenShaConfidenceModifier.WARN
            strength = (
                ShenShaClusterStrength.CONDITIONAL
                if strength is not ShenShaClusterStrength.NONE
                else strength
            )
        elif strength is ShenShaClusterStrength.WEAK and not applied:
            state = ShenShaClusterState.CONDITIONAL
            modifier = ShenShaConfidenceModifier.QUALIFY
        else:
            state = ShenShaClusterState.ACTIVE
            modifier = ShenShaConfidenceModifier.STRENGTHEN
        traces.append(
            f"TR-P7-SS-CL-{cluster_id}:members={len(members)};applied={len(applied)};"
            f"blocked={len(blocked)};strength={strength.value};state={state.value}"
        )
    return ShenShaClusterResult(
        cluster_id=cluster_id,
        state=state,
        members=tuple(members),
        applied_members=tuple(applied),
        blocked_members=tuple(blocked),
        cluster_strength=strength,
        supported_domains=supported,
        dependency_state=dependency,
        confidence_modifier=modifier,
        conditions=tuple(conditions),
        warnings=tuple(warnings),
        evidence_ids=tuple(dict.fromkeys(evidence)),
        trace_ids=tuple(traces),
    )


def _quality(cluster: ShenShaClusterResult, facts: UpstreamShenShaFacts) -> tuple[int, int, int]:
    """Rank by quality and domain support, never by raw member count."""
    strength = STRENGTH_RANK.get(cluster.cluster_strength.value, 0)
    domain = 0
    for item in cluster.supported_domains:
        domain = max(domain, DOMAIN_RANK.get(facts.domain_support.get(item, ""), 0))
    if cluster.dependency_state is ShenShaDependencyState.SATISFIED:
        domain += 1
    applied_quality = len(cluster.applied_members)
    return (strength, domain, 1 if applied_quality else 0)


def evaluate_shen_sha_ecosystem(
    collection: ShenShaInterpretationCollection,
    facts: UpstreamShenShaFacts,
    *,
    analysis_id: str,
) -> ShenShaEcosystemResult:
    """Assemble twelve cluster families. Dominant is quality, not count."""
    clusters = tuple(evaluate_cluster(cluster_id, collection, facts) for cluster_id in CANONICAL_CLUSTER_IDS)
    active = tuple(
        item.cluster_id
        for item in clusters
        if item.state in {ShenShaClusterState.ACTIVE, ShenShaClusterState.CONDITIONAL}
        and item.cluster_strength not in {ShenShaClusterStrength.NONE, ShenShaClusterStrength.UNRESOLVED}
    )
    inactive = tuple(item.cluster_id for item in clusters if item.state is ShenShaClusterState.INACTIVE)
    blocked = tuple(item.cluster_id for item in clusters if item.state is ShenShaClusterState.BLOCKED)
    ranked = sorted(
        (item for item in clusters if item.cluster_id in active),
        key=lambda item: _quality(item, facts),
        reverse=True,
    )
    dominant = ""
    supporting = ""
    conditions = ["source:shen_sha_ecosystem"]
    if not facts.mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    if ranked:
        dominant = ranked[0].cluster_id
        non_risk = [item for item in ranked[1:] if item.cluster_id != CLUSTER_RISK]
        if non_risk:
            supporting = non_risk[0].cluster_id
        elif len(ranked) > 1:
            supporting = ranked[1].cluster_id
    elif any(item.state is ShenShaClusterState.UNRESOLVED for item in clusters if item.members):
        conditions.append("dominant:unresolved")
    evidence = tuple(item for cluster in clusters for item in cluster.evidence_ids)
    traces = tuple(item for cluster in clusters for item in cluster.trace_ids)
    if active and not facts.mc01_bound:
        status = EvaluationStatus.PARTIALLY_RESOLVED
        eco_state = "conditional"
        confidence = ConfidenceValue(summary="low")
    elif active:
        status = EvaluationStatus.RESOLVED
        eco_state = "active"
        confidence = ConfidenceValue(summary="moderate")
    elif any(item.state is ShenShaClusterState.UNRESOLVED for item in clusters):
        status = EvaluationStatus.PARTIALLY_RESOLVED
        eco_state = "unresolved"
        confidence = ConfidenceValue(summary="low")
    else:
        status = EvaluationStatus.PARTIALLY_RESOLVED if collection.items else EvaluationStatus.NOT_EVALUATED
        eco_state = "inactive"
        confidence = ConfidenceValue(summary="low")
    return ShenShaEcosystemResult(
        analysis_id=analysis_id,
        state=status,
        clusters=clusters,
        active_clusters=active,
        inactive_clusters=inactive,
        blocked_clusters=blocked,
        dominant_cluster=dominant,
        supporting_cluster=supporting,
        ecosystem_state=eco_state,
        conditions=tuple(conditions),
        warnings=(WARNING_NO_STRUCTURAL_PROMOTION,),
        evidence_ids=tuple(dict.fromkeys(evidence)),
        trace_ids=traces + ("TR-P7-SS-ECO-001",),
        confidence=confidence,
    )

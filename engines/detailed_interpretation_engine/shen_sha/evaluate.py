"""Deterministic per-star Shen Sha secondary-evidence evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from engines.detailed_interpretation_engine.enums import (
    ShenShaConfidenceModifier,
    ShenShaDependencyState,
    ShenShaInterpretationState,
    ShenShaModifierState,
)
from engines.detailed_interpretation_engine.shen_sha.constants import (
    CONDITION_DETECTED,
    CONDITION_MC01_NOT_BOUND,
    LOW_BANDS,
    STAR_CATEGORIES,
    STAR_REQUIRED_DOMAINS,
    SUPPORTED_BANDS,
    UNRESOLVED_BANDS,
    WARNING_NO_STRUCTURAL_PROMOTION,
    WARNING_STAR_IDS,
)
from engines.detailed_interpretation_engine.shen_sha.facts import DetectedShenSha, UpstreamShenShaFacts
from engines.detailed_interpretation_engine.shen_sha.models import ShenShaInterpretationResult
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class DependencyGate:
    """Resolved dependency posture for one star or cluster."""

    state: ShenShaDependencyState
    supported_domains: tuple[str, ...]
    best_band: str


def _band_for(domain: str, facts: UpstreamShenShaFacts) -> str:
    if domain == "risk" and facts.risk_surface and domain not in facts.domain_support:
        return "present"
    if domain == "protection" and facts.rescue_present:
        return "present"
    return facts.domain_support.get(domain, "")


def resolve_dependency_gate(
    required: tuple[str, ...],
    facts: UpstreamShenShaFacts,
) -> DependencyGate:
    """Gate required domains. Missing MC-01 stays unresolved, not invented."""
    if not required:
        return DependencyGate(ShenShaDependencyState.NOT_AVAILABLE, (), "")
    bands = tuple((domain, _band_for(domain, facts) or "unresolved") for domain in required)
    supported = tuple(domain for domain, band in bands if band in SUPPORTED_BANDS)
    unresolved = tuple(domain for domain, band in bands if band in UNRESOLVED_BANDS)
    low = tuple(domain for domain, band in bands if band in LOW_BANDS)
    ranked = [band for _, band in bands]
    best = max(ranked, key=lambda item: (item in SUPPORTED_BANDS, item in {"moderate", "present"}, item))
    if supported:
        return DependencyGate(ShenShaDependencyState.SATISFIED, supported, best)
    if low:
        return DependencyGate(ShenShaDependencyState.BLOCKED, (), best if best in LOW_BANDS else "low")
    if unresolved or not facts.mc01_bound:
        return DependencyGate(ShenShaDependencyState.UNRESOLVED, (), "unresolved")
    return DependencyGate(ShenShaDependencyState.BLOCKED, (), best if best in LOW_BANDS else "low")


def _trace(star_id: str, detected: bool, gate: DependencyGate, modifier: ShenShaModifierState) -> str:
    dependency = ",".join(gate.supported_domains) if gate.supported_domains else gate.state.value
    return (
        f"TR-P7-SS-{star_id}:star={star_id};detected={str(detected).lower()};"
        f"dependency={dependency};result:modifier_state={modifier.value}"
    )


def evaluate_shen_sha(match: DetectedShenSha, facts: UpstreamShenShaFacts) -> ShenShaInterpretationResult:
    """Interpret one detected star as secondary evidence only."""
    star_id = match.shen_sha_id
    required = STAR_REQUIRED_DOMAINS.get(star_id, ())
    categories = STAR_CATEGORIES.get(star_id, ())
    gate = resolve_dependency_gate(required, facts)
    conditions = [CONDITION_DETECTED, f"dependency:{gate.state.value}"]
    warnings = [WARNING_NO_STRUCTURAL_PROMOTION]
    if not facts.mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    is_warning_star = star_id in WARNING_STAR_IDS
    if gate.state is ShenShaDependencyState.SATISFIED:
        modifier = ShenShaModifierState.WARNING if is_warning_star else ShenShaModifierState.APPLIED
        confidence_mod = ShenShaConfidenceModifier.WARN if is_warning_star else ShenShaConfidenceModifier.STRENGTHEN
        state = ShenShaInterpretationState.APPLIED
        confidence = ConfidenceValue(summary="moderate")
    elif gate.state is ShenShaDependencyState.PARTIAL:
        modifier = ShenShaModifierState.WARNING if is_warning_star else ShenShaModifierState.QUALIFIED
        confidence_mod = ShenShaConfidenceModifier.WARN if is_warning_star else ShenShaConfidenceModifier.QUALIFY
        state = ShenShaInterpretationState.APPLIED
        confidence = ConfidenceValue(summary="low")
    elif gate.state is ShenShaDependencyState.BLOCKED:
        modifier = ShenShaModifierState.WARNING if is_warning_star else ShenShaModifierState.BLOCKED
        confidence_mod = ShenShaConfidenceModifier.WARN if is_warning_star else ShenShaConfidenceModifier.BLOCKED
        state = ShenShaInterpretationState.BLOCKED_NO_DEPENDENCY
        confidence = ConfidenceValue(summary="low")
        warnings.append("warning:dependency_blocked")
    else:
        modifier = ShenShaModifierState.UNRESOLVED
        confidence_mod = ShenShaConfidenceModifier.NO_EFFECT
        state = ShenShaInterpretationState.UNRESOLVED
        confidence = ConfidenceValue(summary="low")
        warnings.append("warning:dependency_unresolved")
    if gate.state is ShenShaDependencyState.BLOCKED and is_warning_star:
        state = ShenShaInterpretationState.DETECTED_NOT_MATERIAL
    supported = gate.supported_domains if modifier in {ShenShaModifierState.APPLIED, ShenShaModifierState.QUALIFIED, ShenShaModifierState.WARNING, ShenShaModifierState.WEAK_SUPPORT} else ()
    if modifier is ShenShaModifierState.BLOCKED:
        supported = ()
        confidence_mod = ShenShaConfidenceModifier.BLOCKED
    return ShenShaInterpretationResult(
        shen_sha_id=star_id,
        state=state,
        detected=True,
        positions=match.positions,
        categories=categories,
        supported_domains=supported,
        required_dependencies=required,
        dependency_state=gate.state,
        modifier_state=modifier,
        confidence_modifier=confidence_mod,
        conditions=tuple(conditions),
        warnings=tuple(warnings),
        evidence_ids=(match.evidence_id,),
        trace_ids=(_trace(star_id, True, gate, modifier),),
        confidence=confidence,
    )

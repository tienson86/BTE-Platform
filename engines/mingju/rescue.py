"""Rescue targeting registered Damage. No orphan Rescue."""

from __future__ import annotations

from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power, is_material
from engines.mingju.models import DamageResult, MingJuContext, RescueFinding, RescueResult
from engines.mingju.serialization import clamp_confidence


def _strength(power: float) -> str:
    if power >= 4.0:
        return "strong"
    if power >= 2.2:
        return "moderate"
    return "minor"


def _rescue(
    book: RecordBook,
    rescue_type: str,
    source: str,
    target_ids: tuple[str, ...],
    strength: str,
    evidence_ids: tuple[str, ...],
    rule_id: str,
) -> RescueFinding:
    rescue_id = book.next_id("RSC-MC")
    trace_id = book.add_trace("rescue", rule_id, f"mc01.rescue.{rescue_type}", evidence_ids)
    return RescueFinding(
        rescue_id=rescue_id,
        rescue_type=rescue_type,
        source=source,
        target_damage_ids=target_ids,
        strength=strength,
        reliability="conditional",
        coverage="partial" if strength != "strong" else "substantial",
        damage_offset=None,
        evidence_ids=evidence_ids,
        trace_ids=(trace_id,),
        rule_id=rule_id,
        confidence=clamp_confidence(0.8 if strength != "minor" else 0.68),
    )


def evaluate_rescue(
    context: MingJuContext,
    damage: DamageResult,
    book: RecordBook,
) -> RescueResult:
    """Register Rescue only against existing Damage plus an active mechanism."""
    if damage.state != AnalysisState.RESOLVED.value:
        return RescueResult(state=AnalysisState.UNRESOLVED.value)
    findings: list[RescueFinding] = []
    for item in damage.findings:
        if item.damage_type == "hurting_officer_attacks_officer":
            seal_power = family_power(context.activations, "resource")
            if is_material(context.activations, "zheng_yin") or is_material(context.activations, "pian_yin"):
                evidence_id = book.add_evidence(
                    "rescue",
                    "mc01.rescue.seal_controls_hurting_officer",
                    source="mingju.rescue",
                    target_damage_id=item.damage_id,
                )
                findings.append(
                    _rescue(
                        book,
                        "seal_controls_hurting_officer",
                        "resource",
                        (item.damage_id,),
                        _strength(seal_power),
                        (evidence_id,),
                        "MC-RSC-SG-001",
                    )
                )
        elif item.damage_type in {"mixed_officer_killer", "killer_overloads_weak_day_master"}:
            if is_material(context.activations, "zheng_yin") or is_material(context.activations, "pian_yin"):
                evidence_id = book.add_evidence(
                    "rescue",
                    "mc01.rescue.seal_transforms_killer",
                    source="mingju.rescue",
                    target_damage_id=item.damage_id,
                )
                findings.append(
                    _rescue(
                        book,
                        "seal_transforms_killer",
                        "resource",
                        (item.damage_id,),
                        _strength(family_power(context.activations, "resource")),
                        (evidence_id,),
                        "MC-RSC-SHA-001",
                    )
                )
        elif item.damage_type == "peer_robs_wealth":
            if is_material(context.activations, "zheng_guan") or is_material(context.activations, "qi_sha"):
                evidence_id = book.add_evidence(
                    "rescue",
                    "mc01.rescue.officer_controls_peer",
                    source="mingju.rescue",
                    target_damage_id=item.damage_id,
                )
                findings.append(
                    _rescue(
                        book,
                        "officer_controls_peer",
                        "officer",
                        (item.damage_id,),
                        _strength(family_power(context.activations, "officer")),
                        (evidence_id,),
                        "MC-RSC-PEER-001",
                    )
                )
        elif item.damage_type == "wealth_overloads_weak_day_master":
            if family_power(context.activations, "resource") >= 1.5:
                evidence_id = book.add_evidence(
                    "rescue",
                    "mc01.rescue.resource_restores_structure",
                    source="mingju.rescue",
                    target_damage_id=item.damage_id,
                )
                findings.append(
                    _rescue(
                        book,
                        "resource_restores_structure",
                        "resource",
                        (item.damage_id,),
                        _strength(family_power(context.activations, "resource")),
                        (evidence_id,),
                        "MC-RSC-WL-001",
                    )
                )
        elif item.damage_type == "owl_robs_food":
            if is_material(context.activations, "zheng_cai") or is_material(context.activations, "pian_cai"):
                evidence_id = book.add_evidence(
                    "rescue",
                    "mc01.rescue.wealth_bridges_structure",
                    source="mingju.rescue",
                    target_damage_id=item.damage_id,
                )
                findings.append(
                    _rescue(
                        book,
                        "wealth_bridges_structure",
                        "wealth",
                        (item.damage_id,),
                        _strength(family_power(context.activations, "wealth")),
                        (evidence_id,),
                        "MC-RSC-OWL-001",
                    )
                )
        elif item.damage_type == "resource_overload":
            if family_power(context.activations, "output") >= 1.0:
                evidence_id = book.add_evidence(
                    "rescue",
                    "mc01.rescue.output_releases_excess",
                    source="mingju.rescue",
                    target_damage_id=item.damage_id,
                )
                findings.append(
                    _rescue(
                        book,
                        "output_releases_excess",
                        "output",
                        (item.damage_id,),
                        _strength(family_power(context.activations, "output")),
                        (evidence_id,),
                        "MC-RSC-RES-001",
                    )
                )
    evidence_ids = tuple(eid for item in findings for eid in item.evidence_ids)
    return RescueResult(
        state=AnalysisState.RESOLVED.value,
        findings=tuple(findings),
        evidence_ids=evidence_ids,
        confidence=clamp_confidence(0.8 if findings else 0.9),
    )

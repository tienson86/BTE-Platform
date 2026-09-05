"""Canonical Damage detection. Co-presence alone does not confirm Damage."""

from __future__ import annotations

from engines.mingju.constants import GOD_FAMILY, STRONG_DM_LEVELS, WEAK_DM_LEVELS
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power, god_power, is_material, present_ids
from engines.mingju.models import DamageFinding, DamageResult, MingJuContext, PatternDecision
from engines.mingju.serialization import clamp_confidence


def _severity(source_power: float, target_power: float) -> str:
    if target_power <= 0:
        return "minor"
    ratio = source_power / max(target_power, 0.15)
    if ratio >= 2.2:
        return "critical"
    if ratio >= 1.45:
        return "major"
    if ratio >= 0.9:
        return "moderate"
    return "minor"


def _directness(context: MingJuContext, source_id: str, target_id: str) -> str:
    source_visible = any(
        item.god_id == source_id and item.layer == "visible" for item in context.activations
    )
    target_visible = any(
        item.god_id == target_id and item.layer == "visible" for item in context.activations
    )
    return "direct" if source_visible and target_visible else "indirect"


def _confirm(
    book: RecordBook,
    damage_type: str,
    source: str,
    target: str,
    severity: str,
    directness: str,
    evidence_ids: tuple[str, ...],
    rule_id: str,
    causal_group: str,
    confidence: float,
) -> DamageFinding:
    damage_id = book.next_id("DMG-MC")
    trace_id = book.add_trace("damage", rule_id, f"mc01.damage.{damage_type}", evidence_ids)
    return DamageFinding(
        damage_id=damage_id,
        damage_type=damage_type,
        source=source,
        target=target,
        severity=severity,
        directness=directness,
        reversibility="conditional",
        state="confirmed",
        evidence_ids=evidence_ids,
        trace_ids=(trace_id,),
        rule_id=rule_id,
        confidence=clamp_confidence(confidence),
        causal_group=causal_group,
    )


def evaluate_damage(
    context: MingJuContext,
    pattern: PatternDecision,
    book: RecordBook,
) -> DamageResult:
    """Register Damage only when source, relation, target, and effect are active."""
    if pattern.state != AnalysisState.RESOLVED.value:
        return DamageResult(state=AnalysisState.UNRESOLVED.value)
    findings: list[DamageFinding] = []
    activations = context.activations
    pattern_id = pattern.pattern_id
    present = present_ids(activations)
    weak_dm = context.day_master_strength_level.lower() in WEAK_DM_LEVELS
    strong_dm = context.day_master_strength_level.lower() in STRONG_DM_LEVELS

    if "shang_guan" in present and "zheng_guan" in present:
        evidence_id = book.add_evidence(
            "damage_candidate",
            "mc01.damage.hurting_officer_copresent",
            source="mingju.damage",
            source_id="shang_guan",
            target_id="zheng_guan",
        )
        if is_material(activations, "shang_guan") and is_material(activations, "zheng_guan"):
            if pattern_id in {"zheng_guan", "qi_sha"} or GOD_FAMILY.get(pattern_id) == "officer":
                findings.append(
                    _confirm(
                        book,
                        "hurting_officer_attacks_officer",
                        "shang_guan",
                        "zheng_guan",
                        _severity(god_power(activations, "shang_guan"), god_power(activations, "zheng_guan")),
                        _directness(context, "shang_guan", "zheng_guan"),
                        (evidence_id,),
                        "MC-DMG-SG-001",
                        "officer_attack",
                        0.84,
                    )
                )

    if "pian_yin" in present and "shi_shen" in present:
        evidence_id = book.add_evidence(
            "damage_candidate",
            "mc01.damage.owl_copresent",
            source="mingju.damage",
            source_id="pian_yin",
            target_id="shi_shen",
        )
        if (
            is_material(activations, "pian_yin")
            and is_material(activations, "shi_shen")
            and pattern_id in {"shi_shen", "shang_guan"}
        ):
            findings.append(
                _confirm(
                    book,
                    "owl_robs_food",
                    "pian_yin",
                    "shi_shen",
                    _severity(god_power(activations, "pian_yin"), god_power(activations, "shi_shen")),
                    _directness(context, "pian_yin", "shi_shen"),
                    (evidence_id,),
                    "MC-DMG-OWL-001",
                    "resource_output",
                    0.82,
                )
            )

    peer_id = "jie_cai" if is_material(activations, "jie_cai") else "bi_jian"
    wealth_id = "zheng_cai" if god_power(activations, "zheng_cai") >= god_power(activations, "pian_cai") else "pian_cai"
    if peer_id in present and wealth_id in present:
        evidence_id = book.add_evidence(
            "damage_candidate",
            "mc01.damage.peer_wealth_copresent",
            source="mingju.damage",
            source_id=peer_id,
            target_id=wealth_id,
        )
        if (
            is_material(activations, peer_id)
            and is_material(activations, wealth_id)
            and (
                pattern_id in {"zheng_cai", "pian_cai"}
                or GOD_FAMILY.get(pattern_id) == "wealth"
            )
        ):
            findings.append(
                _confirm(
                    book,
                    "peer_robs_wealth",
                    peer_id,
                    wealth_id,
                    _severity(god_power(activations, peer_id), god_power(activations, wealth_id)),
                    _directness(context, peer_id, wealth_id),
                    (evidence_id,),
                    "MC-DMG-PEER-001",
                    "companion_wealth",
                    0.8,
                )
            )

    if "zheng_guan" in present and "qi_sha" in present:
        evidence_id = book.add_evidence(
            "damage_candidate",
            "mc01.damage.officer_killer_copresent",
            source="mingju.damage",
            source_id="qi_sha",
            target_id="zheng_guan",
        )
        guan_power = god_power(activations, "zheng_guan")
        sha_power = god_power(activations, "qi_sha")
        dominant = max(guan_power, sha_power)
        weaker = min(guan_power, sha_power)
        both_material = is_material(activations, "zheng_guan") and is_material(activations, "qi_sha")
        no_hierarchy = weaker > 0 and dominant / max(weaker, 0.15) < 2.4
        if both_material and no_hierarchy and pattern.family != "follow":
            findings.append(
                _confirm(
                    book,
                    "mixed_officer_killer",
                    "qi_sha",
                    "zheng_guan",
                    "moderate" if no_hierarchy else "minor",
                    _directness(context, "qi_sha", "zheng_guan"),
                    (evidence_id,),
                    "MC-DMG-MIX-001",
                    "guan_sha_conflict",
                    0.78,
                )
            )

    wealth_force = family_power(activations, "wealth")
    if weak_dm and wealth_force >= 3.0 and (
        pattern_id in {"zheng_cai", "pian_cai"} or GOD_FAMILY.get(pattern_id) == "wealth" or wealth_force >= 4.0
    ):
        evidence_id = book.add_evidence(
            "damage",
            "mc01.damage.wealth_overloads_weak_dm",
            source="mingju.damage",
            wealth_force=wealth_force,
            day_master_strength_level=context.day_master_strength_level,
        )
        findings.append(
            _confirm(
                book,
                "wealth_overloads_weak_day_master",
                "wealth",
                "day_master",
                "major" if wealth_force >= 4.5 else "moderate",
                "indirect",
                (evidence_id,),
                "MC-DMG-WL-001",
                "capacity_mismatch",
                0.8,
            )
        )

    if weak_dm and is_material(activations, "qi_sha") and god_power(activations, "qi_sha") >= 2.5:
        evidence_id = book.add_evidence(
            "damage",
            "mc01.damage.killer_overloads_weak_dm",
            source="mingju.damage",
            sha_power=god_power(activations, "qi_sha"),
        )
        findings.append(
            _confirm(
                book,
                "killer_overloads_weak_day_master",
                "qi_sha",
                "day_master",
                "major",
                "indirect",
                (evidence_id,),
                "MC-DMG-KS-001",
                "capacity_mismatch",
                0.81,
            )
        )

    output_force = family_power(activations, "output")
    resource_force = family_power(activations, "resource")
    if strong_dm and resource_force >= 3.5 and output_force < 1.2:
        evidence_id = book.add_evidence(
            "damage",
            "mc01.damage.resource_overload",
            source="mingju.damage",
            resource_force=resource_force,
            output_force=output_force,
        )
        findings.append(
            _confirm(
                book,
                "resource_overload",
                "resource",
                "output",
                "moderate",
                "indirect",
                (evidence_id,),
                "MC-DMG-RES-001",
                "flow_block",
                0.76,
            )
        )

    evidence_ids = tuple(eid for item in findings for eid in item.evidence_ids)
    return DamageResult(
        state=AnalysisState.RESOLVED.value,
        findings=tuple(findings),
        evidence_ids=evidence_ids,
        confidence=clamp_confidence(0.83 if findings else 0.9),
    )

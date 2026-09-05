"""Collect canonical evidence. Does not invent Pattern, Ten Gods, or Shen Sha."""

from __future__ import annotations

from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import (
    CombinationState,
    EvaluationStatus,
    PriorityTier,
    ShenShaClusterState,
    TenGodPresenceState,
    TenGodStructuralRole,
)
from engines.detailed_interpretation_engine.evidence_priority.candidates import EvidenceCandidate
from engines.detailed_interpretation_engine.evidence_priority.constants import (
    CRITICAL_DAMAGE_SEVERITIES,
    GOD_FAMILY_DOMAIN,
    MAJOR_COMBINATION_IDS,
    PATTERN_FAMILY_DOMAIN,
    SHEN_SHA_TIER_CEILING,
    TIER_INDEX,
)
from engines.detailed_interpretation_engine.evidence_priority.labels import (
    ACHIEVEMENT_LABELS,
    CAREER_LABELS,
    CONDITION_LABELS,
    INTEGRITY_LABELS,
    cluster_label,
    combination_label,
    damage_label,
    god_label,
    profile_label,
    rescue_label,
    star_label,
)
from engines.detailed_interpretation_engine.mc01 import Mc01StructuralSnapshot, snapshot_from_live_payload
from engines.detailed_interpretation_engine.ten_gods.combinations.helpers import ACTIVE_STATES
from engines.detailed_interpretation_engine.ten_gods.constants import LABEL_TO_GOD_ID
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_STRUCTURAL = ConfidenceValue(summary="structural")
_UNRESOLVED_STATES = frozenset(
    {
        EvaluationStatus.UNRESOLVED.value,
        EvaluationStatus.NOT_EVALUATED.value,
        EvaluationStatus.NOT_APPLICABLE.value,
    }
)


def collect_candidates(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> list[EvidenceCandidate]:
    """Gather existing MC-01 and Pack 07 findings as rankable candidates."""
    data = payload or {}
    snapshot = snapshot_from_live_payload(data)
    mingju = _mingju_view(data)
    interpretation = context.runtime.interpretation
    items: list[EvidenceCandidate] = []
    items.extend(_from_pattern(snapshot, interpretation.ten_gods.ecosystem.driver))
    items.extend(_from_integrity(snapshot))
    items.extend(_from_grade(snapshot))
    items.extend(_from_purity(snapshot, has_damage=bool(snapshot.damage_ids if snapshot else ())))
    items.extend(_from_damage_rescue(snapshot, mingju))
    items.extend(_from_profiles(snapshot, mingju))
    items.extend(_from_conditions(mingju, snapshot))
    items.extend(_from_ecosystem(interpretation.ten_gods.ecosystem, snapshot))
    items.extend(_from_combinations(interpretation.ten_gods.combinations))
    items.extend(_from_ten_gods(interpretation.ten_gods.natal, snapshot))
    items.extend(_from_shen_sha(interpretation.shen_sha))
    return items


def score_engine_grade(payload: Mapping[str, Any] | None) -> str:
    """Observe ScoreEngine customer grade. Never used as MC-01 Grade."""
    score = _mapping((payload or {}).get("score"))
    return str(score.get("grade") or "").strip()


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _mingju_view(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Prefer nested public profiles; keep snapshot Damage/Rescue identifiers."""
    snapshot = _mapping(payload.get("_mingju"))
    public = _mapping(payload.get("mingju"))
    merged = dict(snapshot)
    merged.update(public)
    if snapshot.get("damage"):
        merged["damage"] = snapshot["damage"]
    if snapshot.get("rescue"):
        merged["rescue"] = snapshot["rescue"]
    return merged


def _trace(*parts: str) -> tuple[str, ...]:
    token = "-".join(part for part in parts if part)
    return (f"TR-P7-EPR-{token}",) if token else ()


def _pattern_god_id(label: str) -> str:
    return LABEL_TO_GOD_ID.get(label.strip(), "")


def _pattern_domain(label: str) -> str:
    return PATTERN_FAMILY_DOMAIN.get(label.strip(), "pattern")


def _assignment_ready(state: str, subject: str) -> bool:
    return bool(subject.strip()) and state not in _UNRESOLVED_STATES


def _from_pattern(snapshot: Mc01StructuralSnapshot | None, driver: Any) -> list[EvidenceCandidate]:
    if snapshot is None or not snapshot.pattern:
        return []
    god_id = _pattern_god_id(snapshot.pattern)
    driver_subject = str(getattr(driver, "subject", "") or "")
    same_driver = bool(driver_subject) and driver_subject in {god_id, snapshot.pattern}
    sources = [f"mc01.pattern:{snapshot.pattern}"]
    supporting: list[str] = []
    if same_driver:
        sources.append(f"ecosystem.driver:{driver_subject}")
        supporting.append("di04.driver")
    return [
        EvidenceCandidate(
            semantic_key="pattern.primary",
            source_kind="pattern",
            source_refs=tuple(sources),
            domain="pattern",
            category="driver",
            evidence_type="structural",
            tier=PriorityTier.P0,
            customer_label=snapshot.pattern,
            tier_reason="tier:P0:pattern_backbone",
            confidence=_STRUCTURAL,
            confidence_source="mc01.pattern",
            trace_ids=_trace("pattern", god_id or "primary"),
            supporting_evidence=tuple(supporting),
            node_kind="pattern.primary",
            merge_origin="pattern" + ("+driver" if same_driver else ""),
        )
    ]


def _from_integrity(snapshot: Mc01StructuralSnapshot | None) -> list[EvidenceCandidate]:
    if snapshot is None or not snapshot.integrity:
        return []
    label = INTEGRITY_LABELS.get(snapshot.integrity, snapshot.integrity)
    return [
        EvidenceCandidate(
            semantic_key="integrity.state",
            source_kind="integrity",
            source_refs=(f"mc01.integrity:{snapshot.integrity}",),
            domain="integrity",
            category="structural",
            evidence_type="structural",
            tier=PriorityTier.P0,
            customer_label=label,
            tier_reason="tier:P0:integrity_backbone",
            confidence=_STRUCTURAL,
            confidence_source="mc01.integrity",
            trace_ids=_trace("integrity", snapshot.integrity),
            node_kind="integrity.state",
        )
    ]


def _from_grade(snapshot: Mc01StructuralSnapshot | None) -> list[EvidenceCandidate]:
    if snapshot is None or not snapshot.grade:
        return []
    return [
        EvidenceCandidate(
            semantic_key="grade.value",
            source_kind="grade",
            source_refs=(f"mc01.grade:{snapshot.grade}",),
            domain="grade",
            category="structural",
            evidence_type="structural",
            tier=PriorityTier.P0,
            customer_label=snapshot.grade,
            tier_reason="tier:P0:mc01_structural_grade",
            confidence=_STRUCTURAL,
            confidence_source="mc01.grade",
            trace_ids=_trace("grade", snapshot.grade),
            node_kind="grade.value",
        )
    ]


def _from_purity(
    snapshot: Mc01StructuralSnapshot | None,
    *,
    has_damage: bool,
) -> list[EvidenceCandidate]:
    if snapshot is None or not snapshot.purity or has_damage:
        return []
    mixed = snapshot.purity in {"mixed", "heavily_mixed", "structurally_impure"}
    if not mixed:
        return []
    return [
        EvidenceCandidate(
            semantic_key="purity.state",
            source_kind="purity",
            source_refs=(f"mc01.purity:{snapshot.purity}",),
            domain="pattern",
            category="supporting",
            evidence_type="structural",
            tier=PriorityTier.P4,
            customer_label="Pha tạp chưa thành tổn thương",
            tier_reason="tier:P4:purity_without_damage",
            confidence=_STRUCTURAL,
            confidence_source="mc01.purity",
            trace_ids=_trace("purity", snapshot.purity),
            node_kind="purity.state",
        )
    ]


def _damage_rows(snapshot: Mc01StructuralSnapshot | None, mingju: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in mingju.get("damage") or ():
        if isinstance(item, Mapping):
            rows.append(dict(item))
    if rows:
        return rows
    if snapshot is None:
        return []
    return [{"damage_id": item, "damage_type": "", "severity": ""} for item in snapshot.damage_ids]


def _rescue_rows(snapshot: Mc01StructuralSnapshot | None, mingju: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in mingju.get("rescue") or ():
        if isinstance(item, Mapping):
            rows.append(dict(item))
    if rows:
        return rows
    if snapshot is None:
        return []
    return [{"rescue_id": item, "rescue_type": "", "target_damage_ids": []} for item in snapshot.rescue_ids]


def _damage_tier(severity: str) -> PriorityTier:
    token = severity.strip().lower()
    if token in CRITICAL_DAMAGE_SEVERITIES:
        return PriorityTier.P0
    if token in {"major"}:
        return PriorityTier.P1
    if token in {"minor"}:
        return PriorityTier.P2
    return PriorityTier.P1


def _from_damage_rescue(
    snapshot: Mc01StructuralSnapshot | None,
    mingju: Mapping[str, Any],
) -> list[EvidenceCandidate]:
    rescued: set[str] = set()
    items: list[EvidenceCandidate] = []
    for row in _rescue_rows(snapshot, mingju):
        targets = tuple(str(item) for item in (row.get("target_damage_ids") or ()) if item)
        rescued.update(targets)
        rescue_id = str(row.get("rescue_id") or row.get("rescue_type") or "rescue")
        rescue_type = str(row.get("rescue_type") or "")
        strength = str(row.get("strength") or "")
        tier = PriorityTier.P0 if strength in CRITICAL_DAMAGE_SEVERITIES else PriorityTier.P3
        if strength == "major":
            tier = PriorityTier.P1
        items.append(
            EvidenceCandidate(
                semantic_key=f"rescue:{rescue_id}",
                source_kind="rescue",
                source_refs=(f"mc01.rescue:{rescue_id}",),
                domain="capacity",
                category="opportunity",
                evidence_type="structural",
                tier=tier,
                customer_label=rescue_label(rescue_type, "Cứu giải cấu trúc"),
                tier_reason="tier:rescue:does_not_delete_damage",
                confidence=_STRUCTURAL,
                confidence_source="mc01.rescue",
                conditions=(CONDITION_LABELS.get(rescue_type, ""),)
                if CONDITION_LABELS.get(rescue_type)
                else (),
                trace_ids=_trace("rescue", rescue_id),
                supporting_evidence=targets,
                node_kind="rescue.item",
            )
        )
    for row in _damage_rows(snapshot, mingju):
        damage_id = str(row.get("damage_id") or row.get("damage_type") or "damage")
        damage_type = str(row.get("damage_type") or "")
        severity = str(row.get("severity") or "")
        is_rescued = damage_id in rescued
        items.append(
            EvidenceCandidate(
                semantic_key=f"damage:{damage_id}",
                source_kind="damage",
                source_refs=(f"mc01.damage:{damage_id}",),
                domain="risk",
                category="risk",
                evidence_type="risk",
                tier=_damage_tier(severity),
                customer_label=damage_label(damage_type, "Tổn thương cấu trúc"),
                tier_reason="tier:damage:visible_with_or_without_rescue",
                confidence=_STRUCTURAL,
                confidence_source="mc01.damage",
                conditions=(CONDITION_LABELS.get(damage_type, ""),)
                if CONDITION_LABELS.get(damage_type)
                else (),
                trace_ids=_trace("damage", damage_id),
                node_kind="damage.item",
                rescued=is_rescued,
            )
        )
    return items


def _split_profile_ref(raw: str) -> tuple[str, str]:
    if ":" in raw:
        left, right = raw.split(":", 1)
        return left.strip(), right.strip()
    return raw.strip(), ""


def _from_profiles(
    snapshot: Mc01StructuralSnapshot | None,
    mingju: Mapping[str, Any],
) -> list[EvidenceCandidate]:
    items: list[EvidenceCandidate] = []
    achievement = _mapping(mingju.get("achievement"))
    capabilities = [
        str(item) for item in (achievement.get("dominant_capabilities") or ()) if item
    ]
    if not capabilities and snapshot and snapshot.achievement:
        capabilities = [part.strip() for part in snapshot.achievement.split(",") if part.strip()]
    if capabilities:
        labels = [ACHIEVEMENT_LABELS.get(item, item) for item in capabilities]
        domain = "academic" if "academic" in capabilities else "career"
        items.append(
            EvidenceCandidate(
                semantic_key="achievement.drivers",
                source_kind="achievement",
                source_refs=tuple(f"mc01.achievement:{item}" for item in capabilities),
                domain=domain,
                category="opportunity",
                evidence_type="domain",
                tier=PriorityTier.P1,
                customer_label=" · ".join(labels),
                tier_reason="tier:P1:achievement_drivers",
                confidence=_STRUCTURAL,
                confidence_source="mc01.achievement",
                trace_ids=_trace("achievement"),
                node_kind="achievement.drivers",
                merge_origin="achievement",
            )
        )
    wealth = _mapping(mingju.get("wealth"))
    wealth_dims = [item for item in (wealth.get("dimensions") or ()) if isinstance(item, Mapping)]
    if wealth_dims:
        for row in wealth_dims:
            dimension = str(row.get("dimension") or "")
            classification = str(row.get("classification") or "")
            polarity = str(row.get("polarity") or "")
            category = "risk" if polarity == "higher_is_riskier" or "volatil" in dimension else "opportunity"
            if classification in {"below_average", "low", "very_low"} and dimension != "wealth_volatility":
                category = "risk"
            items.append(
                EvidenceCandidate(
                    semantic_key=f"wealth:{dimension}",
                    source_kind="wealth",
                    source_refs=(f"mc01.wealth:{dimension}",),
                    domain="wealth",
                    category=category,
                    evidence_type="domain",
                    tier=PriorityTier.P1,
                    customer_label=profile_label(dimension, classification),
                    tier_reason="tier:P1:wealth_dimension_split",
                    confidence=_STRUCTURAL,
                    confidence_source="mc01.wealth",
                    trace_ids=_trace("wealth", dimension),
                    node_kind=f"wealth.{dimension}",
                )
            )
    elif snapshot and snapshot.wealth_profile:
        dimension, classification = _split_profile_ref(snapshot.wealth_profile)
        items.append(
            EvidenceCandidate(
                semantic_key=f"wealth:{dimension or 'profile'}",
                source_kind="wealth",
                source_refs=(f"mc01.wealth:{snapshot.wealth_profile}",),
                domain="wealth",
                category="opportunity",
                evidence_type="domain",
                tier=PriorityTier.P1,
                customer_label=profile_label(dimension, classification) or snapshot.wealth_profile,
                tier_reason="tier:P1:wealth_profile",
                confidence=_STRUCTURAL,
                confidence_source="mc01.wealth",
                trace_ids=_trace("wealth"),
                node_kind="wealth.profile",
            )
        )
    career = _mapping(mingju.get("career"))
    styles = [str(item) for item in (career.get("dominant_work_styles") or ()) if item]
    if not styles and snapshot and snapshot.career_profile:
        styles = [part.strip() for part in snapshot.career_profile.split(",") if part.strip()]
    if styles:
        labels = [CAREER_LABELS.get(item, item) for item in styles]
        items.append(
            EvidenceCandidate(
                semantic_key="career.drivers",
                source_kind="career",
                source_refs=tuple(f"mc01.career:{item}" for item in styles),
                domain="career",
                category="opportunity",
                evidence_type="domain",
                tier=PriorityTier.P1,
                customer_label=" · ".join(labels),
                tier_reason="tier:P1:career_structural",
                confidence=_STRUCTURAL,
                confidence_source="mc01.career",
                trace_ids=_trace("career"),
                node_kind="career.drivers",
            )
        )
    return items


def _from_conditions(
    mingju: Mapping[str, Any],
    snapshot: Mc01StructuralSnapshot | None,
) -> list[EvidenceCandidate]:
    decision = _mapping(mingju.get("decision"))
    conditions = [str(item) for item in (decision.get("conditions") or ()) if str(item).strip()]
    warnings = [str(item) for item in (decision.get("risks") or ()) if str(item).strip()]
    items: list[EvidenceCandidate] = []
    if not conditions and snapshot and snapshot.integrity in CONDITION_LABELS:
        conditions = [CONDITION_LABELS[snapshot.integrity]]
    for index, text in enumerate(conditions):
        mapped = CONDITION_LABELS.get(text, text)
        label = mapped if any(ord(char) > 127 for char in mapped) else ""
        if not label:
            continue
        items.append(
            EvidenceCandidate(
                semantic_key=f"condition:{index}",
                source_kind="condition",
                source_refs=(f"mc01.condition:{index}",),
                domain="capacity",
                category="condition",
                evidence_type="condition",
                tier=PriorityTier.P1,
                customer_label=label,
                tier_reason="tier:P1:expression_condition",
                confidence=_STRUCTURAL,
                confidence_source="mc01.decision.conditions",
                trace_ids=_trace("condition", str(index)),
                node_kind="condition.item",
            )
        )
    if snapshot and snapshot.integrity in {"mixed", "damaged_but_rescued", "conditionally_complete"}:
        fallback = CONDITION_LABELS.get("resource_overload") or CONDITION_LABELS.get("mixed")
        if fallback and not items:
            items.append(
                EvidenceCandidate(
                    semantic_key="condition:integrity",
                    source_kind="condition",
                    source_refs=(f"mc01.integrity:{snapshot.integrity}",),
                    domain="capacity",
                    category="condition",
                    evidence_type="condition",
                    tier=PriorityTier.P1,
                    customer_label=fallback,
                    tier_reason="tier:P1:integrity_expression_condition",
                    confidence=_STRUCTURAL,
                    confidence_source="mc01.integrity",
                    trace_ids=_trace("condition", "integrity"),
                    node_kind="condition.item",
                )
            )
    for index, text in enumerate(warnings):
        if not any(ord(char) > 127 for char in text):
            continue
        items.append(
            EvidenceCandidate(
                semantic_key=f"warning:{index}",
                source_kind="warning",
                source_refs=(f"mc01.warning:{index}",),
                domain="risk",
                category="warning",
                evidence_type="warning",
                tier=PriorityTier.P2,
                customer_label=text,
                tier_reason="tier:P2:customer_warning",
                confidence=_STRUCTURAL,
                confidence_source="mc01.decision.risks",
                trace_ids=_trace("warning", str(index)),
                node_kind="warning.item",
            )
        )
    return items


def _from_ecosystem(ecosystem: Any, snapshot: Mc01StructuralSnapshot | None) -> list[EvidenceCandidate]:
    items: list[EvidenceCandidate] = []
    pattern_god = _pattern_god_id(snapshot.pattern) if snapshot else ""
    driver = ecosystem.driver
    if _assignment_ready(driver.state.value, driver.subject) and driver.subject not in {
        pattern_god,
        snapshot.pattern if snapshot else "",
    }:
        items.append(
            EvidenceCandidate(
                semantic_key="ecosystem.driver",
                source_kind="ten_gods_ecosystem",
                source_refs=(f"di04.driver:{driver.subject}",),
                domain=_pattern_domain(snapshot.pattern) if snapshot else "pattern",
                category="driver",
                evidence_type="balance",
                tier=PriorityTier.P0,
                customer_label=god_label(driver.subject),
                tier_reason="tier:P0:consumed_di04_driver",
                confidence=driver.confidence,
                confidence_source="di04.driver",
                trace_ids=driver.evidence_ids or _trace("driver", driver.subject),
                node_kind="ecosystem.driver",
            )
        )
    bottleneck = ecosystem.bottleneck
    if _assignment_ready(bottleneck.state.value, bottleneck.subject):
        items.append(
            EvidenceCandidate(
                semantic_key="ecosystem.bottleneck",
                source_kind="ten_gods_ecosystem",
                source_refs=(f"di04.bottleneck:{bottleneck.subject}",),
                domain=GOD_FAMILY_DOMAIN.get(bottleneck.subject, "capacity"),
                category="bottleneck",
                evidence_type="balance",
                tier=PriorityTier.P0,
                customer_label=god_label(bottleneck.subject),
                tier_reason="tier:P0:critical_bottleneck_must_surface",
                confidence=bottleneck.confidence,
                confidence_source="di04.bottleneck",
                trace_ids=bottleneck.evidence_ids or _trace("bottleneck", bottleneck.subject),
                node_kind="ecosystem.bottleneck",
            )
        )
    for role_name, assignment in (
        ("excessive", ecosystem.excessive),
        ("blocked", ecosystem.blocked),
        ("suppressed", ecosystem.suppressed),
    ):
        if not _assignment_ready(assignment.state.value, assignment.subject):
            continue
        items.append(
            EvidenceCandidate(
                semantic_key=f"ecosystem.{role_name}",
                source_kind="ten_gods_ecosystem",
                source_refs=(f"di04.{role_name}:{assignment.subject}",),
                domain=GOD_FAMILY_DOMAIN.get(assignment.subject, "capacity"),
                category="risk",
                evidence_type="balance",
                tier=PriorityTier.P1,
                customer_label=god_label(assignment.subject),
                tier_reason=f"tier:P1:ecosystem_{role_name}",
                confidence=assignment.confidence,
                confidence_source=f"di04.{role_name}",
                trace_ids=assignment.evidence_ids or _trace(role_name, assignment.subject),
                node_kind=f"ecosystem.{role_name}",
            )
        )
    return items


def _from_combinations(collection: Any) -> list[EvidenceCandidate]:
    items: list[EvidenceCandidate] = []
    for item in collection.items:
        if item.source_combination_id or not item.combination_id:
            continue
        label = combination_label(item.combination_id)
        if not label:
            continue
        if item.state in ACTIVE_STATES:
            major = item.combination_id in MAJOR_COMBINATION_IDS or bool(item.damage_ids)
            tier = PriorityTier.P1 if major and item.state is CombinationState.CONFIRMED else PriorityTier.P2
            category = "risk" if item.risk_expressions and not item.positive_expressions else "combination"
            if item.damage_ids:
                category = "risk"
            elif item.positive_expressions:
                category = "opportunity"
            items.append(
                EvidenceCandidate(
                    semantic_key=f"combination:{item.combination_id}",
                    source_kind="combination",
                    source_refs=(f"di02.{item.combination_id}",),
                    domain="capacity",
                    category=category,
                    evidence_type="combination",
                    tier=tier,
                    customer_label=label,
                    tier_reason="tier:combination:active_chain",
                    confidence=item.confidence,
                    confidence_source="di02.combination",
                    conditions=item.conditions,
                    trace_ids=item.trace_ids or _trace("combination", item.combination_id),
                    node_kind=f"ten_god_chain.{item.combination_id}",
                )
            )
            continue
        items.append(
            EvidenceCandidate(
                semantic_key=f"combination:{item.combination_id}",
                source_kind="combination",
                source_refs=(f"di02.{item.combination_id}",),
                domain="capacity",
                category="supporting",
                evidence_type="combination",
                tier=PriorityTier.P4,
                customer_label=label,
                tier_reason="tier:P4:inactive_or_unresolved_chain",
                confidence=item.confidence,
                confidence_source="di02.combination",
                trace_ids=item.trace_ids or _trace("combination", item.combination_id),
                node_kind=f"ten_god_chain.{item.combination_id}",
            )
        )
    return items


def _from_ten_gods(collection: Any, snapshot: Mc01StructuralSnapshot | None) -> list[EvidenceCandidate]:
    pattern_god = _pattern_god_id(snapshot.pattern) if snapshot else ""
    items: list[EvidenceCandidate] = []
    for item in collection.items:
        if item.ten_god_id == pattern_god:
            continue
        if item.presence_state in {TenGodPresenceState.ABSENT, TenGodPresenceState.UNRESOLVED}:
            continue
        if item.state is EvaluationStatus.UNRESOLVED:
            continue
        if item.structural_role is TenGodStructuralRole.PRIMARY_PATTERN:
            continue
        hidden_only = item.presence_state is TenGodPresenceState.HIDDEN_ONLY
        items.append(
            EvidenceCandidate(
                semantic_key=f"ten_god:{item.ten_god_id}",
                source_kind="ten_god",
                source_refs=(f"di01.{item.ten_god_id}",),
                domain=GOD_FAMILY_DOMAIN.get(item.ten_god_id, "capacity"),
                category="supporting",
                evidence_type="structural",
                tier=PriorityTier.P4 if hidden_only else PriorityTier.P2,
                customer_label=god_label(item.ten_god_id),
                tier_reason="tier:P2:material_ten_god" if not hidden_only else "tier:P4:hidden_only",
                confidence=item.confidence,
                confidence_source="di01.ten_god",
                conditions=item.conditions,
                trace_ids=item.trace_ids or _trace("ten_god", item.ten_god_id),
                node_kind=f"ten_god.{item.ten_god_id}",
            )
        )
    return items


def _clamp_shen_sha(tier: PriorityTier) -> PriorityTier:
    if TIER_INDEX.get(tier.value, 99) < TIER_INDEX.get(SHEN_SHA_TIER_CEILING.value, 99):
        return SHEN_SHA_TIER_CEILING
    return tier


def _from_shen_sha(shell: Any) -> list[EvidenceCandidate]:
    items: list[EvidenceCandidate] = []
    clustered: set[str] = set()
    for cluster in shell.ecosystem.clusters:
        if cluster.state is ShenShaClusterState.UNRESOLVED or not cluster.members:
            continue
        clustered.update(member.shen_sha_id for member in cluster.members)
        label = cluster_label(cluster.cluster_id)
        if not label:
            continue
        if cluster.state is ShenShaClusterState.ACTIVE:
            items.append(
                EvidenceCandidate(
                    semantic_key=f"shen_sha_cluster:{cluster.cluster_id}",
                    source_kind="shen_sha_cluster",
                    source_refs=(f"di06.{cluster.cluster_id}",) + tuple(
                        f"di05.{item}" for item in cluster.applied_members
                    ),
                    domain=(cluster.supported_domains[0] if cluster.supported_domains else "protection"),
                    category="cluster",
                    evidence_type="cluster",
                    tier=_clamp_shen_sha(PriorityTier.P2),
                    customer_label=label,
                    tier_reason="tier:P2:active_shen_sha_cluster_ceiling",
                    confidence=ConfidenceValue(summary="secondary"),
                    confidence_source="di06.cluster",
                    conditions=cluster.conditions,
                    trace_ids=cluster.trace_ids or _trace("cluster", cluster.cluster_id),
                    node_kind=f"shen_sha_cluster.{cluster.cluster_id}",
                )
            )
            continue
        tier = PriorityTier.P4 if cluster.state is ShenShaClusterState.BLOCKED else PriorityTier.P5
        items.append(
            EvidenceCandidate(
                semantic_key=f"shen_sha_cluster:{cluster.cluster_id}",
                source_kind="shen_sha_cluster",
                source_refs=(f"di06.{cluster.cluster_id}",),
                domain="protection",
                category="supporting",
                evidence_type="cluster",
                tier=tier,
                customer_label=label,
                tier_reason="tier:shen_sha:not_dominant",
                confidence=ConfidenceValue(summary="secondary"),
                confidence_source="di06.cluster",
                trace_ids=cluster.trace_ids or _trace("cluster", cluster.cluster_id),
                node_kind=f"shen_sha_cluster.{cluster.cluster_id}",
                filtered=cluster.state is ShenShaClusterState.UNRESOLVED,
            )
        )
    for item in shell.individual.items:
        if not item.detected or item.shen_sha_id in clustered:
            continue
        label = star_label(item.shen_sha_id)
        if not label:
            continue
        applied = item.modifier_state.value in {"applied", "weak_support", "qualified"}
        items.append(
            EvidenceCandidate(
                semantic_key=f"shen_sha:{item.shen_sha_id}",
                source_kind="shen_sha",
                source_refs=(f"di05.{item.shen_sha_id}",),
                domain=(item.supported_domains[0] if item.supported_domains else "protection"),
                category="supporting",
                evidence_type="cluster",
                tier=_clamp_shen_sha(PriorityTier.P3) if applied else PriorityTier.P5,
                customer_label=label,
                tier_reason="tier:shen_sha:secondary_evidence",
                confidence=item.confidence,
                confidence_source="di05.shen_sha",
                conditions=item.conditions,
                trace_ids=item.trace_ids or _trace("shen_sha", item.shen_sha_id),
                node_kind=f"shen_sha.{item.shen_sha_id}",
            )
        )
    return items

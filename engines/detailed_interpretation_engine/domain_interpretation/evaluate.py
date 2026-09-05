"""Assemble DomainInterpretationResult objects from ranked evidence."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    DAMAGE_SOURCE_KINDS,
    HIGH_BANDS,
    LOW_BANDS,
    MAIN_DOMAIN_IDS,
    OUTPUT_WEALTH_COMBINATIONS,
    PEER_WEALTH_COMBINATIONS,
    RISK_CATEGORIES,
    SUPPORT_DOMAIN_IDS,
)
from engines.detailed_interpretation_engine.domain_interpretation.drivers import elect_canonical_driver
from engines.detailed_interpretation_engine.domain_interpretation.facts import (
    DomainFacts,
    classification_of,
)
from engines.detailed_interpretation_engine.domain_interpretation.labels import (
    CONDITION_LABELS,
    DAMAGE_LABELS,
    DRIVER_LABELS,
    OPPORTUNITY_LABELS,
    RISK_LABELS,
    SUMMARY_TEMPLATES,
    UNRESOLVED_COPY,
    capability_label,
    damage_label,
)
from engines.detailed_interpretation_engine.domain_interpretation.roles import (
    copied_priority,
    damage_risk_label,
    evidence_ids_of,
    label_of,
    pick_role,
    scoped_findings,
    shen_sha_findings,
    trace_ids_of,
)
from engines.detailed_interpretation_engine.domain_interpretation.states import (
    axis_map,
    band_state,
    has_major_damage,
    is_split,
    strongest_band,
    synthesize_state,
    weakest_band,
)
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult
from engines.detailed_interpretation_engine.enums import DomainState
from engines.detailed_interpretation_engine.evidence import EvidencePriorityFinding
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_AUTHORITY_AXES = {
    "formal_authority": "authority",
    "organizational_authority": "institutional_career",
    "managerial_authority": "management",
    "command_authority": "leadership",
    "professional_authority": "academic",
    "decision_authority": "leadership",
    "authority_stability": "stability",
}
_CAREER_AXES = {
    "organizational_fit": "institutional_fit",
    "autonomy_need": "autonomy_need",
    "leadership_fit": "leadership_fit",
    "management_fit": "management_fit",
    "specialist_fit": "specialist_fit",
    "technical_fit": "technical_fit",
    "academic_fit": "academic_fit",
    "creative_fit": "creative_fit",
    "entrepreneurial_fit": "entrepreneurial_fit",
    "public_facing_fit": "public_facing_fit",
    "career_stability": "career_stability",
}
_SUPPORT_FROM_ACHIEVEMENT = {
    "creative": "creative",
    "academic": "academic",
    "leadership": "leadership",
    "management": "management",
    "learning": "academic",
}


def evaluate_main_domains(facts: DomainFacts) -> dict[str, DomainInterpretationResult]:
    """Build the six published natal domains."""
    return {
        "authority": evaluate_authority(facts),
        "career": evaluate_career(facts),
        "wealth": evaluate_wealth(facts),
        "relationship": evaluate_relationship(facts),
        "legacy": evaluate_legacy(facts),
        "vitality": evaluate_vitality(facts),
    }


def evaluate_support_domains(facts: DomainFacts) -> dict[str, DomainInterpretationResult]:
    """Minimal internal DI-08 support domains. Not customer sections."""
    results: dict[str, DomainInterpretationResult] = {}
    for domain_id in SUPPORT_DOMAIN_IDS:
        source = _SUPPORT_FROM_ACHIEVEMENT.get(domain_id, "")
        classification = classification_of(facts.achievement, source) if source else ""
        if domain_id == "personal_growth":
            classification = strongest_band(
                (
                    classification_of(facts.achievement, "academic"),
                    "moderate" if facts.integrity in {"mixed", "conditionally_complete"} else "",
                )
            )
        if not classification:
            results[domain_id] = _result(domain_id, facts, DomainState.UNRESOLVED, {}, missing=True)
            continue
        state = synthesize_state((classification,), facts=facts)
        dimensions = {domain_id: classification}
        results[domain_id] = _result(domain_id, facts, state, dimensions)
    return results


def evaluate_authority(facts: DomainFacts) -> DomainInterpretationResult:
    """Explain Achievement.authority and Quan/Sát evidence. Not a job-title forecast."""
    dimensions = axis_map(facts.achievement, _AUTHORITY_AXES)
    if "institutional_fit" in facts.career:
        dimensions.setdefault(
            "organizational_authority",
            facts.career["institutional_fit"].classification,
        )
    if "management_fit" in facts.career:
        dimensions.setdefault("managerial_authority", facts.career["management_fit"].classification)
    if "leadership_fit" in facts.career:
        dimensions.setdefault("command_authority", facts.career["leadership_fit"].classification)
    pressure = "elevated" if "resource_overload" in facts.damage_types else "moderate"
    dimensions["authority_pressure"] = pressure
    formal = dimensions.get("formal_authority", "")
    # Authority ≠ Leadership ≠ Management: do not promote Quan from management/leadership fits.
    if formal:
        state = synthesize_state((formal,), facts=facts)
    elif dimensions.get("managerial_authority") or dimensions.get("command_authority"):
        state = DomainState.MODERATE
        if has_major_damage(facts):
            state = DomainState.CONDITIONAL
    else:
        state = DomainState.UNRESOLVED
    risks, risk = _authority_risks(facts, dimensions)
    opportunities = _opportunities(facts, ("professional_authority", "management_capacity"))
    return _result(
        "authority",
        facts,
        state,
        dimensions,
        risks=risks,
        risk=risk,
        opportunities=opportunities,
        conditions=_conditions(facts, state, "requires_structural_integrity"),
    )


def evaluate_career(facts: DomainFacts) -> DomainInterpretationResult:
    """Explain CareerProfile. Does not emit an exact profession."""
    dimensions = axis_map(facts.career, _CAREER_AXES)
    if not dimensions and facts.work_styles:
        for style in facts.work_styles:
            key = _style_to_fit(style)
            if key:
                dimensions[key] = "above_average"
    pressure = "elevated" if has_major_damage(facts) else "moderate"
    dimensions["career_pressure"] = pressure
    core_keys = ("academic_fit", "management_fit", "leadership_fit", "entrepreneurial_fit")
    core = tuple(dimensions[key] for key in core_keys if key in dimensions)
    if not core and facts.work_styles:
        core = ("above_average",)
    missing = not core and not facts.work_styles
    split = is_split(
        strongest_band(tuple(dimensions.get(key, "") for key in ("academic_fit", "leadership_fit"))),
        classification_of(facts.career, "management_fit") or dimensions.get("management_fit", ""),
    )
    # Leadership ≠ Management: preserve a split only when one is high and the other is low.
    if dimensions.get("leadership_fit") in HIGH_BANDS and dimensions.get("management_fit") in LOW_BANDS:
        split = True
    state = synthesize_state(core, facts=facts, split=split, missing=missing)
    risks: list[str] = []
    risk = ""
    if dimensions.get("management_fit") in LOW_BANDS and (
        dimensions.get("leadership_fit") in HIGH_BANDS or "leadership_command" in facts.work_styles
    ):
        risks.append("management_gap")
        risk = "management_gap"
    if "managerial" in facts.work_styles and dimensions.get("academic_fit") in LOW_BANDS:
        risks.append("role_mismatch")
        risk = risk or "role_mismatch"
    opportunities = _opportunities(facts, ("academic_capacity", "management_capacity", "leadership_capacity"))
    condition = ""
    if risk == "management_gap" or state in {DomainState.STRONG, DomainState.CONDITIONAL}:
        condition = "requires_operational_systems"
    return _result(
        "career",
        facts,
        state,
        dimensions,
        risks=tuple(dict.fromkeys(risks)),
        risk=risk,
        opportunities=opportunities,
        conditions=_conditions(facts, state, condition),
    )


def evaluate_wealth(facts: DomainFacts) -> DomainInterpretationResult:
    """Explain WealthProfile. Creation ≠ Retention. Do not infer 'rich'."""
    creation = classification_of(facts.wealth, "wealth_creation")
    retention = classification_of(facts.wealth, "wealth_retention")
    accumulation = classification_of(facts.wealth, "wealth_accumulation")
    expansion = classification_of(facts.wealth, "business_expansion")
    volatility = classification_of(facts.wealth, "financial_volatility")
    dimensions = {
        key: value
        for key, value in {
            "creation": creation,
            "commercialization": expansion,
            "cashflow": creation,
            "retention": retention,
            "accumulation": accumulation,
            "expansion": expansion,
            "capital_discipline": retention,
            "volatility": volatility,
            "wealth_sustainability": _sustainability(retention, accumulation, volatility),
        }.items()
        if value
    }
    missing = not (creation or retention or accumulation)
    split = is_split(strongest_band((retention, accumulation)), creation) or is_split(
        creation, strongest_band((retention, accumulation))
    )
    state = synthesize_state(
        tuple(item for item in (creation, retention, accumulation) if item),
        facts=facts,
        split=split,
        missing=missing,
    )
    risks: list[str] = []
    risk = ""
    leakage = ""
    if creation in LOW_BANDS:
        leakage = "creation"
    if retention in LOW_BANDS:
        risks.append("poor_retention")
        risk = "poor_retention"
        leakage = leakage or "retention"
    if volatility in HIGH_BANDS:
        risks.append("high_volatility")
        risk = risk or "high_volatility"
    opportunities: tuple[str, ...] = ()
    if retention in HIGH_BANDS or accumulation in HIGH_BANDS:
        opportunities = ("retention_strength",)
    elif creation in HIGH_BANDS:
        opportunities = ("creation_capacity",)
    condition = "requires_retention_discipline" if retention in LOW_BANDS or volatility in HIGH_BANDS else ""
    if state in {DomainState.STRONG, DomainState.CONDITIONAL, DomainState.FRAGMENTED}:
        condition = condition or "requires_structural_integrity"
    return _result(
        "wealth",
        facts,
        state,
        dimensions,
        risks=tuple(risks),
        risk=risk,
        leakage=leakage,
        opportunities=opportunities,
        conditions=_conditions(facts, state, condition),
    )


def evaluate_relationship(facts: DomainFacts) -> DomainInterpretationResult:
    """Structural relationship view. Hồng Loan / Thiên Hỷ stay secondary."""
    peer_conflict = any(item in PEER_WEALTH_COMBINATIONS for item in facts.combination_ids)
    scoped = scoped_findings(facts.ep, "relationship")
    structural = tuple(item for item in scoped if item.source_kind not in {"shen_sha", "shen_sha_cluster"})
    if not structural and not peer_conflict:
        return _result("relationship", facts, DomainState.UNRESOLVED, {}, missing=True)
    dimensions = {
        "compatibility": "moderate" if structural else "",
        "communication": "below_average" if peer_conflict else "moderate",
        "trust": "moderate",
        "commitment": "moderate",
        "relationship_support": "moderate" if structural else "",
        "relationship_conflict": "above_average" if peer_conflict else "moderate",
        "independence": classification_of(facts.achievement, "independence") or "moderate",
        "dependency": "moderate",
        "mutual_growth": "moderate",
        "relationship_resilience": "moderate",
        "relationship_sustainability": "moderate",
    }
    dimensions = {key: value for key, value in dimensions.items() if value}
    state = DomainState.MODERATE
    if peer_conflict:
        state = DomainState.FRAGMENTED
    risks = ("communication_gap",) if peer_conflict else ()
    return _result(
        "relationship",
        facts,
        state,
        dimensions,
        risks=risks,
        risk="communication_gap" if peer_conflict else "",
        leakage="communication" if peer_conflict else "",
        opportunities=(),
        conditions=_conditions(facts, state, "requires_communication_support" if peer_conflict else ""),
        ignore_chart_driver=True,
    )


def evaluate_legacy(facts: DomainFacts) -> DomainInterpretationResult:
    """Explain knowledge/creative transmission. Not fertility or child count."""
    knowledge = classification_of(facts.achievement, "academic")
    creative = classification_of(facts.achievement, "creative")
    business = classification_of(facts.achievement, "entrepreneurship")
    dimensions = {
        key: value
        for key, value in {
            "knowledge_legacy": knowledge,
            "creative_legacy": creative,
            "business_legacy": business,
            "institutional_legacy": classification_of(facts.achievement, "institutional_career"),
            "legacy_sustainability": knowledge or creative,
            "legacy_visibility": classification_of(facts.achievement, "public_visibility"),
        }.items()
        if value
    }
    missing = not dimensions
    state = synthesize_state(tuple(dimensions.values()), facts=facts, missing=missing)
    risks = ("transmission_gap",) if knowledge in LOW_BANDS or missing else ()
    return _result(
        "legacy",
        facts,
        state,
        dimensions,
        risks=risks,
        risk="transmission_gap" if risks else "",
        leakage="transmission" if risks else "",
        opportunities=("knowledge_legacy",) if knowledge else (),
        conditions=_conditions(facts, state, "requires_structural_integrity"),
    )


def evaluate_vitality(facts: DomainFacts) -> DomainInterpretationResult:
    """Capacity / stress / recovery. Not disease or life expectancy."""
    overload = "resource_overload" in facts.damage_types
    output_combo = any(item in OUTPUT_WEALTH_COMBINATIONS for item in facts.combination_ids)
    capacity = "above_average" if facts.integrity not in {"failed", "damaged"} else "below_average"
    if facts.integrity in {"mixed", "conditionally_complete", "damaged_but_rescued"}:
        capacity = "moderate"
    stress = "above_average" if overload else "moderate"
    recovery = "below_average" if overload and not output_combo else "moderate"
    if facts.has_rescue and overload:
        recovery = "moderate"
    resilience = "above_average" if facts.has_rescue else "moderate"
    dimensions = {
        "capacity": capacity,
        "stress": stress,
        "recovery": recovery,
        "resilience": resilience,
        "health_expression": "moderate",
        "energy_efficiency": "below_average" if overload else "moderate",
        "energy_stability": "moderate" if facts.integrity == "mixed" else capacity,
        "fatigue_risk": "above_average" if overload else "moderate",
        "burnout_risk": "above_average" if overload else "moderate",
    }
    split = is_split(capacity, recovery)
    state = synthesize_state((capacity, recovery), facts=facts, split=split)
    if overload and state in {DomainState.STRONG, DomainState.VERY_STRONG, DomainState.MODERATE}:
        state = DomainState.CONDITIONAL if not split else DomainState.FRAGMENTED
    risks: list[str] = []
    risk = ""
    if recovery in LOW_BANDS:
        risks.append("poor_recovery")
        risk = "poor_recovery"
    if overload:
        risks.append("stress_overload")
        risk = risk or "stress_overload"
    return _result(
        "vitality",
        facts,
        state,
        dimensions,
        risks=tuple(risks),
        risk=risk,
        leakage="recovery" if recovery in LOW_BANDS else ("stress" if overload else ""),
        opportunities=("recovery_discipline",) if overload else (),
        conditions=_conditions(facts, state, "requires_recovery_space" if overload else ""),
        warnings=("stress_overload",) if overload else (),
        ignore_chart_driver=True,
    )


def domain_order(facts: DomainFacts) -> tuple[str, ...]:
    """Copy Evidence Priority ranked_domains. Append unpublished mains without reranking."""
    ordered: list[str] = []
    for domain_id in facts.ep.ranked_domains:
        if domain_id in MAIN_DOMAIN_IDS and domain_id not in ordered:
            ordered.append(domain_id)
    for domain_id in MAIN_DOMAIN_IDS:
        if domain_id not in ordered:
            ordered.append(domain_id)
    return tuple(ordered)


def _result(
    domain_id: str,
    facts: DomainFacts,
    state: DomainState,
    dimensions: dict[str, str],
    *,
    risks: tuple[str, ...] = (),
    risk: str = "",
    leakage: str = "",
    opportunities: tuple[str, ...] = (),
    conditions: tuple[str, ...] = (),
    warnings: tuple[str, ...] = (),
    missing: bool = False,
    ignore_chart_driver: bool = False,
) -> DomainInterpretationResult:
    _ = ignore_chart_driver
    findings = scoped_findings(facts.ep, domain_id)
    secondary = shen_sha_findings(facts.ep, domain_id)
    if missing:
        state = DomainState.UNRESOLVED
    support_finding = pick_role(findings, "support", facts.ep)
    bottleneck_finding = pick_role(findings, "bottleneck", facts.ep)
    risk_finding = pick_role(findings, "risk", facts.ep)
    opportunity_finding = pick_role(findings, "opportunity", facts.ep)
    condition_finding = pick_role(findings, "condition", facts.ep)
    elected = elect_canonical_driver(domain_id, facts, dimensions, state)
    driver = elected.label
    driver_id = elected.driver_id
    support_finding = _usable_support(support_finding, bottleneck_finding, risk_finding, facts)
    bottleneck = _domain_bottleneck(
        domain_id,
        facts,
        dimensions,
        bottleneck_finding,
    )
    support = label_of(support_finding) or _support_fallback(domain_id, facts)
    if support and bottleneck and support == bottleneck:
        support_finding = None
        support = _support_fallback(domain_id, facts)
        if support == bottleneck:
            support = ""
    if not risk:
        risk = _code_from_label(label_of(risk_finding)) or (risks[0] if risks else "")
    if not opportunities and opportunity_finding:
        mapped = _code_from_label(label_of(opportunity_finding))
        if mapped:
            opportunities = (mapped,)
    condition = label_of(condition_finding)
    if not condition and conditions:
        first = conditions[0]
        condition = CONDITION_LABELS.get(first, first)
    if state is DomainState.UNRESOLVED:
        summary = UNRESOLVED_COPY
        driver = ""
        driver_id = "not_applicable"
        support = ""
        bottleneck = ""
        risk = ""
        opportunities = ()
        conditions = ()
        warnings = ()
        leakage = ""
    else:
        summary = _summary(domain_id, state, facts, dimensions)
    blocked = {
        item.finding_id
        for item in (bottleneck_finding, risk_finding)
        if item is not None and item.finding_id
    }
    driver_evidence = _driver_evidence_ids(findings, blocked)
    used = tuple(
        item
        for item in (support_finding, bottleneck_finding, risk_finding, opportunity_finding, condition_finding)
        if item is not None
    )
    evidence = evidence_ids_of(findings if findings else used)
    confidence = _confidence(state, secondary)
    warning_labels = tuple(RISK_LABELS.get(item, item) for item in warnings)
    if secondary and state is not DomainState.UNRESOLVED:
        warning_labels = warning_labels + tuple(
            item.customer_label for item in secondary if item.customer_label and "TR-P7" not in item.customer_label
        )[:1]
    return DomainInterpretationResult(
        domain_id=domain_id,
        state=state,
        priority=copied_priority(findings),
        strengths=_strengths(domain_id, facts, dimensions),
        risks=tuple(RISK_LABELS.get(item, item) for item in risks),
        opportunities=tuple(OPPORTUNITY_LABELS.get(item, item) for item in opportunities),
        conditions=tuple(item for item in ((condition,) if condition else conditions) if item),
        warnings=warning_labels,
        driver=driver,
        driver_id=driver_id,
        driver_evidence_ids=driver_evidence,
        support=support,
        bottleneck=bottleneck,
        risk=RISK_LABELS.get(risk, risk),
        condition=condition,
        leakage=leakage,
        confidence=confidence,
        supporting_evidence_ids=evidence,
        evidence_ids=evidence,
        trace_ids=trace_ids_of(domain_id, findings),
        dimensions=dimensions,
        driver_source=f"domain.driver:{driver_id}" if driver_id else "",
        support_source=_source_of(support_finding, domain_id, "support"),
        bottleneck_source=_source_of(bottleneck_finding, domain_id, "bottleneck"),
        customer_summary=summary,
    )


def _authority_risks(facts: DomainFacts, dimensions: dict[str, str]) -> tuple[tuple[str, ...], str]:
    risks: list[str] = []
    if dimensions.get("authority_pressure") == "elevated":
        risks.append("pressure_overload")
    if classification_of(facts.achievement, "authority") in LOW_BANDS and (
        classification_of(facts.achievement, "leadership") in HIGH_BANDS
        or classification_of(facts.achievement, "management") in HIGH_BANDS
    ):
        risks.append("authority_conflict")
    risk = risks[0] if risks else ""
    extra = damage_risk_label(facts.damage_types)
    if extra and extra not in risks:
        pass
    return tuple(risks), risk


def _opportunities(facts: DomainFacts, preferred: tuple[str, ...]) -> tuple[str, ...]:
    available: list[str] = []
    for item in preferred:
        if item == "academic_capacity" and (
            "academic" in facts.dominant_capabilities or "academic_research" in facts.work_styles
        ):
            available.append(item)
        elif item == "management_capacity" and (
            "management" in facts.dominant_capabilities or "managerial" in facts.work_styles
        ):
            available.append(item)
        elif item == "leadership_capacity" and (
            "leadership" in facts.dominant_capabilities or "leadership_command" in facts.work_styles
        ):
            available.append(item)
        elif item == "professional_authority" and "academic" in facts.dominant_capabilities:
            available.append(item)
    return tuple(available[:2])


def _conditions(facts: DomainFacts, state: DomainState, extra: str) -> tuple[str, ...]:
    items: list[str] = []
    if extra:
        items.append(CONDITION_LABELS.get(extra, extra))
    if state in {DomainState.STRONG, DomainState.CONDITIONAL, DomainState.FRAGMENTED}:
        if facts.integrity in {"mixed", "conditionally_complete"} and CONDITION_LABELS["requires_structural_integrity"] not in items:
            items.append(CONDITION_LABELS["requires_structural_integrity"])
        if "resource_overload" in facts.damage_types:
            release = CONDITION_LABELS["requires_output_release"]
            if release not in items:
                items.append(release)
    return tuple(dict.fromkeys(item for item in items if item))


def _usable_support(
    finding: EvidencePriorityFinding | None,
    bottleneck_finding: EvidencePriorityFinding | None,
    risk_finding: EvidencePriorityFinding | None,
    facts: DomainFacts,
) -> EvidencePriorityFinding | None:
    """Support enables the driver. It is not a high-priority risk copy."""
    if finding is None:
        return None
    blocked = {
        item.finding_id
        for item in (bottleneck_finding, risk_finding)
        if item is not None and item.finding_id
    }
    blocked.update(facts.ep.bottleneck_ids)
    blocked.update(facts.ep.risk_evidence)
    if finding.finding_id in blocked:
        return None
    if finding.source_kind in DAMAGE_SOURCE_KINDS or finding.category in RISK_CATEGORIES:
        return None
    label = finding.customer_label.strip()
    if label and label in set(DAMAGE_LABELS.values()):
        return None
    if bottleneck_finding is not None and label and label == bottleneck_finding.customer_label.strip():
        return None
    return finding


def _domain_bottleneck(
    domain_id: str,
    facts: DomainFacts,
    dimensions: dict[str, str],
    finding: EvidencePriorityFinding | None,
) -> str:
    """Bottleneck may consume Damage/Risk. It is never a Driver label."""
    if domain_id == "vitality" and "resource_overload" in facts.damage_types:
        return damage_label("resource_overload")
    if finding is not None and finding.source_kind not in DAMAGE_SOURCE_KINDS:
        if finding.category in RISK_CATEGORIES or finding.source_kind in {"combination", "ten_god", "wealth"}:
            text = label_of(finding)
            if text and text not in set(DRIVER_LABELS.values()):
                return text
    return label_of(finding) or _bottleneck_fallback(domain_id, facts, dimensions)


def _driver_evidence_ids(
    findings: tuple[EvidencePriorityFinding, ...],
    blocked: set[str],
) -> tuple[str, ...]:
    """Evidence that explains the elected mechanism, excluding risk/damage."""
    items: list[str] = []
    for finding in findings:
        if not finding.finding_id or finding.finding_id in blocked:
            continue
        if finding.source_kind in DAMAGE_SOURCE_KINDS or finding.category in RISK_CATEGORIES:
            continue
        items.append(finding.finding_id)
        if len(items) >= 4:
            break
    return tuple(items)


def _support_fallback(domain_id: str, facts: DomainFacts) -> str:
    if facts.has_rescue and facts.rescue_types:
        return "Cứu giải cấu trúc còn hiệu lực"
    if domain_id == "career" and "academic" in facts.dominant_capabilities:
        return capability_label("academic")
    if domain_id == "authority" and facts.pattern:
        return facts.pattern
    if domain_id == "wealth" and classification_of(facts.wealth, "wealth_accumulation"):
        return "Tích lũy"
    return facts.pattern


def _bottleneck_fallback(domain_id: str, facts: DomainFacts, dimensions: dict[str, str]) -> str:
    if domain_id == "authority" and dimensions.get("authority_pressure") == "elevated":
        return RISK_LABELS["pressure_overload"]
    if domain_id == "wealth":
        if dimensions.get("creation") in LOW_BANDS:
            return "Tạo tài"
        if dimensions.get("retention") in LOW_BANDS:
            return "Giữ tài"
        if dimensions.get("volatility") in HIGH_BANDS:
            return "Biến động tài"
    if domain_id == "career" and dimensions.get("management_fit") in LOW_BANDS:
        return RISK_LABELS["management_gap"]
    if domain_id == "vitality" and dimensions.get("recovery") in LOW_BANDS:
        return RISK_LABELS["poor_recovery"]
    if domain_id == "relationship" and dimensions.get("communication") in LOW_BANDS:
        return RISK_LABELS["communication_gap"]
    if domain_id == "legacy" and not dimensions.get("knowledge_legacy"):
        return RISK_LABELS["transmission_gap"]
    if domain_id in {"career", "vitality"} and "resource_overload" in facts.damage_types:
        return damage_label("resource_overload")
    bottleneck = pick_role(scoped_findings(facts.ep, domain_id), "bottleneck")
    return label_of(bottleneck)


def _strengths(domain_id: str, facts: DomainFacts, dimensions: dict[str, str]) -> tuple[str, ...]:
    items: list[str] = []
    if domain_id == "career":
        items.extend(capability_label(item) for item in facts.work_styles[:3])
    elif domain_id == "wealth":
        if dimensions.get("retention") in HIGH_BANDS:
            items.append("Giữ tài")
        if dimensions.get("accumulation") in HIGH_BANDS:
            items.append("Tích lũy")
    elif domain_id == "authority":
        items.extend(capability_label(item) for item in facts.dominant_capabilities[:2])
    elif domain_id == "legacy" and dimensions.get("knowledge_legacy"):
        items.append("Di sản tri thức")
    return tuple(dict.fromkeys(item for item in items if item))


def _summary(domain_id: str, state: DomainState, facts: DomainFacts, dimensions: dict[str, str]) -> str:
    template = SUMMARY_TEMPLATES.get((domain_id, state.value), "")
    if domain_id == "wealth" and is_split(
        strongest_band((dimensions.get("retention", ""), dimensions.get("accumulation", ""))),
        dimensions.get("creation", ""),
    ):
        return SUMMARY_TEMPLATES[("wealth", DomainState.FRAGMENTED.value)]
    if template:
        return template
    if domain_id == "relationship":
        return UNRESOLVED_COPY if state is DomainState.UNRESOLVED else "Quan hệ cần đọc theo năng lực giao tiếp và tin cậy, không theo sao Hồng Loan."
    return ""


def _sustainability(retention: str, accumulation: str, volatility: str) -> str:
    held = strongest_band((retention, accumulation))
    if not held:
        return ""
    if volatility in HIGH_BANDS:
        return "moderate"
    return held


def _style_to_fit(style: str) -> str:
    mapping = {
        "academic_research": "academic_fit",
        "managerial": "management_fit",
        "leadership_command": "leadership_fit",
        "entrepreneurial": "entrepreneurial_fit",
        "structured_institutional": "organizational_fit",
        "technical": "technical_fit",
        "creative": "creative_fit",
        "public_facing": "public_facing_fit",
        "independent": "autonomy_need",
        "specialist": "specialist_fit",
    }
    return mapping.get(style, "")


def _confidence(state: DomainState, secondary: tuple[EvidencePriorityFinding, ...]) -> ConfidenceValue:
    if state is DomainState.UNRESOLVED:
        return ConfidenceValue(summary="insufficient")
    summary = "structural"
    if secondary:
        summary = "structural_qualified"
    return ConfidenceValue(summary=summary)


def _source_of(finding: EvidencePriorityFinding | None, domain_id: str, role: str) -> str:
    if finding is None:
        return f"mc01.{domain_id}:{role}" if role else f"mc01.{domain_id}"
    refs = ",".join(finding.source_refs) if finding.source_refs else finding.source_kind
    return refs


def _code_from_label(label: str) -> str:
    inverted = {value: key for key, value in {**RISK_LABELS, **OPPORTUNITY_LABELS}.items()}
    return inverted.get(label, "")

"""Build TV-01 comparative decision facts from frozen evidence. No new Canonical math."""

from __future__ import annotations

from consulting.marriage.models.comparison import (
    DirectionalAssessment,
    MarriageComparisonFact,
    MarriageComparisonResult,
    MarriageDomainComparison,
    MarriageOverallComparison,
)
from consulting.marriage.models.enums import (
    ComparisonFactKind,
    CompatibilityLevel,
    DirectionalAssessmentState,
    DirectionalSupportState,
    DomainDecisionState,
    EvidenceResolutionStatus,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    PresenceBand,
    RelationshipSubject,
)
from consulting.marriage.models.evidence import MarriageEvidence, ResolvedMarriageEvidence
from consulting.marriage.models.finding import MarriageFinding
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot, UsefulGodSnapshot
from consulting.marriage.policy.catalog import is_wealth_pressure_role, is_wealth_role, normalize_role

_PROMINENT = frozenset({EvidenceSignificance.MAJOR, EvidenceSignificance.CRITICAL})
_D2_SUPPORT = frozenset(
    {
        MarriageEvidenceType.STEM_COMBINATION,
        MarriageEvidenceType.BRANCH_COMBINATION,
        MarriageEvidenceType.BRANCH_MEETING,
    }
)
_D2_CONFLICT = frozenset(
    {
        MarriageEvidenceType.STEM_CONTROL,
        MarriageEvidenceType.BRANCH_CLASH,
        MarriageEvidenceType.BRANCH_HARM,
        MarriageEvidenceType.BRANCH_PUNISHMENT,
        MarriageEvidenceType.BRANCH_BREAK,
    }
)
_D2_KEEP = _D2_SUPPORT | _D2_CONFLICT
_AUTHORITY_HINTS = ("quan", "sat", "kien loc", "kien_loc")
_EXPRESSION_HINTS = ("thuc than", "thuong quan", "thuc_than", "thuong_quan")
_RESPONSIBILITY_HINTS = ("quan", "sat", "kien")


def build_marriage_comparison(result: MarriageDecisionResult) -> MarriageComparisonResult:
    """Derive comparative structure from evidence, resolution, and snapshots."""
    overlay = {item.evidence_id: item for item in result.resolved_evidence}
    findings = result.findings
    natal = [
        item
        for item in result.evidence
        if item.scope not in {"reference"}
    ]
    facts: list[MarriageComparisonFact] = []
    facts.extend(_d1_facts(natal, overlay, findings, result.canonical_a, result.canonical_b))
    facts.extend(_d2_facts(natal, overlay, findings))
    facts.extend(_d3_facts(natal, overlay, findings))
    facts.extend(_d5_facts(natal, overlay, findings))
    facts.extend(_d8_facts(natal, overlay, findings))
    facts.extend(_d4_derived(facts, findings))
    facts.extend(_d6_derived(facts, findings))
    facts = _renumber(facts)
    domains = {
        MarriageDomain.FIVE_ELEMENTS: _domain_from_facts(
            MarriageDomain.FIVE_ELEMENTS,
            facts,
            result.canonical_a,
            result.canonical_b,
            _d1_mutual(facts),
        ),
        MarriageDomain.STEM_BRANCH: _domain_from_facts(
            MarriageDomain.STEM_BRANCH,
            facts,
            result.canonical_a,
            result.canonical_b,
            _d2_mutual(facts),
        ),
        MarriageDomain.TEN_GODS: _domain_from_facts(
            MarriageDomain.TEN_GODS,
            facts,
            result.canonical_a,
            result.canonical_b,
            _d3_mutual(facts),
        ),
        MarriageDomain.INTERACTION: _domain_from_facts(
            MarriageDomain.INTERACTION,
            facts,
            result.canonical_a,
            result.canonical_b,
            _derived_mutual(facts, MarriageDomain.INTERACTION),
        ),
        MarriageDomain.FINANCE: _domain_from_facts(
            MarriageDomain.FINANCE,
            facts,
            result.canonical_a,
            result.canonical_b,
            _d5_mutual(facts),
        ),
        MarriageDomain.FAMILY: _domain_from_facts(
            MarriageDomain.FAMILY,
            facts,
            result.canonical_a,
            result.canonical_b,
            _derived_mutual(facts, MarriageDomain.FAMILY),
        ),
        MarriageDomain.CHILDREN: _unavailable_domain(MarriageDomain.CHILDREN),
        MarriageDomain.LUCK: _domain_from_facts(
            MarriageDomain.LUCK,
            facts,
            result.canonical_a,
            result.canonical_b,
            _d8_mutual(facts),
        ),
    }
    overall = _overall_comparison(result, facts, domains[MarriageDomain.FIVE_ELEMENTS])
    return MarriageComparisonResult(
        five_elements=domains[MarriageDomain.FIVE_ELEMENTS],
        stem_branch=domains[MarriageDomain.STEM_BRANCH],
        ten_gods=domains[MarriageDomain.TEN_GODS],
        interaction=domains[MarriageDomain.INTERACTION],
        finance=domains[MarriageDomain.FINANCE],
        family=domains[MarriageDomain.FAMILY],
        children=domains[MarriageDomain.CHILDREN],
        luck=domains[MarriageDomain.LUCK],
        overall=overall,
        facts=facts,
    )


def _d1_facts(
    evidence: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
    findings: list[MarriageFinding],
    snapshot_a: MarriageCanonicalSnapshot,
    snapshot_b: MarriageCanonicalSnapshot,
) -> list[MarriageComparisonFact]:
    """Directional five-element facts plus unmatched useful-god needs."""
    facts: list[MarriageComparisonFact] = []
    for item in evidence:
        if item.domain is not MarriageDomain.FIVE_ELEMENTS:
            continue
        if item.scope == "timing":
            continue
        template = _predicate_stem(item.predicate)
        element = str(item.technical_payload.get("element") or _predicate_tail(item.predicate))
        need_side = str(item.technical_payload.get("need_side") or "")
        kind = ComparisonFactKind.SUPPORT
        if item.evidence_type is MarriageEvidenceType.UNFAVORABLE_ACTIVATION:
            kind = ComparisonFactKind.CONFLICT
        facts.append(
            _fact(
                domain=MarriageDomain.FIVE_ELEMENTS,
                kind=kind,
                subject=item.subject,
                template_key=template,
                slots={"element": element, "need_side": need_side},
                evidence_ids=(item.evidence_id,),
                findings=findings,
                overlay=overlay,
                significance=item.significance,
                confidence=item.confidence,
            )
        )
    facts.extend(_need_facts(snapshot_a, RelationshipSubject.B_TO_A, "A", findings))
    facts.extend(_need_facts(snapshot_b, RelationshipSubject.A_TO_B, "B", findings))
    return facts


def _need_facts(
    snapshot: MarriageCanonicalSnapshot,
    subject: RelationshipSubject,
    need_side: str,
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Copy published useful-god needs. Do not infer missing elements."""
    useful = snapshot.useful_god
    facts: list[MarriageComparisonFact] = []
    for element in _named_elements(useful.useful):
        facts.append(
            _fact(
                domain=MarriageDomain.FIVE_ELEMENTS,
                kind=ComparisonFactKind.NEED,
                subject=subject,
                template_key="useful_need",
                slots={"element": element, "need_side": need_side},
                evidence_ids=(),
                findings=findings,
                overlay={},
                significance=EvidenceSignificance.MAJOR,
                confidence=0.0,
            )
        )
    return facts


def _d2_facts(
    evidence: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Marriage-relevant stem/branch interactions. Not every raw pair."""
    selected = _select_stem_branch(evidence)
    facts: list[MarriageComparisonFact] = []
    for item in selected:
        template = _predicate_stem(item.predicate)
        slots = _d2_slots(item)
        kind = ComparisonFactKind.SUPPORT if item.evidence_type in _D2_SUPPORT else ComparisonFactKind.CONFLICT
        fact = _fact(
            domain=MarriageDomain.STEM_BRANCH,
            kind=kind,
            subject=item.subject,
            template_key=template,
            slots=slots,
            evidence_ids=(item.evidence_id,),
            findings=findings,
            overlay=overlay,
            significance=item.significance,
            confidence=item.confidence,
        )
        facts.append(fact)
        if fact.rescued:
            facts.append(
                _fact(
                    domain=MarriageDomain.STEM_BRANCH,
                    kind=ComparisonFactKind.RESCUE,
                    subject=item.subject,
                    template_key="rescued_interaction",
                    slots=slots,
                    evidence_ids=(item.evidence_id,),
                    findings=findings,
                    overlay=overlay,
                    significance=item.significance,
                    rescued=True,
                    residual=True,
                    confidence=item.confidence,
                )
            )
    return facts


def _select_stem_branch(evidence: list[MarriageEvidence]) -> list[MarriageEvidence]:
    """Keep marriage-relevant D2 atoms. Prefer day pillars and major significance."""
    candidates = [
        item
        for item in evidence
        if item.domain is MarriageDomain.STEM_BRANCH and item.evidence_type in _D2_KEEP
    ]
    ranked = sorted(candidates, key=_d2_rank)
    seen: set[tuple[str, str, str]] = set()
    selected: list[MarriageEvidence] = []
    for item in ranked:
        key = (item.evidence_type.value, str(item.technical_payload.get("relation_id") or ""), item.subject.value)
        if key in seen:
            continue
        if not _d2_relevant(item):
            continue
        seen.add(key)
        selected.append(item)
    return selected


def _d2_relevant(item: MarriageEvidence) -> bool:
    """Day/year interactions and major atoms stay; skip indiscriminate hour pairs."""
    if item.significance in _PROMINENT:
        return True
    slots = _slot_pair(item.predicate)
    if "day" in slots:
        return True
    if "year" in slots and item.significance is EvidenceSignificance.MODERATE:
        return True
    return False


def _d2_rank(item: MarriageEvidence) -> tuple[int, int, str]:
    """Deterministic priority: significance, day involvement, evidence id."""
    order = {
        EvidenceSignificance.CRITICAL: 0,
        EvidenceSignificance.MAJOR: 1,
        EvidenceSignificance.MODERATE: 2,
        EvidenceSignificance.MINOR: 3,
    }
    slots = _slot_pair(item.predicate)
    day_rank = 0 if "day" in slots else 1
    return (order.get(item.significance, 4), day_rank, item.evidence_id)


def _d2_slots(item: MarriageEvidence) -> dict[str, str]:
    """Expose pillar slots and relation type without raw rule dumps."""
    slots = _slot_pair(item.predicate)
    relation_id = str(item.technical_payload.get("relation_id") or "")
    values = {
        "relation_type": item.evidence_type.value,
        "relation_id": relation_id,
        "slot_a": slots[0] if len(slots) > 0 else "",
        "slot_b": slots[1] if len(slots) > 1 else "",
    }
    refs = item.source_refs
    if len(refs) >= 2:
        values["can_chi_a"] = str(refs[0].value or "")
        values["can_chi_b"] = str(refs[1].value or "")
    return values


def _d3_facts(
    evidence: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Role/ten-god directional complement and pressure."""
    facts: list[MarriageComparisonFact] = []
    for item in evidence:
        if item.domain is not MarriageDomain.TEN_GODS:
            continue
        role = str(item.technical_payload.get("role") or _predicate_tail(item.predicate))
        need_side = str(item.technical_payload.get("need_side") or "")
        kind = ComparisonFactKind.SUPPORT
        template = _predicate_stem(item.predicate)
        if item.evidence_type is MarriageEvidenceType.TEN_GOD_PRESSURE:
            kind = ComparisonFactKind.CONFLICT
        theme = _role_theme(role)
        facts.append(
            _fact(
                domain=MarriageDomain.TEN_GODS,
                kind=kind,
                subject=item.subject,
                template_key=template,
                slots={"role": role, "need_side": need_side, "theme": theme},
                evidence_ids=(item.evidence_id,),
                findings=findings,
                overlay=overlay,
                significance=item.significance,
                confidence=item.confidence,
            )
        )
    return facts


def _d5_facts(
    evidence: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Finance comparison from wealth-role evidence only. No wealth prediction."""
    facts: list[MarriageComparisonFact] = []
    for item in evidence:
        if item.domain is not MarriageDomain.FINANCE:
            continue
        role = str(item.technical_payload.get("role") or _predicate_tail(item.predicate))
        template = _predicate_stem(item.predicate)
        if item.evidence_type is MarriageEvidenceType.ROLE_COMPLEMENT:
            theme = "earning_role_complement"
            kind = ComparisonFactKind.SUPPORT
        else:
            theme = "resource_competition"
            kind = ComparisonFactKind.CONFLICT
        facts.append(
            _fact(
                domain=MarriageDomain.FINANCE,
                kind=kind,
                subject=item.subject,
                template_key=template,
                slots={"role": role, "theme": theme},
                evidence_ids=(item.evidence_id,),
                findings=findings,
                overlay=overlay,
                significance=item.significance,
                confidence=item.confidence,
            )
        )
    return facts


def _d8_facts(
    evidence: list[MarriageEvidence],
    overlay: dict[str, ResolvedMarriageEvidence],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Timing activates natal structure. It does not rewrite compatibility."""
    facts: list[MarriageComparisonFact] = []
    for item in evidence:
        if item.domain is not MarriageDomain.LUCK:
            continue
        template = _predicate_stem(item.predicate)
        element = str(item.technical_payload.get("element") or "")
        person = str(item.technical_payload.get("side") or "")
        kind = (
            ComparisonFactKind.SUPPORT
            if item.evidence_type is MarriageEvidenceType.LUCK_ALIGNMENT
            else ComparisonFactKind.CONFLICT
        )
        facts.append(
            _fact(
                domain=MarriageDomain.LUCK,
                kind=kind,
                subject=item.subject,
                template_key=template,
                slots={"element": element, "person": person},
                evidence_ids=(item.evidence_id,),
                findings=findings,
                overlay=overlay,
                significance=item.significance,
                confidence=item.confidence,
            )
        )
    return facts


def _d4_derived(
    facts: list[MarriageComparisonFact],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Derive practical interaction tendencies only from D1–D3 facts."""
    derived: list[MarriageComparisonFact] = []
    d1 = [item for item in facts if item.domain is MarriageDomain.FIVE_ELEMENTS]
    d2 = [item for item in facts if item.domain is MarriageDomain.STEM_BRANCH]
    d3 = [item for item in facts if item.domain is MarriageDomain.TEN_GODS]
    derived.extend(
        _derived_if(
            MarriageDomain.INTERACTION,
            "communication_support",
            ComparisonFactKind.SUPPORT,
            [item for item in d2 if item.kind is ComparisonFactKind.SUPPORT],
            findings,
        )
    )
    derived.extend(
        _derived_if(
            MarriageDomain.INTERACTION,
            "communication_friction",
            ComparisonFactKind.CONFLICT,
            [item for item in d2 if item.kind is ComparisonFactKind.CONFLICT and item.template_key != "rescued_interaction"],
            findings,
        )
    )
    derived.extend(
        _derived_if(
            MarriageDomain.INTERACTION,
            "decision_style_tension",
            ComparisonFactKind.CONFLICT,
            [item for item in d3 if item.kind is ComparisonFactKind.CONFLICT],
            findings,
        )
    )
    control = [
        item
        for item in d2 + d3
        if item.template_key in {"stem_control", "role_pressure"}
    ]
    derived.extend(
        _derived_if(
            MarriageDomain.INTERACTION,
            "control_tension",
            ComparisonFactKind.CONFLICT,
            control,
            findings,
        )
    )
    mixed_d1 = bool(
        any(item.kind is ComparisonFactKind.SUPPORT for item in d1)
        and any(item.kind is ComparisonFactKind.CONFLICT for item in d1)
    )
    if mixed_d1:
        sources = [item for item in d1 if item.kind in {ComparisonFactKind.SUPPORT, ComparisonFactKind.CONFLICT}]
        derived.extend(
            _derived_if(
                MarriageDomain.INTERACTION,
                "adaptive_interaction",
                ComparisonFactKind.DERIVED,
                sources,
                findings,
            )
        )
    rescued = [item for item in d2 if item.kind is ComparisonFactKind.RESCUE]
    derived.extend(
        _derived_if(
            MarriageDomain.INTERACTION,
            "conflict_resolution_capacity",
            ComparisonFactKind.RESCUE,
            rescued,
            findings,
        )
    )
    return derived


def _d6_derived(
    facts: list[MarriageComparisonFact],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Family comparison only when D2/D3 already supply enough structure."""
    d2 = [item for item in facts if item.domain is MarriageDomain.STEM_BRANCH]
    d3 = [item for item in facts if item.domain is MarriageDomain.TEN_GODS]
    yearish = [
        item
        for item in d2
        if item.slots.get("slot_a") == "year" or item.slots.get("slot_b") == "year"
    ]
    role_support = [item for item in d3 if item.kind is ComparisonFactKind.SUPPORT]
    role_pressure = [item for item in d3 if item.kind is ComparisonFactKind.CONFLICT]
    if not d3 or (not yearish and not role_support and not role_pressure):
        return []
    derived: list[MarriageComparisonFact] = []
    responsibility = [
        item
        for item in role_support
        if _slot_has_hint(item.slots.get("role"), _RESPONSIBILITY_HINTS)
    ]
    derived.extend(
        _derived_if(
            MarriageDomain.FAMILY,
            "responsibility_alignment",
            ComparisonFactKind.SUPPORT,
            responsibility or role_support[:1],
            findings,
        )
    )
    authority = [
        item
        for item in role_pressure
        if _slot_has_hint(item.slots.get("role"), _AUTHORITY_HINTS)
    ]
    derived.extend(
        _derived_if(
            MarriageDomain.FAMILY,
            "authority_tension",
            ComparisonFactKind.CONFLICT,
            authority,
            findings,
        )
    )
    household = [item for item in d2 if item.kind is ComparisonFactKind.SUPPORT]
    derived.extend(
        _derived_if(
            MarriageDomain.FAMILY,
            "household_cooperation",
            ComparisonFactKind.SUPPORT,
            household[:2],
            findings,
        )
    )
    return derived


def _derived_if(
    domain: MarriageDomain,
    template_key: str,
    kind: ComparisonFactKind,
    sources: list[MarriageComparisonFact],
    findings: list[MarriageFinding],
) -> list[MarriageComparisonFact]:
    """Create one derived fact bound to existing source evidence/findings."""
    if not sources:
        return []
    evidence_ids = tuple(eid for item in sources for eid in item.evidence_ids)
    finding_ids = tuple(fid for item in sources for fid in item.finding_ids)
    if not evidence_ids and not finding_ids:
        return []
    return [
        MarriageComparisonFact(
            fact_id="CF-TEMP",
            domain=domain,
            kind=kind,
            subject=RelationshipSubject.SHARED,
            template_key=template_key,
            slots={"source_count": str(len(sources))},
            evidence_ids=tuple(dict.fromkeys(evidence_ids)),
            finding_ids=tuple(dict.fromkeys(finding_ids)),
            significance=sources[0].significance,
            rescued=kind is ComparisonFactKind.RESCUE,
            confidence=min((item.confidence for item in sources if item.confidence), default=0.0),
        )
    ]


def _domain_from_facts(
    domain: MarriageDomain,
    facts: list[MarriageComparisonFact],
    snapshot_a: MarriageCanonicalSnapshot,
    snapshot_b: MarriageCanonicalSnapshot,
    mutual_state: str,
) -> MarriageDomainComparison:
    """Assemble one domain comparison from already derived facts."""
    members = [
        item
        for item in facts
        if item.domain is domain and item.kind is not ComparisonFactKind.NEED
    ]
    available = bool(members)
    a_to_b = _assessment(domain, RelationshipSubject.A_TO_B, facts, snapshot_a, snapshot_b)
    b_to_a = _assessment(domain, RelationshipSubject.B_TO_A, facts, snapshot_a, snapshot_b)
    strengths = [item for item in members if item.kind is ComparisonFactKind.SUPPORT]
    risks = [item for item in members if item.kind is ComparisonFactKind.CONFLICT]
    rescue = [item for item in members if item.kind is ComparisonFactKind.RESCUE]
    limitations: list[str] = []
    if not available:
        limitations.append("insufficient_comparison_evidence")
    return MarriageDomainComparison(
        domain=domain,
        a_to_b=a_to_b,
        b_to_a=b_to_a,
        mutual_state=mutual_state,
        strengths=strengths,
        risks=risks,
        rescue=rescue,
        limitations=limitations,
        conclusion_key=mutual_state if available else "insufficient",
        confidence=_confidence(members),
        available=available,
    )


def _unavailable_domain(domain: MarriageDomain) -> MarriageDomainComparison:
    """Conservative empty domain. No fabrication."""
    empty = DirectionalAssessment(
        subject=RelationshipSubject.A_TO_B,
        state=DirectionalAssessmentState.INSUFFICIENT,
    )
    other = DirectionalAssessment(
        subject=RelationshipSubject.B_TO_A,
        state=DirectionalAssessmentState.INSUFFICIENT,
    )
    return MarriageDomainComparison(
        domain=domain,
        a_to_b=empty,
        b_to_a=other,
        mutual_state=DirectionalSupportState.INSUFFICIENT.value,
        limitations=["insufficient_comparison_evidence"],
        conclusion_key="insufficient",
        available=False,
    )


def _assessment(
    domain: MarriageDomain,
    subject: RelationshipSubject,
    facts: list[MarriageComparisonFact],
    snapshot_a: MarriageCanonicalSnapshot,
    snapshot_b: MarriageCanonicalSnapshot,
) -> DirectionalAssessment:
    """Build one-way assessment. Snapshot needs are copied, not invented."""
    members = [
        item
        for item in facts
        if item.domain is domain and item.subject is subject and item.kind is not ComparisonFactKind.NEED
    ]
    need_side = "B" if subject is RelationshipSubject.A_TO_B else "A"
    need_snapshot = snapshot_b if need_side == "B" else snapshot_a
    needed: tuple[str, ...] = ()
    temperature = None
    if domain is MarriageDomain.FIVE_ELEMENTS:
        needed = _named_elements(need_snapshot.useful_god.useful)
        temperature = need_snapshot.useful_god.temperature_need
    elif domain is MarriageDomain.TEN_GODS:
        needed = _named_roles(need_snapshot.useful_god)
    support = [item for item in members if item.kind is ComparisonFactKind.SUPPORT]
    conflict = [item for item in members if item.kind is ComparisonFactKind.CONFLICT]
    state = DirectionalAssessmentState.NEUTRAL
    if not members and domain not in {MarriageDomain.FIVE_ELEMENTS, MarriageDomain.TEN_GODS}:
        state = DirectionalAssessmentState.INSUFFICIENT
    elif support and conflict:
        state = DirectionalAssessmentState.MIXED
    elif support:
        state = DirectionalAssessmentState.SUPPORT
    elif conflict:
        state = DirectionalAssessmentState.PRESSURE
    elif needed:
        state = DirectionalAssessmentState.NEUTRAL
    provided = tuple(
        item.slots.get("element") or item.slots.get("role") or ""
        for item in support
        if item.slots.get("element") or item.slots.get("role")
    )
    activated = tuple(
        item.slots.get("element") or item.slots.get("role") or ""
        for item in conflict
        if item.slots.get("element") or item.slots.get("role")
    )
    return DirectionalAssessment(
        subject=subject,
        state=state,
        needed=needed,
        provided=tuple(dict.fromkeys(value for value in provided if value)),
        activated_unfavorable=tuple(dict.fromkeys(value for value in activated if value)),
        temperature_need=temperature,
    )


def _d1_mutual(facts: list[MarriageComparisonFact]) -> str:
    """Five-element mutual state from directional support and pressure."""
    a_support = _has(facts, MarriageDomain.FIVE_ELEMENTS, RelationshipSubject.A_TO_B, ComparisonFactKind.SUPPORT)
    b_support = _has(facts, MarriageDomain.FIVE_ELEMENTS, RelationshipSubject.B_TO_A, ComparisonFactKind.SUPPORT)
    a_pressure = _has(facts, MarriageDomain.FIVE_ELEMENTS, RelationshipSubject.A_TO_B, ComparisonFactKind.CONFLICT)
    b_pressure = _has(facts, MarriageDomain.FIVE_ELEMENTS, RelationshipSubject.B_TO_A, ComparisonFactKind.CONFLICT)
    return _mutual_from_flags(a_support, b_support, a_pressure, b_pressure)


def _d2_mutual(facts: list[MarriageComparisonFact]) -> str:
    """Stem/branch mutual state from harmony versus conflict facts."""
    support = any(
        item.domain is MarriageDomain.STEM_BRANCH and item.kind is ComparisonFactKind.SUPPORT
        for item in facts
    )
    conflict = any(
        item.domain is MarriageDomain.STEM_BRANCH
        and item.kind is ComparisonFactKind.CONFLICT
        and item.template_key != "rescued_interaction"
        for item in facts
    )
    if support and conflict:
        return DirectionalSupportState.MIXED_SUPPORT_PRESSURE.value
    if support:
        return DirectionalSupportState.MUTUAL_SUPPORT.value
    if conflict:
        return DirectionalSupportState.MUTUAL_PRESSURE.value
    return DirectionalSupportState.INSUFFICIENT.value


def _d3_mutual(facts: list[MarriageComparisonFact]) -> str:
    """Role mutual state from directional complement and pressure."""
    a_support = _has(facts, MarriageDomain.TEN_GODS, RelationshipSubject.A_TO_B, ComparisonFactKind.SUPPORT)
    b_support = _has(facts, MarriageDomain.TEN_GODS, RelationshipSubject.B_TO_A, ComparisonFactKind.SUPPORT)
    a_pressure = _has(facts, MarriageDomain.TEN_GODS, RelationshipSubject.A_TO_B, ComparisonFactKind.CONFLICT)
    b_pressure = _has(facts, MarriageDomain.TEN_GODS, RelationshipSubject.B_TO_A, ComparisonFactKind.CONFLICT)
    return _mutual_from_flags(a_support, b_support, a_pressure, b_pressure)


def _d5_mutual(facts: list[MarriageComparisonFact]) -> str:
    """Finance mutual state. Distinguishes complement versus competition."""
    support = any(item.domain is MarriageDomain.FINANCE and item.kind is ComparisonFactKind.SUPPORT for item in facts)
    conflict = any(item.domain is MarriageDomain.FINANCE and item.kind is ComparisonFactKind.CONFLICT for item in facts)
    if support and conflict:
        return "spending_risk_mismatch"
    if support:
        return "shared_financial_support"
    if conflict:
        return "resource_competition"
    return DirectionalSupportState.INSUFFICIENT.value


def _d8_mutual(facts: list[MarriageComparisonFact]) -> str:
    """Timing mutual state. Asymmetric when only one chart activates."""
    members = [item for item in facts if item.domain is MarriageDomain.LUCK]
    if not members:
        return DirectionalSupportState.INSUFFICIENT.value
    persons = {item.slots.get("person") for item in members if item.slots.get("person")}
    support = any(item.kind is ComparisonFactKind.SUPPORT for item in members)
    conflict = any(item.kind is ComparisonFactKind.CONFLICT for item in members)
    if len(persons) == 1:
        return "asymmetric_timing"
    if support and conflict:
        return "mixed_timing"
    if support:
        return "supportive_period"
    if conflict:
        return "sensitive_period"
    return DirectionalSupportState.INSUFFICIENT.value


def _derived_mutual(facts: list[MarriageComparisonFact], domain: MarriageDomain) -> str:
    """Mutual key for derived domains."""
    members = [item for item in facts if item.domain is domain]
    if not members:
        return DirectionalSupportState.INSUFFICIENT.value
    support = any(item.kind is ComparisonFactKind.SUPPORT for item in members)
    conflict = any(item.kind is ComparisonFactKind.CONFLICT for item in members)
    if support and conflict:
        return DirectionalSupportState.MIXED_SUPPORT_PRESSURE.value
    if support:
        return DirectionalSupportState.MUTUAL_SUPPORT.value
    if conflict:
        return DirectionalSupportState.MUTUAL_PRESSURE.value
    return "derived_present"


def _mutual_from_flags(a_support: bool, b_support: bool, a_pressure: bool, b_pressure: bool) -> str:
    """Map directional flags onto the required semantic mutual states."""
    if not (a_support or b_support or a_pressure or b_pressure):
        return DirectionalSupportState.INSUFFICIENT.value
    if a_support and b_support and (a_pressure or b_pressure):
        return DirectionalSupportState.MIXED_SUPPORT_PRESSURE.value
    if a_support and b_support:
        return DirectionalSupportState.MUTUAL_SUPPORT.value
    if a_pressure and b_pressure and not (a_support or b_support):
        return DirectionalSupportState.MUTUAL_PRESSURE.value
    if a_support and not b_support and not a_pressure:
        return DirectionalSupportState.A_SUPPORTS_B.value
    if b_support and not a_support and not b_pressure:
        return DirectionalSupportState.B_SUPPORTS_A.value
    if (a_support ^ b_support) or (a_pressure ^ b_pressure):
        return DirectionalSupportState.ASYMMETRIC_SUPPORT.value
    if a_pressure or b_pressure:
        return DirectionalSupportState.MIXED_SUPPORT_PRESSURE.value
    return DirectionalSupportState.INSUFFICIENT.value


def _overall_comparison(
    result: MarriageDecisionResult,
    facts: list[MarriageComparisonFact],
    d1: MarriageDomainComparison,
) -> MarriageOverallComparison:
    """Answer Q1–Q7 from comparison facts. Keep overall.state algorithm unchanged."""
    support = [item for item in facts if item.kind is ComparisonFactKind.SUPPORT]
    conflict = [
        item
        for item in facts
        if item.kind is ComparisonFactKind.CONFLICT and item.template_key != "rescued_interaction"
    ]
    rescue = [item for item in facts if item.kind is ComparisonFactKind.RESCUE]
    a_support = [item for item in support if item.subject is RelationshipSubject.A_TO_B]
    b_support = [item for item in support if item.subject is RelationshipSubject.B_TO_A]
    support_band = _band(support)
    conflict_band = _band(conflict)
    rescue_band = _band(rescue)
    overall_state = result.overall.state or DomainDecisionState.INSUFFICIENT
    level = _compatibility_level(overall_state, d1.mutual_state, support_band, conflict_band, rescue_band)
    major_conflict = _major(conflict)
    q3 = "balanced_support"
    if a_support and not b_support:
        q3 = "a_supports_more"
    elif b_support and not a_support:
        q3 = "b_supports_more"
    elif not a_support and not b_support:
        q3 = "support_not_directional"
    q2 = "mutual_material_support" if a_support and b_support else "limited_or_one_way"
    if not support:
        q2 = "support_not_established"
    q5 = "major_conflict_mitigated" if rescue and major_conflict else "rescue_not_established"
    if rescue and not major_conflict:
        q5 = "rescue_present"
    if major_conflict and not rescue:
        q5 = "conflict_unmitigated"
    q6 = "maintainable_if_managed"
    if overall_state is DomainDecisionState.SUPPORTIVE:
        q6 = "structure_supports_long_term"
    elif overall_state in {DomainDecisionState.PRESSURED, DomainDecisionState.CRITICAL}:
        q6 = "needs_active_management"
    elif overall_state is DomainDecisionState.INSUFFICIENT:
        q6 = "insufficient"
    q7 = major_conflict[0].template_key if major_conflict else ("keep_support_habits" if support else "insufficient")
    q4 = major_conflict[0].template_key if major_conflict else "no_major_conflict_isolated"
    return MarriageOverallComparison(
        q1_compatibility=overall_state.value,
        q2_mutual_support=q2,
        q3_asymmetry=q3,
        q4_conflict=q4,
        q5_rescue=q5,
        q6_long_term=q6,
        q7_condition=q7,
        support_strength=support_band,
        conflict_strength=conflict_band,
        rescue_strength=rescue_band,
        compatibility_level=level,
        five_element_state=_as_d1_state(d1.mutual_state),
        major_harmony_fact_ids=[item.fact_id for item in _major(support)[:5]],
        major_conflict_fact_ids=[item.fact_id for item in major_conflict[:5]],
        rescue_fact_ids=[item.fact_id for item in rescue[:5]],
        explanation_keys=[
            "overall_state_unchanged",
            "presence_bands_from_significance",
            "no_numeric_score",
        ],
    )


def _compatibility_level(
    overall_state: DomainDecisionState,
    d1_mutual: str,
    support: PresenceBand,
    conflict: PresenceBand,
    rescue: PresenceBand,
) -> CompatibilityLevel:
    """Finer grain only when existing states already distinguish it safely."""
    _ = (conflict, rescue)
    if overall_state is DomainDecisionState.INSUFFICIENT:
        return CompatibilityLevel.INSUFFICIENT
    if overall_state is DomainDecisionState.CRITICAL:
        return CompatibilityLevel.HIGHLY_PRESSURED
    if overall_state is DomainDecisionState.PRESSURED:
        return CompatibilityLevel.PRESSURED
    if overall_state is DomainDecisionState.MIXED:
        return CompatibilityLevel.MIXED
    if overall_state is DomainDecisionState.SUPPORTIVE:
        if d1_mutual == DirectionalSupportState.MUTUAL_SUPPORT.value and support is PresenceBand.PROMINENT:
            return CompatibilityLevel.VERY_SUPPORTIVE
        return CompatibilityLevel.SUPPORTIVE
    return CompatibilityLevel.MIXED


def _as_d1_state(value: str) -> DirectionalSupportState:
    """Parse D1 mutual key onto the required enum."""
    try:
        return DirectionalSupportState(value)
    except ValueError:
        return DirectionalSupportState.INSUFFICIENT


def _band(items: list[MarriageComparisonFact]) -> PresenceBand:
    """Qualitative presence from existing significance. No invented weights."""
    if not items:
        return PresenceBand.NONE
    if any(item.significance in _PROMINENT for item in items):
        return PresenceBand.PROMINENT
    return PresenceBand.PRESENT


def _major(items: list[MarriageComparisonFact]) -> list[MarriageComparisonFact]:
    """Order prominent facts first, then remaining facts deterministically."""
    prominent = [item for item in items if item.significance in _PROMINENT]
    rest = [item for item in items if item not in prominent]
    return prominent + rest


def _has(
    facts: list[MarriageComparisonFact],
    domain: MarriageDomain,
    subject: RelationshipSubject,
    kind: ComparisonFactKind,
) -> bool:
    """Return True when a directional fact of this class exists."""
    return any(
        item.domain is domain and item.subject is subject and item.kind is kind
        for item in facts
    )


def _fact(
    *,
    domain: MarriageDomain,
    kind: ComparisonFactKind,
    subject: RelationshipSubject,
    template_key: str,
    slots: dict[str, str],
    evidence_ids: tuple[str, ...],
    findings: list[MarriageFinding],
    overlay: dict[str, ResolvedMarriageEvidence],
    significance: EvidenceSignificance,
    rescued: bool | None = None,
    residual: bool = False,
    confidence: float = 0.0,
) -> MarriageComparisonFact:
    """Bind one fact to evidence and findings. Customer text is not stored here."""
    resolved = [overlay[eid] for eid in evidence_ids if eid in overlay]
    is_rescued = rescued if rescued is not None else any(
        item.status is EvidenceResolutionStatus.RESCUED for item in resolved
    )
    residual_flag = residual or any(item.residual_impact == "rescued_residual" for item in resolved)
    finding_ids = tuple(
        item.finding_id
        for item in findings
        if any(eid in item.evidence_ids for eid in evidence_ids)
    )
    return MarriageComparisonFact(
        fact_id="CF-TEMP",
        domain=domain,
        kind=kind,
        subject=subject,
        template_key=template_key,
        slots=slots,
        evidence_ids=evidence_ids,
        finding_ids=finding_ids,
        significance=significance,
        rescued=is_rescued,
        residual=residual_flag,
        confidence=confidence,
    )


def _renumber(facts: list[MarriageComparisonFact]) -> list[MarriageComparisonFact]:
    """Assign stable comparison fact ids after the full set is known."""
    numbered: list[MarriageComparisonFact] = []
    for index, item in enumerate(facts, start=1):
        numbered.append(
            MarriageComparisonFact(
                fact_id=f"CF-{index:04d}",
                domain=item.domain,
                kind=item.kind,
                subject=item.subject,
                template_key=item.template_key,
                slots=item.slots,
                evidence_ids=item.evidence_ids,
                finding_ids=item.finding_ids,
                significance=item.significance,
                rescued=item.rescued,
                residual=item.residual,
                confidence=item.confidence,
            )
        )
    return numbered


def _named_elements(items: list | None) -> tuple[str, ...]:
    """Copy published useful/favorable element identities."""
    names: list[str] = []
    for item in items or ():
        if item.element is None:
            continue
        value = item.element.value
        if value not in names:
            names.append(value)
    return tuple(names)


def _named_roles(useful: UsefulGodSnapshot) -> tuple[str, ...]:
    """Copy published useful/favorable role names."""
    names: list[str] = []
    for item in (*(useful.useful or ()), *(useful.favorable or ())):
        if item.role and item.role not in names:
            names.append(item.role)
    return tuple(names)


def _role_theme(role: str) -> str:
    """Map a published role onto a customer-relevant theme. Not psychology."""
    folded = normalize_role(role)
    if is_wealth_pressure_role(role) or "kiep tai" in folded:
        return "competition"
    if is_wealth_role(role) or "tai" in folded:
        return "finance"
    if _slot_has_hint(role, _AUTHORITY_HINTS):
        return "control"
    if _slot_has_hint(role, _EXPRESSION_HINTS):
        return "expression"
    if "kien" in folded or "an" == folded:
        return "resource"
    if "ty kiep" in folded or "kiep" in folded:
        return "competition"
    return "support"


def _slot_has_hint(value: str | None, hints: tuple[str, ...]) -> bool:
    """Return True when a published label contains a known role hint."""
    folded = normalize_role(value)
    return any(hint in folded for hint in hints)


def _predicate_stem(predicate: str | None) -> str:
    """Return the semantic prefix of an evidence predicate."""
    if not predicate:
        return ""
    return predicate.split(":")[0]


def _predicate_tail(predicate: str | None) -> str:
    """Return the first slotted value of an evidence predicate."""
    if not predicate or ":" not in predicate:
        return ""
    parts = predicate.split(":")
    return parts[1] if len(parts) > 1 else ""


def _slot_pair(predicate: str | None) -> tuple[str, ...]:
    """Extract pillar slots from a stem/branch predicate."""
    if not predicate:
        return ()
    parts = predicate.split(":")
    slots = [item for item in parts if item in {"year", "month", "day", "hour"}]
    return tuple(slots)


def _confidence(items: list[MarriageComparisonFact]) -> float:
    """Copy mean evidence confidence. Empty set is zero."""
    values = [item.confidence for item in items if item.confidence]
    if not values:
        return 0.0
    return sum(values) / len(values)

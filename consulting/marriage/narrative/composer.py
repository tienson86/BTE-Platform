"""Deterministic narrative composer. Communication only. No new conclusions."""

from __future__ import annotations

from consulting.marriage.models.enums import ComparisonFactKind, FindingType, MarriageDomain, RelationshipSubject
from consulting.marriage.models.narrative import (
    MarriageNarrativeBlock,
    MarriageNarrativeHighlight,
    MarriageNarrativeResult,
    MarriageNarrativeSection,
)
from consulting.marriage.narrative.catalog import (
    NarrativeEntry,
    action_entry,
    confidence_sentence,
    domain_entry,
    domain_title,
    finding_entry,
    limitation_domain,
    limitation_hour,
    overall_entry,
    rescued_sentence,
    timing_entry,
)
from consulting.marriage.narrative.input import (
    ComparisonNarrativeFact,
    DomainNarrativeInput,
    FindingNarrativeInput,
    NarrativeInput,
    RecommendationNarrativeInput,
)
from consulting.marriage.narrative.repetition import RepetitionGuard
from consulting.marriage.narrative.versions import (
    AUDIENCE_CUSTOMER,
    LANGUAGE_VI,
    NARRATIVE_CATALOG_VERSION,
    NARRATIVE_COMPOSER_VERSION,
    NARRATIVE_VERSION,
)

_OPTIONAL_DOMAINS = frozenset(
    {
        MarriageDomain.INTERACTION,
        MarriageDomain.FAMILY,
        MarriageDomain.CHILDREN,
    }
)
_GENDER_LABEL = {"male": "Nam", "female": "Nữ"}


class CanonicalNarrativeComposer:
    """Compose Vietnamese narrative from Decision/Recommendation facts only."""

    def compose(self, payload: NarrativeInput) -> MarriageNarrativeResult:
        """Build structured narrative. Does not mutate Decision or Recommendation."""
        guard = RepetitionGuard()
        findings = {item.finding_id: item for item in payload.findings}
        sections = [
            _identity_section(payload),
            _overall_section(payload, guard),
            _comparison_section(payload, guard),
            _domain_section(payload, findings, guard),
            *_timing_sections(payload, guard),
            _action_section(payload, guard),
            _confidence_section(payload),
        ]
        highlights = _highlights(payload, findings)
        return MarriageNarrativeResult(
            consultation_id=payload.consultation_id,
            language=payload.language or LANGUAGE_VI,
            audience=payload.audience or AUDIENCE_CUSTOMER,
            version=NARRATIVE_VERSION,
            catalog_version=NARRATIVE_CATALOG_VERSION,
            composer_version=NARRATIVE_COMPOSER_VERSION,
            sections=[item for item in sections if item is not None],
            highlights=highlights,
        )


def _identity_section(payload: NarrativeInput) -> MarriageNarrativeSection:
    """Name the couple from presentation-safe labels only."""
    gender_a = _GENDER_LABEL[payload.person_a_gender.value]
    gender_b = _GENDER_LABEL[payload.person_b_gender.value]
    text = (
        f"{payload.person_a_label} ({gender_a}) và {payload.person_b_label} ({gender_b}) "
        "được đọc như một hồ sơ tư vấn hôn nhân, không như một bản tính điểm."
    )
    return MarriageNarrativeSection(
        section_id="identity",
        title_key="marriage.section.identity",
        blocks=[_block("identity-label", "observation", "marriage.identity.couple", text)],
    )


def _overall_section(
    payload: NarrativeInput,
    guard: RepetitionGuard,
) -> MarriageNarrativeSection:
    """Marriage conclusion first: compatibility, support, conflict, horizon, condition."""
    entry = overall_entry(payload.overall_state.value)
    guard.claim_catalog(entry.key)
    guard.register_text(entry.observation)
    questions = payload.overall_comparison
    blocks = [
        _block(
            "overall-headline",
            "observation",
            entry.key,
            entry.headline,
            source_finding_ids=list(payload.headline_finding_ids),
            confidence=payload.overall_confidence,
        ),
        _block(
            "overall-summary",
            "observation",
            entry.key,
            entry.observation,
            source_finding_ids=list(payload.headline_finding_ids),
            confidence=payload.overall_confidence,
        ),
    ]
    if questions is not None:
        blocks.extend(
            [
                _block(
                    "overall-q1",
                    "observation",
                    "marriage.overall.q1",
                    f"Mức tương hợp: {questions.q1_text}",
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
                _block(
                    "overall-q2",
                    "observation",
                    "marriage.overall.q2",
                    f"Bổ trợ hai chiều: {questions.q2_text}",
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
                _block(
                    "overall-q3",
                    "observation",
                    "marriage.overall.q3",
                    questions.q3_text,
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
                _block(
                    "overall-q4",
                    "observation",
                    "marriage.overall.q4",
                    f"Điểm xung lớn nhất: {questions.q4_text}",
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
                _block(
                    "overall-q5",
                    "observation",
                    "marriage.overall.q5",
                    questions.q5_text,
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
                _block(
                    "overall-q6",
                    "observation",
                    "marriage.overall.q6",
                    f"Khả năng đi lâu dài: {questions.q6_text}",
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
                _block(
                    "overall-q7",
                    "observation",
                    "marriage.overall.q7",
                    f"Điều kiện quan trọng: {questions.q7_text}",
                    source_finding_ids=list(payload.headline_finding_ids),
                ),
            ]
        )
    return MarriageNarrativeSection(
        section_id="overall",
        title_key="marriage.section.overall",
        blocks=blocks,
    )


def _comparison_section(
    payload: NarrativeInput,
    guard: RepetitionGuard,
) -> MarriageNarrativeSection | None:
    """Render directional comparison facts. Does not invent new conclusions."""
    facts = list(payload.comparison_facts)
    if not facts:
        return None
    blocks: list[MarriageNarrativeBlock] = []
    for item in facts:
        catalog_key = f"marriage.fact.{item.template_key}"
        if not guard.claim_text(item.text):
            continue
        guard.register_text(item.text)
        stage = _comparison_stage(item)
        text = item.text
        if item.rescued and item.kind is ComparisonFactKind.CONFLICT:
            text = f"{text}. {rescued_sentence()}"
        blocks.append(
            _block(
                f"cmp-{item.fact_id.lower()}",
                stage,
                catalog_key,
                text,
                domain=item.domain,
                source_finding_ids=list(item.finding_ids),
            )
        )
    if not blocks:
        return None
    return MarriageNarrativeSection(
        section_id="comparison",
        title_key="marriage.section.comparison",
        blocks=blocks,
    )


def _comparison_stage(item: ComparisonNarrativeFact) -> str:
    """Group comparison facts for report cards without extra prose."""
    if item.kind is ComparisonFactKind.RESCUE:
        return "rescue"
    if item.kind is ComparisonFactKind.CONFLICT:
        return "conflict"
    if item.subject is RelationshipSubject.A_TO_B:
        return "a_to_b"
    if item.subject is RelationshipSubject.B_TO_A:
        return "b_to_a"
    return "harmony"


def _domain_section(
    payload: NarrativeInput,
    findings: dict[str, FindingNarrativeInput],
    guard: RepetitionGuard,
) -> MarriageNarrativeSection | None:
    """Explain available domains once. Skip empty optional domains."""
    blocks: list[MarriageNarrativeBlock] = []
    for domain in payload.domains:
        if domain.domain is MarriageDomain.LUCK and _has_timing(payload):
            continue
        if not _publish_domain(domain):
            continue
        blocks.extend(_domain_blocks(domain, payload, findings, guard))
    if not blocks:
        return None
    return MarriageNarrativeSection(
        section_id="domains",
        title_key="marriage.section.domains",
        blocks=blocks,
    )


def _timing_sections(
    payload: NarrativeInput,
    guard: RepetitionGuard,
) -> list[MarriageNarrativeSection]:
    """Timing exists only when valid timing findings or actions exist."""
    if not _has_timing(payload):
        return []
    states = _timing_states(payload)
    blocks: list[MarriageNarrativeBlock] = []
    for state in states:
        entry = timing_entry(state)
        if not guard.claim_catalog(entry.key):
            continue
        guard.register_text(entry.observation)
        source_ids = [
            item.finding_id
            for item in payload.findings
            if item.finding_type is FindingType.TIMING
        ]
        rec_ids = [
            item.recommendation_id
            for item in payload.recommendations
            if item.action_type.value == "timing_awareness"
        ]
        blocks.append(
            _block(
                f"timing-{state}",
                "observation",
                entry.key,
                f"{entry.headline}. {entry.observation}",
                domain=MarriageDomain.LUCK,
                source_finding_ids=source_ids,
                source_recommendation_ids=rec_ids,
            )
        )
    if not blocks:
        return []
    return [
        MarriageNarrativeSection(
            section_id="timing",
            title_key="marriage.section.timing",
            domain=MarriageDomain.LUCK,
            blocks=blocks,
        )
    ]


def _action_section(
    payload: NarrativeInput,
    guard: RepetitionGuard,
) -> MarriageNarrativeSection:
    """Communicate B04 actions. Merge identical intents; do not copy domain explanation."""
    grouped: dict[str, list[RecommendationNarrativeInput]] = {}
    for item in payload.recommendations:
        key = f"{item.action_type.value}:{item.objective or ''}"
        grouped.setdefault(key, []).append(item)
    blocks: list[MarriageNarrativeBlock] = []
    for items in grouped.values():
        item = items[0]
        if not guard.claim_action(item.action_type.value, item.objective):
            continue
        entry = action_entry(item.action_type)
        if entry is None:
            continue
        guard.claim_catalog(entry.key)
        text = f"{entry.headline}. {entry.action_bridge}"
        if any("rescued" in rec.conditions for rec in items):
            text = f"{text} {rescued_sentence()}"
        rec_ids = [rec.recommendation_id for rec in items]
        finding_ids = list(dict.fromkeys(fid for rec in items for fid in rec.source_finding_ids))
        blocks.append(
            _block(
                f"action-{rec_ids[0]}",
                "action",
                entry.key,
                text,
                domain=item.domain,
                source_finding_ids=finding_ids,
                source_recommendation_ids=rec_ids,
                priority=item.action_priority.value if item.action_priority else None,
                confidence=item.confidence,
            )
        )
    if not blocks:
        blocks.append(
            _block(
                "action-none",
                "action",
                "marriage.action.none",
                "Hồ sơ hiện không công bố hành động độc lập ngoài việc đọc nhận định đã có.",
            )
        )
    return MarriageNarrativeSection(
        section_id="actions",
        title_key="marriage.section.actions",
        blocks=blocks,
    )


def _confidence_section(payload: NarrativeInput) -> MarriageNarrativeSection:
    """State confidence and data limits. Missing data is not a marital defect."""
    blocks = [
        _block(
            "confidence-level",
            "observation",
            f"marriage.confidence.{payload.confidence_level.value}",
            confidence_sentence(payload.confidence_level.value),
            confidence=payload.overall_confidence,
        )
    ]
    if not payload.hour_known or "birth_time_unknown" in payload.limitations:
        blocks.append(
            _block(
                "limit-hour",
                "observation",
                "marriage.limit.hour",
                limitation_hour(),
            )
        )
    for domain in payload.domains:
        if domain.domain in _OPTIONAL_DOMAINS and not _publish_domain(domain):
            title = domain_title(domain.domain)
            blocks.append(
                _block(
                    f"limit-{domain.domain.value}",
                    "observation",
                    "marriage.limit.domain",
                    f"{title}: {limitation_domain()}",
                    domain=domain.domain,
                )
            )
            break
    return MarriageNarrativeSection(
        section_id="confidence",
        title_key="marriage.section.confidence",
        blocks=blocks,
    )


def _domain_blocks(
    domain: DomainNarrativeInput,
    payload: NarrativeInput,
    findings: dict[str, FindingNarrativeInput],
    guard: RepetitionGuard,
) -> list[MarriageNarrativeBlock]:
    """One domain: state, explanation, contributing findings, action refs."""
    if domain.state is None:
        return []
    entry = domain_entry(domain.domain, domain.state.value)
    if entry is None:
        return []
    guard.claim_catalog(entry.key)
    guard.register_text(entry.reason)
    blocks = [
        _block(
            f"domain-{domain.domain.value}-state",
            "observation",
            entry.key,
            f"{entry.headline}. {entry.reason} {entry.impact}",
            domain=domain.domain,
            source_finding_ids=list(domain.finding_ids),
            confidence=domain.confidence,
        )
    ]
    for finding_id in domain.finding_ids:
        finding = findings.get(finding_id)
        if finding is None or finding.finding_type is FindingType.CONDITION:
            continue
        if not guard.claim_finding(finding.semantic_key, finding.finding_id):
            continue
        matching = [
            item
            for item in payload.comparison_facts
            if finding_id in item.finding_ids and item.kind is not ComparisonFactKind.NEED
        ]
        if matching:
            blocks.extend(_domain_fact_blocks(payload, domain.domain, finding.finding_id, guard))
            continue
        finding_text = _finding_text(finding)
        if finding_text is None:
            continue
        if not guard.claim_catalog(finding_text.key):
            continue
        if not guard.claim_text(finding_text.observation):
            continue
        if guard.opening_repeats(finding_text.observation):
            continue
        guard.register_text(finding_text.observation)
        blocks.append(
            _block(
                f"finding-{finding.finding_id}",
                "reason",
                finding_text.key,
                finding_text.observation,
                domain=finding.domain,
                source_finding_ids=[finding.finding_id],
                confidence=finding.confidence,
            )
        )
    rec_ids = [
        item.recommendation_id
        for item in payload.recommendations
        if item.domain is domain.domain
    ]
    if rec_ids:
        blocks.append(
            _block(
                f"domain-{domain.domain.value}-actions",
                "action_bridge",
                f"marriage.domain.{domain.domain.value}.action_ref",
                "Phần khuyến nghị tương ứng được nêu ở kế hoạch hành động, không lặp lại giải thích miền.",
                domain=domain.domain,
                source_recommendation_ids=rec_ids,
            )
        )
    return blocks


def _domain_fact_blocks(
    payload: NarrativeInput,
    domain: MarriageDomain,
    finding_id: str,
    guard: RepetitionGuard,
) -> list[MarriageNarrativeBlock]:
    """Explain a finding with specific comparison facts when they exist."""
    blocks: list[MarriageNarrativeBlock] = []
    for item in payload.comparison_facts:
        if item.domain is not domain:
            continue
        if finding_id not in item.finding_ids:
            continue
        if item.kind is ComparisonFactKind.NEED:
            continue
        if not guard.claim_text(item.text):
            continue
        guard.register_text(item.text)
        text = item.text
        if item.rescued and item.kind is ComparisonFactKind.CONFLICT:
            text = f"{text}. {rescued_sentence()}"
        blocks.append(
            _block(
                f"finding-{finding_id}-{item.template_key}",
                "reason",
                f"marriage.fact.{item.template_key}",
                text,
                domain=domain,
                source_finding_ids=[finding_id],
            )
        )
    return blocks


def _finding_text(finding: FindingNarrativeInput) -> NarrativeEntry | None:
    """Map a finding onto catalog wording. Preserve rescued condition."""
    entry = finding_entry(finding.domain, finding.finding_type)
    if entry is None:
        return None
    text = entry.observation
    if "rescued" in finding.conditions:
        text = f"{text} {rescued_sentence()}"
    return NarrativeEntry(entry.key, entry.headline, text, entry.reason, entry.impact, entry.action_bridge)


def _highlights(
    payload: NarrativeInput,
    findings: dict[str, FindingNarrativeInput],
) -> list[MarriageNarrativeHighlight]:
    """Short specific comparison highlights. Generic finding labels are not used."""
    if payload.comparison_facts:
        items: list[MarriageNarrativeHighlight] = []
        items.extend(_fact_highlights("strength", payload.comparison_facts, ComparisonFactKind.SUPPORT, 4))
        items.extend(_fact_highlights("risk", payload.comparison_facts, ComparisonFactKind.CONFLICT, 4))
        return items
    items = []
    items.extend(_highlight_group("strength", payload.strength_finding_ids, findings, 3))
    items.extend(_highlight_group("risk", payload.risk_finding_ids, findings, 3))
    return items


def _fact_highlights(
    kind: str,
    facts: list[ComparisonNarrativeFact],
    fact_kind: ComparisonFactKind,
    limit: int,
) -> list[MarriageNarrativeHighlight]:
    """Build highlights from comparison sentences."""
    items: list[MarriageNarrativeHighlight] = []
    seen: set[str] = set()
    for fact in facts:
        if fact.kind is not fact_kind:
            continue
        if fact.text in seen:
            continue
        seen.add(fact.text)
        items.append(
            MarriageNarrativeHighlight(
                highlight_id=f"{kind}-{fact.template_key}-{len(items)}",
                kind=kind,
                catalog_key=f"marriage.fact.{fact.template_key}",
                text=fact.text,
                source_finding_ids=list(fact.finding_ids),
            )
        )
        if len(items) >= limit:
            break
    return items


def _highlight_group(
    kind: str,
    finding_ids: list[str],
    findings: dict[str, FindingNarrativeInput],
    limit: int,
) -> list[MarriageNarrativeHighlight]:
    """Build up to `limit` highlights of one kind."""
    items: list[MarriageNarrativeHighlight] = []
    seen: set[str] = set()
    for finding_id in finding_ids:
        finding = findings.get(finding_id)
        if finding is None:
            continue
        entry = finding_entry(finding.domain, finding.finding_type)
        if entry is None:
            continue
        key = entry.key
        if key in seen:
            continue
        seen.add(key)
        items.append(
            MarriageNarrativeHighlight(
                highlight_id=f"{kind}-{finding.finding_id}",
                kind=kind,
                catalog_key=entry.key,
                text=entry.headline,
                source_finding_ids=[finding.finding_id],
            )
        )
        if len(items) >= limit:
            break
    return items


def _publish_domain(domain: DomainNarrativeInput) -> bool:
    """Publish only available domains with a real semantic state."""
    if not domain.available or domain.state is None:
        return False
    if domain.state.value == "insufficient":
        return False
    return True


def _has_timing(payload: NarrativeInput) -> bool:
    """True when timing findings or timing recommendations exist."""
    if any(item.finding_type is FindingType.TIMING for item in payload.findings):
        return True
    return any(item.action_type.value == "timing_awareness" for item in payload.recommendations)


def _timing_states(payload: NarrativeInput) -> list[str]:
    """Derive timing labels from finding keys. Never emit calendar years."""
    states: list[str] = []
    for item in payload.findings:
        if item.finding_type is not FindingType.TIMING:
            continue
        key = item.semantic_key or ""
        if "misalignment" in key or "unfavorable" in key:
            label = "sensitive"
        elif "alignment" in key:
            label = "supportive"
        else:
            label = "mixed"
        if label not in states:
            states.append(label)
    if not states:
        states.append("stable")
    return states


def _block(
    block_id: str,
    stage: str,
    catalog_key: str,
    text: str,
    *,
    domain: MarriageDomain | None = None,
    source_finding_ids: list[str] | None = None,
    source_recommendation_ids: list[str] | None = None,
    priority: str | None = None,
    confidence: float | None = None,
) -> MarriageNarrativeBlock:
    """Create one narrative block."""
    return MarriageNarrativeBlock(
        block_id=block_id,
        stage=stage,
        catalog_key=catalog_key,
        text=text,
        domain=domain,
        source_finding_ids=list(source_finding_ids or []),
        source_recommendation_ids=list(source_recommendation_ids or []),
        visibility="customer",
        priority=priority,
        confidence=confidence,
    )

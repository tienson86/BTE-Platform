"""RB05-D phone domain insights, 4+2 findings, and customer-safe evidence."""

from __future__ import annotations

from collections import OrderedDict

from engines.number_energy.constants import CUSTOMER_PRESENTATION_CONTEXTS
from engines.number_energy.findings_catalog import (
    ALLOWED_EVIDENCE_SOURCES,
    BALANCE_CAT_LEAD,
    BALANCE_MIXED,
    CAREER_HAS_DN,
    CAREER_QUIET,
    CAREER_TY_DN,
    CAUTION_CAT_COUNT,
    CAUTION_SPEECH,
    DOMAIN_TITLES,
    GOLDEN_DOMAINS,
    INTERACTION_DN_DN,
    INTERACTION_DN_TY,
    INTERACTION_HH_SK,
    INTERACTION_SK_TY,
    INTERACTION_TY_DN,
    LABEL_HUO_HAI,
    LABEL_SHENG_QI,
    LABEL_TIAN_YI,
    LABEL_YAN_NIAN,
    PERSONALITY_DN,
    PERSONALITY_GENERIC,
    PERSONALITY_SK,
    PERSONALITY_TY,
    REL_HAS_SK,
    REL_QUIET,
    SOURCE_CHAIN,
    SOURCE_ENERGY_DISTRIBUTION,
    SOURCE_LATER_OUTCOME,
    SOURCE_PAIR_OCCURRENCES,
    SOURCE_PAIR_SUMMARY,
    SOURCE_TRIPLE_OCCURRENCES,
    SOURCE_WEALTH_FLOW,
    STRENGTH_CAREER_REPEAT,
    STRENGTH_CAREER_RESULT,
    STRENGTH_KHAU_TAI,
    STRENGTH_QUY_NHAN,
    WEALTH_DN_TY,
    WEALTH_HAS_TIAN_YI,
    WEALTH_NO_TIAN_YI,
    WEALTH_SK_TY,
    DomainTemplate,
    FindingTemplate,
)
from engines.number_energy.types import (
    CustomerPairOccurrence,
    CustomerTripleOccurrence,
    DomainInsightView,
    EnergyDistributionRow,
    EvidenceGroupView,
    EvidenceRefView,
    FindingView,
    LaterOutcomeView,
    NumberEnergyChainView,
    PairSummaryView,
    WealthFlowView,
)

FEATURED_TRIPLE_PRIORITY = "FEATURED"


def build_phone_findings(
    purpose_context: str,
    pair_occurrences: tuple[CustomerPairOccurrence, ...],
    pair_summary: PairSummaryView | None,
    energy_distribution: tuple[EnergyDistributionRow, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
) -> tuple[
    tuple[DomainInsightView, ...],
    tuple[FindingView, ...],
    tuple[FindingView, ...],
    tuple[EvidenceGroupView, ...],
]:
    """Emit five domains, strengths/cautions, and evidence for customer-facing numbers."""
    if purpose_context not in CUSTOMER_PRESENTATION_CONTEXTS:
        return (), (), (), ()
    signals = _signals(energy_distribution, pair_summary, triples, chain)
    domains = _domains(signals, triples, chain, wealth_flow, later_outcome)
    strengths = _strengths(signals, triples)
    cautions = _cautions(signals, pair_occurrences, triples, pair_summary)
    evidence = _evidence(
        pair_occurrences,
        pair_summary,
        energy_distribution,
        triples,
        chain,
        wealth_flow,
        later_outcome,
    )
    return domains, strengths, cautions, evidence


def _signals(
    distribution: tuple[EnergyDistributionRow, ...],
    pair_summary: PairSummaryView | None,
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
) -> dict[str, object]:
    """Collect structural flags from RB05-A/B objects only."""
    counts = {row.energy_label: row.count for row in distribution}
    interactions = {item.interaction_label for item in triples}
    return {
        "tian_yi": counts.get(LABEL_TIAN_YI, 0),
        "sheng_qi": counts.get(LABEL_SHENG_QI, 0),
        "yan_nian": counts.get(LABEL_YAN_NIAN, 0),
        "huo_hai": counts.get(LABEL_HUO_HAI, 0),
        "supportive": pair_summary.supportive_pair_count if pair_summary else 0,
        "challenging": pair_summary.challenging_pair_count if pair_summary else 0,
        "has_sk_ty": INTERACTION_SK_TY in interactions,
        "has_ty_dn": INTERACTION_TY_DN in interactions,
        "has_dn_ty": INTERACTION_DN_TY in interactions,
        "has_hh_sk": INTERACTION_HH_SK in interactions,
        "has_dn_dn": INTERACTION_DN_DN in interactions,
        "primary": chain.primary_energy_label if chain else None,
        "terminal": chain.terminal_energy_label if chain else None,
    }


def _is_golden(signals: dict[str, object]) -> bool:
    """Golden phone: 2 TY, 2 SK, 3 DN, 1 HH, SK→TY, TY→DN, DN→TY, 7 Cát / 1 Hung."""
    return (
        signals["tian_yi"] == 2
        and signals["sheng_qi"] == 2
        and signals["yan_nian"] == 3
        and signals["huo_hai"] == 1
        and signals["supportive"] == 7
        and signals["challenging"] == 1
        and bool(signals["has_sk_ty"])
        and bool(signals["has_ty_dn"])
        and bool(signals["has_dn_ty"])
    )


def _domains(
    signals: dict[str, object],
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
) -> tuple[DomainInsightView, ...]:
    """Always five domains, Golden copy when the structural lock matches."""
    templates = GOLDEN_DOMAINS if _is_golden(signals) else _fallback_domains(signals)
    return tuple(
        _domain_card(index, template, triples, chain, wealth_flow, later_outcome)
        for index, template in enumerate(templates)
    )


def _fallback_domains(signals: dict[str, object]) -> tuple[DomainTemplate, ...]:
    """Select Knowledge 10/13 templates when the Golden composition does not apply."""
    return (
        _wealth_template(signals),
        _career_template(signals),
        _relationship_template(signals),
        _personality_template(signals),
        _balance_template(signals),
    )


def _wealth_template(signals: dict[str, object]) -> DomainTemplate:
    """Wealth domain from Thiên Y presence and SOURCE→TY direction."""
    if int(signals["tian_yi"]) <= 0:
        return WEALTH_NO_TIAN_YI
    if signals["has_sk_ty"]:
        return WEALTH_SK_TY
    if signals["has_dn_ty"]:
        return WEALTH_DN_TY
    return WEALTH_HAS_TIAN_YI


def _career_template(signals: dict[str, object]) -> DomainTemplate:
    """Career domain from Diên Niên count and TY→DN."""
    if int(signals["yan_nian"]) >= 3 and signals["has_ty_dn"]:
        return GOLDEN_DOMAINS[1]
    if signals["has_ty_dn"]:
        return CAREER_TY_DN
    if int(signals["yan_nian"]) >= 1:
        return CAREER_HAS_DN
    return CAREER_QUIET


def _relationship_template(signals: dict[str, object]) -> DomainTemplate:
    """Relationship domain from Sinh Khí; no marriage prediction."""
    if int(signals["sheng_qi"]) >= 2:
        return GOLDEN_DOMAINS[2]
    if int(signals["sheng_qi"]) >= 1:
        return REL_HAS_SK
    return REL_QUIET


def _personality_template(signals: dict[str, object]) -> DomainTemplate:
    """Personality follows chain primary, not a single pair."""
    primary = signals["primary"]
    if primary == LABEL_YAN_NIAN:
        return PERSONALITY_DN if not _is_golden(signals) else GOLDEN_DOMAINS[3]
    if primary == LABEL_SHENG_QI:
        return PERSONALITY_SK
    if primary == LABEL_TIAN_YI:
        return PERSONALITY_TY
    return PERSONALITY_GENERIC


def _balance_template(signals: dict[str, object]) -> DomainTemplate:
    """Balance from Cát/Hung pair counts, not a score."""
    if int(signals["supportive"]) > int(signals["challenging"]):
        return BALANCE_CAT_LEAD
    return BALANCE_MIXED


def _domain_card(
    index: int,
    template: DomainTemplate,
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
) -> DomainInsightView:
    """Attach customer-safe refs already emitted by RB05-A/B/C."""
    return DomainInsightView(
        id=f"DI-{index + 1:02d}",
        domain=template.domain,
        conclusion=template.conclusion,
        narrative=template.narrative,
        caution=template.caution,
        conclusion_key=template.conclusion_key,
        narrative_key=template.narrative_key,
        caution_key=template.caution_key,
        evidence_refs=_domain_refs(
            template.domain, triples, chain, wealth_flow, later_outcome
        ),
    )


def _domain_refs(
    domain: str,
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
) -> tuple[EvidenceRefView, ...]:
    """Map each required domain to existing pair/triple/wealth/chain objects."""
    refs: list[EvidenceRefView] = []
    if domain == DOMAIN_TITLES[0]:
        refs.extend(_triple_refs(triples, (INTERACTION_SK_TY, INTERACTION_DN_TY)))
        if wealth_flow is not None and wealth_flow.stages:
            stage = wealth_flow.stages[0]
            refs.append(EvidenceRefView(SOURCE_WEALTH_FLOW, stage.id, stage.evidence))
        if later_outcome and later_outcome.terminal_pair_digits:
            refs.append(
                EvidenceRefView(
                    SOURCE_LATER_OUTCOME,
                    later_outcome.terminal_pair_digits,
                    later_outcome.terminal_energy_label,
                )
            )
    elif domain == DOMAIN_TITLES[1]:
        refs.extend(_triple_refs(triples, (INTERACTION_TY_DN, INTERACTION_DN_TY)))
        refs.extend(_distribution_ref(LABEL_YAN_NIAN, chain))
    elif domain == DOMAIN_TITLES[2]:
        refs.extend(_triple_refs(triples, (INTERACTION_SK_TY,)))
        refs.extend(_distribution_ref(LABEL_SHENG_QI, chain))
    elif domain == DOMAIN_TITLES[3]:
        if chain and chain.primary_energy_label:
            refs.append(
                EvidenceRefView(SOURCE_CHAIN, "primary_energy_label", chain.primary_energy_label)
            )
        refs.extend(_triple_refs(triples, (INTERACTION_DN_DN,)))
    else:
        refs.append(EvidenceRefView(SOURCE_PAIR_SUMMARY, "pair_counts", None))
        refs.extend(_triple_refs(triples, (INTERACTION_HH_SK,)))
    return tuple(refs) if refs else (EvidenceRefView(SOURCE_PAIR_SUMMARY, "pair_counts", None),)


def _triple_refs(
    triples: tuple[CustomerTripleOccurrence, ...],
    interactions: tuple[str, ...],
) -> list[EvidenceRefView]:
    """Collect triple digits for named directed interactions."""
    wanted = set(interactions)
    return [
        EvidenceRefView(SOURCE_TRIPLE_OCCURRENCES, item.digits, item.interaction_label)
        for item in triples
        if item.interaction_label in wanted
    ]


def _distribution_ref(
    label: str,
    chain: NumberEnergyChainView | None,
) -> list[EvidenceRefView]:
    """Point at distribution label; add chain primary when it matches."""
    refs = [EvidenceRefView(SOURCE_ENERGY_DISTRIBUTION, label, label)]
    if chain and chain.primary_energy_label == label:
        refs.append(EvidenceRefView(SOURCE_CHAIN, "primary_energy_label", label))
    return refs


def _strengths(
    signals: dict[str, object],
    triples: tuple[CustomerTripleOccurrence, ...],
) -> tuple[FindingView, ...]:
    """Activate catalog strengths only when the matching triple/count exists."""
    findings: list[FindingView] = []
    if signals["has_sk_ty"]:
        findings.append(_finding("ST-01", STRENGTH_QUY_NHAN, triples, INTERACTION_SK_TY))
    if int(signals["yan_nian"]) >= 2 or signals["has_dn_dn"]:
        findings.append(
            _finding("ST-02", STRENGTH_CAREER_REPEAT, triples, INTERACTION_DN_DN)
        )
    if signals["has_dn_ty"]:
        findings.append(
            _finding("ST-03", STRENGTH_CAREER_RESULT, triples, INTERACTION_DN_TY)
        )
    if signals["has_hh_sk"]:
        findings.append(_finding("ST-04", STRENGTH_KHAU_TAI, triples, INTERACTION_HH_SK))
    return tuple(findings)


def _cautions(
    signals: dict[str, object],
    pairs: tuple[CustomerPairOccurrence, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
    pair_summary: PairSummaryView | None,
) -> tuple[FindingView, ...]:
    """Speech caution from Họa Hại; educational Cát-count for every phone."""
    findings: list[FindingView] = []
    if int(signals["huo_hai"]) >= 1:
        refs = [
            EvidenceRefView(SOURCE_PAIR_OCCURRENCES, item.pair_digits, item.display_name)
            for item in pairs
            if item.display_name == LABEL_HUO_HAI
        ]
        refs.extend(_triple_refs(triples, (INTERACTION_HH_SK,)))
        findings.append(_finding_with_refs("CA-01", CAUTION_SPEECH, tuple(refs)))
    cat_refs: tuple[EvidenceRefView, ...] = ()
    if pair_summary is not None:
        cat_refs = (
            EvidenceRefView(
                SOURCE_PAIR_SUMMARY,
                "pair_counts",
                (
                    f"{pair_summary.pair_count} cặp · "
                    f"{pair_summary.supportive_pair_count} Cát · "
                    f"{pair_summary.challenging_pair_count} Hung"
                ),
            ),
        )
    if not cat_refs:
        cat_refs = (EvidenceRefView(SOURCE_PAIR_SUMMARY, "pair_counts", None),)
    findings.append(_finding_with_refs("CA-02", CAUTION_CAT_COUNT, cat_refs))
    return tuple(findings)


def _finding(
    finding_id: str,
    template: FindingTemplate,
    triples: tuple[CustomerTripleOccurrence, ...],
    interaction: str,
) -> FindingView:
    """Finding with triple evidence, or pair_summary if that triple is absent."""
    refs = tuple(_triple_refs(triples, (interaction,)))
    if not refs:
        refs = (EvidenceRefView(SOURCE_PAIR_SUMMARY, "pair_counts", None),)
    return _finding_with_refs(finding_id, template, refs)


def _finding_with_refs(
    finding_id: str,
    template: FindingTemplate,
    refs: tuple[EvidenceRefView, ...],
) -> FindingView:
    """Bind catalog copy to already-built refs."""
    return FindingView(
        id=finding_id,
        title=template.title,
        summary=template.summary,
        semantic_key=template.semantic_key,
        evidence_refs=refs,
    )


def _evidence(
    pairs: tuple[CustomerPairOccurrence, ...],
    pair_summary: PairSummaryView | None,
    distribution: tuple[EnergyDistributionRow, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
) -> tuple[EvidenceGroupView, ...]:
    """Grouped customer evidence. Score is intentionally omitted until RB05-E."""
    groups: list[EvidenceGroupView] = []
    pair_items = _pair_group_items(pairs)
    if pair_items:
        groups.append(
            EvidenceGroupView("Cặp năng lượng", SOURCE_PAIR_OCCURRENCES, pair_items)
        )
    featured = tuple(
        EvidenceRefView(SOURCE_TRIPLE_OCCURRENCES, item.digits, item.interaction_label)
        for item in triples
        if item.priority == FEATURED_TRIPLE_PRIORITY
    )
    if featured:
        groups.append(
            EvidenceGroupView("Bộ ba nổi bật", SOURCE_TRIPLE_OCCURRENCES, featured)
        )
    if wealth_flow is not None:
        stage_items = tuple(
            EvidenceRefView(SOURCE_WEALTH_FLOW, stage.id, stage.evidence or stage.headline)
            for stage in wealth_flow.stages
            if stage.interpretation_status == "DEFINED"
        )
        if stage_items:
            groups.append(EvidenceGroupView("Dòng tài vận", SOURCE_WEALTH_FLOW, stage_items))
    if later_outcome and later_outcome.terminal_pair_digits:
        groups.append(
            EvidenceGroupView(
                "Năng lượng kết",
                SOURCE_LATER_OUTCOME,
                (
                    EvidenceRefView(
                        SOURCE_LATER_OUTCOME,
                        later_outcome.terminal_pair_digits,
                        later_outcome.terminal_energy_label,
                    ),
                ),
            )
        )
    if chain and chain.primary_energy_label:
        highlight = _prominent_labels(chain)
        groups.append(
            EvidenceGroupView(
                "Trường nổi bật",
                SOURCE_CHAIN,
                (EvidenceRefView(SOURCE_CHAIN, "primary_energy_label", highlight),),
            )
        )
    if pair_summary is not None:
        groups.append(
            EvidenceGroupView(
                "Tổng cặp",
                SOURCE_PAIR_SUMMARY,
                (
                    EvidenceRefView(
                        SOURCE_PAIR_SUMMARY,
                        "pair_counts",
                        (
                            f"{pair_summary.pair_count} cặp · "
                            f"{pair_summary.supportive_pair_count} Cát · "
                            f"{pair_summary.challenging_pair_count} Hung"
                        ),
                    ),
                ),
            )
        )
    present = tuple(
        EvidenceRefView(SOURCE_ENERGY_DISTRIBUTION, row.energy_label, str(row.count))
        for row in distribution
        if row.count > 0
    )
    if present:
        groups.append(
            EvidenceGroupView("Phân bố", SOURCE_ENERGY_DISTRIBUTION, present)
        )
    for group in groups:
        assert group.source in ALLOWED_EVIDENCE_SOURCES
        for item in group.items:
            assert item.source in ALLOWED_EVIDENCE_SOURCES
    return tuple(groups)


def _pair_group_items(
    pairs: tuple[CustomerPairOccurrence, ...],
) -> tuple[EvidenceRefView, ...]:
    """Group pair digits by energy label, preserving duplicate order."""
    grouped: OrderedDict[str, list[str]] = OrderedDict()
    for item in pairs:
        grouped.setdefault(item.display_name, []).append(item.pair_digits)
    return tuple(
        EvidenceRefView(SOURCE_PAIR_OCCURRENCES, " / ".join(digits), label)
        for label, digits in grouped.items()
    )


def _prominent_labels(chain: NumberEnergyChainView) -> str:
    """Primary, then terminal, then remaining secondaries — Golden DN · TY · SK."""
    labels: list[str] = []
    if chain.primary_energy_label:
        labels.append(chain.primary_energy_label)
    if chain.terminal_energy_label and chain.terminal_energy_label not in labels:
        labels.append(chain.terminal_energy_label)
    for item in chain.secondary_energy_labels:
        if item not in labels:
            labels.append(item)
    return " · ".join(labels)

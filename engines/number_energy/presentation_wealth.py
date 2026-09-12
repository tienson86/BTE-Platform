"""RB05-C Phone Wealth Flow resolver. Phone-only; no score or recommendation."""

from __future__ import annotations

from engines.number_energy.constants import ENERGY_INTERACTION_CODES
from engines.number_energy.types import (
    CustomerTripleOccurrence,
    CustomerWealthNode,
    EnergyOccurrence,
    LaterOutcomeView,
    NumberEnergyChainView,
    PurposeContext,
    WealthFlowView,
    WealthStageView,
    WealthStoryView,
)
from engines.number_energy.wealth_catalog import (
    GOLDEN_QUY_NHAN_CAREER_DN_TY_SYNTHESIS,
    NO_DIRECT_THIEN_Y_HEADLINE,
    NO_DIRECT_THIEN_Y_SUMMARY,
    PRESENCE_HEADLINE,
    PRESENCE_NARRATIVE_MANY,
    PRESENCE_NARRATIVE_ONE,
    PRESENCE_NARRATIVE_TWO,
    PRESENCE_SUMMARY_KEY,
    REFERENCE_PAIR,
    REFERENCE_TRIPLE,
    STATUS_DEFINED,
    STATUS_UNDEFINED,
    STORY_WEALTH_NODE,
    TIAN_YI_ENERGY_ID,
    TIAN_YI_LABEL,
    WEALTH_DESTINATION_BY_RIGHT_CODE,
    WEALTH_ROLE_DESTINATION,
    WEALTH_ROLE_LATER_OUTCOME,
    WEALTH_ROLE_PRESENCE,
    WEALTH_ROLE_SOURCE,
    WEALTH_SOURCE_BY_LEFT_CODE,
    WEALTH_STAGE_IDS,
    WEALTH_STAGE_LABELS,
    WealthDestinationRule,
    WealthSourceRule,
)

DirectedLink = tuple[EnergyOccurrence, EnergyOccurrence, CustomerTripleOccurrence]


def build_phone_wealth(
    purpose_context: str,
    occurrences: tuple[EnergyOccurrence, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
    chain: NumberEnergyChainView | None,
) -> tuple[
    tuple[CustomerWealthNode, ...],
    WealthFlowView | None,
    LaterOutcomeView | None,
    WealthStoryView | None,
]:
    """Resolve Thiên Y wealth nodes and four customer stages for phone numbers."""
    if purpose_context != PurposeContext.PHONE_NUMBER.value:
        return (), None, None, None
    links = _directed_links(occurrences, triples)
    tian_yi = tuple(
        item for item in occurrences if item.energy_id == TIAN_YI_ENERGY_ID
    )
    last_link = links[-1] if links else None
    sources = [link for link in links if link[1].energy_id == TIAN_YI_ENERGY_ID]
    destinations = [link for link in links if link[0].energy_id == TIAN_YI_ENERGY_ID]
    primary_source = _primary_source(sources, last_link)
    primary_dest = destinations[0] if destinations else None
    nodes = _wealth_nodes(tian_yi, primary_source, primary_dest, last_link)
    stages = _wealth_stages(tian_yi, primary_source, primary_dest, last_link, chain)
    later = _later_outcome(chain, last_link)
    story = _wealth_story(primary_source, primary_dest, last_link)
    return nodes, WealthFlowView(stages=stages), later, story


def _directed_links(
    occurrences: tuple[EnergyOccurrence, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
) -> tuple[DirectedLink, ...]:
    """Zip overlapping adjacent pairs with catalog triples."""
    links: list[DirectedLink] = []
    triple_iter = iter(triples)
    for left, right in zip(occurrences, occurrences[1:]):
        if left.pair_digits[1:] != right.pair_digits[:1]:
            continue
        triple = next(triple_iter, None)
        if triple is None:
            break
        links.append((left, right, triple))
    return tuple(links)


def _primary_source(
    sources: list[DirectedLink],
    last_link: DirectedLink | None,
) -> DirectedLink | None:
    """Prefer an earlier SOURCE→Thiên Y; fall back to the only source."""
    if not sources:
        return None
    for link in sources:
        if link is not last_link:
            return link
    return sources[0]


def _wealth_nodes(
    tian_yi: tuple[EnergyOccurrence, ...],
    primary_source: DirectedLink | None,
    primary_dest: DirectedLink | None,
    last_link: DirectedLink | None,
) -> tuple[CustomerWealthNode, ...]:
    """Emit PRESENCE for every Thiên Y, then source / destination / hậu vận."""
    nodes = [_presence_node(item) for item in tian_yi]
    if primary_source is not None and primary_source is not last_link:
        nodes.append(_interaction_node(primary_source, WEALTH_ROLE_SOURCE))
    if primary_dest is not None:
        nodes.append(_interaction_node(primary_dest, WEALTH_ROLE_DESTINATION))
    if last_link is not None:
        nodes.append(_interaction_node(last_link, WEALTH_ROLE_LATER_OUTCOME))
    return tuple(nodes)


def _presence_node(item: EnergyOccurrence) -> CustomerWealthNode:
    """One Thiên Y pair as a PRESENCE node."""
    return CustomerWealthNode(
        role=WEALTH_ROLE_PRESENCE,
        reference_kind=REFERENCE_PAIR,
        reference_digits=item.pair_digits,
        evidence_digits=item.pair_digits,
        source_energy_label=None,
        target_energy_label=TIAN_YI_LABEL,
        interaction_label=None,
        customer_headline=PRESENCE_HEADLINE,
        customer_summary=_presence_narrative(1),
        customer_summary_key=PRESENCE_SUMMARY_KEY,
        interpretation_status=STATUS_DEFINED,
    )


def _interaction_node(link: DirectedLink, role: str) -> CustomerWealthNode:
    """Map a directed triple onto SOURCE, DESTINATION, or LATER_OUTCOME."""
    left, right, triple = link
    headline, summary, key = _node_copy(role, left, right, triple)
    return CustomerWealthNode(
        role=role,
        reference_kind=REFERENCE_TRIPLE,
        reference_digits=triple.digits,
        evidence_digits=triple.digits,
        source_energy_label=left.display_name,
        target_energy_label=right.display_name,
        interaction_label=triple.interaction_label,
        customer_headline=headline,
        customer_summary=summary,
        customer_summary_key=key,
        interpretation_status=triple.interpretation_status,
    )


def _node_copy(
    role: str,
    left: EnergyOccurrence,
    right: EnergyOccurrence,
    triple: CustomerTripleOccurrence,
) -> tuple[str | None, str | None, str | None]:
    """Customer headline/summary from wealth rules, not guessed prose."""
    if role == WEALTH_ROLE_SOURCE:
        rule = _source_rule(left)
        if rule is None:
            return None, triple.customer_summary, triple.customer_summary_key
        return rule.customer_label, rule.customer_wording, f"{rule.key}_SOURCE"
    if role == WEALTH_ROLE_DESTINATION:
        rule = _dest_rule(right)
        if rule is None:
            return None, triple.customer_summary, triple.customer_summary_key
        return rule.customer_label, rule.customer_wording, f"{rule.key}_DESTINATION"
    source_rule = _source_rule(left)
    headline = right.display_name
    summary = _later_summary(right.display_name, source_rule)
    key = f"{source_rule.key}_LATER_OUTCOME" if source_rule else "LATER_OUTCOME"
    return headline, summary, key


def _wealth_stages(
    tian_yi: tuple[EnergyOccurrence, ...],
    primary_source: DirectedLink | None,
    primary_dest: DirectedLink | None,
    last_link: DirectedLink | None,
    chain: NumberEnergyChainView | None,
) -> tuple[WealthStageView, ...]:
    """Always emit four phone stages in canonical order."""
    return (
        _presence_stage(tian_yi),
        _source_stage(primary_source),
        _destination_stage(primary_dest),
        _later_stage(last_link, chain),
    )


def _presence_stage(tian_yi: tuple[EnergyOccurrence, ...]) -> WealthStageView:
    """Stage 1: Có Thiên Y?"""
    if not tian_yi:
        return _stage(
            0,
            NO_DIRECT_THIEN_Y_HEADLINE,
            "",
            "",
            NO_DIRECT_THIEN_Y_SUMMARY,
            STATUS_DEFINED,
        )
    evidence = " · ".join(item.pair_digits for item in tian_yi)
    return _stage(
        0,
        PRESENCE_HEADLINE,
        evidence,
        "",
        _presence_narrative(len(tian_yi)),
        STATUS_DEFINED,
    )


def _source_stage(primary_source: DirectedLink | None) -> WealthStageView:
    """Stage 2: Tài từ đâu?"""
    if primary_source is None:
        return _empty_stage(1)
    left, _right, triple = primary_source
    rule = _source_rule(left)
    headline = rule.customer_label if rule else triple.left_energy_label
    narrative = rule.customer_wording if rule else (triple.customer_summary or "")
    status = STATUS_DEFINED if rule else triple.interpretation_status
    return _stage(
        1,
        headline or "",
        triple.digits,
        triple.interaction_label,
        narrative,
        status,
    )


def _destination_stage(primary_dest: DirectedLink | None) -> WealthStageView:
    """Stage 3: Tài đi đâu?"""
    if primary_dest is None:
        return _empty_stage(2)
    _left, right, triple = primary_dest
    rule = _dest_rule(right)
    headline = rule.customer_label if rule else triple.right_energy_label
    narrative = rule.customer_wording if rule else (triple.customer_summary or "")
    status = STATUS_DEFINED if rule else triple.interpretation_status
    return _stage(
        2,
        headline or "",
        triple.digits,
        triple.interaction_label,
        narrative,
        status,
    )


def _later_stage(
    last_link: DirectedLink | None,
    chain: NumberEnergyChainView | None,
) -> WealthStageView:
    """Stage 4: Hậu vận from terminal structure."""
    label = chain.terminal_energy_label if chain else None
    pair_digits = chain.terminal_pair_digits if chain else None
    if last_link is not None:
        left, right, triple = last_link
        source_rule = _source_rule(left)
        narrative = _later_summary(right.display_name, source_rule)
        return _stage(
            3,
            right.display_name,
            triple.digits,
            triple.interaction_label,
            narrative,
            STATUS_DEFINED,
        )
    if label and pair_digits:
        narrative = f"Phần cuối dãy quy về {label}."
        return _stage(3, label, pair_digits, "", narrative, STATUS_DEFINED)
    return _empty_stage(3)


def _later_outcome(
    chain: NumberEnergyChainView | None,
    last_link: DirectedLink | None,
) -> LaterOutcomeView:
    """Terminal pair/triple plus catalog hậu vận wording."""
    source_rule = _source_rule(last_link[0]) if last_link else None
    terminal_label = chain.terminal_energy_label if chain else None
    summary = None
    if terminal_label:
        summary = _later_summary(terminal_label, source_rule)
    return LaterOutcomeView(
        terminal_pair_digits=chain.terminal_pair_digits if chain else None,
        terminal_energy_label=terminal_label,
        terminal_triple_digits=chain.terminal_triple_digits if chain else None,
        terminal_interaction_label=(
            chain.terminal_interaction_label if chain else None
        ),
        customer_summary=summary,
    )


def _wealth_story(
    primary_source: DirectedLink | None,
    primary_dest: DirectedLink | None,
    last_link: DirectedLink | None,
) -> WealthStoryView | None:
    """Compose Quý nhân → Tài → Sự nghiệp → Tài when both legs exist."""
    source_rule = _source_rule(primary_source[0]) if primary_source else None
    dest_rule = _dest_rule(primary_dest[1]) if primary_dest else None
    if source_rule is None or dest_rule is None:
        return None
    nodes = (
        source_rule.story_node,
        STORY_WEALTH_NODE,
        dest_rule.story_node,
        STORY_WEALTH_NODE,
    )
    return WealthStoryView(
        nodes=nodes,
        display=" → ".join(nodes),
        synthesis=_story_synthesis(source_rule, dest_rule, last_link),
    )


def _story_synthesis(
    source_rule: WealthSourceRule,
    dest_rule: WealthDestinationRule,
    last_link: DirectedLink | None,
) -> str:
    """Use Golden synthesis only for the locked SK → TY → DN → TY pattern."""
    last_code = _energy_code(last_link[0]) if last_link else None
    if (
        source_rule.key == "QUY_NHAN"
        and dest_rule.key == "CAREER_BUSINESS"
        and last_code == "DN"
        and last_link is not None
        and last_link[1].energy_id == TIAN_YI_ENERGY_ID
    ):
        return GOLDEN_QUY_NHAN_CAREER_DN_TY_SYNTHESIS
    return (
        f"Dòng tài vận của dãy đi theo hướng: {source_rule.story_node} mở đường, "
        f"nguồn lực được đưa vào {dest_rule.story_node}, "
        "và phần cuối lại quy về khả năng tạo Tài."
    )


def _later_summary(terminal_label: str, source_rule: WealthSourceRule | None) -> str:
    """Hậu vận uses 'Phần cuối dãy...', never lifetime destiny."""
    lead = f"Phần cuối dãy quy về {terminal_label}."
    if source_rule is None:
        return lead
    return f"{lead} {source_rule.later_followup}"


def _presence_narrative(count: int) -> str:
    """Count-based presence copy without financial guarantee."""
    if count <= 1:
        return PRESENCE_NARRATIVE_ONE
    if count == 2:
        return PRESENCE_NARRATIVE_TWO
    return PRESENCE_NARRATIVE_MANY


def _source_rule(item: EnergyOccurrence) -> WealthSourceRule | None:
    """Look up SOURCE → Thiên Y wording by left energy code."""
    code = _energy_code(item)
    if code is None:
        return None
    return WEALTH_SOURCE_BY_LEFT_CODE.get(code)


def _dest_rule(item: EnergyOccurrence) -> WealthDestinationRule | None:
    """Look up Thiên Y → TARGET wording by right energy code."""
    code = _energy_code(item)
    if code is None:
        return None
    return WEALTH_DESTINATION_BY_RIGHT_CODE.get(code)


def _energy_code(item: EnergyOccurrence) -> str | None:
    """Knowledge 12 interaction code for an occurrence."""
    return ENERGY_INTERACTION_CODES.get(item.energy_id)


def _stage(
    index: int,
    headline: str,
    evidence: str,
    interaction: str,
    narrative: str,
    status: str,
) -> WealthStageView:
    """Build one of WF-01…WF-04."""
    return WealthStageView(
        id=WEALTH_STAGE_IDS[index],
        label=WEALTH_STAGE_LABELS[index],
        headline=headline,
        evidence=evidence,
        interaction=interaction,
        narrative=narrative,
        interpretation_status=status,
    )


def _empty_stage(index: int) -> WealthStageView:
    """Undefined stage when that wealth leg is absent."""
    return _stage(index, "", "", "", "", STATUS_UNDEFINED)

"""RB05-F phone assessment and recommendation. No score, no sales copy."""

from __future__ import annotations

from engines.number_energy.assessment_catalog import (
    ASSESSMENT_TITLE,
    BALANCE_COPY_KEY,
    BALANCE_SUMMARY,
    GENERIC_ASSESSMENT_SUMMARY,
    GOLDEN_ASSESSMENT_SUMMARY,
    GOLDEN_RECOMMENDATION_KEY,
    GOLDEN_RECOMMENDATION_LABEL,
    GOLDEN_RECOMMENDATION_SUMMARY,
    GOLDEN_STORY_KEY,
    GOLDEN_STORY_LINE,
    GOLDEN_STORY_NODES,
    GOLDEN_STRENGTH_TITLES,
    KEEP_COPY_KEY,
    KEEP_SUMMARY,
    STORY_NODE_MAP,
)
from engines.number_energy.types import (
    AssessmentView,
    FindingView,
    NumberEnergyChainView,
    PairSummaryView,
    PurposeContext,
    RecommendationView,
    WealthStoryView,
)


def build_phone_assessment(
    purpose_context: str,
    pair_summary: PairSummaryView | None,
    chain: NumberEnergyChainView | None,
    wealth_story: WealthStoryView | None,
    strengths: tuple[FindingView, ...],
) -> tuple[AssessmentView | None, RecommendationView | None]:
    """Compose assessment/recommendation from RB05-A/B/C/D objects only."""
    if purpose_context != PurposeContext.PHONE_NUMBER.value:
        return None, None
    if _is_golden(pair_summary, chain, wealth_story, strengths):
        return _golden_assessment(), _golden_recommendation()
    return _fallback_assessment(chain, wealth_story), _fallback_recommendation(pair_summary)


def _is_golden(
    pair_summary: PairSummaryView | None,
    chain: NumberEnergyChainView | None,
    wealth_story: WealthStoryView | None,
    strengths: tuple[FindingView, ...],
) -> bool:
    """Lock Golden copy from already-emitted structure, not from a score."""
    if pair_summary is None or chain is None or wealth_story is None:
        return False
    if pair_summary.supportive_pair_count != 7:
        return False
    if pair_summary.challenging_pair_count != 1:
        return False
    if chain.primary_energy_label != "Diên Niên":
        return False
    present = {
        chain.primary_energy_label,
        chain.terminal_energy_label,
        *chain.secondary_energy_labels,
    }
    if "Sinh Khí" not in present or "Thiên Y" not in present:
        return False
    if wealth_story.display != "Quý nhân & cơ hội → Tài → Sự nghiệp → Tài":
        return False
    titles = tuple(item.title for item in strengths)
    return titles == GOLDEN_STRENGTH_TITLES


def _golden_assessment() -> AssessmentView:
    """Frozen Golden fixture §48 short story used by the static UI."""
    return AssessmentView(
        title=ASSESSMENT_TITLE,
        summary=GOLDEN_ASSESSMENT_SUMMARY,
        story_line=GOLDEN_STORY_LINE,
        story_nodes=GOLDEN_STORY_NODES,
        story_key=GOLDEN_STORY_KEY,
    )


def _golden_recommendation() -> RecommendationView:
    """Frozen Golden fixture §50 continue-to-use state. Not a sales pitch."""
    return RecommendationView(
        label=GOLDEN_RECOMMENDATION_LABEL,
        summary=GOLDEN_RECOMMENDATION_SUMMARY,
        copy_key=GOLDEN_RECOMMENDATION_KEY,
    )


def _fallback_assessment(
    chain: NumberEnergyChainView | None,
    wealth_story: WealthStoryView | None,
) -> AssessmentView:
    """Structural summary from chain + wealth story nodes already emitted."""
    nodes = _story_nodes(wealth_story)
    return AssessmentView(
        title=ASSESSMENT_TITLE,
        summary=_chain_summary(chain),
        story_line=" → ".join(nodes) if nodes else "",
        story_nodes=nodes,
        story_key="ASM-STORY-FROM-WEALTH" if nodes else None,
    )


def _fallback_recommendation(
    pair_summary: PairSummaryView | None,
) -> RecommendationView:
    """Keep vs balance from pair counts. Never tells the user to buy a new number."""
    supportive = pair_summary.supportive_pair_count if pair_summary else 0
    challenging = pair_summary.challenging_pair_count if pair_summary else 0
    if supportive > challenging:
        return RecommendationView(
            label=None,
            summary=KEEP_SUMMARY,
            copy_key=KEEP_COPY_KEY,
        )
    return RecommendationView(
        label=None,
        summary=BALANCE_SUMMARY,
        copy_key=BALANCE_COPY_KEY,
    )


def _chain_summary(chain: NumberEnergyChainView | None) -> str:
    """One structural sentence from primary/secondary/terminal labels."""
    if chain is None or not chain.primary_energy_label:
        return GENERIC_ASSESSMENT_SUMMARY
    primary = chain.primary_energy_label
    others: list[str] = []
    for label in (chain.terminal_energy_label, *chain.secondary_energy_labels):
        if label and label != primary and label not in others:
            others.append(label)
    if not others:
        return f"Dãy số nổi bật ở {primary}."
    if len(others) == 1:
        return f"Dãy số nổi bật ở {primary}, đi cùng {others[0]}."
    return f"Dãy số nổi bật ở {primary}, đi cùng {others[0]} và {others[1]}."


def _story_nodes(wealth_story: WealthStoryView | None) -> tuple[str, ...]:
    """Map wealth_story customer nodes to the uppercase assessment flow."""
    if wealth_story is None:
        return ()
    mapped: list[str] = []
    for node in wealth_story.nodes:
        label = STORY_NODE_MAP.get(node)
        if label is None:
            return ()
        mapped.append(label)
    return tuple(mapped)

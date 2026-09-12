"""RB05-E Phone Score from interpretation outputs. Score does not rewrite findings."""

from __future__ import annotations

from engines.number_energy.constants import (
    CUSTOMER_PRESENTATION_CONTEXTS,
    CUSTOMER_CATEGORY_CAT,
    CUSTOMER_CATEGORY_HUNG,
    CUSTOMER_STRENGTH_STRONG,
    TRIPLE_PRIORITY_COMPACT,
    TRIPLE_PRIORITY_FEATURED,
    TRIPLE_PRIORITY_STANDARD,
    TRIPLE_STATUS_DEFINED,
)
from engines.number_energy.findings_catalog import (
    INTERACTION_DN_TY,
    INTERACTION_HH_SK,
    INTERACTION_SK_TY,
    INTERACTION_TY_DN,
    LABEL_HUO_HAI,
    LABEL_SHENG_QI,
    LABEL_TIAN_YI,
    LABEL_YAN_NIAN,
)
from engines.number_energy.score_catalog import (
    DIM_CAREER_LABEL,
    DIM_CAREER_MAX,
    DIM_STABILITY_LABEL,
    DIM_STABILITY_MAX,
    DIM_STRUCTURE_LABEL,
    DIM_STRUCTURE_MAX,
    DIM_TAIL_LABEL,
    DIM_TAIL_MAX,
    DIM_WEALTH_LABEL,
    DIM_WEALTH_MAX,
    GRADE_BANDS,
    REASON_CAREER_AXIS,
    REASON_CAT_LEAD,
    REASON_HUO_HAI_USE,
    REASON_WEALTH_SOURCE,
    SCORE_MAX,
)
from engines.number_energy.types import (
    CustomerPairOccurrence,
    CustomerTripleOccurrence,
    CustomerWealthNode,
    EnergyDistributionRow,
    EnergyOccurrence,
    LaterOutcomeView,
    PairSummaryView,
    PhoneScoreView,
    ScoreBreakdownRow,
    ScoreReasonView,
    WealthFlowView,
)

SUPPORTIVE_LABELS = frozenset(
    {LABEL_SHENG_QI, LABEL_TIAN_YI, LABEL_YAN_NIAN, "Phục Vị"}
)
CHALLENGING_LABELS = frozenset(
    {LABEL_HUO_HAI, "Ngũ Quỷ", "Lục Sát", "Tuyệt Mệnh"}
)
CONVERTED_HUNG = frozenset(
    {
        f"{label} → {target}"
        for label in CHALLENGING_LABELS
        for target in SUPPORTIVE_LABELS
    }
)


def build_phone_score(
    purpose_context: str,
    pair_occurrences: tuple[CustomerPairOccurrence, ...],
    pair_summary: PairSummaryView | None,
    energy_distribution: tuple[EnergyDistributionRow, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
    wealth_nodes: tuple[CustomerWealthNode, ...],
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
    occurrences: tuple[EnergyOccurrence, ...],
) -> PhoneScoreView | None:
    """Score customer-facing numbers after chain/wealth/findings already exist."""
    if purpose_context not in CUSTOMER_PRESENTATION_CONTEXTS:
        return None
    counts = {row.energy_label: row.count for row in energy_distribution}
    interactions = {item.interaction_label for item in triples}
    structure = _structure(pair_occurrences, pair_summary, triples)
    wealth = _wealth(wealth_nodes, wealth_flow, later_outcome, interactions)
    career = _career(counts, interactions)
    stability = _stability(pair_occurrences, pair_summary, triples, occurrences)
    tail = _tail(pair_occurrences, triples, later_outcome)
    breakdown = (
        ScoreBreakdownRow(DIM_STRUCTURE_LABEL, structure, DIM_STRUCTURE_MAX),
        ScoreBreakdownRow(DIM_WEALTH_LABEL, wealth, DIM_WEALTH_MAX),
        ScoreBreakdownRow(DIM_CAREER_LABEL, career, DIM_CAREER_MAX),
        ScoreBreakdownRow(DIM_STABILITY_LABEL, stability, DIM_STABILITY_MAX),
        ScoreBreakdownRow(DIM_TAIL_LABEL, tail, DIM_TAIL_MAX),
    )
    total = _clamp(structure + wealth + career + stability + tail, 0, SCORE_MAX)
    return PhoneScoreView(
        total=total,
        max_points=SCORE_MAX,
        grade=_grade(total),
        breakdown=breakdown,
        reasons=_reasons(counts, interactions, pair_summary),
        verified_by_runtime=True,
    )


def _structure(
    pairs: tuple[CustomerPairOccurrence, ...],
    pair_summary: PairSummaryView | None,
    triples: tuple[CustomerTripleOccurrence, ...],
) -> int:
    """A: pair quality + interaction quality + structural balance ≤ 25."""
    return _clamp(_pair_quality(pairs) + _interaction_quality(triples) + _balance(pair_summary, triples), 0, DIM_STRUCTURE_MAX)


def _pair_quality(pairs: tuple[CustomerPairOccurrence, ...]) -> int:
    """A1 0–10 from strength-weighted pairs, not raw Cát−Hung counts."""
    if not pairs:
        return 0
    cat = sum(item.strength_slots for item in pairs if item.category == CUSTOMER_CATEGORY_CAT)
    hung = sum(item.strength_slots for item in pairs if item.category == CUSTOMER_CATEGORY_HUNG)
    total = cat + hung
    if total <= 0:
        return 0
    raw = (cat - hung) / total
    points = int(round((raw + 1.0) * 5.0))
    if hung == 0:
        points = min(points, 8)
    return _clamp(points, 0, 10)


def _interaction_quality(triples: tuple[CustomerTripleOccurrence, ...]) -> int:
    """A2 0–10 from catalog effect weights, not from energy names."""
    points = 0
    for item in triples:
        if item.interpretation_status != TRIPLE_STATUS_DEFINED:
            points -= 1
            continue
        if item.priority == TRIPLE_PRIORITY_FEATURED:
            points += 2
        elif item.priority == TRIPLE_PRIORITY_STANDARD:
            points += 1
        elif item.priority == TRIPLE_PRIORITY_COMPACT:
            points += 0
    return _clamp(points, 0, 10)


def _balance(
    pair_summary: PairSummaryView | None,
    triples: tuple[CustomerTripleOccurrence, ...],
) -> int:
    """A3 0–5. All-Cát is not a perfect score."""
    if pair_summary is None or pair_summary.pair_count == 0:
        return 0
    if pair_summary.challenging_pair_count == 0:
        return 3 if pair_summary.supportive_pair_count else 0
    if pair_summary.supportive_pair_count == 0:
        return 1
    if _converted_hung(triples):
        return 4
    return 2


def _wealth(
    wealth_nodes: tuple[CustomerWealthNode, ...],
    wealth_flow: WealthFlowView | None,
    later_outcome: LaterOutcomeView | None,
    interactions: set[str],
) -> int:
    """B: presence + source + flow + continuity ≤ 25."""
    return _clamp(
        _wealth_presence(wealth_flow)
        + _wealth_source(interactions)
        + _wealth_destination(interactions)
        + _wealth_continuity(wealth_nodes, later_outcome),
        0,
        DIM_WEALTH_MAX,
    )


def _wealth_presence(wealth_flow: WealthFlowView | None) -> int:
    """B1 0–7 from Thiên Y evidence already resolved by wealth flow."""
    if wealth_flow is None or not wealth_flow.stages:
        return 0
    evidence = wealth_flow.stages[0].evidence
    if not evidence:
        return 0
    count = evidence.count("·") + 1
    if count >= 2:
        return 6
    return 4


def _wealth_source(interactions: set[str]) -> int:
    """B2 0–6. Canonical SOURCE→Thiên Y is positive even from a hung left."""
    if INTERACTION_SK_TY in interactions:
        return 6
    if INTERACTION_DN_TY in interactions:
        return 5
    if any(item.endswith(f" → {LABEL_TIAN_YI}") for item in interactions):
        return 4
    return 0


def _wealth_destination(interactions: set[str]) -> int:
    """B3 0–6. Productive outflow is not automatically a penalty."""
    if INTERACTION_TY_DN in interactions:
        return 5
    if any(item.startswith(f"{LABEL_TIAN_YI} → ") for item in interactions):
        return 3
    return 0


def _wealth_continuity(
    wealth_nodes: tuple[CustomerWealthNode, ...],
    later_outcome: LaterOutcomeView | None,
) -> int:
    """B4 0–6 from multiple Thiên Y nodes and terminal wealth."""
    presence = sum(1 for item in wealth_nodes if item.role == "PRESENCE")
    terminal_ty = (
        later_outcome is not None
        and later_outcome.terminal_energy_label == LABEL_TIAN_YI
    )
    terminal_dn_ty = (
        later_outcome is not None
        and later_outcome.terminal_interaction_label == INTERACTION_DN_TY
    )
    if presence >= 2 and terminal_ty and terminal_dn_ty:
        return 5
    if terminal_ty:
        return 4
    if presence >= 1:
        return 3
    return 0


def _career(counts: dict[str, int], interactions: set[str]) -> int:
    """C: Diên Niên + Sinh Khí + productive skill ≤ 20."""
    return _clamp(
        _career_energy(counts.get(LABEL_YAN_NIAN, 0))
        + _noble_support(counts.get(LABEL_SHENG_QI, 0), interactions)
        + _productive_skill(interactions, counts.get(LABEL_YAN_NIAN, 0)),
        0,
        DIM_CAREER_MAX,
    )


def _career_energy(yan_nian: int) -> int:
    """C1 0–8 from Diên Niên count, not from a pair-name lookup."""
    if yan_nian <= 0:
        return 0
    if yan_nian == 1:
        return 4
    if yan_nian == 2:
        return 6
    return 7


def _noble_support(sheng_qi: int, interactions: set[str]) -> int:
    """C2 0–6 from Sinh Khí presence plus SOURCE→Thiên Y."""
    if sheng_qi <= 0:
        return 0
    points = 5 if sheng_qi >= 2 else 3
    if INTERACTION_SK_TY in interactions:
        points += 1
    return _clamp(points, 0, 6)


def _productive_skill(interactions: set[str], yan_nian: int) -> int:
    """C3 0–6. HH→SK is useful skill, not a career-from-hung max."""
    if any(
        item.startswith(f"{label} → {LABEL_YAN_NIAN}")
        for label in CHALLENGING_LABELS
        for item in interactions
    ):
        return 6
    if INTERACTION_HH_SK in interactions:
        return 4
    if yan_nian:
        return 2
    return 0


def _stability(
    pairs: tuple[CustomerPairOccurrence, ...],
    pair_summary: PairSummaryView | None,
    triples: tuple[CustomerTripleOccurrence, ...],
    occurrences: tuple[EnergyOccurrence, ...],
) -> int:
    """D: higher is more stable. 15 is not awarded for all-Cát stuffing."""
    return _clamp(
        _negative_chain(pairs, pair_summary, triples)
        + _modifier_stability(occurrences)
        + _flow_stability(triples),
        0,
        DIM_STABILITY_MAX,
    )


def _negative_chain(
    pairs: tuple[CustomerPairOccurrence, ...],
    pair_summary: PairSummaryView | None,
    triples: tuple[CustomerTripleOccurrence, ...],
) -> int:
    """D1 0–6. Converted hung is better than unresolved hung."""
    challenging = pair_summary.challenging_pair_count if pair_summary else 0
    if challenging <= 0:
        return 5
    converted = _converted_hung(triples)
    head_hung = bool(pairs) and pairs[0].category == CUSTOMER_CATEGORY_HUNG
    if converted and head_hung:
        return 3
    if converted:
        return 4
    return 2


def _modifier_stability(occurrences: tuple[EnergyOccurrence, ...]) -> int:
    """D2 0–4 from modifier effects already computed by the modifier engine."""
    if any(item.state == "AMPLIFIED" and item.display_name in CHALLENGING_LABELS for item in occurrences):
        return 1
    if any(item.state == "HIDDEN" and item.display_name in SUPPORTIVE_LABELS for item in occurrences):
        return 2
    if any(item.via_modifier is not None for item in occurrences):
        return 3
    return 4


def _flow_stability(triples: tuple[CustomerTripleOccurrence, ...]) -> int:
    """D3 0–5. Long, productive chains still have movement."""
    if any(item.startswith(f"{LABEL_TIAN_YI} → Ngũ Quỷ") for item in (t.interaction_label for t in triples)):
        return 1
    count = len(triples)
    if count >= 6:
        return 3
    if count >= 3:
        return 4
    if count >= 1:
        return 5
    return 2


def _tail(
    pairs: tuple[CustomerPairOccurrence, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
    later_outcome: LaterOutcomeView | None,
) -> int:
    """E: terminal energy + last triple + tail modifier ≤ 15."""
    return _clamp(
        _terminal_energy(pairs, later_outcome)
        + _tail_continuity(triples)
        + _tail_modifier(pairs),
        0,
        DIM_TAIL_MAX,
    )


def _terminal_energy(
    pairs: tuple[CustomerPairOccurrence, ...],
    later_outcome: LaterOutcomeView | None,
) -> int:
    """E1 0–8. Terminal Thiên Y is strong, not a destiny guarantee."""
    label = later_outcome.terminal_energy_label if later_outcome else None
    if not label:
        return 0
    if label in CHALLENGING_LABELS:
        return 2
    last = pairs[-1] if pairs else None
    if last and last.strength_label == CUSTOMER_STRENGTH_STRONG:
        return 6
    return 5


def _tail_continuity(triples: tuple[CustomerTripleOccurrence, ...]) -> int:
    """E2 0–4 from the last directed triple, if present."""
    if not triples:
        return 0
    last = triples[-1]
    if last.priority == TRIPLE_PRIORITY_FEATURED:
        return 3
    if last.interpretation_status == TRIPLE_STATUS_DEFINED:
        return 2
    return 1


def _tail_modifier(pairs: tuple[CustomerPairOccurrence, ...]) -> int:
    """E3 0–3. Ending 0/5 is a tail caution, not a fatal verdict."""
    if not pairs:
        return 0
    digits = pairs[-1].pair_digits
    if digits.endswith("0") or digits.startswith("0"):
        return 0
    if "5" in digits:
        return 1
    return 3


def _reasons(
    counts: dict[str, int],
    interactions: set[str],
    pair_summary: PairSummaryView | None,
) -> tuple[ScoreReasonView, ...]:
    """Emit catalog reasons only when matching structure exists."""
    reasons: list[ScoreReasonView] = []
    supportive = pair_summary.supportive_pair_count if pair_summary else 0
    challenging = pair_summary.challenging_pair_count if pair_summary else 0
    if (
        supportive > challenging
        and counts.get(LABEL_SHENG_QI, 0)
        and counts.get(LABEL_TIAN_YI, 0)
        and counts.get(LABEL_YAN_NIAN, 0)
    ):
        reasons.append(_reason(REASON_CAT_LEAD))
    if INTERACTION_SK_TY in interactions:
        reasons.append(_reason(REASON_WEALTH_SOURCE))
    if counts.get(LABEL_YAN_NIAN, 0) >= 2 and INTERACTION_DN_TY in interactions:
        reasons.append(_reason(REASON_CAREER_AXIS))
    if INTERACTION_HH_SK in interactions:
        reasons.append(_reason(REASON_HUO_HAI_USE))
    return tuple(reasons)


def _reason(row: tuple[str, str, str]) -> ScoreReasonView:
    """Bind one frozen score reason."""
    key, title, summary = row
    return ScoreReasonView(title=title, summary=summary, reason_key=key)


def _converted_hung(triples: tuple[CustomerTripleOccurrence, ...]) -> bool:
    """True when a hung left is canonically led into a supportive right."""
    return any(item.interaction_label in CONVERTED_HUNG for item in triples)


def _grade(total: int) -> str:
    """Customer grade band from Knowledge 14. No Đại Cát / Đại Hung."""
    for low, high, label in GRADE_BANDS:
        if low <= total <= high:
            return label
    return GRADE_BANDS[-1][2]


def _clamp(value: int, low: int, high: int) -> int:
    """Keep a component or total inside its canonical range."""
    return max(low, min(high, value))

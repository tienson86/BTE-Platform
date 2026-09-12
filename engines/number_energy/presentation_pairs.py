"""RB05-A customer-safe pair structure for adapter input.

Presentation mapping only. Does not score, resolve triples, or invent wealth.
"""

from __future__ import annotations

from collections import Counter

from engines.number_energy.constants import (
    CHALLENGING_ENERGY_IDS,
    CUSTOMER_CATEGORY_CAT,
    CUSTOMER_CATEGORY_HUNG,
    CUSTOMER_CATEGORY_LABELS,
    CUSTOMER_STRENGTH_LIGHT,
    ENERGY_DISPLAY_NAMES,
    ENERGY_DISTRIBUTION_ORDER,
    PAIR_LOOKUP,
    RANK_TO_STRENGTH_LABEL,
    RANK_TO_STRENGTH_SLOTS,
    STRENGTH_SLOT_COUNT,
)
from engines.number_energy.types import (
    CustomerPairOccurrence,
    EnergyDistributionRow,
    EnergyOccurrence,
    PairSummaryView,
)


def build_pair_occurrences(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[CustomerPairOccurrence, ...]:
    """Map overlapping pairs to customer-safe objects, preserving order."""
    return tuple(
        _customer_pair(index, item) for index, item in enumerate(occurrences)
    )


def build_pair_summary(
    occurrences: tuple[EnergyOccurrence, ...],
) -> PairSummaryView:
    """Count Cát/Hung *pairs* and expose pair-layer lead / terminal labels."""
    supportive = sum(1 for item in occurrences if _is_supportive(item))
    challenging = sum(1 for item in occurrences if not _is_supportive(item))
    primary = _leading_energy_label(occurrences)
    last = occurrences[-1] if occurrences else None
    return PairSummaryView(
        pair_count=len(occurrences),
        supportive_pair_count=supportive,
        challenging_pair_count=challenging,
        primary_energy_label=primary,
        terminal_energy_label=last.display_name if last else None,
        terminal_pair_digits=last.pair_digits if last else None,
    )


def build_energy_distribution(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[EnergyDistributionRow, ...]:
    """Emit all eight catalog energies, including zeros, in canonical order."""
    counts = Counter(item.energy_id for item in occurrences)
    return tuple(
        EnergyDistributionRow(
            energy_label=ENERGY_DISPLAY_NAMES[energy_id],
            count=counts.get(energy_id, 0),
        )
        for energy_id in ENERGY_DISTRIBUTION_ORDER
    )


def _customer_pair(index: int, item: EnergyOccurrence) -> CustomerPairOccurrence:
    """Build one customer pair from the strength matrix, not from rank leakage."""
    category = (
        CUSTOMER_CATEGORY_HUNG
        if item.energy_id in CHALLENGING_ENERGY_IDS
        else CUSTOMER_CATEGORY_CAT
    )
    rank = _matrix_rank(item.pair_digits, item.strength_rank)
    slots = RANK_TO_STRENGTH_SLOTS.get(rank, 1)
    label = RANK_TO_STRENGTH_LABEL.get(rank, CUSTOMER_STRENGTH_LIGHT)
    return CustomerPairOccurrence(
        index=index,
        pair_digits=item.pair_digits,
        display_name=item.display_name,
        category=category,
        category_label=CUSTOMER_CATEGORY_LABELS[category],
        strength_label=label,
        strength_slots=slots,
        strength_visual=_strength_visual(slots),
    )


def _strength_visual(slots: int) -> tuple[bool, bool, bool, bool]:
    """Four customer dots; filled count comes from matrix tier, not rank leak."""
    filled = max(0, min(slots, STRENGTH_SLOT_COUNT))
    return (
        filled >= 1,
        filled >= 2,
        filled >= 3,
        filled >= 4,
    )


def _matrix_rank(pair_digits: str, fallback_rank: int | None) -> int:
    """Read intrinsic pair tier from PAIR_LOOKUP (Knowledge 03)."""
    table = PAIR_LOOKUP.get(pair_digits)
    if table is not None:
        return table[1]
    if fallback_rank is not None and fallback_rank in RANK_TO_STRENGTH_LABEL:
        return fallback_rank
    return 4


def _is_supportive(item: EnergyOccurrence) -> bool:
    """Cát includes Phục Vị (supportive_stabilizing)."""
    return item.energy_id not in CHALLENGING_ENERGY_IDS


def _leading_energy_label(occurrences: tuple[EnergyOccurrence, ...]) -> str | None:
    """Pair-layer lead: highest frequency, first-seen on ties. Not chain.primary."""
    if not occurrences:
        return None
    counts = Counter(item.energy_id for item in occurrences)
    first_index: dict[str, int] = {}
    for index, item in enumerate(occurrences):
        if item.energy_id not in first_index:
            first_index[item.energy_id] = index
    energy_id = min(counts.keys(), key=lambda key: (-counts[key], first_index[key]))
    sample = next(item for item in occurrences if item.energy_id == energy_id)
    return sample.display_name

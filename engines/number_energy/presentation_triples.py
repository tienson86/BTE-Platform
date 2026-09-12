"""RB05-B customer-safe triples and chain. No score or wealth-flow stages."""

from __future__ import annotations

from collections import Counter

from engines.number_energy.constants import (
    ENERGY_DISPLAY_NAMES,
    ENERGY_DISTRIBUTION_ORDER,
    ENERGY_INTERACTION_CODES,
    SUPPORTIVE_ENERGY_IDS,
    TRIPLE_STATUS_DEFINED,
    TRIPLE_STATUS_UNDEFINED,
)
from engines.number_energy.triple_catalog import lookup_triple
from engines.number_energy.types import (
    CustomerTripleOccurrence,
    EnergyOccurrence,
    NumberEnergyChainView,
)


def build_triple_occurrences(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[CustomerTripleOccurrence, ...]:
    """Build overlapping triples in source order and attach catalog keys."""
    triples: list[CustomerTripleOccurrence] = []
    for index, (left, right) in enumerate(zip(occurrences, occurrences[1:])):
        if left.pair_digits[1:] != right.pair_digits[:1]:
            continue
        digits = left.pair_digits[0] + right.pair_digits
        interaction_id = _interaction_id(left.energy_id, right.energy_id)
        row = lookup_triple(interaction_id) if interaction_id else None
        defined = row is not None and interaction_id is not None
        triples.append(
            CustomerTripleOccurrence(
                index=index,
                digits=digits,
                left_pair_digits=left.pair_digits,
                right_pair_digits=right.pair_digits,
                left_energy_label=left.display_name,
                right_energy_label=right.display_name,
                interaction_label=f"{left.display_name} → {right.display_name}",
                canonical_meaning_key=interaction_id if defined else None,
                customer_summary_key=(
                    f"{interaction_id}_CUSTOMER" if defined else None
                ),
                customer_title=row["customer_title"] if row else None,
                customer_summary=row["customer_summary"] if row else None,
                priority=row["priority"] if row else None,
                domains=row["domains"] if row else (),
                interpretation_status=(
                    TRIPLE_STATUS_DEFINED if defined else TRIPLE_STATUS_UNDEFINED
                ),
            )
        )
    return tuple(triples)


def build_chain(
    occurrences: tuple[EnergyOccurrence, ...],
    triples: tuple[CustomerTripleOccurrence, ...],
) -> NumberEnergyChainView:
    """Pair-layer chain: frequency primary, last pair/triple as terminal."""
    primary_id, primary_label, primary_pairs = _primary(occurrences)
    secondary = _secondary_labels(occurrences, primary_id)
    last = occurrences[-1] if occurrences else None
    last_triple = triples[-1] if triples else None
    terminal_label = last.display_name if last else None
    summary = None
    if primary_label and terminal_label:
        summary = f"{primary_label} chủ đạo, kết {terminal_label}"
    return NumberEnergyChainView(
        primary_energy_label=primary_label,
        primary_energy_pairs=primary_pairs,
        secondary_energy_labels=secondary,
        terminal_pair_digits=last.pair_digits if last else None,
        terminal_energy_label=terminal_label,
        terminal_triple_digits=last_triple.digits if last_triple else None,
        terminal_interaction_label=(
            last_triple.interaction_label if last_triple else None
        ),
        dominant_flow_summary=summary,
    )


def _interaction_id(source_energy_id: str, target_energy_id: str) -> str | None:
    """Build Knowledge 12 interaction_id from engine energy ids."""
    source = ENERGY_INTERACTION_CODES.get(source_energy_id)
    target = ENERGY_INTERACTION_CODES.get(target_energy_id)
    if source is None or target is None:
        return None
    return f"{source}_TO_{target}"


def _primary(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[str | None, str | None, tuple[str, ...]]:
    """Highest pair frequency, first-seen on ties."""
    if not occurrences:
        return None, None, ()
    counts = Counter(item.energy_id for item in occurrences)
    first_index: dict[str, int] = {}
    for index, item in enumerate(occurrences):
        if item.energy_id not in first_index:
            first_index[item.energy_id] = index
    energy_id = min(counts.keys(), key=lambda key: (-counts[key], first_index[key]))
    sample = next(item for item in occurrences if item.energy_id == energy_id)
    pairs = tuple(
        item.pair_digits for item in occurrences if item.energy_id == energy_id
    )
    return energy_id, sample.display_name, pairs


def _secondary_labels(
    occurrences: tuple[EnergyOccurrence, ...],
    primary_id: str | None,
) -> tuple[str, ...]:
    """Supportive energies present besides primary, catalog order."""
    present = {item.energy_id for item in occurrences}
    labels: list[str] = []
    for energy_id in ENERGY_DISTRIBUTION_ORDER:
        if energy_id == primary_id:
            continue
        if energy_id not in present:
            continue
        if energy_id not in SUPPORTIVE_ENERGY_IDS:
            continue
        labels.append(ENERGY_DISPLAY_NAMES[energy_id])
    return tuple(labels)

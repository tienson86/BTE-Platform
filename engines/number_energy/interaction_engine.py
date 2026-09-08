"""Sequence interactions: repetition, control, approved chain, undefined."""

from __future__ import annotations

from collections import Counter

from engines.number_energy.constants import (
    APPROVED_SUPPORTIVE_CHAIN_ID,
    APPROVED_SUPPORTIVE_CHAIN_SEQUENCE,
    CONTROL_RELATIONS,
    FU_WEI_ID,
    FU_WEI_SUPPORT_ENERGIES,
    HUO_HAI_ID,
)
from engines.number_energy.types import (
    EnergyOccurrence,
    EnergyState,
    ParsedNumber,
    SequenceSummary,
    UndefinedSegment,
)

_MODIFIER_STATES = frozenset(
    {
        EnergyState.HIDDEN.value,
        EnergyState.AMPLIFIED.value,
    }
)


def apply_interactions(
    parsed: ParsedNumber,
    adjacent: tuple[EnergyOccurrence, ...],
    bridged: tuple[EnergyOccurrence, ...],
    undefined: tuple[UndefinedSegment, ...],
) -> tuple[
    tuple[EnergyOccurrence, ...],
    tuple[UndefinedSegment, ...],
    SequenceSummary,
    tuple[str, ...],
    str,
    tuple[str, ...],
]:
    """Apply frozen V1 interaction rules to merged occurrences.

    Returns occurrences, undefined segments, summary, approved patterns,
    primary sequence state, and all sequence states.
    """
    merged = _sort_occurrences((*adjacent, *bridged))
    energy_counts = Counter(item.energy_id for item in merged)
    present = {item.energy_id for item in merged}
    updated: list[EnergyOccurrence] = []
    seen_counts: dict[str, int] = {}

    for item in merged:
        seen_counts[item.energy_id] = seen_counts.get(item.energy_id, 0) + 1
        state, notes = _resolve_occurrence_state(
            item=item,
            seen_count=seen_counts[item.energy_id],
            energy_counts=energy_counts,
            present=present,
        )
        updated.append(
            EnergyOccurrence(
                occurrence_id=item.occurrence_id,
                source_span=item.source_span,
                source_digits=item.source_digits,
                pair_digits=item.pair_digits,
                energy_id=item.energy_id,
                display_name=item.display_name,
                strength_rank=item.strength_rank,
                classification=item.classification,
                state=state,
                via_modifier=item.via_modifier,
                notes=notes,
            )
        )

    occurrences = tuple(updated)
    approved = _approved_patterns(parsed)
    summary = _build_summary(occurrences, present, approved)
    sequence_states, primary = _sequence_states(
        occurrences=occurrences,
        undefined=undefined,
        approved=approved,
    )
    return occurrences, undefined, summary, approved, primary, sequence_states


def _sort_occurrences(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[EnergyOccurrence, ...]:
    """Order by source span, then adjacent before bridged windows."""
    return tuple(
        sorted(
            occurrences,
            key=lambda item: (item.source_span[0], item.source_span[1], item.occurrence_id),
        )
    )


def _resolve_occurrence_state(
    *,
    item: EnergyOccurrence,
    seen_count: int,
    energy_counts: Counter[str],
    present: set[str],
) -> tuple[str, str]:
    """Assign one frozen state without inventing new control relations."""
    notes = [item.notes]
    controller = CONTROL_RELATIONS.get(item.energy_id)
    has_controller = controller is not None and controller in present

    if item.energy_id == HUO_HAI_ID:
        notes.append(
            "Họa Hại needs cát tinh combination; no direct single-pair control in V1"
        )
    if item.energy_id == FU_WEI_ID:
        if present & FU_WEI_SUPPORT_ENERGIES:
            notes.append("Phục Vị is supported by Sinh Khí or Thiên Y")
        else:
            notes.append("Phục Vị alone does not neutralize strong challenging energy")
        notes.append("Phục Vị may prolong whatever energy precedes it")

    if item.state in _MODIFIER_STATES:
        if energy_counts[item.energy_id] > 1:
            notes.append("same energy also repeats in this sequence")
        if has_controller:
            notes.append(
                f"{item.display_name} has a frozen controller present; "
                "modifier state is kept"
            )
        return item.state, "; ".join(notes)

    if has_controller:
        notes.append(
            f"{item.display_name} is CONTROLLED by "
            f"{_display_controller(controller)}"
        )
        if energy_counts[item.energy_id] > 1:
            notes.append("same energy also repeats in this sequence")
        return EnergyState.CONTROLLED.value, "; ".join(notes)

    if energy_counts[item.energy_id] > 1 and seen_count > 1:
        notes.append("same energy appears repeatedly in close sequence")
        return EnergyState.REPEATED.value, "; ".join(notes)

    return item.state, "; ".join(notes)


def _display_controller(energy_id: str | None) -> str:
    """Map controller id to display name used in notes."""
    names = {
        "sheng_qi": "Sinh Khí",
        "tian_yi": "Thiên Y",
        "yan_nian": "Diên Niên",
    }
    return names.get(energy_id or "", energy_id or "")


def _approved_patterns(parsed: ParsedNumber) -> tuple[str, ...]:
    """Recognize only the frozen catalog sequence ``141319``."""
    sequence = "".join(str(digit) for digit in parsed.raw_digits)
    if sequence == APPROVED_SUPPORTIVE_CHAIN_SEQUENCE:
        return (APPROVED_SUPPORTIVE_CHAIN_ID,)
    return ()


def _build_summary(
    occurrences: tuple[EnergyOccurrence, ...],
    present: set[str],
    approved: tuple[str, ...],
) -> SequenceSummary:
    """Aggregate frequency and control without numeric scoring."""
    counts = Counter(item.energy_id for item in occurrences)
    max_count = max(counts.values(), default=0)
    dominant = tuple(
        sorted(energy_id for energy_id, count in counts.items() if count == max_count)
    )
    ranks = [item.strength_rank for item in occurrences if item.strength_rank is not None]
    repeated = tuple(
        sorted(energy_id for energy_id, count in counts.items() if count > 1)
    )
    controlled = tuple(
        sorted(
            {
                item.energy_id
                for item in occurrences
                if item.state == EnergyState.CONTROLLED.value
            }
        )
    )
    challenging = tuple(
        sorted(
            {
                item.energy_id
                for item in occurrences
                if item.classification == "challenging"
                and item.energy_id not in controlled
                and CONTROL_RELATIONS.get(item.energy_id) not in present
            }
        )
    )
    return SequenceSummary(
        dominant_energy_ids=dominant,
        strongest_rank=min(ranks) if ranks else None,
        repeated_energy_ids=repeated,
        controlled_energy_ids=controlled,
        challenging_without_control=challenging,
        fu_wei_supported=FU_WEI_ID in present
        and bool(present & FU_WEI_SUPPORT_ENERGIES),
        approved_supportive_chain=APPROVED_SUPPORTIVE_CHAIN_ID in approved,
    )


def _sequence_states(
    *,
    occurrences: tuple[EnergyOccurrence, ...],
    undefined: tuple[UndefinedSegment, ...],
    approved: tuple[str, ...],
) -> tuple[tuple[str, ...], str]:
    """Choose sequence-level states. Undefined V1 spans win as primary."""
    states: list[str] = []
    if undefined:
        states.append(EnergyState.UNKNOWN_OR_NOT_DEFINED.value)
    occ_states = [item.state for item in occurrences]
    for candidate in (
        EnergyState.CONTROLLED.value,
        EnergyState.REPEATED.value,
        EnergyState.HIDDEN.value,
        EnergyState.AMPLIFIED.value,
        EnergyState.NORMAL.value,
    ):
        if candidate in occ_states:
            states.append(candidate)
    if approved and EnergyState.REPEATED.value not in states and occurrences:
        states.append(EnergyState.REPEATED.value)
    if not states:
        states.append(EnergyState.UNKNOWN_OR_NOT_DEFINED.value)
    unique = tuple(dict.fromkeys(states))
    return unique, unique[0]

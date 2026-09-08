"""Layer 4: A-0-B and A-5-B underlying pairs."""

from __future__ import annotations

from engines.number_energy.constants import (
    CONSECUTIVE_MODIFIER_REASON,
    ENERGY_CLASSIFICATION,
    ENERGY_DISPLAY_NAMES,
    UNKNOWN_REASON_NOT_FROZEN,
    UNUSED_MODIFIER_REASON,
    is_modifier,
    is_ordinary_gua,
)
from engines.number_energy.pair_engine import resolve_pair
from engines.number_energy.types import (
    EnergyOccurrence,
    EnergyState,
    ParsedNumber,
    UndefinedSegment,
)


def generate_modifier_pairs(
    parsed: ParsedNumber,
) -> tuple[tuple[EnergyOccurrence, ...], tuple[UndefinedSegment, ...]]:
    """Generate HIDDEN/AMPLIFIED occurrences from frozen A-M-B windows.

    Consecutive modifiers and unused edge modifiers are not frozen in V1.
    """
    digits = parsed.raw_digits
    occurrences: list[EnergyOccurrence] = []
    undefined: list[UndefinedSegment] = []
    used_modifiers: set[int] = set()
    occ_index = 0

    undefined.extend(_consecutive_modifier_segments(digits))

    for start in range(len(digits) - 2):
        left, modifier, right = digits[start], digits[start + 1], digits[start + 2]
        if not (
            is_ordinary_gua(left)
            and is_modifier(modifier)
            and is_ordinary_gua(right)
        ):
            continue
        if is_modifier(digits[start + 1]) and _touches_consecutive_modifiers(
            digits, start + 1
        ):
            continue
        resolved = resolve_pair(left, right)
        source_digits = f"{left}{modifier}{right}"
        span = (start, start + 2)
        if resolved is None:
            undefined.append(
                UndefinedSegment(
                    source_span=span,
                    source_digits=source_digits,
                    state=EnergyState.UNKNOWN_OR_NOT_DEFINED.value,
                    reason=UNKNOWN_REASON_NOT_FROZEN,
                )
            )
            continue
        energy_id, rank = resolved
        state = (
            EnergyState.HIDDEN.value
            if modifier == 0
            else EnergyState.AMPLIFIED.value
        )
        note = (
            "underlying pair hidden or attenuated by 0"
            if modifier == 0
            else "underlying pair activated or amplified by 5"
        )
        occurrences.append(
            EnergyOccurrence(
                occurrence_id=f"mod-{occ_index:03d}",
                source_span=span,
                source_digits=source_digits,
                pair_digits=f"{left}{right}",
                energy_id=energy_id,
                display_name=ENERGY_DISPLAY_NAMES[energy_id],
                strength_rank=rank,
                classification=ENERGY_CLASSIFICATION[energy_id],
                state=state,
                via_modifier=modifier,
                notes=note,
            )
        )
        used_modifiers.add(start + 1)
        occ_index += 1

    undefined.extend(_unused_modifier_segments(digits, used_modifiers))
    return tuple(occurrences), tuple(undefined)


def _touches_consecutive_modifiers(digits: tuple[int, ...], index: int) -> bool:
    """Return True if the modifier at ``index`` sits next to another modifier."""
    if index > 0 and is_modifier(digits[index - 1]):
        return True
    if index + 1 < len(digits) and is_modifier(digits[index + 1]):
        return True
    return False


def _consecutive_modifier_segments(
    digits: tuple[int, ...],
) -> list[UndefinedSegment]:
    """Flag consecutive 0/5 runs as not frozen in V1."""
    segments: list[UndefinedSegment] = []
    index = 0
    while index < len(digits):
        if not is_modifier(digits[index]):
            index += 1
            continue
        end = index
        while end + 1 < len(digits) and is_modifier(digits[end + 1]):
            end += 1
        if end > index:
            source = "".join(str(digits[pos]) for pos in range(index, end + 1))
            segments.append(
                UndefinedSegment(
                    source_span=(index, end),
                    source_digits=source,
                    state=EnergyState.UNKNOWN_OR_NOT_DEFINED.value,
                    reason=CONSECUTIVE_MODIFIER_REASON,
                )
            )
        index = end + 1
    return segments


def _unused_modifier_segments(
    digits: tuple[int, ...],
    used_modifiers: set[int],
) -> list[UndefinedSegment]:
    """Flag 0/5 that do not sit in a frozen A-M-B window."""
    segments: list[UndefinedSegment] = []
    index = 0
    while index < len(digits):
        if not is_modifier(digits[index]) or index in used_modifiers:
            index += 1
            continue
        if _touches_consecutive_modifiers(digits, index):
            index += 1
            continue
        segments.append(
            UndefinedSegment(
                source_span=(index, index),
                source_digits=str(digits[index]),
                state=EnergyState.UNKNOWN_OR_NOT_DEFINED.value,
                reason=UNUSED_MODIFIER_REASON,
            )
        )
        index += 1
    return segments

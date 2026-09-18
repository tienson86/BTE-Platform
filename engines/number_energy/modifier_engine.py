"""Layer 4: zero/five-modified underlying pairs."""

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

    # A-0-5-B is one customer-visible chain. Resolve it before three-digit
    # windows so both modifier positions stay attached to the underlying pair.
    for start in range(len(digits) - 3):
        left, zero, five, right = digits[start : start + 4]
        if not (
            is_ordinary_gua(left)
            and zero == 0
            and five == 5
            and is_ordinary_gua(right)
        ):
            continue
        resolved = resolve_pair(left, right)
        if resolved is None:
            continue
        energy_id, rank = resolved
        occurrences.append(
            EnergyOccurrence(
                occurrence_id=f"mod-{occ_index:03d}",
                source_span=(start, start + 3),
                source_digits=f"{left}05{right}",
                pair_digits=f"{left}{right}",
                energy_id=energy_id,
                display_name=ENERGY_DISPLAY_NAMES[energy_id],
                strength_rank=rank,
                classification=ENERGY_CLASSIFICATION[energy_id],
                state=EnergyState.HIDDEN.value,
                via_modifier=0,
                notes="underlying pair hidden by 0 then exposed and extended by 5",
            )
        )
        used_modifiers.update({start + 1, start + 2})
        occ_index += 1

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

    for start in range(len(digits) - 2):
        left, right, modifier = digits[start], digits[start + 1], digits[start + 2]
        if not (
            is_ordinary_gua(left)
            and is_ordinary_gua(right)
            and is_modifier(modifier)
        ):
            continue

        modifier_digits = (modifier,)
        source_digits = f"{left}{right}{modifier}"
        span = (start, start + 2)
        if (
            modifier == 0
            and start + 3 < len(digits)
            and digits[start + 3] == 5
        ):
            modifier_digits = (0, 5)
            source_digits += "5"
            span = (start, start + 3)
        elif _touches_consecutive_modifiers(digits, start + 2):
            continue

        resolved = resolve_pair(left, right)
        if resolved is None:
            continue
        energy_id, rank = resolved
        state = (
            EnergyState.HIDDEN.value
            if modifier_digits[0] == 0
            else EnergyState.AMPLIFIED.value
        )
        occurrences.append(
            EnergyOccurrence(
                occurrence_id=f"post-{occ_index:03d}",
                source_span=span,
                source_digits=source_digits,
                pair_digits=f"{left}{right}",
                energy_id=energy_id,
                display_name=ENERGY_DISPLAY_NAMES[energy_id],
                strength_rank=rank,
                classification=ENERGY_CLASSIFICATION[energy_id],
                state=state,
                via_modifier=modifier_digits[0],
                notes="formed energy modified from the trailing position",
            )
        )
        used_modifiers.update(range(start + 2, span[1] + 1))
        occ_index += 1

    undefined.extend(_consecutive_modifier_segments(digits, used_modifiers))
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
    used_modifiers: set[int],
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
            if all(pos in used_modifiers for pos in range(index, end + 1)):
                index = end + 1
                continue
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

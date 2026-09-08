"""Layer 3: adjacent ordinary gua pairs -> NORMAL Du Niên occurrences."""

from __future__ import annotations

from engines.number_energy.constants import (
    ENERGY_CLASSIFICATION,
    ENERGY_DISPLAY_NAMES,
    LINE_DIFF_TO_ENERGY,
    LINE_ORDER,
    PAIR_LOOKUP,
    TRIGRAM_VECTORS,
    UNKNOWN_REASON_NOT_FROZEN,
    is_ordinary_gua,
)
from engines.number_energy.types import (
    EnergyOccurrence,
    EnergyState,
    ParsedNumber,
    UndefinedSegment,
)


def derive_energy_id(left: int, right: int) -> str | None:
    """Derive Du Niên energy from frozen line-difference vectors.

    Returns ``None`` when a digit is not an ordinary gua (including 0 and 5).
    """
    if left not in TRIGRAM_VECTORS or right not in TRIGRAM_VECTORS:
        return None
    left_vector = TRIGRAM_VECTORS[left]
    right_vector = TRIGRAM_VECTORS[right]
    changed = frozenset(
        LINE_ORDER[index]
        for index in range(3)
        if left_vector[index] != right_vector[index]
    )
    return LINE_DIFF_TO_ENERGY[changed]


def resolve_pair(left: int, right: int) -> tuple[str, int] | None:
    """Derive energy by line difference, then validate against the pair table."""
    energy_id = derive_energy_id(left, right)
    if energy_id is None:
        return None
    pair_digits = f"{left}{right}"
    table = PAIR_LOOKUP.get(pair_digits)
    if table is None:
        return None
    table_energy, rank = table
    if table_energy != energy_id:
        return None
    return energy_id, rank


def generate_adjacent_pairs(
    parsed: ParsedNumber,
) -> tuple[tuple[EnergyOccurrence, ...], tuple[UndefinedSegment, ...]]:
    """Generate NORMAL occurrences for every adjacent ordinary gua pair.

    Pairs involving ``0`` or ``5`` are skipped; they are never ordinary
    Du Niên pair digits in V1.
    """
    digits = parsed.raw_digits
    occurrences: list[EnergyOccurrence] = []
    undefined: list[UndefinedSegment] = []
    occ_index = 0
    for start in range(len(digits) - 1):
        left = digits[start]
        right = digits[start + 1]
        if not (is_ordinary_gua(left) and is_ordinary_gua(right)):
            continue
        resolved = resolve_pair(left, right)
        source_digits = f"{left}{right}"
        span = (start, start + 1)
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
        occurrences.append(
            EnergyOccurrence(
                occurrence_id=f"adj-{occ_index:03d}",
                source_span=span,
                source_digits=source_digits,
                pair_digits=source_digits,
                energy_id=energy_id,
                display_name=ENERGY_DISPLAY_NAMES[energy_id],
                strength_rank=rank,
                classification=ENERGY_CLASSIFICATION[energy_id],
                state=EnergyState.NORMAL.value,
                via_modifier=None,
                notes="adjacent ordinary pair",
            )
        )
        occ_index += 1
    return tuple(occurrences), tuple(undefined)

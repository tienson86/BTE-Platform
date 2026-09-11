"""Customer reading payload. Presentation only; no new pair or score rules."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from engines.number_energy.catalog import ENERGY_CATALOG
from engines.number_energy.constants import (
    CHALLENGING_ENERGY_IDS,
    ENERGY_DISPLAY_NAMES,
    FORCE_LABELS,
    INCOMPLETE_CUSTOMER_NOTICE,
    PHONE_CCCD_NOTE,
    PHONE_CONSECUTIVE_CHALLENGING,
    PHONE_CONSECUTIVE_CHALLENGING_SOFT,
    PHONE_ENDING_CHALLENGING,
    PHONE_ENDING_SUPPORTIVE,
    PHONE_ENDING_UNKNOWN,
    PHONE_FORCE_SHORT,
    PHONE_FORCE_WINS,
    PHONE_INTERIOR_ZERO_NOTE,
    PHONE_LEADING_ZERO_NOTE,
    PHONE_LIFTED_NOTE,
    PHONE_PURPOSE_NOTE,
    PHONE_SUPPORTIVE_BALANCED,
    PHONE_SUPPORTIVE_FEW,
    PHONE_SUPPORTIVE_SKEWED,
    STATE_CUSTOMER_LABELS,
    SUPPORTIVE_ENERGY_IDS,
    SUPPORTIVE_THEME_SHORT,
    UNDEFINED_REASON_CUSTOMER_VI,
)
from engines.number_energy.phone_input import has_interior_zero
from engines.number_energy.types import (
    EnergyOccurrence,
    NumberEnergyResult,
    PurposeContext,
    UndefinedSegment,
)


def qi_force(rank: int | None) -> int:
    """Map frozen rank 1–4 to internal force 4–1. Rank 1 is strongest."""
    if rank is None or rank < 1 or rank > 4:
        return 0
    return 5 - rank


def build_reading(result: NumberEnergyResult) -> dict[str, Any]:
    """Build the customer-facing reading object for UI rendering."""
    is_phone = result.purpose_context == PurposeContext.PHONE_NUMBER.value
    occurrences = result.occurrences
    pairs = [_pair_payload(item) for item in occurrences]
    groups = _group_payloads(occurrences)
    triplets = _triplet_payloads(occurrences)
    dominant = _dominant_payload(occurrences, result.summary.dominant_energy_ids)
    ending = _ending_payload(occurrences)
    supportive_ids = _present_ids(occurrences, SUPPORTIVE_ENERGY_IDS)
    challenging_ids = _present_ids(occurrences, CHALLENGING_ENERGY_IDS)
    supportive_count = len(supportive_ids)
    notices = _incomplete_notices(result.undefined_segments)
    interior_zero = is_phone and has_interior_zero(result.analyzed_input)
    if interior_zero:
        notices.append(PHONE_INTERIOR_ZERO_NOTE)
    balance_note = _supportive_balance_note(occurrences, supportive_count)
    consecutive_note = _consecutive_challenging_note(occurrences, is_phone)
    lifted = _lifted_pairs(occurrences) if is_phone else []
    force_notes = _force_notes(lifted) if is_phone else []
    if consecutive_note:
        notices.append(consecutive_note)
    notices.extend(force_notes)
    summary = (
        _phone_summary(
            result=result,
            dominant=dominant,
            supportive_ids=supportive_ids,
            lifted=lifted,
            interior_zero=interior_zero,
        )
        if is_phone
        else result.narrative.summary
    )
    return {
        "layout": "phone" if is_phone else "generic",
        "version": "1.1" if is_phone else "1.0",
        "display_number": result.input_raw,
        "analyzed_number": result.analyzed_input,
        "leading_zero": result.leading_phone_zero,
        "leading_zero_note": PHONE_LEADING_ZERO_NOTE if result.leading_phone_zero else None,
        "interior_zero_note": PHONE_INTERIOR_ZERO_NOTE if interior_zero else None,
        "pairs": pairs,
        "groups": groups,
        "triplets": triplets,
        "dominant": dominant,
        "ending": ending,
        "supportive_group_count": supportive_count,
        "challenging_group_count": len(challenging_ids),
        "supportive_balance_note": balance_note,
        "consecutive_challenging_note": consecutive_note,
        "lifted": bool(lifted),
        "lifted_note": PHONE_LIFTED_NOTE if lifted else None,
        "force_notes": force_notes,
        "summary": summary,
        "notices": notices,
        "purpose_note": PHONE_PURPOSE_NOTE if is_phone else result.narrative.purpose_focus,
        "cccd_note": PHONE_CCCD_NOTE if is_phone else None,
        "incomplete": bool(result.undefined_segments) or not occurrences,
    }


def _pair_payload(item: EnergyOccurrence) -> dict[str, Any]:
    """Customer pair chip: digits, name, Vietnamese expression, force label."""
    expression = STATE_CUSTOMER_LABELS.get(item.state, "")
    rank = item.strength_rank
    return {
        "pair_digits": item.pair_digits,
        "display_name": item.display_name,
        "energy_id": item.energy_id,
        "kind": "challenging" if item.energy_id in CHALLENGING_ENERGY_IDS else "supportive",
        "expression": expression,
        "force_label": FORCE_LABELS.get(rank or 0, ""),
        "force_level": qi_force(rank),
    }


def _group_payloads(occurrences: tuple[EnergyOccurrence, ...]) -> list[dict[str, Any]]:
    """Group pairs by energy, ordered by frequency then first seen."""
    first_index: dict[str, int] = {}
    pair_map: dict[str, list[str]] = defaultdict(list)
    for index, item in enumerate(occurrences):
        if item.energy_id not in first_index:
            first_index[item.energy_id] = index
        pair_map[item.energy_id].append(item.pair_digits)
    counts = Counter(item.energy_id for item in occurrences)
    ordered = sorted(
        counts.keys(),
        key=lambda energy_id: (-counts[energy_id], first_index[energy_id]),
    )
    groups: list[dict[str, Any]] = []
    for energy_id in ordered:
        catalog = ENERGY_CATALOG[energy_id]
        sample = next(item for item in occurrences if item.energy_id == energy_id)
        groups.append(
            {
                "energy_id": energy_id,
                "display_name": sample.display_name,
                "pairs": pair_map[energy_id],
                "meaning": catalog["customer_summary"],
                "strength": catalog["customer_summary"],
                "watchout": f"{catalog['shadow']}; {catalog['excessive_effect']}",
                "kind": (
                    "challenging"
                    if energy_id in CHALLENGING_ENERGY_IDS
                    else "supportive"
                ),
            }
        )
    return groups


def _triplet_payloads(occurrences: tuple[EnergyOccurrence, ...]) -> list[dict[str, Any]]:
    """Join two adjacent overlapping pairs into a 3-digit presentation window."""
    triplets: list[dict[str, Any]] = []
    for left, right in zip(occurrences, occurrences[1:]):
        if left.pair_digits[1:] != right.pair_digits[:1]:
            continue
        digits = left.pair_digits[0] + right.pair_digits
        triplets.append(
            {
                "digits": digits,
                "left_name": left.display_name,
                "right_name": right.display_name,
                "left_pair": left.pair_digits,
                "right_pair": right.pair_digits,
            }
        )
    return triplets


def _dominant_payload(
    occurrences: tuple[EnergyOccurrence, ...],
    dominant_ids: tuple[str, ...],
) -> dict[str, Any] | None:
    """Pick the highest-frequency energy without numeric scoring."""
    if not occurrences or not dominant_ids:
        return None
    energy_id = dominant_ids[0]
    sample = next(
        (item for item in occurrences if item.energy_id == energy_id),
        occurrences[0],
    )
    pairs = [item.pair_digits for item in occurrences if item.energy_id == energy_id]
    return {
        "energy_id": energy_id,
        "display_name": sample.display_name,
        "pairs": pairs,
        "count": len(pairs),
    }


def _ending_payload(occurrences: tuple[EnergyOccurrence, ...]) -> dict[str, Any]:
    """Last occurrence is the ending energy (năng lượng kết / bộ số cuối)."""
    if not occurrences:
        return {
            "pair_digits": None,
            "display_name": None,
            "kind": "unknown",
            "note": PHONE_ENDING_UNKNOWN,
        }
    last = occurrences[-1]
    if last.energy_id in CHALLENGING_ENERGY_IDS:
        kind = "challenging"
        note = PHONE_ENDING_CHALLENGING
    elif last.energy_id in SUPPORTIVE_ENERGY_IDS:
        kind = "supportive"
        note = PHONE_ENDING_SUPPORTIVE
    else:
        kind = "unknown"
        note = PHONE_ENDING_UNKNOWN
    return {
        "pair_digits": last.pair_digits,
        "display_name": last.display_name,
        "kind": kind,
        "note": note,
    }


def _present_ids(
    occurrences: tuple[EnergyOccurrence, ...],
    allowed: frozenset[str],
) -> list[str]:
    """Unique energy ids from ``allowed``, first-seen order."""
    seen: list[str] = []
    for item in occurrences:
        if item.energy_id in allowed and item.energy_id not in seen:
            seen.append(item.energy_id)
    return seen


def _supportive_balance_note(
    occurrences: tuple[EnergyOccurrence, ...],
    supportive_count: int,
) -> str:
    """Comment on 2–3 supportive groups without turning it into a score."""
    if supportive_count < 2:
        return PHONE_SUPPORTIVE_FEW
    supportive = [item for item in occurrences if item.energy_id in SUPPORTIVE_ENERGY_IDS]
    counts = Counter(item.energy_id for item in supportive)
    ranked = counts.most_common()
    if len(ranked) >= 2 and ranked[0][1] >= 3 and ranked[0][1] >= 2 * ranked[1][1]:
        return PHONE_SUPPORTIVE_SKEWED
    if supportive_count >= 2:
        return PHONE_SUPPORTIVE_BALANCED
    return PHONE_SUPPORTIVE_FEW


def _consecutive_challenging_note(
    occurrences: tuple[EnergyOccurrence, ...],
    is_phone: bool,
) -> str | None:
    """Warn when more than two challenging energies stand in a row."""
    if not is_phone:
        return None
    longest = 0
    run = 0
    for item in occurrences:
        if item.energy_id in CHALLENGING_ENERGY_IDS:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    if longest <= 2:
        return None
    if _total_force(occurrences, SUPPORTIVE_ENERGY_IDS) > _total_force(
        occurrences, CHALLENGING_ENERGY_IDS
    ):
        return PHONE_CONSECUTIVE_CHALLENGING_SOFT
    return PHONE_CONSECUTIVE_CHALLENGING


def _total_force(
    occurrences: tuple[EnergyOccurrence, ...],
    allowed: frozenset[str],
) -> int:
    """Sum internal qi force for a class. Never shown to customers."""
    return sum(
        qi_force(item.strength_rank)
        for item in occurrences
        if item.energy_id in allowed
    )


def _lifted_pairs(
    occurrences: tuple[EnergyOccurrence, ...],
) -> list[tuple[EnergyOccurrence, EnergyOccurrence]]:
    """Challenging energy with a supportive energy immediately to the right."""
    lifted: list[tuple[EnergyOccurrence, EnergyOccurrence]] = []
    for left, right in zip(occurrences, occurrences[1:]):
        if (
            left.energy_id in CHALLENGING_ENERGY_IDS
            and right.energy_id in SUPPORTIVE_ENERGY_IDS
        ):
            lifted.append((left, right))
    return lifted


def _force_notes(
    lifted: list[tuple[EnergyOccurrence, EnergyOccurrence]],
) -> list[str]:
    """Compare adjacent cát/hung force without exposing rank numbers."""
    notes: list[str] = []
    seen: set[str] = set()
    for left, right in lifted:
        wins = qi_force(right.strength_rank) > qi_force(left.strength_rank)
        text = PHONE_FORCE_WINS if wins else PHONE_FORCE_SHORT
        if text not in seen:
            seen.add(text)
            notes.append(text)
    return notes


def _incomplete_notices(undefined: tuple[UndefinedSegment, ...]) -> list[str]:
    """Vietnamese incomplete notices; never emit raw engine tokens."""
    if not undefined:
        return []
    details = "; ".join(
        UNDEFINED_REASON_CUSTOMER_VI.get(item.reason, INCOMPLETE_CUSTOMER_NOTICE)
        for item in undefined
    )
    return [f"{INCOMPLETE_CUSTOMER_NOTICE} {details}".strip()]


def _phone_summary(
    *,
    result: NumberEnergyResult,
    dominant: dict[str, Any] | None,
    supportive_ids: list[str],
    lifted: list[tuple[EnergyOccurrence, EnergyOccurrence]],
    interior_zero: bool,
) -> str:
    """Compose the phone-number customer summary paragraph."""
    parts: list[str] = []
    if result.leading_phone_zero:
        parts.append(PHONE_LEADING_ZERO_NOTE)
    if interior_zero:
        parts.append(PHONE_INTERIOR_ZERO_NOTE)
    if dominant:
        others = [
            ENERGY_DISPLAY_NAMES[energy_id]
            for energy_id in supportive_ids
            if energy_id != dominant["energy_id"]
        ]
        theme_ids = [dominant["energy_id"], *[
            energy_id
            for energy_id in supportive_ids
            if energy_id != dominant["energy_id"]
        ]]
        themes = _theme_clause(theme_ids)
        lead = f"Phần thân số nghiêng mạnh về {dominant['display_name']}"
        if others:
            lead += f", đi cùng {' và '.join(others)}"
        lead += f", nên thiên về {themes}."
        parts.append(lead)
    elif result.occurrences:
        names = _unique_names(result.occurrences)
        parts.append(f"Dãy này xuất hiện các trường khí: {names}.")
    else:
        parts.append(INCOMPLETE_CUSTOMER_NOTICE)
    first_challenging = next(
        (
            item
            for item in result.occurrences
            if item.energy_id in CHALLENGING_ENERGY_IDS
        ),
        None,
    )
    if first_challenging and lifted:
        support_name = lifted[0][1].display_name
        place = (
            "ở đầu phần thân số"
            if first_challenging is result.occurrences[0]
            else "ở phần thân số"
        )
        parts.append(
            f"Điểm cần lưu ý là {first_challenging.display_name} xuất hiện "
            f"{place}; tuy nhiên phía sau có {support_name} nâng đỡ "
            "nên ảnh hưởng được làm mềm hơn."
        )
    elif first_challenging:
        parts.append(
            f"Điểm cần lưu ý là {first_challenging.display_name} xuất hiện "
            "trong dãy, thuộc nhóm trường khí cần kiểm soát."
        )
    return " ".join(parts)


def _theme_clause(energy_ids: list[str]) -> str:
    """Join short supportive themes in first-seen order."""
    phrases: list[str] = []
    for energy_id in energy_ids:
        text = SUPPORTIVE_THEME_SHORT.get(energy_id)
        if text and text not in phrases:
            phrases.append(text)
    if not phrases:
        return "trường khí nội tại của dãy số"
    if len(phrases) == 1:
        return phrases[0]
    flat: list[str] = []
    for item in phrases:
        flat.extend(part.strip() for part in item.split(",") if part.strip())
    if len(flat) == 1:
        return flat[0]
    return ", ".join(flat[:-1]) + " và " + flat[-1]


def _unique_names(occurrences: tuple[EnergyOccurrence, ...]) -> str:
    """Join unique display names in first-seen order."""
    names: list[str] = []
    for item in occurrences:
        if item.display_name not in names:
            names.append(item.display_name)
    return ", ".join(names)

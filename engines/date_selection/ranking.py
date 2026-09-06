"""Personalized ranking for Date Selection.

Eligibility decides membership. Ranking only decides order.
"""

from __future__ import annotations

from engines.date_selection.constants import (
    DAY_RANK_SCORE,
    DIVERSITY_ORDER,
    POSITIVE_DAY_CODES,
    POSITIVE_KE_CODES,
    REJECT_DAY_CODES,
)
from engines.date_selection.models import (
    DaySelection,
    HourRecommendation,
    RankedDate,
)

EXCLUSION_INCOMPATIBLE_TRACH = "incompatible_trach"
EXCLUSION_BAD_LIU_REN = "bad_liu_ren_state"
EXCLUSION_NO_POSITIVE_KE = "no_positive_ke"


def _hour_recommendations(day: DaySelection, person_trach: str) -> list[HourRecommendation]:
    """Collect every positive khắc on same-Trạch hours. Does not pick a single winner."""
    results: list[HourRecommendation] = []
    for hour in day.hours:
        if hour.trach is None or hour.trach.trach_group_code != person_trach:
            continue
        for slot in hour.ke_slots:
            if slot.six_state.code not in POSITIVE_KE_CODES:
                continue
            results.append(
                HourRecommendation(
                    branch=hour.window.branch,
                    time_range=slot.time_range,
                    ke_index=slot.ke_index,
                    classification=slot.six_state.label,
                    primary=False,
                )
            )
    return results


def is_candidate_day(day: DaySelection, person_trach: str) -> bool:
    """True when the day matches personal trạch and a primary positive class."""
    if day.trach is None or day.trach.trach_group_code != person_trach:
        return False
    if day.six_state.code in REJECT_DAY_CODES:
        return False
    return day.six_state.code in POSITIVE_DAY_CODES


def exclusion_reason(day: DaySelection, person_trach: str) -> str | None:
    """Return a frozen exclusion code, or None when the day is eligible.

    Codes:
    - incompatible_trach
    - bad_liu_ren_state
    - no_positive_ke  (existing frozen same-Trạch positive-khắc rule)
    """
    if day.trach is None or day.trach.trach_group_code != person_trach:
        return EXCLUSION_INCOMPATIBLE_TRACH
    if day.six_state.code in REJECT_DAY_CODES or day.six_state.code not in POSITIVE_DAY_CODES:
        return EXCLUSION_BAD_LIU_REN
    if not _hour_recommendations(day, person_trach):
        return EXCLUSION_NO_POSITIVE_KE
    return None
    """Return a frozen exclusion code, or None when the day is eligible.

    Codes:
    - incompatible_trach
    - bad_liu_ren_state
    - no_positive_ke  (existing frozen same-Trạch positive-khắc rule)
    """
    if day.trach is None or day.trach.trach_group_code != person_trach:
        return EXCLUSION_INCOMPATIBLE_TRACH
    if day.six_state.code in REJECT_DAY_CODES or day.six_state.code not in POSITIVE_DAY_CODES:
        return EXCLUSION_BAD_LIU_REN
    if not _hour_recommendations(day, person_trach):
        return EXCLUSION_NO_POSITIVE_KE
    return None


def eligible_dates(days: list[DaySelection], person_trach: str) -> list[RankedDate]:
    """Return every date that passes mandatory selection conditions."""
    selected: list[RankedDate] = []
    for day in days:
        if exclusion_reason(day, person_trach) is not None:
            continue
        selected.append(
            RankedDate(day=day, recommendations=_hour_recommendations(day, person_trach))
        )
    return selected


def rank_dates(days: list[DaySelection], person_trach: str) -> list[RankedDate]:
    """Order all eligible dates. Does not drop a qualifying date.

    Diversity prefers one Đại An, one Tiểu Cát, and one Tốc Hỷ near the top
    when those classes exist. Remaining eligible dates follow by score then day.
    """
    eligible = eligible_dates(days, person_trach)
    scored = sorted(
        eligible,
        key=lambda ranked: (
            -DAY_RANK_SCORE.get(ranked.day.six_state.code, 0),
            ranked.day.calendar.solar_day,
        ),
    )
    ordered: list[RankedDate] = []
    for code in DIVERSITY_ORDER:
        for ranked in scored:
            if ranked.day.six_state.code != code:
                continue
            if _already_selected(ordered, ranked):
                continue
            ordered.append(ranked)
            break
    for ranked in scored:
        if _already_selected(ordered, ranked):
            continue
        ordered.append(ranked)
    if len(ordered) != len(eligible):
        raise RuntimeError("ranking changed eligible membership")
    return ordered


def _already_selected(selected: list[RankedDate], ranked: RankedDate) -> bool:
    return any(
        item.day.calendar.solar_day == ranked.day.calendar.solar_day
        for item in selected
    )

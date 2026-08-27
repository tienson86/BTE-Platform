"""Personalized Top-N ranking for Date Selection."""

from __future__ import annotations

from engines.date_selection.constants import (
    DAY_RANK_SCORE,
    DIVERSITY_ORDER,
    KE_RANK_SCORE,
    MAX_RANKED_DATES,
    POSITIVE_DAY_CODES,
    POSITIVE_KE_CODES,
    REJECT_DAY_CODES,
    REJECT_KE_CODES,
)
from engines.date_selection.models import (
    DaySelection,
    HourRecommendation,
    RankedDate,
)


def _hour_recommendations(day: DaySelection, person_trach: str) -> list[HourRecommendation]:
    picked: list[tuple[int, HourRecommendation]] = []
    for hour in day.hours:
        if hour.trach is None or hour.trach.trach_group_code != person_trach:
            continue
        for slot in hour.ke_slots:
            if slot.six_state.code in REJECT_KE_CODES:
                continue
            score = KE_RANK_SCORE.get(slot.six_state.code, 0)
            if slot.six_state.code not in POSITIVE_KE_CODES and score <= 0:
                continue
            picked.append(
                (
                    score,
                    HourRecommendation(
                        branch=hour.window.branch,
                        time_range=slot.time_range,
                        ke_index=slot.ke_index,
                        classification=slot.six_state.label,
                        primary=False,
                    ),
                )
            )
    picked.sort(key=lambda item: (-item[0], item[1].ke_index, item[1].branch))
    results = [item[1] for item in picked]
    if results:
        results[0].primary = True
    return results[:4]


def is_candidate_day(day: DaySelection, person_trach: str) -> bool:
    """True when the day matches personal trạch and a primary positive class."""
    if day.trach is None or day.trach.trach_group_code != person_trach:
        return False
    if day.six_state.code in REJECT_DAY_CODES:
        return False
    return day.six_state.code in POSITIVE_DAY_CODES


def rank_dates(days: list[DaySelection], person_trach: str) -> list[RankedDate]:
    """
    Return up to five diverse high-quality dates.

    Does not pad to five when fewer valid dates exist.
    Prefers a mix of Đại An, Tiểu Cát, and Tốc Hỷ when available.
    """
    scored: list[tuple[int, RankedDate]] = []
    for day in days:
        if not is_candidate_day(day, person_trach):
            continue
        recs = _hour_recommendations(day, person_trach)
        if not recs:
            continue
        score = DAY_RANK_SCORE.get(day.six_state.code, 0)
        scored.append((score, RankedDate(day=day, recommendations=recs)))

    scored.sort(
        key=lambda item: (
            -item[0],
            item[1].day.calendar.solar_day,
        )
    )

    selected: list[RankedDate] = []
    used_codes: set[str] = set()
    for code in DIVERSITY_ORDER:
        for score, ranked in scored:
            if ranked.day.six_state.code != code:
                continue
            if any(
                item.day.calendar.solar_day == ranked.day.calendar.solar_day
                for item in selected
            ):
                continue
            selected.append(ranked)
            used_codes.add(code)
            break
        if len(selected) >= MAX_RANKED_DATES:
            return selected[:MAX_RANKED_DATES]

    for _score, ranked in scored:
        if len(selected) >= MAX_RANKED_DATES:
            break
        if any(
            item.day.calendar.solar_day == ranked.day.calendar.solar_day
            for item in selected
        ):
            continue
        selected.append(ranked)
    return selected[:MAX_RANKED_DATES]

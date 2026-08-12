"""Life stage entry rules — frozen for Product Context V1.0."""

from __future__ import annotations

from datetime import date

from applications.production.product_context.models import LifeStage, ProductContextInput


def compute_age(
    *,
    birth_year: int,
    birth_month: int = 1,
    birth_day: int = 1,
    as_of: date | None = None,
) -> int:
    """Compute integer age from birth date."""
    as_of = as_of or date.today()
    years = as_of.year - birth_year
    if (as_of.month, as_of.day) < (birth_month, birth_day):
        years -= 1
    return max(0, years)


def resolve_life_stage(data: ProductContextInput) -> tuple[LifeStage, int | None]:
    """
    Resolve life stage.

    Entry rules (age in completed years):
    - CHILD:        0–12
    - TEEN:        13–17
    - YOUNG_ADULT: 18–24
    - ADULT:       25–44
    - MID_CAREER:  45–59
    - SENIOR:      60+

    Explicit life_stage on input wins when provided.
    """
    if data.life_stage is not None:
        age = data.subject_age
        if age is None and data.birth_year is not None:
            as_of = _as_of(data)
            age = compute_age(
                birth_year=data.birth_year,
                birth_month=data.birth_month or 1,
                birth_day=data.birth_day or 1,
                as_of=as_of,
            )
        return data.life_stage, age

    age = data.subject_age
    if age is None:
        if data.birth_year is None:
            # Unknown age → treat as adult for commercial default (safe for CASE-0001/0002).
            return LifeStage.ADULT, None
        as_of = _as_of(data)
        age = compute_age(
            birth_year=data.birth_year,
            birth_month=data.birth_month or 1,
            birth_day=data.birth_day or 1,
            as_of=as_of,
        )

    if age <= 12:
        return LifeStage.CHILD, age
    if age <= 17:
        return LifeStage.TEEN, age
    if age <= 24:
        return LifeStage.YOUNG_ADULT, age
    if age <= 44:
        return LifeStage.ADULT, age
    if age <= 59:
        return LifeStage.MID_CAREER, age
    return LifeStage.SENIOR, age


def _as_of(data: ProductContextInput) -> date:
    if data.as_of_year is not None:
        return date(
            data.as_of_year,
            data.as_of_month or 1,
            data.as_of_day or 1,
        )
    return date.today()

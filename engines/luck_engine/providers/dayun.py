"""Dayun (Đại vận) runtime data provider."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from engines.calendar_engine.solar_terms.engine import SolarTermEngine

from ..exceptions import LuckContextError
from ..models import DayunPeriod
from ._common import (
    CURRENT_AGE_BASIS,
    DAYUN_COUNT,
    DIRECTION_LABELS,
    GENDER_LABELS,
    METHOD_NOTE_VI,
    PRECISION_LEVEL,
    compute_dayun_start_age,
    day_master_of,
    dayun_forward,
    enrich_stem,
    extract_birth_parts,
    resolve_reference_dt,
    stem_yin_yang,
    step_jiazi,
)


class DefaultDayunProvider:
    """
    Generate immutable Dayun decade pillars from BaZi month pillar.

    Runtime data only — does not score favorable / unfavorable luck.
    """

    def __init__(
        self,
        *,
        reference_dt: datetime | None = None,
        dayun_count: int = DAYUN_COUNT,
        terms: SolarTermEngine | None = None,
    ) -> None:
        """Optional reference time for selecting the current decade."""
        self.reference_dt = reference_dt
        self.dayun_count = dayun_count
        self._terms = terms or SolarTermEngine()

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        rule_context: Any | None = None,
    ) -> DayunPeriod:
        """Return the current DayunPeriod; full sequence in metadata."""
        del rule_context
        birth_year, birth_month, birth_day, _h, _m, gender = extract_birth_parts(
            calendar, bazi
        )
        month_pillar = getattr(bazi, "month_pillar", None)
        year_pillar = getattr(bazi, "year_pillar", None)
        if month_pillar is None or year_pillar is None:
            raise LuckContextError("bazi must expose year_pillar and month_pillar")

        month_stem = str(month_pillar.stem)
        month_branch = str(month_pillar.branch)
        year_stem = str(year_pillar.stem)
        day_master = day_master_of(bazi)

        forward = dayun_forward(gender, year_stem)
        step = 1 if forward else -1
        start_age, age_meta = compute_dayun_start_age(
            birth_year,
            birth_month,
            birth_day,
            forward=forward,
            terms=self._terms,
        )

        sequence: list[DayunPeriod] = []
        stem, branch = month_stem, month_branch
        for index in range(self.dayun_count):
            stem, branch = step_jiazi(stem, branch, step)
            pillar_start_age = start_age + index * 10
            pillar_end_age = pillar_start_age + 9
            start_year = birth_year + pillar_start_age
            end_year = start_year + 9
            fields = enrich_stem(stem, branch, day_master)
            sequence.append(
                DayunPeriod(
                    index=index,
                    start_age=pillar_start_age,
                    end_age=pillar_end_age,
                    start_year=start_year,
                    end_year=end_year,
                    heavenly_stem=fields["heavenly_stem"],
                    earthly_branch=fields["earthly_branch"],
                    element=fields["element"],
                    branch_element=fields["branch_element"],
                    yin_yang=fields["yin_yang"],
                    ten_god=fields["ten_god"],
                    hidden_stems=fields["hidden_stems"],
                    metadata={
                        "kind": "dayun",
                        "direction": "forward" if forward else "reverse",
                        "from_month_ganzhi": f"{month_stem} {month_branch}",
                    },
                )
            )

        reference = resolve_reference_dt(calendar, self.reference_dt)
        age = max(0, reference.year - birth_year)
        current = sequence[0]
        for period in sequence:
            if period.start_age <= age <= period.end_age:
                current = period
                break
            if age > period.end_age:
                current = period

        return DayunPeriod(
            index=current.index,
            start_age=current.start_age,
            end_age=current.end_age,
            start_year=current.start_year,
            end_year=current.end_year,
            heavenly_stem=current.heavenly_stem,
            earthly_branch=current.earthly_branch,
            element=current.element,
            branch_element=current.branch_element,
            yin_yang=current.yin_yang,
            ten_god=current.ten_god,
            hidden_stems=current.hidden_stems,
            metadata={
                **dict(current.metadata),
                "sequence": [item.to_dict() for item in sequence],
                "start_age_calc": age_meta,
                "reference_year": reference.year,
                "age_at_reference": age,
                "current_age_for_luck": age,
                "current_age_basis": CURRENT_AGE_BASIS,
                "gender": gender,
                "gender_label": GENDER_LABELS.get(gender, ""),
                "year_stem": year_stem,
                "year_stem_polarity": stem_yin_yang(year_stem),
                "direction": "forward" if forward else "reverse",
                "direction_label": DIRECTION_LABELS["forward" if forward else "reverse"],
                "precision": PRECISION_LEVEL,
                "method_note": METHOD_NOTE_VI,
                "day_master": day_master,
                "sprint": "4.1",
            },
        )

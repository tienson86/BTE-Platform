"""Build InteractionTruthFacts from already-published natal and luck identity."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
    InterpretationFactsBundle,
)
from engines.interpretation_engine.foundation.facts.interaction import (
    InteractionDirection,
    InteractionFactor,
    InteractionPeriodIdentity,
    InteractionSummary,
    InteractionTruthFacts,
)
from engines.interpretation_engine.foundation.status import DataAvailability

_KIND_OVERLAP = "identity_overlap"
_OWNER_USEFUL = "UsefulGodEngine"


def build_interaction_truth_facts(
    facts: InterpretationFactsBundle,
    *,
    luck_payload: Mapping[str, Any] | None = None,
) -> InteractionTruthFacts:
    """Copy natal + luck identities and record exact published-token overlap.

    Does not calculate luck, reselect Useful God, or invent period tokens.
    """
    period = _copy_period_identity(facts, luck_payload)
    diagnostics: list[str] = []
    if period is None or not period.gan_zhi:
        diagnostics.extend((diag.CURRENT_PERIOD_MISSING, diag.INTERACTION_TRUTH_MISSING))
        return _empty_facts(
            period=period,
            facts=facts,
            status=DataAvailability.MISSING,
            confidence="unknown",
            diagnostics=diagnostics,
        )

    useful = facts.useful_god.selected
    if not useful:
        diagnostics.extend((diag.USEFUL_GOD_MISSING, diag.INTERACTION_TRUTH_MISSING))

    if not period.stem:
        diagnostics.append(diag.PERIOD_STEM_UNPUBLISHED)
    if not period.branch:
        diagnostics.append(diag.PERIOD_BRANCH_UNPUBLISHED)
    if not facts.pattern.selected and not facts.pattern.label:
        diagnostics.append(diag.PATTERN_MISSING)
    if not facts.strength.level:
        diagnostics.append(diag.STRENGTH_MISSING)
    if not facts.useful_god.favorable_gods:
        diagnostics.append(diag.HY_MISSING)
    if not facts.useful_god.unfavorable_gods:
        diagnostics.append(diag.KY_MISSING)
    if not period.next_gan_zhi:
        diagnostics.append(diag.NEXT_PERIOD_MISSING)

    period_tokens = _period_tokens(period)
    helpful = _overlap_factors(
        period_tokens,
        natal_items=_support_items(facts),
        polarity="helpful",
        prefix="hy",
    )
    pressure = _overlap_factors(
        period_tokens,
        natal_items=_restrict_items(facts),
        polarity="pressure",
        prefix="ky",
    )
    overlap_count = len(helpful) + len(pressure)
    empty_overlap = overlap_count == 0
    if not helpful and not pressure and useful:
        diagnostics.append(diag.EMPTY_IDENTITY_OVERLAP)

    supported_status = (
        "missing" if not useful else ("overlapped" if helpful else "no_overlap")
    )
    restricted_status = (
        "missing"
        if not facts.useful_god.unfavorable_gods
        else ("overlapped" if pressure else "no_overlap")
    )

    supported = InteractionDirection(
        identities=tuple(
            dict.fromkeys(
                item for item in (useful, *facts.useful_god.favorable_gods) if item
            )
        ),
        overlap_status=supported_status,
        evidence_ids=(
            "UsefulGodEngine.selected",
            "UsefulGodEngine.favorable_gods",
        ),
    )
    restricted = InteractionDirection(
        identities=tuple(item for item in facts.useful_god.unfavorable_gods if item),
        overlap_status=restricted_status,
        evidence_ids=("UsefulGodEngine.unfavorable_gods",),
    )

    status = _status(useful, diagnostics)
    confidence = _confidence(period, facts, useful)
    summary = InteractionSummary(
        period_label=period.label,
        pattern=facts.pattern.label or facts.pattern.selected,
        strength=facts.strength.label or facts.strength.level,
        useful_god=useful,
        overlap_count=overlap_count,
        empty_overlap=empty_overlap,
        status=status.value,
    )
    evidence = _evidence(period, facts, helpful, pressure)
    return InteractionTruthFacts(
        current_period_identity=period,
        interaction_summary=summary,
        helpful_factors=tuple(helpful),
        pressure_factors=tuple(pressure),
        supported_direction=supported,
        restricted_direction=restricted,
        confidence=confidence,
        evidence=evidence,
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        status=status,
    )


def _copy_period_identity(
    facts: InterpretationFactsBundle,
    luck_payload: Mapping[str, Any] | None,
) -> InteractionPeriodIdentity | None:
    """Copy current / next cycle identity. Do not recompute Da Yun."""
    luck = dict(luck_payload or {})
    current_full = luck.get("current_dayun")
    current_full = current_full if isinstance(current_full, Mapping) else {}
    current_cycle = luck.get("current_cycle")
    current_cycle = current_cycle if isinstance(current_cycle, Mapping) else {}
    natal_cycle = facts.luck.current_cycle

    gan_zhi = str(
        current_cycle.get("gan_zhi")
        or current_full.get("ganzhi")
        or current_full.get("gan_zhi")
        or (natal_cycle.gan_zhi if natal_cycle is not None else "")
        or ""
    ).strip()
    if not gan_zhi:
        return None

    stem = str(
        current_full.get("heavenly_stem")
        or current_cycle.get("stem")
        or ""
    ).strip()
    branch = str(
        current_full.get("earthly_branch")
        or current_cycle.get("branch")
        or ""
    ).strip()
    year_start = _as_int(
        current_cycle.get("year_start")
        or current_full.get("start_year")
        or (natal_cycle.year_start if natal_cycle is not None else None)
    )
    year_end = _as_int(
        current_cycle.get("year_end")
        or current_full.get("end_year")
        or (natal_cycle.year_end if natal_cycle is not None else None)
    )
    hidden_raw = current_full.get("hidden_stems") or ()
    hidden = tuple(str(item).strip() for item in hidden_raw if str(item).strip())
    next_gan, next_label = _next_cycle(luck, gan_zhi)
    label = _label(gan_zhi, year_start, year_end)
    return InteractionPeriodIdentity(
        gan_zhi=gan_zhi,
        year_start=year_start,
        year_end=year_end,
        is_current=True,
        label=label,
        stem=stem,
        branch=branch,
        element=str(current_full.get("element") or "").strip(),
        yin_yang=str(current_full.get("yin_yang") or "").strip(),
        ten_god=str(current_full.get("ten_god") or "").strip(),
        hidden_stems=hidden,
        age_start=_as_int(
            current_cycle.get("age_start")
            or current_full.get("start_age")
            or (natal_cycle.age_start if natal_cycle is not None else None)
        ),
        age_end=_as_int(
            current_cycle.get("age_end")
            or current_full.get("end_age")
            or (natal_cycle.age_end if natal_cycle is not None else None)
        ),
        index=_as_int(current_cycle.get("index", current_full.get("index"))),
        direction=str(luck.get("direction") or facts.luck.direction or "").strip(),
        next_gan_zhi=next_gan,
        next_label=next_label,
    )


def _next_cycle(luck: Mapping[str, Any], current_gan: str) -> tuple[str, str]:
    """Copy the already-published next cycle label only."""
    cycles = luck.get("cycles") or []
    if not isinstance(cycles, list):
        return "", ""
    labels: list[tuple[str, str]] = []
    for item in cycles:
        if not isinstance(item, Mapping):
            continue
        gan = str(item.get("gan_zhi") or item.get("ganzhi") or "").strip()
        if not gan:
            continue
        labels.append(
            (
                gan,
                _label(gan, _as_int(item.get("year_start")), _as_int(item.get("year_end"))),
            )
        )
    for index, (gan, label) in enumerate(labels):
        if gan == current_gan and index + 1 < len(labels):
            return labels[index + 1]
    current = luck.get("current_cycle") or luck.get("current_dayun") or {}
    current_index = current.get("index") if isinstance(current, Mapping) else None
    if current_index is None:
        return "", ""
    for item in cycles:
        if not isinstance(item, Mapping):
            continue
        try:
            if int(item.get("index")) == int(current_index) + 1:
                gan = str(item.get("gan_zhi") or item.get("ganzhi") or "").strip()
                return gan, _label(
                    gan,
                    _as_int(item.get("year_start")),
                    _as_int(item.get("year_end")),
                )
        except (TypeError, ValueError):
            continue
    return "", ""


def _period_tokens(period: InteractionPeriodIdentity) -> tuple[tuple[str, str], ...]:
    """Published period identities with their luck field paths."""
    items: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(value: str, field: str) -> None:
        text = value.strip()
        if not text or text in seen:
            return
        seen.add(text)
        items.append((text, field))

    add(period.stem, "LuckEngine.current_dayun.heavenly_stem")
    add(period.branch, "LuckEngine.current_dayun.earthly_branch")
    add(period.element, "LuckEngine.current_dayun.element")
    add(period.ten_god, "LuckEngine.current_dayun.ten_god")
    for stem in period.hidden_stems:
        add(stem, "LuckEngine.current_dayun.hidden_stems")
    return tuple(items)


def _support_items(facts: InterpretationFactsBundle) -> tuple[tuple[str, str], ...]:
    """Natal identities already classified as Useful God or Hỷ."""
    items: list[tuple[str, str]] = []
    if facts.useful_god.selected:
        items.append((facts.useful_god.selected, "UsefulGodEngine.selected"))
    for name in facts.useful_god.favorable_gods:
        if name:
            items.append((name, "UsefulGodEngine.favorable_gods"))
    return tuple(items)


def _restrict_items(facts: InterpretationFactsBundle) -> tuple[tuple[str, str], ...]:
    """Natal identities already classified as Kỵ."""
    return tuple(
        (name, "UsefulGodEngine.unfavorable_gods")
        for name in facts.useful_god.unfavorable_gods
        if name
    )


def _overlap_factors(
    period_tokens: tuple[tuple[str, str], ...],
    natal_items: tuple[tuple[str, str], ...],
    *,
    polarity: str,
    prefix: str,
) -> list[InteractionFactor]:
    """Record exact published-string overlap. Do not infer extra relations."""
    factors: list[InteractionFactor] = []
    seen: set[tuple[str, str]] = set()
    for natal_value, natal_field in natal_items:
        for period_value, period_field in period_tokens:
            if natal_value != period_value:
                continue
            key = (natal_value, period_field)
            if key in seen:
                continue
            seen.add(key)
            index = len(factors)
            factors.append(
                InteractionFactor(
                    fact_id=f"{prefix}_overlap_{index}",
                    kind=_KIND_OVERLAP,
                    natal_identity=natal_value,
                    natal_owner=_OWNER_USEFUL,
                    natal_field=natal_field,
                    period_identity=period_value,
                    period_field=period_field,
                    polarity=polarity,
                    evidence_ids=(period_field, natal_field),
                )
            )
    return factors


def _status(useful: str, diagnostics: list[str]) -> DataAvailability:
    """Availability of interaction comparison, not fortune."""
    if not useful:
        return DataAvailability.PARTIAL
    if diag.PERIOD_STEM_UNPUBLISHED in diagnostics:
        return DataAvailability.PARTIAL
    if diag.PERIOD_BRANCH_UNPUBLISHED in diagnostics:
        return DataAvailability.PARTIAL
    if diag.PATTERN_MISSING in diagnostics or diag.STRENGTH_MISSING in diagnostics:
        return DataAvailability.PARTIAL
    return DataAvailability.AVAILABLE


def _confidence(
    period: InteractionPeriodIdentity,
    facts: InterpretationFactsBundle,
    useful: str,
) -> str:
    """Completeness of upstream evidence. Not a luck score."""
    if not period.gan_zhi:
        return "unknown"
    has_pattern = bool(facts.pattern.selected or facts.pattern.label)
    has_strength = bool(facts.strength.level)
    if useful and has_pattern and has_strength:
        return "high"
    if useful:
        return "medium"
    return "low"


def _evidence(
    period: InteractionPeriodIdentity,
    facts: InterpretationFactsBundle,
    helpful: list[InteractionFactor],
    pressure: list[InteractionFactor],
) -> tuple[str, ...]:
    """Upstream field paths only."""
    refs = [
        "LuckEngine.current_dayun.gan_zhi",
        "UsefulGodEngine.selected",
        "UsefulGodEngine.favorable_gods",
        "UsefulGodEngine.unfavorable_gods",
        "PatternEngine.selected",
        "StrengthEngine.level",
    ]
    if period.stem:
        refs.append("LuckEngine.current_dayun.heavenly_stem")
    if period.branch:
        refs.append("LuckEngine.current_dayun.earthly_branch")
    if period.ten_god:
        refs.append("LuckEngine.current_dayun.ten_god")
    if period.hidden_stems:
        refs.append("LuckEngine.current_dayun.hidden_stems")
    for item in (*helpful, *pressure):
        refs.extend(item.evidence_ids)
    return tuple(dict.fromkeys(refs))


def _empty_facts(
    *,
    period: InteractionPeriodIdentity | None,
    facts: InterpretationFactsBundle,
    status: DataAvailability,
    confidence: str,
    diagnostics: list[str],
) -> InteractionTruthFacts:
    """Honest empty interaction. Never fabricate overlap."""
    return InteractionTruthFacts(
        current_period_identity=period,
        interaction_summary=InteractionSummary(
            period_label=period.label if period is not None else "",
            pattern=facts.pattern.label or facts.pattern.selected,
            strength=facts.strength.label or facts.strength.level,
            useful_god=facts.useful_god.selected,
            overlap_count=0,
            empty_overlap=True,
            status=status.value,
        ),
        helpful_factors=(),
        pressure_factors=(),
        supported_direction=InteractionDirection(
            identities=(),
            overlap_status="missing",
            evidence_ids=(),
        ),
        restricted_direction=InteractionDirection(
            identities=(),
            overlap_status="missing",
            evidence_ids=(),
        ),
        confidence=confidence,
        evidence=(),
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        status=status,
    )


def _label(gan_zhi: str, year_start: int | None, year_end: int | None) -> str:
    """Format already-published gan_zhi plus years."""
    years = f"{year_start}–{year_end}" if year_start and year_end else ""
    return " ".join(part for part in (gan_zhi, years) if part)


def _as_int(value: Any) -> int | None:
    """Parse optional integer fields without inventing values."""
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

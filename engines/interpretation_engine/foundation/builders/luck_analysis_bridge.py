"""Bridge already-published LuckEngine analysis into LuckAnalysisFacts.

Does not calculate luck, match stem names, or infer overlap meaning.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
    InterpretationFactsBundle,
)
from engines.interpretation_engine.foundation.facts.luck_analysis import (
    LuckAnalysisDirection,
    LuckAnalysisFacts,
    LuckAnalysisRelation,
    LuckGoverningRole,
    LuckPeriodIdentity,
)
from engines.interpretation_engine.foundation.status import DataAvailability

_UNDETERMINED = frozenset({"", "unknown", "none", "null"})


def build_luck_analysis_facts(
    facts: InterpretationFactsBundle,
    *,
    luck_payload: Mapping[str, Any] | None = None,
) -> LuckAnalysisFacts:
    """Copy production luck analysis. Never invent helpful or pressure meaning."""
    luck = dict(luck_payload or {})
    period = _copy_period_identity(facts, luck)
    diagnostics: list[str] = []
    if period is None or not period.gan_zhi:
        diagnostics.extend((diag.CURRENT_PERIOD_MISSING, diag.INSUFFICIENT_LUCK_ANALYSIS))
        return _empty_facts(
            period=period,
            facts=facts,
            status=DataAvailability.MISSING,
            confidence="unknown",
            diagnostics=diagnostics,
        )

    if not period.stem:
        diagnostics.append(diag.PERIOD_STEM_UNPUBLISHED)
    if not period.branch:
        diagnostics.append(diag.PERIOD_BRANCH_UNPUBLISHED)
    if not facts.pattern.selected and not facts.pattern.label:
        diagnostics.append(diag.PATTERN_MISSING)
    if not facts.strength.level:
        diagnostics.append(diag.STRENGTH_MISSING)
    if not facts.useful_god.selected:
        diagnostics.append(diag.USEFUL_GOD_MISSING)
    if not facts.useful_god.favorable_gods:
        diagnostics.append(diag.HY_MISSING)
    if not facts.useful_god.unfavorable_gods:
        diagnostics.append(diag.KY_MISSING)
    if not period.next_gan_zhi:
        diagnostics.append(diag.NEXT_PERIOD_MISSING)

    helpful = _production_relation(
        identities=_published_list(luck.get("support_elements")),
        level=str(luck.get("support_level") or period.support_level or ""),
        polarity="helpful",
        source="LuckEngine.support_elements",
        level_source="LuckEngine.support_level",
    )
    pressure = _production_relation(
        identities=_published_list(luck.get("attack_elements")),
        level=str(luck.get("attack_level") or period.attack_level or ""),
        polarity="pressure",
        source="LuckEngine.attack_elements",
        level_source="LuckEngine.attack_level",
    )
    if helpful is None and pressure is None:
        diagnostics.append(diag.INSUFFICIENT_LUCK_ANALYSIS)

    roles = _governing_roles(period, facts)
    useful = tuple(
        dict.fromkeys(
            item for item in (facts.useful_god.selected, *facts.useful_god.favorable_gods) if item
        )
    )
    ky = tuple(item for item in facts.useful_god.unfavorable_gods if item)
    status = _status(period, helpful, pressure, diagnostics)
    confidence = _confidence(luck, facts, period)
    return LuckAnalysisFacts(
        current_period_identity=period,
        governing_roles=roles,
        helpful_relations=() if helpful is None else (helpful,),
        pressure_relations=() if pressure is None else (pressure,),
        supported_direction=LuckAnalysisDirection(
            identities=useful,
            source="UsefulGodEngine.selected",
            evidence_ids=("UsefulGodEngine.selected", "UsefulGodEngine.favorable_gods"),
        ),
        restricted_direction=LuckAnalysisDirection(
            identities=ky,
            source="UsefulGodEngine.unfavorable_gods",
            evidence_ids=("UsefulGodEngine.unfavorable_gods",),
        ),
        confidence=confidence,
        evidence=_evidence(period, helpful, pressure),
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        status=status,
    )


def _copy_period_identity(
    facts: InterpretationFactsBundle,
    luck: Mapping[str, Any],
) -> LuckPeriodIdentity | None:
    """Copy current / next cycle identity and evaluation slots. Do not recompute."""
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
        current_full.get("heavenly_stem") or current_cycle.get("stem") or ""
    ).strip()
    branch = str(
        current_full.get("earthly_branch") or current_cycle.get("branch") or ""
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
    return LuckPeriodIdentity(
        gan_zhi=gan_zhi,
        year_start=year_start,
        year_end=year_end,
        is_current=True,
        label=_label(gan_zhi, year_start, year_end),
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
        support_level=str(luck.get("support_level") or "").strip(),
        attack_level=str(luck.get("attack_level") or "").strip(),
        luck_stage=str(luck.get("luck_stage") or "").strip(),
        luck_strength=_as_float(luck.get("luck_strength")),
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
            (gan, _label(gan, _as_int(item.get("year_start")), _as_int(item.get("year_end"))))
        )
    for index, (gan, label) in enumerate(labels):
        if gan == current_gan and index + 1 < len(labels):
            return labels[index + 1]
    return "", ""


def _governing_roles(
    period: LuckPeriodIdentity,
    facts: InterpretationFactsBundle,
) -> tuple[LuckGoverningRole, ...]:
    """Copy natal governors and LuckEngine period ten-god. Do not infer extras."""
    roles: list[LuckGoverningRole] = []
    if period.ten_god:
        roles.append(
            LuckGoverningRole(
                name=period.ten_god,
                owner="LuckEngine",
                field="LuckEngine.current_dayun.ten_god",
                scope="period",
            )
        )
    pattern = facts.pattern.label or facts.pattern.selected
    if pattern:
        roles.append(
            LuckGoverningRole(
                name=pattern,
                owner="PatternEngine",
                field="PatternEngine.selected",
                scope="natal",
            )
        )
    strength = facts.strength.label or facts.strength.level
    if strength:
        roles.append(
            LuckGoverningRole(
                name=strength,
                owner="StrengthEngine",
                field="StrengthEngine.level",
                scope="natal",
            )
        )
    if facts.useful_god.selected:
        roles.append(
            LuckGoverningRole(
                name=facts.useful_god.selected,
                owner="UsefulGodEngine",
                field="UsefulGodEngine.selected",
                scope="natal",
            )
        )
    for name in facts.useful_god.favorable_gods:
        if name:
            roles.append(
                LuckGoverningRole(
                    name=name,
                    owner="UsefulGodEngine",
                    field="UsefulGodEngine.favorable_gods",
                    scope="natal",
                )
            )
    for name in facts.useful_god.unfavorable_gods:
        if name:
            roles.append(
                LuckGoverningRole(
                    name=name,
                    owner="UsefulGodEngine",
                    field="UsefulGodEngine.unfavorable_gods",
                    scope="natal",
                )
            )
    return tuple(roles)


def _production_relation(
    *,
    identities: tuple[str, ...],
    level: str,
    polarity: str,
    source: str,
    level_source: str,
) -> LuckAnalysisRelation | None:
    """Keep a relation only when LuckEngine already published concrete values."""
    if not identities or _undetermined(level):
        return None
    return LuckAnalysisRelation(
        identities=identities,
        level=level,
        polarity=polarity,
        source=source,
        evidence_ids=(source, level_source),
    )


def _status(
    period: LuckPeriodIdentity,
    helpful: LuckAnalysisRelation | None,
    pressure: LuckAnalysisRelation | None,
    diagnostics: list[str],
) -> DataAvailability:
    """Availability of production luck analysis, not fortune."""
    if not period.gan_zhi:
        return DataAvailability.MISSING
    if helpful is None and pressure is None:
        return DataAvailability.PARTIAL
    if diag.PERIOD_STEM_UNPUBLISHED in diagnostics:
        return DataAvailability.PARTIAL
    return DataAvailability.AVAILABLE


def _confidence(
    luck: Mapping[str, Any],
    facts: InterpretationFactsBundle,
    period: LuckPeriodIdentity,
) -> str:
    """Completeness of upstream evidence. Not a luck score."""
    raw = luck.get("confidence")
    if isinstance(raw, (int, float)):
        if raw >= 0.8:
            return "high"
        if raw >= 0.4:
            return "medium"
        return "low"
    if period.ten_god and facts.useful_god.selected:
        return "medium"
    return "unknown"


def _evidence(
    period: LuckPeriodIdentity,
    helpful: LuckAnalysisRelation | None,
    pressure: LuckAnalysisRelation | None,
) -> tuple[str, ...]:
    """Upstream field paths only."""
    refs = [
        "LuckEngine.current_dayun.gan_zhi",
        "LuckEngine.current_dayun.heavenly_stem",
        "LuckEngine.current_dayun.earthly_branch",
        "LuckEngine.current_dayun.ten_god",
        "LuckEngine.support_elements",
        "LuckEngine.attack_elements",
        "UsefulGodEngine.selected",
        "PatternEngine.selected",
        "StrengthEngine.level",
    ]
    if period.hidden_stems:
        refs.append("LuckEngine.current_dayun.hidden_stems")
    if helpful is not None:
        refs.extend(helpful.evidence_ids)
    if pressure is not None:
        refs.extend(pressure.evidence_ids)
    return tuple(dict.fromkeys(refs))


def _empty_facts(
    *,
    period: LuckPeriodIdentity | None,
    facts: InterpretationFactsBundle,
    status: DataAvailability,
    confidence: str,
    diagnostics: list[str],
) -> LuckAnalysisFacts:
    """Honest empty luck analysis. Never fabricate relations."""
    useful = tuple(item for item in (facts.useful_god.selected, *facts.useful_god.favorable_gods) if item)
    ky = tuple(item for item in facts.useful_god.unfavorable_gods if item)
    return LuckAnalysisFacts(
        current_period_identity=period,
        governing_roles=(),
        helpful_relations=(),
        pressure_relations=(),
        supported_direction=LuckAnalysisDirection(
            identities=tuple(dict.fromkeys(useful)),
            source="UsefulGodEngine.selected",
            evidence_ids=("UsefulGodEngine.selected",),
        ),
        restricted_direction=LuckAnalysisDirection(
            identities=ky,
            source="UsefulGodEngine.unfavorable_gods",
            evidence_ids=("UsefulGodEngine.unfavorable_gods",),
        ),
        confidence=confidence,
        evidence=(),
        diagnostics=tuple(dict.fromkeys(diagnostics)),
        status=status,
    )


def _published_list(value: Any) -> tuple[str, ...]:
    """Copy a published identity list. Empty when unpublished."""
    if not value:
        return ()
    if isinstance(value, str):
        text = value.strip()
        return (text,) if text and not _undetermined(text) else ()
    return tuple(
        str(item).strip()
        for item in value
        if str(item).strip() and not _undetermined(str(item).strip())
    )


def _undetermined(value: str) -> bool:
    """True when production has not determined a concrete evaluation."""
    return value.strip().casefold() in _UNDETERMINED


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


def _as_float(value: Any) -> float | None:
    """Parse optional float fields without inventing values."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

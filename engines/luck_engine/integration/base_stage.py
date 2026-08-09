"""Shared structural-overlap helpers for Luck Analysis impact stages."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from engines.luck_engine.analysis.analysis_context import LuckAnalysisContext
from engines.luck_engine.analysis.impact_models import (
    ImpactConfidence,
    ImpactDelta,
    ImpactDirection,
    ImpactEvidence,
    ImpactScore,
    ImpactSummary,
    StageImpact,
)
from engines.luck_engine.analysis_constants import (
    ANALYSIS_VERSION,
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_NONE,
    DIRECTION_AMPLIFYING,
    DIRECTION_DAMPENING,
    DIRECTION_NEUTRAL,
    DIRECTION_UNRESOLVED,
)
from engines.luck_engine.exceptions import ImpactDependencyError


def require_dependencies(context: LuckAnalysisContext, required: tuple[str, ...], stage_id: str) -> None:
    """Reject execution when required upstream impact outputs are absent."""
    missing = [name for name in required if not context.has_published(name)]
    if missing:
        raise ImpactDependencyError(f"missing_inputs:{stage_id}:{','.join(missing)}")


def iter_timeline_periods(timeline: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Flatten major/annual/monthly periods in stable id order."""
    periods: list[dict[str, Any]] = []
    for key in ("major_cycles", "annual_cycles", "monthly_cycles"):
        for cycle in timeline.get(key) or ():
            if not isinstance(cycle, Mapping):
                continue
            for period in cycle.get("periods") or ():
                if isinstance(period, Mapping):
                    periods.append(dict(period))
    periods.sort(key=lambda item: (str(item.get("layer") or ""), int(item.get("sequence") or 0), str(item.get("period_id") or "")))
    return periods


def token_set(values: Iterable[Any]) -> set[str]:
    """Normalize identity tokens from strings or sequences."""
    tokens: set[str] = set()
    for value in values:
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            tokens.update(token_set(value))
            continue
        text = str(value).strip()
        if text:
            tokens.add(text)
    return tokens


def natal_tokens(timeline: Mapping[str, Any], extra_fields: tuple[str, ...]) -> tuple[set[str], tuple[str, ...]]:
    """Collect natal identity tokens plus requested extra field names."""
    natal = timeline.get("natal_chart") or {}
    if not isinstance(natal, Mapping):
        natal = {}
    fields = extra_fields
    values = [natal.get(name) for name in fields]
    return token_set(values), fields


def snapshot_tokens(snapshot: Mapping[str, Any] | None, fields: tuple[str, ...]) -> tuple[set[str], tuple[str, ...]]:
    """Collect published analysis/decision identity tokens."""
    if not isinstance(snapshot, Mapping):
        return set(), fields
    values = [snapshot.get(name) for name in fields]
    present = tuple(name for name in fields if name in snapshot and snapshot.get(name) not in (None, "", [], {}))
    return token_set(values), present


def classify_period(period: Mapping[str, Any], reference: set[str]) -> str:
    """Classify structural overlap. Match = amplifying, else dampening."""
    period_tokens = token_set(
        (
            period.get("heavenly_stem"),
            period.get("earthly_branch"),
            period.get("ganzhi"),
        )
    )
    if not period_tokens:
        return DIRECTION_UNRESOLVED
    if not reference:
        return DIRECTION_UNRESOLVED
    if period_tokens & reference:
        return DIRECTION_AMPLIFYING
    return DIRECTION_DAMPENING


def resolve_direction(amplifying: int, dampening: int, unresolved: int, total: int) -> str:
    """Majority structural direction."""
    if total == 0 or (amplifying == 0 and dampening == 0):
        return DIRECTION_UNRESOLVED
    if amplifying > dampening:
        return DIRECTION_AMPLIFYING
    if dampening > amplifying:
        return DIRECTION_DAMPENING
    return DIRECTION_NEUTRAL


def resolve_confidence(*, reference_present: bool, classified: int, total: int) -> str:
    """Confidence from evidence completeness, not fortune certainty."""
    if total == 0:
        return CONFIDENCE_NONE
    if not reference_present:
        return CONFIDENCE_LOW
    ratio = classified / total
    if ratio >= 0.8:
        return CONFIDENCE_HIGH
    if ratio >= 0.4:
        return CONFIDENCE_MEDIUM
    return CONFIDENCE_LOW


def build_stage_impact(
    *,
    stage_id: str,
    periods: list[dict[str, Any]],
    reference: set[str],
    consumed_fields: tuple[str, ...],
    reference_present: bool,
) -> StageImpact:
    """Compute one stage impact from declared timeline slots and identity tokens."""
    labels = [classify_period(period, reference) for period in periods]
    amplifying = labels.count(DIRECTION_AMPLIFYING)
    dampening = labels.count(DIRECTION_DAMPENING)
    unresolved = labels.count(DIRECTION_UNRESOLVED)
    total = len(periods)
    classified = amplifying + dampening
    score = 0.0 if total == 0 else round(100.0 * amplifying / total, 4)
    delta = 0.0 if total == 0 else round((amplifying - dampening) / total, 4)
    direction = resolve_direction(amplifying, dampening, unresolved, total)
    confidence = resolve_confidence(
        reference_present=reference_present,
        classified=classified,
        total=total,
    )
    period_ids = tuple(str(item.get("period_id")) for item in periods if item.get("period_id"))
    summary_text = (
        f"{amplifying}/{total} periods share {stage_id} identity tokens."
        if total
        else f"No timeline periods available for {stage_id}."
    )
    return StageImpact(
        stage_id=stage_id,
        direction=ImpactDirection(direction),
        score=ImpactScore(score),
        delta=ImpactDelta(delta),
        confidence=ImpactConfidence(confidence),
        evidence=ImpactEvidence(
            period_ids=period_ids,
            consumed_fields=consumed_fields,
            notes=("structural_overlap_only",),
        ),
        summary=ImpactSummary(
            text=summary_text,
            amplifying_count=amplifying,
            dampening_count=dampening,
            unresolved_count=unresolved,
            period_count=total,
        ),
        analysis_version=ANALYSIS_VERSION,
    )

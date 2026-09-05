"""Read immutable Pack 07 findings. Does not recalculate natal, luck, or Useful God."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult, DomainSection
from engines.detailed_interpretation_engine.enums import DomainState
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.life_optimization.constants import ELEMENT_TOKENS
from engines.detailed_interpretation_engine.temporal import (
    LuckActivationResult,
    LuckInteractionResult,
    TemporalActivationResult,
)


@dataclass(frozen=True, slots=True)
class LifeOptimizationFacts:
    """Inputs Life Optimization may consume. Upstream objects are copied, not mutated."""

    analysis_id: str
    natal: dict[str, DomainInterpretationResult]
    evidence_priority: EvidencePriorityResult
    luck: LuckActivationResult
    interaction: LuckInteractionResult
    temporal: TemporalActivationResult
    useful_god: str
    useful_element: str
    supporting_gods: tuple[str, ...]
    ky_context: tuple[str, ...]
    temperature_label: str
    climate_preference: str
    five_elements: dict[str, str]
    shen_sha_ids: tuple[str, ...]


def collect_life_optimization_facts(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> LifeOptimizationFacts:
    """Snapshot upstream truth for optimization. No new natal calculation."""
    data = payload if isinstance(payload, Mapping) else {}
    useful = _as_map(data.get("useful_god"))
    temperature = _as_map(data.get("temperature"))
    pattern = _as_map(data.get("pattern"))
    shen = context.runtime.interpretation.shen_sha
    return LifeOptimizationFacts(
        analysis_id=context.analysis_id,
        natal=_natal_map(context.runtime.domains),
        evidence_priority=context.runtime.interpretation.evidence_priority,
        luck=context.runtime.temporal.luck_activation,
        interaction=context.runtime.temporal.luck_interaction,
        temporal=context.runtime.temporal.temporal_activation,
        useful_god=_text(useful.get("useful_god") or useful.get("useful_ten_god")),
        useful_element=_element(useful),
        supporting_gods=_string_tuple(useful.get("favorable_gods") or useful.get("supporting_gods")),
        ky_context=_string_tuple(
            useful.get("unfavorable_gods") or useful.get("ky_scope_note") or useful.get("avoidance")
        ),
        temperature_label=_text(
            temperature.get("label")
            or temperature.get("climate_preference_label")
            or useful.get("climate_preference_label")
            or pattern.get("dieu_hau")
        ),
        climate_preference=_text(
            useful.get("climate_preference_label") or temperature.get("climate_preference_label")
        ),
        five_elements=_five_elements(data.get("five_elements")),
        shen_sha_ids=tuple(item.shen_sha_id for item in shen.individual.items if item.shen_sha_id),
    )


def natal_evaluated(facts: LifeOptimizationFacts) -> bool:
    """True when at least one published natal domain has been interpreted."""
    return any(item.state is not DomainState.NOT_EVALUATED for item in facts.natal.values())


def _natal_map(section: DomainSection) -> dict[str, DomainInterpretationResult]:
    return {
        "authority": section.authority.natal,
        "career": section.career.natal,
        "wealth": section.wealth.natal,
        "relationship": section.relationship.natal,
        "legacy": section.legacy.natal,
        "vitality": section.vitality.natal,
    }


def _element(useful: Mapping[str, Any]) -> str:
    text = _text(
        useful.get("useful_element") or useful.get("element") or useful.get("useful_display")
    )
    for token in ELEMENT_TOKENS:
        if token in text:
            return token
    return text


def _five_elements(raw: Any) -> dict[str, str]:
    payload = _as_map(raw)
    scores = payload.get("scores") if isinstance(payload.get("scores"), Mapping) else payload
    if not isinstance(scores, Mapping):
        return {}
    items: dict[str, str] = {}
    for key, value in scores.items():
        token = str(key)
        if token not in ELEMENT_TOKENS:
            continue
        if isinstance(value, Mapping):
            items[token] = _text(value.get("band") or value.get("level") or value.get("role"))
        else:
            items[token] = _text(value)
    return items


def _as_map(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _string_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    return tuple(str(item).strip() for item in value if str(item).strip())

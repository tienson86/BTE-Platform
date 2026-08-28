"""Compose StrengthNarrativeUnit from published Strength / Useful God / Temperature."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.strength.classify import (
    apply_temperature_strength_effect,
    classify_strength_evidence,
)
from engines.narrative_framework.strength.evidence import _payload, bind_strength_evidence
from engines.narrative_framework.strength.impact import build_impact
from engines.narrative_framework.strength.models import StrengthNarrativeUnit
from engines.narrative_framework.strength.observation import build_observation
from engines.narrative_framework.strength.reasoning import build_reasoning
from engines.narrative_framework.strength.recommendation import build_recommendation
from engines.narrative_framework.strength.summary import build_summary


def _status(observation_ok: bool, others_ok: tuple[bool, ...]) -> str:
    if not observation_ok:
        return "insufficient"
    if all(others_ok):
        return "complete"
    return "partial"


def compose_strength_narrative(
    strength: Any,
    useful_god: Any = None,
    temperature: Any = None,
) -> StrengthNarrativeUnit:
    """Evidence → Classification → Observation → Reasoning → Impact → Recommendation → Summary."""
    evidence = bind_strength_evidence(strength, temperature=temperature)
    pack = apply_temperature_strength_effect(
        classify_strength_evidence(evidence),
        _payload(temperature),
    )
    observation = build_observation(pack)
    reasoning = build_reasoning(pack)
    impact = build_impact(pack)
    recommendation = build_recommendation(evidence, useful_god=useful_god, temperature=temperature)
    summary = build_summary(observation, reasoning, impact, recommendation)
    refs = tuple(
        path
        for block in (observation, reasoning, impact, recommendation, summary)
        for path in block.source_paths
    )
    return StrengthNarrativeUnit(
        evidence=evidence,
        observation=observation,
        reasoning=reasoning,
        impact=impact,
        recommendation=recommendation,
        summary=summary,
        status=_status(
            observation.available,
            (
                reasoning.available,
                impact.available,
                recommendation.available,
                summary.available,
            ),
        ),
        evidence_refs=refs,
        evidence_pack=pack,
    )

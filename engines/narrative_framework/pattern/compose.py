"""Compose PatternNarrativeUnit from published Pattern / Useful God / Temperature."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.pattern.classify import classify_pattern_evidence
from engines.narrative_framework.pattern.evidence import bind_pattern_evidence
from engines.narrative_framework.pattern.impact import build_impact
from engines.narrative_framework.pattern.models import PatternNarrativeUnit
from engines.narrative_framework.pattern.observation import build_observation
from engines.narrative_framework.pattern.reasoning import build_reasoning
from engines.narrative_framework.pattern.recommendation import build_recommendation
from engines.narrative_framework.pattern.summary import build_summary


def _status(observation_ok: bool, others_ok: tuple[bool, ...]) -> str:
    if not observation_ok:
        return "insufficient"
    if all(others_ok):
        return "complete"
    return "partial"


def compose_pattern_narrative(
    pattern: Any,
    useful_god: Any = None,
    temperature: Any = None,
) -> PatternNarrativeUnit:
    """Evidence → Classification → Observation → Reasoning → Impact → Recommendation → Summary."""
    evidence = bind_pattern_evidence(pattern, temperature=temperature)
    pack = classify_pattern_evidence(evidence)
    observation = build_observation(pack)
    reasoning = build_reasoning(pack)
    impact = build_impact(pack)
    recommendation = build_recommendation(
        evidence,
        useful_god=useful_god,
        temperature=temperature,
    )
    summary = build_summary(observation, reasoning, impact, recommendation)
    refs = tuple(
        path
        for block in (observation, reasoning, impact, recommendation, summary)
        for path in block.source_paths
    )
    return PatternNarrativeUnit(
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

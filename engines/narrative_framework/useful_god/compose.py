"""Compose UsefulGodNarrativeUnit from published Useful God evidence."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.useful_god.classify import classify_useful_god_evidence
from engines.narrative_framework.useful_god.evidence import bind_useful_god_evidence
from engines.narrative_framework.useful_god.impact import build_impact
from engines.narrative_framework.useful_god.models import UsefulGodNarrativeUnit
from engines.narrative_framework.useful_god.observation import build_observation
from engines.narrative_framework.useful_god.reasoning import build_reasoning
from engines.narrative_framework.useful_god.recommendation import build_recommendation
from engines.narrative_framework.useful_god.summary import build_summary


def _status(observation_ok: bool, others_ok: tuple[bool, ...]) -> str:
    if not observation_ok:
        return "insufficient"
    if all(others_ok):
        return "complete"
    return "partial"


def compose_useful_god_narrative(useful_god: Any) -> UsefulGodNarrativeUnit:
    """Evidence → Classification → Observation → Reasoning → Impact → Recommendation → Summary."""
    evidence = bind_useful_god_evidence(useful_god)
    pack = classify_useful_god_evidence(evidence)
    observation = build_observation(pack)
    reasoning = build_reasoning(pack)
    impact = build_impact(pack)
    recommendation = build_recommendation(evidence)
    summary = build_summary(observation, reasoning, impact, recommendation)
    refs = tuple(
        path
        for block in (observation, reasoning, impact, recommendation, summary)
        for path in block.source_paths
    )
    return UsefulGodNarrativeUnit(
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

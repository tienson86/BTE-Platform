"""Compose LuckNarrativeUnit from published Luck evidence."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.luck.classify import classify_luck_evidence
from engines.narrative_framework.luck.evidence import bind_luck_evidence
from engines.narrative_framework.luck.impact import build_impact
from engines.narrative_framework.luck.models import LuckNarrativeUnit
from engines.narrative_framework.luck.observation import build_observation
from engines.narrative_framework.luck.reasoning import build_reasoning
from engines.narrative_framework.luck.recommendation import build_recommendation
from engines.narrative_framework.luck.summary import build_summary


def _status(observation_ok: bool, others_ok: tuple[bool, ...]) -> str:
    if not observation_ok:
        return "insufficient"
    if all(others_ok):
        return "complete"
    return "partial"


def compose_luck_narrative(luck: Any) -> LuckNarrativeUnit:
    """Evidence → Classification → Observation → Reasoning → Impact → Recommendation → Summary."""
    evidence = bind_luck_evidence(luck)
    pack = classify_luck_evidence(evidence)
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
    return LuckNarrativeUnit(
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

"""Interpretation validator tests (N-IMP-07)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.interpretation import (
    InterpretationBuilder,
    InterpretationNarrative,
    InterpretationValidator,
)
from engines.narrative_v2.interpretation.interpretation_model import InterpretationReference


def _rewrite(case_0001_canonical: dict[str, Any]) -> object:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    return RewriteEngine().rewrite(knowledge, reasoning, evidence)


def test_validator_passes_case_0001(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    narrative = InterpretationBuilder().build(rewrite)
    outcome = InterpretationValidator().validate(narrative, rewrite)
    assert outcome.passed is True


def test_validator_rejects_action_claim(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    narrative = InterpretationBuilder().build(rewrite)
    tainted = InterpretationNarrative(
        overview=narrative.overview,
        observation=narrative.observation,
        reasoning=narrative.reasoning,
        meaning=narrative.meaning,
        impact=narrative.impact,
        recommendation="Bạn nên bổ Hỏa.",
        closing=narrative.closing,
        references=narrative.references,
        metadata=narrative.metadata,
        status=narrative.status,
    )
    outcome = InterpretationValidator().validate(tainted, rewrite)
    assert outcome.passed is False


def test_validator_rejects_missing_trace(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    narrative = InterpretationBuilder().build(rewrite)
    tainted = InterpretationNarrative(
        overview=narrative.overview,
        observation=narrative.observation,
        reasoning=narrative.reasoning,
        meaning=narrative.meaning,
        impact=narrative.impact,
        recommendation=narrative.recommendation,
        closing=narrative.closing,
        references=(
            InterpretationReference(
                field="observation",
                rewrite_ids=(),
                knowledge_ids=(),
                reasoning_ids=(),
                evidence_ids=(),
            ),
        ),
        metadata=narrative.metadata,
        status=narrative.status,
    )
    outcome = InterpretationValidator().validate(tainted, rewrite)
    assert outcome.passed is False

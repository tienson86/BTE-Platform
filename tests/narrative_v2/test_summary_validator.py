"""Summary validator tests (N-IMP-06)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.summary import OverviewSummary, SummaryBuilder, SummaryValidator
from engines.narrative_v2.summary.summary_model import SummaryReference


def _rewrite(case_0001_canonical: dict[str, Any]) -> object:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    return RewriteEngine().rewrite(knowledge, reasoning, evidence)


def test_validator_passes_case_0001(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    overview = SummaryBuilder().build(rewrite)
    outcome = SummaryValidator().validate(overview, rewrite)
    assert outcome.passed is True


def test_validator_rejects_action_claim(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    overview = SummaryBuilder().build(rewrite)
    tainted = OverviewSummary(
        headline=overview.headline,
        summary="Bạn nên bổ Hỏa.",
        identity=overview.identity,
        balance=overview.balance,
        conclusion=overview.conclusion,
        references=overview.references,
        metadata=overview.metadata,
        status=overview.status,
    )
    outcome = SummaryValidator().validate(tainted, rewrite)
    assert outcome.passed is False


def test_validator_rejects_missing_trace(case_0001_canonical: dict[str, Any]) -> None:
    rewrite = _rewrite(case_0001_canonical)
    overview = SummaryBuilder().build(rewrite)
    tainted = OverviewSummary(
        headline=overview.headline,
        summary=overview.summary,
        identity=overview.identity,
        balance=overview.balance,
        conclusion=overview.conclusion,
        references=(
            SummaryReference(
                field="headline",
                rewrite_ids=(),
                knowledge_ids=(),
                reasoning_ids=(),
                evidence_ids=(),
            ),
        ),
        metadata=overview.metadata,
        status=overview.status,
    )
    outcome = SummaryValidator().validate(tainted, rewrite)
    assert outcome.passed is False

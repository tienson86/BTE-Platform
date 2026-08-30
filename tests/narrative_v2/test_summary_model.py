"""OverviewSummary model contract tests (N-IMP-06)."""

from __future__ import annotations

from dataclasses import fields
from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.summary import OverviewSummary, SummaryBuilder
from engines.narrative_v2.summary.summary_model import ALLOWED_STATUSES

CANONICAL_FIELDS = (
    "headline",
    "summary",
    "identity",
    "balance",
    "conclusion",
    "references",
    "metadata",
    "status",
)


def _overview(case_0001_canonical: dict[str, Any]) -> OverviewSummary:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    return SummaryBuilder().build(rewrite)


def test_canonical_public_fields_only() -> None:
    names = tuple(item.name for item in fields(OverviewSummary))
    assert names == CANONICAL_FIELDS


def test_case_0001_status_and_optional_fields(case_0001_canonical: dict[str, Any]) -> None:
    overview = _overview(case_0001_canonical)
    assert overview.status in ALLOWED_STATUSES
    assert overview.status != "complete"
    assert overview.identity is None
    assert overview.balance is None
    assert overview.conclusion is None
    assert overview.headline
    assert overview.summary

"""NarrativeEvidenceContext structure tests (N-IMP-02)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.evidence import EvidenceBuilder, NarrativeEvidenceContext
from engines.narrative_v2.evidence.evidence_registry import ALLOWED_DOMAINS


def test_context_has_required_domains(case_0001_canonical: dict[str, Any]) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    assert isinstance(context, NarrativeEvidenceContext)
    for domain in ALLOWED_DOMAINS:
        assert hasattr(context, domain)
    assert context.references
    assert context.metadata
    assert "headline" not in dict(context.metadata)
    assert "summary" not in dict(context.metadata)
    assert "insight" not in dict(context.metadata)


def test_context_does_not_copy_entire_canonical(
    case_0001_canonical: dict[str, Any],
) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    assert not hasattr(context, "interpretation")
    assert not hasattr(context, "narrative")
    assert not hasattr(context, "report")
    assert not hasattr(context, "canonical_analysis")

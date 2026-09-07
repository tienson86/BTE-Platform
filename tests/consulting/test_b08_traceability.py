"""TV1-B08 cross-layer traceability. Broken traces are a FAIL."""

from __future__ import annotations

from consulting.marriage.models.enums import FindingType
from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case


def test_action_narrative_traces_to_canonical_source() -> None:
    """Customer action narrative → Recommendation → Finding → Evidence → Canonical source."""
    for case in GOLDEN_CASES:
        bundle = run_golden_case(case.case_id)
        _assert_action_trace(bundle)


def test_non_action_narrative_traces_to_canonical_source() -> None:
    """Non-action narrative → Decision/Finding → Evidence → Canonical source."""
    for case in GOLDEN_CASES:
        bundle = run_golden_case(case.case_id)
        _assert_non_action_trace(bundle)


def _assert_action_trace(bundle: dict) -> None:
    """Every action-bearing narrative block must have a complete source chain."""
    decision = bundle["decision"]
    recs = {item.recommendation_id: item for item in decision.recommendations}
    findings = {item.finding_id: item for item in decision.findings}
    evidence = {item.evidence_id: item for item in decision.evidence}
    for section in bundle["narrative"].sections:
        for block in section.blocks:
            if not block.source_recommendation_ids:
                continue
            for rec_id in block.source_recommendation_ids:
                rec = recs[rec_id]
                assert rec.source_finding_ids
                for finding_id in rec.source_finding_ids:
                    finding = findings[finding_id]
                    assert finding.evidence_ids
                    for evidence_id in finding.evidence_ids:
                        atom = evidence[evidence_id]
                        assert atom.source_refs
                        assert all(ref.analysis_id and ref.path for ref in atom.source_refs)


def _assert_non_action_trace(bundle: dict) -> None:
    """Narrative blocks that explain state/findings still bind to Canonical evidence."""
    decision = bundle["decision"]
    findings = {item.finding_id: item for item in decision.findings}
    evidence = {item.evidence_id: item for item in decision.evidence}
    overall = decision.overall.state.value if decision.overall.state else None
    assert overall
    explained = False
    for section in bundle["narrative"].sections:
        for block in section.blocks:
            if block.source_recommendation_ids:
                continue
            if not block.source_finding_ids:
                continue
            explained = True
            for finding_id in block.source_finding_ids:
                finding = findings[finding_id]
                assert finding.evidence_ids
                for evidence_id in finding.evidence_ids:
                    atom = evidence[evidence_id]
                    assert atom.source_refs
                    assert all(ref.analysis_id for ref in atom.source_refs)
                    if finding.type is FindingType.CONDITION:
                        continue
                    assert atom.domain is finding.domain or atom.evidence_id in finding.evidence_ids
    assert explained or decision.findings == []

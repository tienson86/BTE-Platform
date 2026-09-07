"""TV1-B03 finding resolution tests."""

from __future__ import annotations

from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.models.enums import MarriageEvidenceType
from tests.consulting.decision_fixtures import golden_pair, policy_context_for


def test_findings_are_created_from_evidence() -> None:
    """Evidence atoms with the same semantic meaning produce one finding."""
    snapshot_a, snapshot_b = golden_pair()
    evidence = CanonicalEvidenceBuilder().build_from_policy_context(
        policy_context_for(snapshot_a, snapshot_b)
    )
    resolved = MarriageEvidenceResolver().resolve(evidence)
    findings = CanonicalFindingBuilder().build_from_resolved(evidence, resolved)
    assert findings
    for finding in findings:
        assert finding.evidence_ids
        assert all(any(item.evidence_id == evidence_id for item in evidence) for evidence_id in finding.evidence_ids)
        assert finding.version
    useful_findings = [
        item for item in findings if item.semantic_key == "useful_god_support"
    ]
    useful_evidence = [
        item for item in evidence if item.evidence_type is MarriageEvidenceType.USEFUL_GOD_SUPPORT
    ]
    if useful_evidence:
        assert useful_findings
        referenced = {eid for item in useful_findings for eid in item.evidence_ids}
        assert {item.evidence_id for item in useful_evidence} <= referenced or referenced <= {
            item.evidence_id for item in useful_evidence
        }


def test_no_finding_without_evidence() -> None:
    """An empty evidence list yields no findings."""
    assert CanonicalFindingBuilder().build([]) == []
    assert CanonicalFindingBuilder().build_from_resolved([], []) == []

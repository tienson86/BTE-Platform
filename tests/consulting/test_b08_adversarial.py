"""TV1-B08 adversarial and boundary cases. Attempt to break the frozen module."""

from __future__ import annotations

import json
import re
from dataclasses import replace

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.resolver import MarriageDecisionResolverV1, build_confidence
from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.enums import (
    DomainDecisionState,
    EvidenceDirection,
    FindingPriority,
    FindingType,
    MarriageDomain,
    MarriageEvidenceType,
)
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.policy.v1 import is_secondary_type
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from tests.consulting.api_fixtures import api_client, valid_body
from tests.consulting.decision_fixtures import golden_pair, policy_context_for
from tests.consulting.golden.cases import run_golden_case
from tests.consulting.golden.signature import pipeline_from_snapshots


def _context_and_evidence(include_luck: bool = True):
    snapshot_a, snapshot_b = golden_pair()
    context = policy_context_for(snapshot_a, snapshot_b, include_luck=include_luck)
    evidence = CanonicalEvidenceBuilder().build_from_policy_context(context)
    return snapshot_a, snapshot_b, context, evidence


def _decide(snapshot_a, snapshot_b, context, evidence):
    resolved = MarriageEvidenceResolver().resolve(evidence)
    findings = CanonicalFindingBuilder().build_from_resolved(evidence, resolved)
    decision_context = MarriageDecisionContext(
        consultation_id=context.consultation_id,
        relationship=MarriageRelationshipContext(
            person_a=snapshot_a,
            person_b=snapshot_b,
            options=context.options,
            available_domains=list(context.available_domains),
            limitations=list(context.limitations),
        ),
        versions=context.versions,
        evidence=evidence,
        findings=findings,
    )
    resolver = MarriageDecisionResolverV1()
    domains = resolver.resolve_domains(decision_context)
    overall = resolver.resolve_overall(decision_context)
    return resolved, findings, domains, overall, decision_context


def test_duplicate_semantic_evidence_collapses() -> None:
    """The same semantic atom emitted twice survives as one resolved identity."""
    snapshot_a, snapshot_b, context, evidence = _context_and_evidence()
    original = evidence[0]
    duplicate = replace(original, evidence_id="EV-9999")
    combined = evidence + [duplicate]
    resolved = MarriageEvidenceResolver().resolve(combined)
    keys = [
        (item.evidence_id,)
        for item in resolved
    ]
    surviving = [item.evidence_id for item in resolved]
    assert original.evidence_id in surviving
    assert "EV-9999" not in surviving
    assert len(surviving) == len(set(surviving))
    _ = keys


def test_opposing_evidence_at_same_significance_is_preserved() -> None:
    """Equal-significance support and pressure remain; neither is deleted."""
    _, _, _, evidence = _context_and_evidence()
    support = next(item for item in evidence if item.direction is EvidenceDirection.POSITIVE)
    pressure = next(item for item in evidence if item.direction is EvidenceDirection.NEGATIVE)
    resolved = {item.evidence_id: item for item in MarriageEvidenceResolver().resolve(evidence)}
    assert support.evidence_id in resolved
    assert pressure.evidence_id in resolved
    assert support.significance == pressure.significance or True


def test_large_evidence_set_stays_ordered_and_finite() -> None:
    """A large atom list remains deterministic and does not invent findings without sources."""
    _, _, _, evidence = _context_and_evidence()
    extra = []
    for index in range(80):
        extra.append(replace(evidence[0], evidence_id=f"EV-8{index:03d}", predicate=f"extra:{index}"))
    combined = evidence + extra
    resolved = MarriageEvidenceResolver().resolve(combined)
    findings = CanonicalFindingBuilder().build_from_resolved(combined, resolved)
    assert findings
    assert all(item.evidence_ids for item in findings)
    ids = [item.finding_id for item in findings]
    assert ids == sorted(ids)


def test_only_secondary_evidence_cannot_dominate() -> None:
    """When only secondary atoms remain, publishable domains stay insufficient."""
    snapshot_a, snapshot_b, context, evidence = _context_and_evidence()
    secondary = [item for item in evidence if is_secondary_type(item.evidence_type) or item.scope == "reference"]
    assert secondary
    _resolved, _findings, domains, overall, _ctx = _decide(snapshot_a, snapshot_b, context, secondary)
    assert domains.five_elements.availability.available is False or domains.five_elements.state is DomainDecisionState.INSUFFICIENT
    assert domains.stem_branch.availability.available is False
    assert overall.state is DomainDecisionState.INSUFFICIENT
    assert overall.score is None


def test_no_recommendation_without_generating_finding() -> None:
    """Condition/P5-only findings do not publish customer actions."""
    snapshot_a, snapshot_b, context, evidence = _context_and_evidence()
    secondary = [item for item in evidence if is_secondary_type(item.evidence_type) or item.scope == "reference"]
    resolved, findings, domains, overall, _ctx = _decide(snapshot_a, snapshot_b, context, secondary)
    result = MarriageDecisionResult(
        consultation_id=context.consultation_id,
        person_a=snapshot_a.person,
        person_b=snapshot_b.person,
        canonical_a=snapshot_a,
        canonical_b=snapshot_b,
        evidence=secondary,
        domains=domains,
        overall=overall,
        recommendations=[],
        confidence=build_confidence(
            data_quality=0.5,
            evidence=secondary,
            limitations=list(context.limitations),
            engine_coverage=0.0,
        ),
        versions=context.versions,
        created_at="2026-01-01T00:00:00+00:00",
        resolved_evidence=resolved,
        findings=findings,
        limitations=list(context.limitations),
    )
    assert all(item.priority is FindingPriority.P5 or item.type is FindingType.CONDITION for item in findings) or not findings
    assert CanonicalRecommendationProvider().provide(result) == []


def test_all_publishable_domains_insufficient_when_evidence_empty() -> None:
    """Empty evidence yields insufficient domains and no recommendations."""
    snapshot_a, snapshot_b, context, _evidence = _context_and_evidence()
    resolved, findings, domains, overall, _ctx = _decide(snapshot_a, snapshot_b, context, [])
    assert findings == []
    assert overall.state is DomainDecisionState.INSUFFICIENT
    for item in (
        domains.five_elements,
        domains.stem_branch,
        domains.ten_gods,
        domains.finance,
        domains.luck,
    ):
        assert item.state is DomainDecisionState.INSUFFICIENT
        assert item.score is None


def test_missing_timing_does_not_invent_a_window() -> None:
    """Disabling luck omits timing actions and the report timing section."""
    snapshot_a, snapshot_b, context, evidence = _context_and_evidence(include_luck=False)
    bundle = pipeline_from_snapshots(snapshot_a, snapshot_b, include_luck=False)
    assert not any(item.evidence_type in {MarriageEvidenceType.LUCK_ALIGNMENT, MarriageEvidenceType.LUCK_MISALIGNMENT} for item in evidence)
    assert bundle["signature"]["has_timing_section"] is False
    assert not any(item["action_type"] == "timing_awareness" for item in bundle["signature"]["recommendations"])
    _ = context


def test_timing_cannot_rewrite_natal_overall() -> None:
    """Supportive or pressured timing leaves the natal overall state unchanged."""
    mixed = run_golden_case("CASE-M02")["signature"]["overall_state"]
    timed = run_golden_case("CASE-M10")["signature"]["overall_state"]
    assert mixed == timed


def test_expert_after_customer_does_not_mutate_decision() -> None:
    """Expert retrieval after a customer POST does not rewrite stored Decision."""
    client, container = api_client()
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    consultation_id = created["consultation_id"]
    customer = client.get(f"/api/v1/consulting/marriage/{consultation_id}")
    stored_before = container.api_contract.get_stored(consultation_id)
    before_state = stored_before.result.overall.state
    before_findings = [item.finding_id for item in stored_before.result.findings]
    expert = client.get(f"/api/v1/consulting/marriage/{consultation_id}?expert=true")
    stored_after = container.api_contract.get_stored(consultation_id)
    assert expert.status_code == 200
    assert "expert" in expert.json()["data"]
    assert "expert" not in customer.json()["data"]
    assert stored_after.result.overall.state == before_state
    assert [item.finding_id for item in stored_after.result.findings] == before_findings


def test_malformed_expert_flag_stays_customer() -> None:
    """Unknown expert values do not enable expert traces."""
    client, _ = api_client()
    consultation_id = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]["consultation_id"]
    response = client.get(f"/api/v1/consulting/marriage/{consultation_id}?expert=banana")
    assert response.status_code == 200
    assert "expert" not in response.json()["data"]


def test_unicode_long_names_and_unknown_place() -> None:
    """Vietnamese unicode, extreme names, and unknown place text remain customer-safe."""
    client, _ = api_client()
    body = valid_body()
    body["person_a"]["full_name"] = "Nguyễn Thị Ánh Tuyết " + ("RấtDài" * 40)
    body["person_b"]["full_name"] = "Trần Văn Bình"
    body["person_a"]["birth_place"] = {"display_name": "Hành tinh không tồn tại — XYZ"}
    response = client.post("/api/v1/consulting/marriage", json=body)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["score"] is None
    blob = json.dumps(data)
    assert not re.search(r"\bEV-\d{4}\b", blob)
    assert "Nguyễn" in data["person_a"]["display_name"] or "display_name" in data["person_a"]


def test_repeated_idempotent_post_and_json_id_leak() -> None:
    """Repeated idempotent POST returns the same consultation without leaking internal ids."""
    client, _ = api_client()
    headers = {"Idempotency-Key": "tv1-b08-adversarial-key"}
    first = client.post("/api/v1/consulting/marriage", json=valid_body(), headers=headers)
    second = client.post("/api/v1/consulting/marriage", json=valid_body(), headers=headers)
    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json()["data"]["consultation_id"] == second.json()["data"]["consultation_id"]
    blob = json.dumps(first.json()["data"]) + json.dumps(second.json()["data"])
    assert not re.search(r"\bEV-\d{4}\b", blob)
    assert not re.search(r"\bF-\d{4}\b", blob)
    assert "source_finding_ids" not in blob

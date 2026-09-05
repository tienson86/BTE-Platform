"""Deterministic within-tier ranking, groups, and EvidenceGraph assembly."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import SCHEMA_EVIDENCE_PRIORITY
from engines.detailed_interpretation_engine.enums import EvaluationStatus, PriorityTier
from engines.detailed_interpretation_engine.evidence import EvidencePriorityFinding, EvidencePriorityResult
from engines.detailed_interpretation_engine.evidence_priority.candidates import EvidenceCandidate
from engines.detailed_interpretation_engine.evidence_priority.constants import (
    CATEGORY_INDEX,
    DOMAIN_INDEX,
    DOMAIN_ORDER,
    EVIDENCE_PRIORITY_RULESET_VERSION,
    IMPORTANCE_BY_TIER,
    SOURCE_KIND_INDEX,
    TIER_INDEX,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def sort_candidates(items: list[EvidenceCandidate]) -> list[EvidenceCandidate]:
    """Tier always beats score. Confidence cannot promote across tiers."""
    ranked = [item for item in items if not item.filtered]
    ranked.sort(
        key=lambda item: (
            TIER_INDEX.get(item.tier.value, 99),
            CATEGORY_INDEX.get(item.category, 99),
            SOURCE_KIND_INDEX.get(item.source_kind, 99),
            0 if item.category == "risk" and not item.rescued else 1,
            DOMAIN_INDEX.get(item.domain, 99),
            item.semantic_key,
        )
    )
    return ranked


def assemble_result(
    *,
    analysis_id: str,
    items: list[EvidenceCandidate],
    mc01_grade: str,
    score_engine_grade: str,
) -> EvidencePriorityResult:
    """Build the canonical EvidencePriorityResult from merged candidates."""
    ranked = sort_candidates(items)
    findings: list[EvidencePriorityFinding] = []
    for index, item in enumerate(ranked, start=1):
        finding_id = f"E-DI-EPR-{index:03d}"
        findings.append(
            EvidencePriorityFinding(
                finding_id=finding_id,
                node_id=item.node_kind or item.semantic_key,
                tier=item.tier,
                rank=index,
                domain=item.domain,
                category=item.category,
                importance=IMPORTANCE_BY_TIER.get(item.tier.value, "supporting"),
                confidence=item.confidence,
                source_refs=item.source_refs,
                supporting_evidence=item.supporting_evidence,
                conditions=tuple(part for part in item.conditions if part),
                trace_ids=item.trace_ids or (f"TR-P7-EPR-{index:03d}",),
                tier_reason=item.tier_reason,
                merge_origin=item.merge_origin or item.semantic_key,
                confidence_source=item.confidence_source,
                source_kind=item.source_kind,
                semantic_key=item.semantic_key,
                customer_label=item.customer_label,
            )
        )
    dominant = tuple(item.finding_id for item in findings if item.tier is PriorityTier.P0)
    supporting = tuple(
        item.finding_id
        for item in findings
        if item.tier in {PriorityTier.P1, PriorityTier.P2, PriorityTier.P3}
        and item.category not in {"risk", "warning"}
    )
    risk = tuple(item.finding_id for item in findings if item.category == "risk")
    opportunity = tuple(item.finding_id for item in findings if item.category == "opportunity")
    conditions = tuple(item.finding_id for item in findings if item.category == "condition")
    warnings = tuple(item.finding_id for item in findings if item.category == "warning")
    ranked_domains = _ranked_domains(findings)
    graph = _graph(findings)
    traces = tuple(trace for item in findings for trace in item.trace_ids)
    evidence_ids = tuple(item.finding_id for item in findings)
    status = EvaluationStatus.RESOLVED if findings else EvaluationStatus.NOT_EVALUATED
    confidence = ConfidenceValue(summary="structural" if findings else "unresolved")
    return EvidencePriorityResult(
        schema_version=SCHEMA_EVIDENCE_PRIORITY,
        ruleset_version=EVIDENCE_PRIORITY_RULESET_VERSION,
        analysis_id=analysis_id,
        status=status,
        dominant_evidence=dominant,
        supporting_evidence=supporting,
        risk_evidence=risk,
        opportunity_evidence=opportunity,
        conditions=conditions,
        warnings=warnings,
        ranked_domains=ranked_domains,
        graph=graph,
        confidence=confidence,
        evidence_ids=evidence_ids,
        trace_ids=traces,
        findings=tuple(findings),
        mc01_grade=mc01_grade,
        score_engine_grade=score_engine_grade,
        driver_ids=tuple(item.finding_id for item in findings if item.category == "driver"),
        bottleneck_ids=tuple(item.finding_id for item in findings if item.category == "bottleneck"),
    )


def _ranked_domains(findings: list[EvidencePriorityFinding]) -> tuple[str, ...]:
    seen: list[str] = []
    for domain in DOMAIN_ORDER:
        if any(item.domain == domain for item in findings) and domain not in seen:
            seen.append(domain)
    for item in findings:
        if item.domain and item.domain not in seen:
            seen.append(item.domain)
    return tuple(seen)


def _graph(findings: list[EvidencePriorityFinding]) -> dict[str, object]:
    nodes = [
        {
            "node_id": item.node_id,
            "kind": item.source_kind,
            "finding_id": item.finding_id,
            "label": item.customer_label,
            "tier": item.tier.value,
            "domain": item.domain,
        }
        for item in findings
    ]
    edges: list[dict[str, str]] = []
    by_semantic = {item.semantic_key: item for item in findings}
    pattern = by_semantic.get("pattern.primary")
    grade = by_semantic.get("grade.value")
    integrity = by_semantic.get("integrity.state")
    if pattern and grade:
        edges.append(_edge("depends_on", grade.finding_id, pattern.finding_id))
    if pattern and integrity:
        edges.append(_edge("qualifies", integrity.finding_id, pattern.finding_id))
    for item in findings:
        if item.source_kind == "damage" and pattern:
            edges.append(_edge("damages", item.finding_id, pattern.finding_id))
        if item.source_kind == "rescue":
            for target in item.supporting_evidence:
                damage = by_semantic.get(f"damage:{target}")
                if damage:
                    edges.append(_edge("rescues", item.finding_id, damage.finding_id))
        if item.category == "bottleneck" and pattern:
            edges.append(_edge("damages", item.finding_id, pattern.finding_id))
        if item.source_kind == "shen_sha_cluster" and pattern:
            edges.append(_edge("strengthens", item.finding_id, pattern.finding_id))
        if item.source_kind == "combination" and pattern:
            relation = "damages" if item.category == "risk" else "supports"
            edges.append(_edge(relation, item.finding_id, pattern.finding_id))
    return {"nodes": nodes, "edges": edges}


def _edge(relation: str, source: str, target: str) -> dict[str, str]:
    return {
        "edge_id": f"N-DI-EPR-{relation}-{source}-{target}",
        "source": source,
        "target": target,
        "relation": relation,
    }

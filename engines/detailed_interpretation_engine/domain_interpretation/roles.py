"""Pick domain-scoped driver / support / bottleneck from ranked evidence."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    DOMAIN_SCOPES,
    SHEN_SHA_SOURCE_KINDS,
    TIER_RANK,
)
from engines.detailed_interpretation_engine.evidence import EvidencePriorityFinding, EvidencePriorityResult
from engines.detailed_interpretation_engine.evidence_priority.labels import DAMAGE_LABELS

_ROLE_CATEGORY = {
    "driver": ("driver",),
    "support": ("supporting", "combination", "balance"),
    "bottleneck": ("bottleneck", "risk"),
    "risk": ("risk", "warning"),
    "opportunity": ("opportunity",),
    "condition": ("condition",),
}


def scoped_findings(
    ep: EvidencePriorityResult,
    domain_id: str,
    *,
    allow_shen_sha: bool = False,
) -> tuple[EvidencePriorityFinding, ...]:
    """Findings already ranked by Evidence Priority for this domain's scope."""
    scope = DOMAIN_SCOPES.get(domain_id, frozenset({domain_id}))
    items: list[EvidencePriorityFinding] = []
    for finding in ep.findings:
        if finding.domain not in scope and finding.domain != domain_id:
            continue
        if not allow_shen_sha and finding.source_kind in SHEN_SHA_SOURCE_KINDS:
            continue
        items.append(finding)
    return tuple(items)


def copied_priority(findings: tuple[EvidencePriorityFinding, ...]) -> str:
    """Copy the best existing EP tier. Do not recompute rank."""
    if not findings:
        return ""
    best = min(findings, key=lambda item: (TIER_RANK.get(item.tier.value, 9), item.rank))
    return best.tier.value


def pick_role(
    findings: tuple[EvidencePriorityFinding, ...],
    role: str,
    ep: EvidencePriorityResult | None = None,
) -> EvidencePriorityFinding | None:
    """Select the first EP finding already tagged for this domain role."""
    wanted = _ROLE_CATEGORY.get(role, (role,))
    ranked = sorted(findings, key=lambda item: (TIER_RANK.get(item.tier.value, 9), item.rank))
    for finding in ranked:
        if finding.category in wanted:
            return finding
    if role == "driver" and ep is not None:
        return _by_ids(ep, ep.driver_ids, findings)
    if role == "bottleneck" and ep is not None:
        return _by_ids(ep, ep.bottleneck_ids, findings)
    if role == "risk" and ep is not None:
        return _by_ids(ep, ep.risk_evidence, findings)
    if role == "opportunity" and ep is not None:
        return _by_ids(ep, ep.opportunity_evidence, findings)
    if role == "condition" and ep is not None:
        return _by_ids(ep, ep.conditions, findings)
    return None


def shen_sha_findings(ep: EvidencePriorityResult, domain_id: str) -> tuple[EvidencePriorityFinding, ...]:
    """Secondary Shen Sha only. Never used as driver or state."""
    scope = DOMAIN_SCOPES.get(domain_id, frozenset({domain_id}))
    return tuple(
        item
        for item in ep.findings
        if item.source_kind in SHEN_SHA_SOURCE_KINDS
        and (item.domain in scope or item.domain == domain_id)
    )


def evidence_ids_of(findings: tuple[EvidencePriorityFinding, ...]) -> tuple[str, ...]:
    """Stable finding ids already issued by Evidence Priority."""
    return tuple(item.finding_id for item in findings if item.finding_id)


def trace_ids_of(domain_id: str, findings: tuple[EvidencePriorityFinding, ...]) -> tuple[str, ...]:
    """Domain trace plus consumed EP traces."""
    traces = [f"TR-P7-DOM-{domain_id}"]
    for item in findings:
        traces.extend(item.trace_ids)
    return tuple(dict.fromkeys(traces))


def label_of(finding: EvidencePriorityFinding | None, fallback: str = "") -> str:
    """Customer label already published by Evidence Priority."""
    if finding is None:
        return fallback
    text = finding.customer_label.strip()
    if text and "TR-P7" not in text and not text.startswith("E-DI-"):
        return text
    return fallback


def damage_risk_label(damage_types: tuple[str, ...]) -> str:
    """Reuse frozen damage copy when a domain risk is that damage."""
    for item in damage_types:
        mapped = DAMAGE_LABELS.get(item)
        if mapped:
            return mapped
    return ""


def _by_ids(
    ep: EvidencePriorityResult,
    ids: tuple[str, ...],
    scoped: tuple[EvidencePriorityFinding, ...],
) -> EvidencePriorityFinding | None:
    lookup = {item.finding_id: item for item in ep.findings}
    scoped_ids = {item.finding_id for item in scoped}
    for finding_id in ids:
        item = lookup.get(finding_id)
        if item is None:
            continue
        if item.source_kind in SHEN_SHA_SOURCE_KINDS:
            continue
        if item.finding_id not in scoped_ids:
            continue
        return item
    return None

"""Application Composer — map implications to customer domains. No predictions."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAINS,
    KIND_APPLICATION,
)
from engines.interpretation_engine.foundation.narrative.mapping import (
    map_customer_domain,
    rank_key,
)
from engines.interpretation_engine.foundation.narrative.models import (
    ApplicationItem,
    EvidenceGraph,
    EvidenceNode,
)
from engines.interpretation_engine.foundation.narrative.text import fingerprint


def compose_applications(graph: EvidenceGraph) -> tuple[ApplicationItem, ...]:
    """Map interpreted knowledge into supported customer domains.

    Duplicate implications for the same domain keep the higher-ranked copy.
    Outcomes are not predicted.
    """
    ranked = sorted(
        [node for node in graph.nodes if node.kind == KIND_APPLICATION],
        key=lambda item: rank_key(item.domain, item.importance, item.confidence),
        reverse=True,
    )
    chosen: dict[tuple[str, str], ApplicationItem] = {}
    index = 0
    for node in ranked:
        item = _application_from_node(node, index)
        if item is None:
            continue
        index += 1
        key = (item.customer_domain, fingerprint(item.statement))
        existing = chosen.get(key)
        if existing is None:
            chosen[key] = item
            continue
        chosen[key] = ApplicationItem(
            application_id=existing.application_id,
            customer_domain=existing.customer_domain,
            statement=existing.statement,
            evidence_ids=tuple(
                dict.fromkeys([*existing.evidence_ids, *item.evidence_ids])
            ),
            bundle_id=existing.bundle_id,
            domain=existing.domain,
            confidence=existing.confidence,
            importance=existing.importance,
        )
    ordered = sorted(
        chosen.values(),
        key=lambda item: (
            CUSTOMER_DOMAINS.index(item.customer_domain),
            -rank_key(item.domain, item.importance, item.confidence)[0],
        ),
    )
    return tuple(ordered)


def _application_from_node(node: EvidenceNode, index: int) -> ApplicationItem | None:
    """Drop applications that are not in the supported customer-domain set."""
    domain = node.customer_domain or map_customer_domain(_area_prefix(node.statement))
    if domain not in CUSTOMER_DOMAINS:
        return None
    return ApplicationItem(
        application_id=f"app:{node.bundle_id}:{index}",
        customer_domain=domain,
        statement=node.statement,
        evidence_ids=(node.evidence_id, *node.alias_ids),
        bundle_id=node.bundle_id,
        domain=node.domain,
        confidence=node.confidence,
        importance=node.importance,
    )


def _area_prefix(statement: str) -> str:
    """Read an optional `area:` prefix already present on mapped impacts."""
    if ":" not in statement:
        return ""
    return statement.split(":", 1)[0]

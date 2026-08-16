"""Customer-domain mapping, evidence identity, and ranking."""

from __future__ import annotations

from typing import Callable, TypeVar

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_ALIASES,
    CUSTOMER_DOMAIN_DECISION,
    CUSTOMER_DOMAINS,
    DOMAIN_DEFAULT_TOPIC,
    DOMAIN_PRIORITY,
    QUALITY_TRUTH_MARKERS,
    RANK_KEEP_RATIO,
)

T = TypeVar("T")


def map_customer_domain(raw: str) -> str:
    """Map a knowledge application key to a supported customer domain.

    Unknown keys are dropped. No new domains are invented.
    """
    key = str(raw or "").strip()
    if key in CUSTOMER_DOMAINS:
        return key
    return CUSTOMER_DOMAIN_ALIASES.get(key.casefold().replace("-", "_"), "")


def default_topic(domain: str) -> str:
    """Bundle default customer topic. Not an invented implication."""
    return DOMAIN_DEFAULT_TOPIC.get(domain, "")


def customer_relevance(customer_domain: str, engine_truth_ref: str = "") -> float:
    """Higher when the statement already maps to a customer topic or quality gate."""
    relevance = 0.5
    if customer_domain in CUSTOMER_DOMAINS:
        relevance += 0.4
    ref = engine_truth_ref.casefold()
    if any(marker in ref for marker in QUALITY_TRUTH_MARKERS):
        relevance += 0.3
    return min(relevance, 1.0)


def rank_key(
    domain: str,
    importance: float,
    confidence: float,
    relevance: float = 0.5,
) -> tuple[float, float, float, int]:
    """Sort key: importance, confidence, customer relevance, bundle priority."""
    return (
        importance,
        confidence,
        relevance,
        DOMAIN_PRIORITY.get(domain, 0),
    )


def rank_score(
    domain: str,
    importance: float,
    confidence: float,
    relevance: float = 0.5,
) -> float:
    """Scalar rank used to drop lower-coverage copies inside a topic."""
    importance_v, confidence_v, relevance_v, priority = rank_key(
        domain, importance, confidence, relevance
    )
    return (
        importance_v * 4.0
        + confidence_v * 3.0
        + relevance_v * 2.0
        + (priority / 100.0)
    )


def keep_ranked(items: list[T], score_of: Callable[[T], float]) -> list[T]:
    """Keep items within the topic's coverage band. Not a fixed sentence cap."""
    if not items:
        return []
    scores = [float(score_of(item)) for item in items]
    floor = max(scores) * RANK_KEEP_RATIO
    return [item for item, score in zip(items, scores) if score >= floor]


def narrative_topic(
    customer_domain: str,
    domain: str,
    engine_truth_ref: str = "",
) -> str:
    """Customer topic for a copied statement. Quality-gate refs stay Decision."""
    if customer_domain in CUSTOMER_DOMAINS:
        return customer_domain
    ref = str(engine_truth_ref or "").casefold()
    if any(marker in ref for marker in QUALITY_TRUTH_MARKERS):
        return CUSTOMER_DOMAIN_DECISION
    return default_topic(domain)


def evidence_identity(kind: str, engine_truth_ref: str, evidence_id: str) -> str:
    """Stable evidence identity. Prefer engine truth over surface wording."""
    ref = str(engine_truth_ref or "").strip().casefold()
    if ref:
        return f"{kind}:{ref}"
    return f"{kind}:{evidence_id}"

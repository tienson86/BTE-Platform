"""Customer-domain mapping and bundle ranking."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_ALIASES,
    CUSTOMER_DOMAINS,
    DOMAIN_PRIORITY,
)


def map_customer_domain(raw: str) -> str:
    """Map a knowledge application key to a supported customer domain.

    Unknown keys are dropped. No new domains are invented.
    """
    key = str(raw or "").strip()
    if key in CUSTOMER_DOMAINS:
        return key
    return CUSTOMER_DOMAIN_ALIASES.get(key.casefold().replace("-", "_"), "")


def rank_key(domain: str, importance: float, confidence: float) -> tuple[int, float, float]:
    """Sort key: domain priority, then importance, then confidence."""
    return (DOMAIN_PRIORITY.get(domain, 0), importance, confidence)

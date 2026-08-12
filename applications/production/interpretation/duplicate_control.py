"""Deterministic cross-domain duplicate control — no LLM rewrite."""

from __future__ import annotations

from applications.production.interpretation.contracts import DomainClaim
from applications.production.interpretation.theme_keys import THEME_PRIMARY_DOMAIN


def apply_duplicate_policy(
    claims: list[DomainClaim],
) -> tuple[list[DomainClaim], list[str]]:
    """Keep one claim per theme — preferred domain wins.

    Returns kept claims and suppressed claim_ids.
    """
    by_theme: dict[str, list[DomainClaim]] = {}
    for claim in claims:
        by_theme.setdefault(claim.theme_id, []).append(claim)

    kept: list[DomainClaim] = []
    suppressed: list[str] = []
    for theme_id, theme_claims in sorted(by_theme.items()):
        preferred = THEME_PRIMARY_DOMAIN.get(theme_id)
        winner: DomainClaim | None = None
        if preferred:
            for claim in theme_claims:
                if claim.domain == preferred:
                    winner = claim
                    break
        if winner is None:
            winner = theme_claims[0]
        kept.append(winner)
        for claim in theme_claims:
            if claim.claim_id != winner.claim_id:
                suppressed.append(claim.claim_id)
    return kept, suppressed

"""Cross-domain integration — claims/themes, not prose concatenation."""

from __future__ import annotations

from applications.production.interpretation.conflict_control import (
    customer_safe_claims,
    detect_conflicts,
)
from applications.production.interpretation.contracts import (
    DomainInterpretationResult,
    DomainStatus,
    IntegratedInterpretationContext,
)
from applications.production.interpretation.duplicate_control import apply_duplicate_policy


class CrossDomainIntegrator:
    """Integrate domain interpretations into a structured context."""

    def integrate(
        self,
        domains: dict[str, DomainInterpretationResult],
    ) -> IntegratedInterpretationContext:
        """Extract claims, themes, recommendations; apply duplicate/conflict policy."""
        all_claims = []
        recommendations: list[str] = []
        warnings: list[str] = []
        missing_domains: list[str] = []

        for domain_name, result in domains.items():
            if result.status in {
                DomainStatus.NOT_AVAILABLE,
                DomainStatus.INSUFFICIENT,
            }:
                missing_domains.append(domain_name)
                continue
            all_claims.extend(result.claims)
            recommendations.extend(result.recommendations)
            if result.missing_data:
                warnings.append(
                    f"{domain_name}: missing {', '.join(result.missing_data)}"
                )

        kept_claims, suppressed = apply_duplicate_policy(all_claims)
        conflicts = detect_conflicts(domains)
        safe = customer_safe_claims(domains, conflicts)
        for domain_name, text in safe.items():
            if domain_name in domains:
                domains[domain_name].conclusion = text

        themes = sorted({claim.theme_id for claim in kept_claims})
        # Deduplicate recommendations preserving order.
        unique_recs: list[str] = []
        seen: set[str] = set()
        for item in recommendations:
            key = item.strip().lower()
            if key and key not in seen:
                seen.add(key)
                unique_recs.append(item)

        return IntegratedInterpretationContext(
            claims=kept_claims,
            themes=themes,
            recommendations=unique_recs[:8],
            warnings=warnings,
            missing_domains=missing_domains,
            conflicts=conflicts,
            suppressed_duplicates=suppressed,
            domain_results=domains,
        )

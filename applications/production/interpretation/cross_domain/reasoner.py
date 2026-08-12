"""Cross-Domain Reasoning Engine — deterministic entry point."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.claim_normalizer import (
    normalize_claims,
)
from applications.production.interpretation.cross_domain.executive_plan import (
    build_executive_claim_plan,
)
from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningInput,
    CrossDomainReasoningResult,
    RelationType,
    ThemeStatus,
)
from applications.production.interpretation.cross_domain.relation_engine import (
    detect_relations,
)
from applications.production.interpretation.cross_domain.theme_engine import (
    derive_themes,
)

ENGINE_VERSION = "1.1.0"


class CrossDomainReasoner:
    """Reason across domains — no prose, no LLM, no case branches."""

    def reason(self, data: CrossDomainReasoningInput) -> CrossDomainReasoningResult:
        """Produce CrossDomainReasoningResult from canonical input."""
        claims = normalize_claims(data)
        relations = detect_relations(claims)
        themes = derive_themes(claims, relations, data.question_context)
        plan = build_executive_claim_plan(claims, themes, relations)

        agreements: list[str] = []
        tensions: list[str] = []
        conflicts: list[str] = []
        unresolved: list[str] = []
        customer_safe: list[str] = []

        for relation in relations:
            rid = relation.relation_id
            if relation.relation_type in {
                RelationType.AGREEMENT,
                RelationType.REINFORCEMENT,
            }:
                agreements.append(rid)
            elif relation.relation_type in {
                RelationType.CONDITIONAL_NUANCE,
                RelationType.DEPENDENCY_OVERRIDE,
                RelationType.DIFFERENT_SCOPE,
            }:
                tensions.append(rid)
            elif relation.relation_type == RelationType.TRUE_CONFLICT:
                conflicts.append(rid)
            elif relation.relation_type == RelationType.UNRESOLVED:
                unresolved.append(rid)
            if relation.unresolved_blocker:
                unresolved.append(relation.unresolved_blocker)
            if relation.customer_safe_state:
                customer_safe.append(relation.customer_safe_state)

        primary = next(
            (t for t in themes if t.status == ThemeStatus.PRIMARY),
            None,
        )
        suppressed = [
            t.theme_id for t in themes if t.status == ThemeStatus.SUPPRESSED
        ]

        versions = dict(data.versions)
        versions["cross_domain_reasoner"] = ENGINE_VERSION

        return CrossDomainReasoningResult(
            claims=claims,
            relations=relations,
            agreements=agreements,
            tensions=tensions,
            conflicts=conflicts,
            unresolved=sorted(set(unresolved)),
            themes=themes,
            primary_theme=primary.theme_id if primary else "",
            executive_claim_plan=plan,
            question_context=data.question_context,
            customer_safe_conclusions=list(dict.fromkeys(customer_safe)),
            diagnostics={
                "missing_domains": list(data.missing_domains),
                "suppressed_themes": suppressed,
                "claim_count": len(claims),
                "relation_count": len(relations),
                "primary_theme_label": primary.label if primary else "",
                "why_primary": (
                    {
                        "theme_id": primary.theme_id,
                        "salience": primary.salience,
                        "customer_value": primary.customer_value,
                        "supporting_claims": list(primary.supporting_claims),
                        "domains": list(primary.domains),
                    }
                    if primary
                    else {}
                ),
            },
            versions=versions,
        )

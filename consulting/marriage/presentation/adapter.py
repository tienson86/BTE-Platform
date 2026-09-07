"""Semantic presentation adapter. Maps Decision facts. Does not invent score or actions."""

from __future__ import annotations

from consulting.marriage.dto.presentation import (
    MarriageConfidenceView,
    MarriageDomainView,
    MarriageFindingView,
    MarriageHeroView,
    MarriageIdentityView,
    MarriagePresentationResult,
    MarriageRecommendationView,
    MarriageTimingView,
)
from consulting.marriage.models.decision import MarriageDomainDecision
from consulting.marriage.models.enums import FindingType, MarriageDomain
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.presentation.contract import MarriagePresentationAdapter
from consulting.marriage.presentation.labels import (
    CONFIDENCE_LABEL,
    DOMAIN_TITLE,
    GENDER_DISPLAY,
    OPTIONAL_DOMAINS,
    OVERALL_STATE_HEADLINE,
    OVERALL_STATE_LABEL,
    PRIORITY_LABEL,
    SEMANTIC_UNAVAILABLE,
)


class SemanticMarriagePresentationAdapter(MarriagePresentationAdapter):
    """TV1-B07 customer presentation mapping. Score and grade stay unavailable."""

    def adapt(self, decision: MarriageDecisionResult) -> MarriagePresentationResult:
        """Build a presentation result from factual Decision fields only."""
        overall = decision.overall
        state = overall.state
        headline = OVERALL_STATE_HEADLINE.get(state, "") if state else ""
        state_label = OVERALL_STATE_LABEL.get(state, "") if state else ""
        strengths = _findings_of(decision, FindingType.STRENGTH, FindingType.SUPPORT)
        risks = _findings_of(decision, FindingType.RISK, FindingType.BOTTLENECK)
        return MarriagePresentationResult(
            identity=MarriageIdentityView(
                person_a_name=decision.person_a.display_name,
                person_b_name=decision.person_b.display_name,
                person_a_gender_display=GENDER_DISPLAY.get(decision.person_a.gender),
                person_b_gender_display=GENDER_DISPLAY.get(decision.person_b.gender),
            ),
            hero=MarriageHeroView(
                score_display=SEMANTIC_UNAVAILABLE,
                grade_display=SEMANTIC_UNAVAILABLE,
                title=headline,
                summary=f"Nền tảng hiện ở trạng thái: {state_label}" if state_label else headline,
                top_strengths=[item.title for item in strengths[:3]],
                top_risks=[item.title for item in risks[:3]],
            ),
            strengths=strengths,
            risks=risks,
            domains=_published_domains(decision),
            recommendations=_recommendations(decision),
            confidence=MarriageConfidenceView(
                level_display=CONFIDENCE_LABEL.get(decision.confidence.level, ""),
                summary=None,
                limitations=list(decision.limitations),
            ),
            timing=_timing(decision),
            disclaimer=None,
        )


def _findings_of(
    decision: MarriageDecisionResult,
    *kinds: FindingType,
) -> list[MarriageFindingView]:
    """Copy finding identity labels. Do not expose internal finding ids to titles."""
    allowed = set(kinds)
    views: list[MarriageFindingView] = []
    for item in decision.findings:
        if item.type not in allowed:
            continue
        title = "Điểm hỗ trợ" if item.type in {FindingType.STRENGTH, FindingType.SUPPORT} else "Điểm cần lưu ý"
        views.append(
            MarriageFindingView(
                finding_id=item.finding_id,
                title=title,
                summary=title,
                domain=item.domain.value,
            )
        )
    return views


def _published_domains(decision: MarriageDecisionResult) -> list[MarriageDomainView]:
    """Render only domains with a publishable semantic state."""
    views: list[MarriageDomainView] = []
    for item in _iter_domains(decision):
        if not _is_published(item):
            continue
        state = item.state.value if item.state else None
        views.append(
            MarriageDomainView(
                domain=item.domain.value,
                title=DOMAIN_TITLE.get(item.domain, item.domain.value),
                summary=state or "",
                score_display=None,
                grade_display=None,
                available=True,
            )
        )
    return views


def _recommendations(decision: MarriageDecisionResult) -> list[MarriageRecommendationView]:
    """Copy B04 recommendation identities. Do not create new actions."""
    views: list[MarriageRecommendationView] = []
    for item in decision.recommendations:
        priority = None
        if item.action_priority is not None:
            priority = PRIORITY_LABEL.get(item.action_priority, item.action_priority.value)
        views.append(
            MarriageRecommendationView(
                recommendation_id=item.recommendation_id,
                title=item.action_type.value,
                summary=item.objective or item.action_type.value,
                priority=priority,
            )
        )
    return views


def _timing(decision: MarriageDecisionResult) -> MarriageTimingView | None:
    """Return timing only when the Decision actually published it."""
    luck = decision.domains.luck
    if not _is_published(luck):
        return None
    if decision.timing is None:
        return None
    return MarriageTimingView(summary=luck.state.value if luck.state else "", periods=[])


def _iter_domains(decision: MarriageDecisionResult) -> tuple[MarriageDomainDecision, ...]:
    """Frozen domain order from Decision."""
    domains = decision.domains
    return (
        domains.five_elements,
        domains.stem_branch,
        domains.ten_gods,
        domains.finance,
        domains.luck,
        domains.interaction,
        domains.family,
        domains.children,
    )


def _is_published(domain: MarriageDomainDecision) -> bool:
    """True when the domain has a customer-visible semantic state."""
    if domain.domain in OPTIONAL_DOMAINS:
        if not domain.availability.available or domain.state is None:
            return False
        if domain.state.value == "insufficient":
            return False
    if not domain.availability.available or domain.state is None:
        return False
    return domain.state.value != "insufficient"


def unpublished_optional_domains(decision: MarriageDecisionResult) -> list[MarriageDomain]:
    """Optional domains omitted from cards because Decision marked them insufficient."""
    omitted: list[MarriageDomain] = []
    lookup = {
        MarriageDomain.INTERACTION: decision.domains.interaction,
        MarriageDomain.FAMILY: decision.domains.family,
        MarriageDomain.CHILDREN: decision.domains.children,
    }
    for domain, item in lookup.items():
        if not _is_published(item):
            omitted.append(domain)
    return omitted

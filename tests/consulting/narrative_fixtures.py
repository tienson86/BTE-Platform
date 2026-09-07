"""Shared helpers for TV1-B05 narrative and report tests."""

from __future__ import annotations

from consulting.marriage.narrative.composer import CanonicalNarrativeComposer
from consulting.marriage.narrative.input import NarrativeInput, narrative_input_from_decision
from consulting.marriage.narrative.versions import AUDIENCE_CUSTOMER, LANGUAGE_VI
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.report.profile import MarriageReportProfileV1
from consulting.marriage.models.narrative import MarriageNarrativeResult
from consulting.marriage.models.report import MarriageReportModel
from consulting.marriage.models.result import MarriageDecisionResult
from tests.consulting.decision_fixtures import build_test_decision


def decision_with_recommendations() -> MarriageDecisionResult:
    """B03 decision plus frozen B04 recommendations. No narrative mutation."""
    decision = build_test_decision()
    decision.recommendations = CanonicalRecommendationProvider().provide(decision)
    return decision


def compose_narrative(
    decision: MarriageDecisionResult | None = None,
) -> tuple[MarriageDecisionResult, NarrativeInput, MarriageNarrativeResult]:
    """Compose narrative from Decision/Recommendation only."""
    result = decision if decision is not None else decision_with_recommendations()
    payload = narrative_input_from_decision(
        result,
        language=LANGUAGE_VI,
        audience=AUDIENCE_CUSTOMER,
    )
    narrative = CanonicalNarrativeComposer().compose(payload)
    return result, payload, narrative


def compose_report_bundle(
    decision: MarriageDecisionResult | None = None,
) -> tuple[MarriageDecisionResult, NarrativeInput, MarriageNarrativeResult, MarriageReportModel]:
    """Compose narrative and semantic report together."""
    result, payload, narrative = compose_narrative(decision)
    report = MarriageReportProfileV1().compose(payload, narrative)
    return result, payload, narrative, report

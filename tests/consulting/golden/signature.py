"""TV-01 Golden semantic signature. Freezes meaning, not IDs or prose."""

from __future__ import annotations

from typing import Any

from consulting.marriage.models.narrative import MarriageNarrativeResult
from consulting.marriage.models.report import MarriageReportModel
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.narrative.composer import CanonicalNarrativeComposer
from consulting.marriage.narrative.input import narrative_input_from_decision
from consulting.marriage.narrative.versions import AUDIENCE_CUSTOMER, LANGUAGE_VI
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from consulting.marriage.report.profile import MarriageReportProfileV1
from tests.consulting.decision_fixtures import build_test_decision


def pipeline_from_snapshots(snapshot_a, snapshot_b, **policy_kwargs: object) -> dict[str, Any]:
    """Run Decision → Recommendation → Narrative → Report and return a signature."""
    decision = build_test_decision(snapshot_a, snapshot_b, **policy_kwargs)
    decision.recommendations = CanonicalRecommendationProvider().provide(decision)
    payload = narrative_input_from_decision(
        decision,
        language=LANGUAGE_VI,
        audience=AUDIENCE_CUSTOMER,
    )
    narrative = CanonicalNarrativeComposer().compose(payload)
    report = MarriageReportProfileV1().compose(payload, narrative)
    return {
        "decision": decision,
        "narrative": narrative,
        "report": report,
        "signature": semantic_signature(decision, narrative, report),
    }


def semantic_signature(
    decision: MarriageDecisionResult,
    narrative: MarriageNarrativeResult,
    report: MarriageReportModel,
) -> dict[str, Any]:
    """Stable semantic truth. Omits consultation_id, timestamps, and full prose."""
    domains = decision.domains
    domain_map = {
        "five_elements": domains.five_elements,
        "stem_branch": domains.stem_branch,
        "ten_gods": domains.ten_gods,
        "interaction": domains.interaction,
        "finance": domains.finance,
        "family": domains.family,
        "children": domains.children,
        "luck": domains.luck,
    }
    return {
        "overall_state": decision.overall.state.value if decision.overall.state else None,
        "score": decision.overall.score,
        "grade": None if decision.overall.grade is None else decision.overall.grade.value,
        "confidence_level": decision.confidence.level.value,
        "limitations": list(decision.limitations),
        "domain_availability": {
            key: item.availability.available for key, item in domain_map.items()
        },
        "domain_states": {
            key: item.state.value if item.state else None for key, item in domain_map.items()
        },
        "evidence": [
            {
                "type": item.evidence_type.value,
                "subject": item.subject.value,
                "direction": item.direction.value,
                "domain": item.domain.value,
                "predicate": item.predicate,
            }
            for item in decision.evidence
        ],
        "findings": [
            {
                "semantic_key": item.semantic_key,
                "type": item.type.value,
                "domain": item.domain.value,
                "priority": item.priority.value,
                "source_count": len(item.evidence_ids),
            }
            for item in decision.findings
        ],
        "recommendations": [
            {
                "action_type": item.action_type.value,
                "domain": item.domain.value,
                "objective": item.objective,
                "priority": item.action_priority.value if item.action_priority else None,
                "urgency": item.urgency.value if item.urgency else None,
                "timing_key": item.timing_key,
                "source_count": len(item.source_finding_ids),
            }
            for item in decision.recommendations
        ],
        "narrative_keys": [
            block.catalog_key
            for section in narrative.sections
            for block in section.blocks
            if block.catalog_key
        ],
        "report_sections": [item.section_id for item in report.sections],
        "has_timing_section": any(item.section_id == "timing" for item in report.sections),
    }


def evidence_type_set(signature: dict[str, Any]) -> set[str]:
    """Return unique evidence types from a signature."""
    return {item["type"] for item in signature["evidence"]}


def recommendation_types(signature: dict[str, Any]) -> set[str]:
    """Return unique recommendation action types from a signature."""
    return {item["action_type"] for item in signature["recommendations"]}

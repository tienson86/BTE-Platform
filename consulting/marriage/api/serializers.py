"""Public DTO serialization. Copies B05 semantics. Does not compose new wording."""

from __future__ import annotations

from consulting.marriage.assessment.projector import project_marriage_assessment
from consulting.marriage.api.versions import API_VERSION, API_VERSION_TOKEN
from consulting.marriage.dto.history import MarriageHistoryRecord, MarriageStoredResult
from consulting.marriage.dto.response import MarriageConsultationSummary, RuntimeError, RuntimeWarning
from consulting.marriage.models.decision import MarriageDomainDecision
from consulting.marriage.models.enums import MarriageDomain, MarriageRuntimeStatus
from consulting.marriage.models.narrative import MarriageNarrativeResult
from consulting.marriage.models.report import MarriageReportModel, ReportBlock, ReportSection
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.report.access import customer_sections, expert_sections
from consulting.marriage.report.versions import report_profile_token

_PUBLIC_ERROR_MESSAGES = {
    "VALIDATION_ERROR": "Request validation failed.",
    "NOT_FOUND": "The requested consultation was not found.",
    "CONFLICT": "The idempotency key conflicts with a different request.",
    "INTERNAL_ERROR": "An unexpected error occurred.",
}

_WARNING_DESCRIPTIONS = {
    "BIRTH_TIME_UNKNOWN": "Birth time was not provided. This is a data limitation, not a marital indication.",
    "TIMEZONE_UNSPECIFIED": "Timezone was not provided.",
    "DOMAIN_UNAVAILABLE": "This domain does not have enough structural data.",
    "TIMING_UNAVAILABLE": "Timing coverage is not available for this consultation.",
}

_OPTIONAL_DOMAINS = (
    MarriageDomain.INTERACTION,
    MarriageDomain.FAMILY,
    MarriageDomain.CHILDREN,
)


def public_version_bundle(result: MarriageDecisionResult) -> dict[str, str | None]:
    """API v1 plus bound behavior versions. Versions stay independent."""
    return {
        "api_version": API_VERSION,
        "api_contract": API_VERSION_TOKEN,
        "module_version": result.versions.module_version,
        "policy_version": result.versions.decision_profile_version,
        "score_model_version": result.versions.score_model_version,
        "narrative_version": result.versions.narrative_version,
        "report_profile_version": report_profile_token(),
    }


def serialize_error(
    *,
    code: str,
    stage: str,
    retryable: bool = False,
    consultation_id: str | None = None,
    trace_id: str | None = None,
    detail: str | None = None,
) -> dict[str, object]:
    """Build a public error object. No traceback or filesystem paths."""
    message = _PUBLIC_ERROR_MESSAGES.get(code, _PUBLIC_ERROR_MESSAGES["INTERNAL_ERROR"])
    if code == "VALIDATION_ERROR" and detail and _is_safe_detail(detail):
        message = detail
    return {
        "code": code,
        "stage": stage,
        "message": message,
        "retryable": retryable,
        "consultation_id": consultation_id,
        "trace_id": trace_id or consultation_id,
    }


def serialize_warning(warning: RuntimeWarning) -> dict[str, str | None]:
    """Serialize a structured warning. Missing hour is not marital risk."""
    description = _WARNING_DESCRIPTIONS.get(warning.code, warning.message_key or warning.code)
    return {
        "code": warning.code,
        "description": description,
        "affected_domain": warning.affected_domain,
    }


def collect_warnings(stored: MarriageStoredResult) -> list[dict[str, str | None]]:
    """Runtime warnings plus unavailable-domain notices. Does not change Decision."""
    items = [serialize_warning(item) for item in stored.warnings]
    domains = stored.result.domains
    for domain in (domains.interaction, domains.family, domains.children):
        if not _domain_published(domain):
            items.append(
                {
                    "code": "DOMAIN_UNAVAILABLE",
                    "description": _WARNING_DESCRIPTIONS["DOMAIN_UNAVAILABLE"],
                    "affected_domain": domain.domain.value,
                }
            )
    if not _domain_published(domains.luck):
        items.append(
            {
                "code": "TIMING_UNAVAILABLE",
                "description": _WARNING_DESCRIPTIONS["TIMING_UNAVAILABLE"],
                "affected_domain": MarriageDomain.LUCK.value,
            }
        )
    return items


def serialize_consultation(stored: MarriageStoredResult, *, expert: bool) -> dict[str, object]:
    """Public consultation resource. Customer mode hides internal ids."""
    result = stored.result
    overall = result.overall
    payload: dict[str, object] = {
        "consultation_id": result.consultation_id,
        "status": stored.status.value,
        "created_at": result.created_at,
        "person_a": _person_summary(result, "a"),
        "person_b": _person_summary(result, "b"),
        "overall_state": overall.state.value if overall.state else None,
        "score": None,
        "grade": None,
        "confidence": {
            "level": result.confidence.level.value,
            "overall": result.confidence.overall,
        },
        "limitations": list(result.limitations),
        "versions": public_version_bundle(result),
        "headline": _headline(stored.narrative),
        "action_themes": _action_themes(result),
        "assessment_cards": serialize_assessment_cards(result),
    }
    if expert:
        payload["expert"] = _expert_trace(stored)
    return payload


def serialize_summary(stored: MarriageStoredResult) -> dict[str, object]:
    """Lightweight summary. No Evidence/Finding graph."""
    result = stored.result
    report = stored.report_model
    return {
        "consultation_id": result.consultation_id,
        "overall_state": result.overall.state.value if result.overall.state else None,
        "headline": _headline(stored.narrative),
        "executive_summary": _section_body(report, "executive_summary"),
        "top_strengths": _section_titles(report, "strengths"),
        "top_risks": _section_titles(report, "risks"),
        "top_action_themes": _action_themes(result),
        "assessment_cards": serialize_assessment_cards(result),
        "confidence": {
            "level": result.confidence.level.value,
            "overall": result.confidence.overall,
        },
        "limitations": list(result.limitations),
        "score": None,
        "grade": None,
    }


def summary_dto(stored: MarriageStoredResult) -> MarriageConsultationSummary:
    """ABC summary wrapper. Correlation ids are not Canonical-native analysis ids."""
    data = serialize_summary(stored)
    confidence = data["confidence"]
    assert isinstance(confidence, dict)
    return MarriageConsultationSummary(
        consultation_id=stored.result.consultation_id,
        person_a_analysis_id=stored.result.person_a.analysis_id,
        person_b_analysis_id=stored.result.person_b.analysis_id,
        score=None,
        grade=None,
        confidence=stored.result.confidence.overall,
        overall_state=str(data["overall_state"]) if data["overall_state"] else None,
        headline=str(data["headline"]) if data["headline"] else None,
        executive_summary=str(data["executive_summary"]) if data["executive_summary"] else None,
        top_strengths=list(data["top_strengths"]) if isinstance(data["top_strengths"], list) else [],
        top_risks=list(data["top_risks"]) if isinstance(data["top_risks"], list) else [],
        top_action_themes=list(data["top_action_themes"]) if isinstance(data["top_action_themes"], list) else [],
        limitations=list(stored.result.limitations),
        confidence_level=stored.result.confidence.level.value,
    )


def serialize_report(stored: MarriageStoredResult, *, expert: bool) -> dict[str, object]:
    """Semantic report resource. No renderer data."""
    model = stored.report_model
    if model is None:
        return {
            "consultation_id": stored.result.consultation_id,
            "score": None,
            "grade": None,
            "sections": [],
        }
    sections = expert_sections(model) if expert else customer_sections(model)
    return {
        "consultation_id": stored.result.consultation_id,
        "score": None,
        "grade": None,
        "metadata": {
            "consultation_id": model.metadata.consultation_id,
            "language": model.metadata.language,
            "audience": "expert" if expert else "customer",
            "narrative_version": model.metadata.narrative_version,
            "report_profile_version": model.metadata.report_profile_version,
            "person_a_correlation_id": model.metadata.person_a_correlation_id,
            "person_b_correlation_id": model.metadata.person_b_correlation_id,
        },
        "sections": [_serialize_section(item, expert=expert) for item in sections],
    }


def serialize_history_row(row: MarriageHistoryRecord) -> dict[str, object]:
    """History row from stored facts. Not rendered prose."""
    return {
        "consultation_id": row.consultation_id,
        "created_at": row.created_at,
        "overall_state": row.overall_state,
        "score": None,
        "grade": None,
        "status": row.status,
        "display_identity": row.display_label,
        "person_a_correlation_id": row.person_a_analysis_id,
        "person_b_correlation_id": row.person_b_analysis_id,
    }


def serialize_envelope(
    *,
    status: MarriageRuntimeStatus,
    data: dict[str, object] | None,
    warnings: list[dict[str, str | None]] | None = None,
    errors: list[dict[str, object]] | None = None,
    versions: dict[str, str | None] | None = None,
) -> dict[str, object]:
    """TV-01 response envelope. Business status is independent of HTTP."""
    return {
        "status": status.value,
        "data": data,
        "warnings": warnings or [],
        "errors": errors or [],
        "version_bundle": versions or {"api_version": API_VERSION},
    }


def serialize_runtime_error(error: RuntimeError, consultation_id: str | None) -> dict[str, object]:
    """Map a runtime error onto the public error object."""
    return serialize_error(
        code=error.code,
        stage=error.stage,
        retryable=error.retryable,
        consultation_id=consultation_id,
        detail=error.technical_detail,
    )


def _person_summary(result: MarriageDecisionResult, side: str) -> dict[str, str | None]:
    """Presentation-safe identity. Correlation id is not a Canonical-native analysis id."""
    person = result.person_a if side == "a" else result.person_b
    return {
        "display_name": person.display_name,
        "gender": person.gender.value,
        "correlation_id": person.analysis_id,
    }


def serialize_assessment_cards(result: MarriageDecisionResult) -> list[dict[str, object]]:
    """Public Assessment cards. Raw Decision stays internal."""
    if result.assessment is None:
        result.assessment = project_marriage_assessment(result)
    cards: list[dict[str, object]] = []
    for card in result.assessment.cards:
        cards.append(
            {
                "question_id": card.question_id,
                "question": card.question,
                "answer": card.answer,
                "supporting_facts": list(card.supporting_facts),
                "confidence": card.confidence,
                "limitations": list(card.limitations),
            }
        )
    return cards


def _headline(narrative: MarriageNarrativeResult | None) -> str | None:
    """Copy the overall headline already composed by Narrative."""
    if narrative is None:
        return None
    for section in narrative.sections:
        if section.section_id != "overall":
            continue
        for block in section.blocks:
            if block.block_id == "overall-headline":
                return block.text
    return None


def _action_themes(result: MarriageDecisionResult) -> list[str]:
    """Unique B04 action types. No new recommendations."""
    seen: list[str] = []
    for item in result.recommendations:
        value = item.action_type.value
        if value not in seen:
            seen.append(value)
    return seen


def _section_body(report: MarriageReportModel | None, section_id: str) -> str | None:
    """Copy an existing report section body. Prefer the first Assessment answer."""
    section = _find_section(report, section_id)
    if section is None:
        return None
    for block in section.blocks:
        if block.kind == "answer" and block.body:
            return block.body
    for block in section.blocks:
        if block.body:
            return block.body
    return section.summary


def _section_titles(report: MarriageReportModel | None, section_id: str) -> list[str]:
    """Copy existing highlight titles from a report section."""
    section = _find_section(report, section_id)
    if section is None:
        return []
    titles: list[str] = []
    for block in section.blocks:
        if block.kind == "highlight" and block.title:
            titles.append(block.title)
    return titles


def _find_section(report: MarriageReportModel | None, section_id: str) -> ReportSection | None:
    """Find a report section by id."""
    if report is None:
        return None
    for item in report.sections:
        if item.section_id == section_id:
            return item
    return None


def _serialize_section(section: ReportSection, *, expert: bool) -> dict[str, object]:
    """Serialize one semantic section."""
    return {
        "section_id": section.section_id,
        "title": section.title,
        "summary": section.summary,
        "blocks": [_serialize_block(item, expert=expert) for item in section.blocks],
    }


def _serialize_block(block: ReportBlock, *, expert: bool) -> dict[str, object]:
    """Serialize one semantic block. Customer omits internal source ids."""
    payload: dict[str, object] = {
        "block_id": _public_block_id(block.block_id, expert=expert),
        "kind": block.kind,
        "title": block.title,
        "body": block.body,
        "semantic_key": block.semantic_key,
        "state": block.state,
        "domain": block.domain.value if block.domain else None,
        "visibility": block.visibility,
    }
    if expert:
        payload["source_finding_ids"] = list(block.source_finding_ids)
        payload["source_recommendation_ids"] = list(block.source_recommendation_ids)
    return payload


def _expert_trace(stored: MarriageStoredResult) -> dict[str, object]:
    """Controlled expert trace. No stack traces or implementation classes."""
    result = stored.result
    return {
        "decision_trace": {
            "overall_state": result.overall.state.value if result.overall.state else None,
            "domain_states": [
                {
                    "domain": item.domain.value,
                    "available": item.availability.available,
                    "state": item.state.value if item.state else None,
                }
                for item in _iter_domains(result)
            ],
        },
        "finding_references": [
            {
                "finding_id": item.finding_id,
                "domain": item.domain.value,
                "type": item.type.value,
            }
            for item in result.findings
        ],
        "evidence_references": [
            {"evidence_id": item.evidence_id, "domain": item.domain.value}
            for item in result.evidence
        ],
        "recommendation_references": [
            {
                "recommendation_id": item.recommendation_id,
                "action_type": item.action_type.value,
                "source_finding_ids": list(item.source_finding_ids),
            }
            for item in result.recommendations
        ],
        "version_bundle": public_version_bundle(result),
        "methodology": {
            "narrative_version": stored.narrative.version if stored.narrative else None,
            "report_profile_version": report_profile_token(),
        },
    }


def _iter_domains(result: MarriageDecisionResult) -> tuple[MarriageDomainDecision, ...]:
    """Frozen domain order."""
    domains = result.domains
    return (
        domains.five_elements,
        domains.stem_branch,
        domains.ten_gods,
        domains.interaction,
        domains.finance,
        domains.family,
        domains.children,
        domains.luck,
    )


def _domain_published(domain: MarriageDomainDecision) -> bool:
    """True when the domain has a publishable semantic state."""
    if not domain.availability.available or domain.state is None:
        return False
    return domain.state.value != "insufficient"


def _public_block_id(block_id: str, *, expert: bool) -> str:
    """Customer mode must not leak Finding/Evidence ids through block ids."""
    if expert:
        return block_id
    if "F-" in block_id or "EV-" in block_id:
        return block_id.replace("F-", "finding-").replace("EV-", "evidence-")
    return block_id


def _is_safe_detail(detail: str) -> bool:
    """Allow short validation codes. Reject paths and tracebacks."""
    if len(detail) > 80:
        return False
    lowered = detail.lower()
    if "traceback" in lowered or "\\" in detail or "/" in detail:
        return False
    return True

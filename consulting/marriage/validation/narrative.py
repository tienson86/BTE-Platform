"""TV1-B05 narrative and report validation. Does not replace B04 recommendation rules."""

from __future__ import annotations

import re

from consulting.marriage.exceptions import MarriageNarrativeError
from consulting.marriage.models.narrative import MarriageNarrativeBlock, MarriageNarrativeResult
from consulting.marriage.models.report import MarriageReportModel, ReportBlock
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.report.access import customer_visible_text, expert_visible_text
from consulting.marriage.report.labels import RENDERER_TOKENS
from consulting.marriage.report.versions import REQUIRED_CUSTOMER_SECTIONS
from consulting.marriage.validation.recommendation import MarriageRecommendationValidation

_FORBIDDEN_CLAIMS = (
    "chắc chắn",
    "nhất định",
    "ngoại tình",
    "không nên cưới",
    "must marry",
    "must not marry",
    "certain divorce",
    "grade a",
    "grade b",
    "grade c",
    "/100",
)

_TECHNICAL_ID = re.compile(r"\b(?:EV|F)-\d{4}\b")
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
_PERCENT = re.compile(r"\d+\s*%")
_SCORE = re.compile(r"\b\d{1,3}\s*/\s*100\b")


class MarriageNarrativeValidation(MarriageRecommendationValidation):
    """Validate narrative source-trace, wording, and no-score contracts."""

    def validate_narrative(
        self,
        decision: MarriageDecisionResult,
        narrative: MarriageNarrativeResult,
    ) -> None:
        """Fail closed when narrative invents meaning or forbidden claims."""
        finding_ids = {item.finding_id for item in decision.findings}
        rec_ids = {item.recommendation_id for item in decision.recommendations}
        if not narrative.sections:
            raise MarriageNarrativeError("narrative_sections_missing")
        if not narrative.version or narrative.version == "unbound":
            raise MarriageNarrativeError("narrative_version_unbound")
        for section in narrative.sections:
            if not section.blocks:
                raise MarriageNarrativeError(f"orphan_section:{section.section_id}")
            for block in section.blocks:
                _validate_block(block, finding_ids, rec_ids)
        if decision.overall.score is not None or decision.overall.grade is not None:
            raise MarriageNarrativeError("score_must_remain_unavailable")
        if decision.versions.score_model_version not in {None, "unavailable"}:
            if decision.overall.score is not None:
                raise MarriageNarrativeError("score_fabricated")


class MarriageReportValidation(MarriageNarrativeValidation):
    """Validate semantic report story, modes, and renderer-free model."""

    def validate_report(
        self,
        decision: MarriageDecisionResult,
        narrative: MarriageNarrativeResult,
        report: MarriageReportModel,
    ) -> None:
        """Fail closed when the report diverges from Narrative/Decision."""
        self.validate_narrative(decision, narrative)
        section_ids = [item.section_id for item in report.sections]
        for required in REQUIRED_CUSTOMER_SECTIONS:
            if required not in section_ids:
                raise MarriageNarrativeError(f"required_section_missing:{required}")
        finding_ids = {item.finding_id for item in decision.findings}
        rec_ids = {item.recommendation_id for item in decision.recommendations}
        for section in report.sections:
            for block in section.blocks:
                _validate_report_block(block, finding_ids, rec_ids)
        customer_text = customer_visible_text(report)
        _reject_forbidden(customer_text)
        if _TECHNICAL_ID.search(customer_text):
            raise MarriageNarrativeError("customer_technical_id_exposed")
        if _YEAR.search(customer_text):
            raise MarriageNarrativeError("timing_year_invented")
        expert_text = expert_visible_text(report)
        if decision.findings and not any(item.finding_id in expert_text for item in decision.findings):
            raise MarriageNarrativeError("expert_trace_missing")
        hero = next(item for item in report.sections if item.section_id == "compatibility_hero")
        if not any(block.kind == "decision_state" for block in hero.blocks):
            raise MarriageNarrativeError("hero_semantic_state_missing")
        if any(block.kind in {"gauge", "score", "percent"} for block in hero.blocks):
            raise MarriageNarrativeError("hero_score_fabricated")
        _reject_unavailable_domains(decision, report)
        if report.metadata.narrative_version != narrative.version:
            raise MarriageNarrativeError("report_narrative_version_mismatch")
        if report.metadata.person_a_correlation_id != decision.person_a.analysis_id:
            raise MarriageNarrativeError("correlation_id_mismatch")


def _validate_block(
    block: MarriageNarrativeBlock,
    finding_ids: set[str],
    rec_ids: set[str],
) -> None:
    """Trace one narrative block to Decision/Finding/Recommendation."""
    if not block.catalog_key:
        raise MarriageNarrativeError(f"catalog_key_missing:{block.block_id}")
    _reject_forbidden(block.text)
    for finding_id in block.source_finding_ids:
        if finding_id not in finding_ids:
            raise MarriageNarrativeError(f"narrative_finding_unresolved:{block.block_id}:{finding_id}")
    for rec_id in block.source_recommendation_ids:
        if rec_id not in rec_ids:
            raise MarriageNarrativeError(f"narrative_recommendation_unresolved:{block.block_id}:{rec_id}")
    if block.stage == "action" and block.block_id != "action-none" and not block.source_recommendation_ids:
        if block.catalog_key != "marriage.action.none":
            raise MarriageNarrativeError(f"action_without_recommendation:{block.block_id}")


def _validate_report_block(
    block: ReportBlock,
    finding_ids: set[str],
    rec_ids: set[str],
) -> None:
    """Trace one report block and reject renderer-specific data."""
    for token in RENDERER_TOKENS:
        blob = f"{block.kind} {block.title or ''} {block.body or ''} {block.semantic_key or ''}"
        if token in blob.lower() and token in (block.kind or "").lower():
            raise MarriageNarrativeError(f"renderer_kind:{block.block_id}:{token}")
    if block.kind in {"pdf", "docx", "html", "css"}:
        raise MarriageNarrativeError(f"renderer_kind:{block.block_id}")
    _reject_forbidden(f"{block.title or ''} {block.body or ''}")
    for finding_id in block.source_finding_ids:
        if finding_id not in finding_ids:
            raise MarriageNarrativeError(f"report_finding_unresolved:{block.block_id}:{finding_id}")
    for rec_id in block.source_recommendation_ids:
        if rec_id not in rec_ids:
            raise MarriageNarrativeError(f"report_recommendation_unresolved:{block.block_id}:{rec_id}")


def _reject_forbidden(text: str) -> None:
    """Reject fortune claims and fabricated scores."""
    lowered = text.lower()
    for phrase in _FORBIDDEN_CLAIMS:
        if phrase in lowered:
            raise MarriageNarrativeError(f"forbidden_claim:{phrase}")
    if _SCORE.search(text) or _PERCENT.search(text):
        raise MarriageNarrativeError("score_or_percent_fabricated")


def _reject_unavailable_domains(decision: MarriageDecisionResult, report: MarriageReportModel) -> None:
    """Unavailable D4/D6/D7 must not appear as published domain analysis."""
    unavailable = {
        item.domain.value
        for item in (
            decision.domains.interaction,
            decision.domains.family,
            decision.domains.children,
        )
        if not item.availability.available or (item.state and item.state.value == "insufficient")
    }
    domain_section = next(item for item in report.sections if item.section_id == "domain_analysis")
    for block in domain_section.blocks:
        if block.visibility == "expert":
            continue
        if block.domain and block.domain.value in unavailable and block.kind == "domain_summary":
            raise MarriageNarrativeError(f"unavailable_domain_published:{block.domain.value}")

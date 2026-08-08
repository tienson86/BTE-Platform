"""NarrativeResult validator — Sprint D2 quality gate."""

from __future__ import annotations

import logging

from engines.narrative_engine.runtime.models import OFFICIAL_COMPONENT_ORDER

from .constants import INSUFFICIENT_EVIDENCE_NARRATIVE
from .language_rules import LanguageRuleEngine
from .models import NarrativeResult, ResultStatus

logger = logging.getLogger(__name__)


class NarrativeResultValidator:
    """
    Validate NarrativeResult integrity and writing-system constraints.

    Ensures traceability and forbids invented unsupported prose patterns.
    """

    def __init__(self, language_rules: LanguageRuleEngine | None = None) -> None:
        self._rules = language_rules or LanguageRuleEngine()

    def validate(self, result: NarrativeResult) -> tuple[str, ...]:
        """Return issue codes (empty means accepted)."""
        issues: list[str] = []
        expected_ids = [f"sec-{item.value}" for item in OFFICIAL_COMPONENT_ORDER]
        actual_ids = [section.id for section in result.sections]
        if actual_ids != expected_ids:
            issues.append("section_order_mismatch")

        for section in result.sections:
            for paragraph in section.paragraphs:
                if paragraph.insufficient_data:
                    if paragraph.text != INSUFFICIENT_EVIDENCE_NARRATIVE:
                        issues.append(f"insufficient_text_mismatch:{paragraph.id}")
                    continue
                if not paragraph.evidence_refs and not paragraph.interpretation_refs:
                    issues.append(f"missing_trace:{paragraph.id}")
                if not self._rules.is_allowed(paragraph.text):
                    issues.append(f"forbidden_wording:{paragraph.id}")
            for recommendation in section.recommendations:
                if recommendation.insufficient_data:
                    continue
                if not recommendation.evidence_refs and not recommendation.interpretation_refs:
                    issues.append(f"missing_trace_rec:{recommendation.id}")
                if not self._rules.is_allowed(recommendation.action):
                    issues.append(f"forbidden_wording_rec:{recommendation.id}")

        summary = result.summary
        for flag in summary.insufficient_flags:
            if flag == "identity" and summary.identity != INSUFFICIENT_EVIDENCE_NARRATIVE:
                issues.append("summary_identity_flag_mismatch")
        logger.info("result_validator.issues=%s", len(issues))
        return tuple(issues)

    def apply(self, result: NarrativeResult, issues: tuple[str, ...]) -> NarrativeResult:
        """Return result with validation issues and corrected status."""
        if issues:
            status = ResultStatus.FAILED
        elif result.summary.insufficient_flags or any(
            section.insufficient_data for section in result.sections
        ):
            status = ResultStatus.PARTIAL_INSUFFICIENT
        else:
            status = ResultStatus.COMPLETE
        return NarrativeResult(
            summary=result.summary,
            sections=result.sections,
            recommendations=result.recommendations,
            confidence=result.confidence,
            status=status,
            run_id=result.run_id,
            source_fingerprint=dict(result.source_fingerprint),
            metadata=dict(result.metadata),
            validation_issues=issues,
        )

"""NarrativeResultComposer — Sprint D2 orchestration."""

from __future__ import annotations

import logging
from statistics import fmean
from typing import Any

from engines.narrative_engine.runtime.models import (
    ComponentType,
    NarrativeTree,
    TreeStatus,
)
from engines.narrative_engine.runtime.exceptions import NarrativeRuntimeValidationError

from .executive_summary_composer import ExecutiveSummaryComposer
from .models import NarrativeResult, ResultStatus
from .result_validator import NarrativeResultValidator
from .section_composer import SectionComposer
from .source_factory import build_composition_source

logger = logging.getLogger(__name__)


class NarrativeResultComposer:
    """
    Transform NarrativeTree + factual sources into NarrativeResult.

    Implements:
    Paragraph Builder, Language Rule Engine, Tone Resolver,
    Sentence Composer, Section Composer, Executive Summary Composer,
    Recommendation Composer, Narrative Validator.
    """

    version = "d2.0.0"

    def __init__(
        self,
        section_composer: SectionComposer | None = None,
        executive_summary_composer: ExecutiveSummaryComposer | None = None,
        result_validator: NarrativeResultValidator | None = None,
    ) -> None:
        self._sections = section_composer or SectionComposer()
        self._executive = executive_summary_composer or ExecutiveSummaryComposer()
        self._validator = result_validator or NarrativeResultValidator()

    def compose(
        self,
        tree: NarrativeTree,
        *,
        analysis: Any = None,
        interpretation: Any = None,
    ) -> NarrativeResult:
        """Compose NarrativeResult from a validated NarrativeTree."""
        if tree.status == TreeStatus.INVALID:
            raise NarrativeRuntimeValidationError(
                "Cannot compose NarrativeResult from invalid NarrativeTree."
            )

        source = build_composition_source(
            tree,
            analysis=analysis,
            interpretation=interpretation,
        )
        logger.info(
            "result_composer.start run_id=%s facts=%s interp_facts=%s",
            tree.run_id,
            len(source.facts),
            len(source.interpretation_facts),
        )

        sections = tuple(
            self._sections.compose(node, source) for node in tree.nodes
        )
        summary = self._executive.compose(sections)
        recommendations = tuple(
            item
            for section in sections
            if section.id == f"sec-{ComponentType.RECOMMENDATION.value}"
            for item in section.recommendations
        )
        confidences = [section.confidence for section in sections if section.confidence > 0]
        confidence = round(fmean(confidences), 4) if confidences else 0.0

        result = NarrativeResult(
            summary=summary,
            sections=sections,
            recommendations=recommendations,
            confidence=confidence,
            status=ResultStatus.PARTIAL_INSUFFICIENT,
            run_id=tree.run_id,
            source_fingerprint={
                "tree_status": tree.status.value,
                "runtime": "pack05_narrative_d1",
                "composer": self.version,
            },
            metadata={
                "section_count": len(sections),
                "insufficient_section_count": sum(
                    1 for section in sections if section.insufficient_data
                ),
            },
        )
        issues = self._validator.validate(result)
        result = self._validator.apply(result, issues)
        logger.info(
            "result_composer.done run_id=%s status=%s issues=%s",
            result.run_id,
            result.status.value,
            len(result.validation_issues),
        )
        return result

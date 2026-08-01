"""Scoring Interpreter service — orchestration for scoring business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.constants import (
    SCORING_INTERPRETER_ID,
    SCORING_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.extractor import (
    ScoringFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.models import (
    ScoringComponentResult,
    ScoringInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.rule_engine import (
    ScoringInterpretationRuleEngine,
    ScoringRuleEngineResult,
)

logger = logging.getLogger(__name__)


class ScoringInterpreterService:
    """Build ScoringInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 ``09_final_score`` rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: ScoringFactExtractor | None = None,
        rule_engine: ScoringInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or ScoringFactExtractor()
        self.rule_engine = rule_engine or ScoringInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> ScoringInterpretationSection | None:
        """Interpret scoring from context.final_result.

        Returns None when FinalResult has no scoring payload / scores.
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "scoring_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{SCORING_INTERPRETER_ID}_{context.id}"

        typed = ScoringInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=SCORING_SECTION_TYPE,
                title_ref="scoring.title",
                interpreter_id=SCORING_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("scoring_interpreter_ok",),
                attributes={},
            ),
            overall=engine_result.overall,
            dimensions=engine_result.dimensions,
            confidence=engine_result.confidence,
            quality=engine_result.quality,
            overall_score=engine_result.overall_score,
            confidence_value=engine_result.confidence_value,
            grade=engine_result.grade,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("scoring_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=SCORING_SECTION_TYPE,
            title_ref="scoring.title",
            interpreter_id=SCORING_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("scoring_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return ScoringInterpretationSection(
            section=section,
            overall=typed.overall,
            dimensions=typed.dimensions,
            confidence=typed.confidence,
            quality=typed.quality,
            overall_score=typed.overall_score,
            confidence_value=typed.confidence_value,
            grade=typed.grade,
            components=typed.components,
            matched_rules=typed.matched_rules,
            reasoning=typed.reasoning,
            source_final_result_id=typed.source_final_result_id,
            success=typed.success,
            messages=typed.messages,
        )

    def interpret_final_result(
        self,
        final_result: FinalResult,
        *,
        context_id: str = "adhoc",
    ) -> ScoringInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="scoring_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: ScoringRuleEngineResult,
    ) -> dict[str, ScoringComponentResult]:
        """Map engine results into Overall/Dimension/Confidence/Quality."""
        grade = engine_result.grade
        return {
            "overall": ScoringComponentResult(
                component_id="overall",
                value=grade or str(engine_result.overall_score),
                score=engine_result.overall_score,
                count=len(engine_result.overall),
                items=engine_result.overall,
                description="Overall Score",
            ),
            "dimensions": ScoringComponentResult(
                component_id="dimensions",
                value=",".join(
                    item.label or item.item_id for item in engine_result.dimensions
                ),
                score=sum(item.value for item in engine_result.dimensions),
                count=len(engine_result.dimensions),
                items=engine_result.dimensions,
                description="Dimension Scores",
            ),
            "confidence": ScoringComponentResult(
                component_id="confidence",
                value=(
                    engine_result.confidence[0].level
                    if engine_result.confidence
                    else ""
                ),
                score=engine_result.confidence_value,
                count=len(engine_result.confidence),
                items=engine_result.confidence,
                description="Confidence",
            ),
            "quality": ScoringComponentResult(
                component_id="quality",
                value=grade,
                score=engine_result.overall_score,
                count=len(engine_result.quality),
                items=engine_result.quality,
                description="Quality (Grade / Rating)",
            ),
        }

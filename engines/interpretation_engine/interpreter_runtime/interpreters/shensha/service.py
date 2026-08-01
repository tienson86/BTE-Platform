"""Shensha Interpreter service — orchestration for shensha business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.constants import (
    SHENSHA_INTERPRETER_ID,
    SHENSHA_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.extractor import (
    ShenshaFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.models import (
    ShenshaComponentResult,
    ShenshaInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.rule_engine import (
    ShenshaInterpretationRuleEngine,
    ShenshaRuleEngineResult,
)

logger = logging.getLogger(__name__)


class ShenshaInterpreterService:
    """Build ShenshaInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 than_sat + shensha score rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: ShenshaFactExtractor | None = None,
        rule_engine: ShenshaInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or ShenshaFactExtractor()
        self.rule_engine = rule_engine or ShenshaInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> ShenshaInterpretationSection | None:
        """Interpret Shensha from context.final_result.

        Returns None when FinalResult has no shensha payload.
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "shensha_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{SHENSHA_INTERPRETER_ID}_{context.id}"

        typed = ShenshaInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=SHENSHA_SECTION_TYPE,
                title_ref="shensha.title",
                interpreter_id=SHENSHA_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("shensha_interpreter_ok",),
                attributes={},
            ),
            detected=engine_result.detected,
            importance=engine_result.importance,
            priorities=engine_result.priorities,
            explanations=engine_result.explanations,
            shensha_score=engine_result.shensha_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("shensha_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=SHENSHA_SECTION_TYPE,
            title_ref="shensha.title",
            interpreter_id=SHENSHA_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("shensha_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return ShenshaInterpretationSection(
            section=section,
            detected=typed.detected,
            importance=typed.importance,
            priorities=typed.priorities,
            explanations=typed.explanations,
            shensha_score=typed.shensha_score,
            components=typed.components,
            matched_rules=typed.matched_rules,
            confidence=typed.confidence,
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
    ) -> ShenshaInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="shensha_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: ShenshaRuleEngineResult,
    ) -> dict[str, ShenshaComponentResult]:
        """Map engine results into Detected/Importance/Priority/Explanation."""
        return {
            "detected": ShenshaComponentResult(
                component_id="detected",
                value=",".join(
                    item.label or item.item_id for item in engine_result.detected
                ),
                score=sum(item.score for item in engine_result.detected),
                count=len(engine_result.detected),
                items=engine_result.detected,
                description="All detected Shensha",
            ),
            "importance": ShenshaComponentResult(
                component_id="importance",
                value=",".join(
                    f"{item.label}:{item.importance}"
                    for item in engine_result.importance
                ),
                score=float(
                    sum(item.importance_rank for item in engine_result.importance)
                ),
                count=len(engine_result.importance),
                items=engine_result.importance,
                description="Shensha Importance",
            ),
            "priority": ShenshaComponentResult(
                component_id="priority",
                value=",".join(
                    f"{item.label}:{item.priority}" for item in engine_result.priorities
                ),
                score=sum(item.score for item in engine_result.priorities),
                count=len(engine_result.priorities),
                items=engine_result.priorities,
                description="Shensha Priority",
            ),
            "explanation": ShenshaComponentResult(
                component_id="explanation",
                value=",".join(
                    item.label or item.item_id for item in engine_result.explanations
                ),
                score=float(len(engine_result.explanations)),
                count=len(engine_result.explanations),
                items=engine_result.explanations,
                description="Shensha Explanation",
            ),
        }
